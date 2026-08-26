import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from scripts.orchestration_queue import (
    ACTIVE_TRANSITIONS,
    QueueError,
    build_transition,
    create_draft,
    main,
    ordered_snapshots,
    read_events,
    snapshot_digest,
    transition,
    validate_event,
    validate_history,
    validate_queue,
    validate_transition_change,
    validate_work_order,
)


FIXTURES = Path("platform/orchestration/fixtures/007a")


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def valid_pair(work_order_id="WO-TEST-001", event_id="EV-TEST-001",
               created_at="2026-08-26T06:00:00Z", priority=50):
    snapshot = fixture("valid-work-order.json")
    snapshot.update(
        work_order_id=work_order_id,
        created_at=created_at,
        updated_at=created_at,
        last_event_id=event_id,
        priority=priority,
    )
    event = json.loads((FIXTURES / "valid-events.jsonl").read_text(encoding="utf-8"))
    event.update(
        event_id=event_id,
        work_order_id=work_order_id,
        timestamp=created_at,
        resulting_snapshot_digest=snapshot_digest(snapshot),
    )
    return snapshot, event


class ValidationTests(unittest.TestCase):
    def test_valid_fixtures_pass(self):
        snapshot = fixture("valid-work-order.json")
        events = read_events(FIXTURES / "valid-events.jsonl")
        validate_history(snapshot, events)

    def test_missing_scope_fixture_fails(self):
        with self.assertRaisesRegex(QueueError, "permitted_paths"):
            validate_work_order(fixture("invalid-missing-scope.json"))

    def test_nonzero_budget_fixture_fails(self):
        with self.assertRaisesRegex(QueueError, "budget_ceiling"):
            validate_work_order(fixture("invalid-nonzero-budget.json"))

    def test_illegal_transition_fixture_fails(self):
        snapshot = fixture("valid-work-order.json")
        events = read_events(FIXTURES / "invalid-illegal-transition.jsonl")
        with self.assertRaisesRegex(QueueError, "illegal transition"):
            validate_history(snapshot, events)

    def test_duplicate_event_fixture_fails(self):
        snapshot = fixture("valid-work-order.json")
        events = read_events(FIXTURES / "invalid-duplicate-event.jsonl")
        with self.assertRaisesRegex(QueueError, "duplicate event replay differs"):
            validate_history(snapshot, events)

    def test_malformed_timestamp_fails(self):
        snapshot, _ = valid_pair()
        snapshot["created_at"] = "2026-08-26 06:00:00"
        with self.assertRaisesRegex(QueueError, "UTC"):
            validate_work_order(snapshot)

    def test_unsupported_schema_fails(self):
        snapshot, _ = valid_pair()
        snapshot["schema_version"] = 2
        with self.assertRaisesRegex(QueueError, "unsupported"):
            validate_work_order(snapshot)

    def test_absolute_and_parent_paths_fail(self):
        for path in ("C:/secret/file", "/etc/passwd", "docs/../secret"):
            snapshot, _ = valid_pair()
            snapshot["permitted_paths"] = [path]
            with self.subTest(path=path), self.assertRaises(QueueError):
                validate_work_order(snapshot)

    def test_credential_bearing_value_fails(self):
        snapshot, _ = valid_pair()
        snapshot["objective"] = "Use ghp_abcdefghijklmnopqrstuvwxyz123456"
        with self.assertRaisesRegex(QueueError, "credential"):
            validate_work_order(snapshot)

    def test_duplicate_list_entry_fails(self):
        snapshot, _ = valid_pair()
        snapshot["capability_tags"] = ["queue", "queue"]
        with self.assertRaisesRegex(QueueError, "duplicates"):
            validate_work_order(snapshot)


class QueueOperationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name) / "queue"

    def tearDown(self):
        self.temporary.cleanup()

    def add(self, work_order_id="WO-TEST-001", event_id="EV-TEST-001",
            created_at="2026-08-26T06:00:00Z", priority=50):
        snapshot, event = valid_pair(work_order_id, event_id, created_at, priority)
        self.assertEqual(create_draft(self.root, snapshot, event), "created")
        return snapshot, event

    def test_create_and_validate_queue(self):
        self.add()
        self.assertEqual(validate_queue(self.root), [])

    def test_create_replay_is_idempotent_only_if_exact(self):
        snapshot, event = self.add()
        before = sorted((path.relative_to(self.root), path.read_bytes())
                        for path in self.root.rglob("*.*"))
        self.assertEqual(create_draft(self.root, snapshot, event), "replayed")
        changed = copy.deepcopy(snapshot)
        changed["objective"] = "Different objective"
        with self.assertRaisesRegex(QueueError, "different content|digest"):
            create_draft(self.root, changed, event)
        after = sorted((path.relative_to(self.root), path.read_bytes())
                       for path in self.root.rglob("*.*"))
        self.assertEqual(before, after)

    def test_duplicate_work_order_id_fails(self):
        self.add()
        snapshot, event = valid_pair("WO-TEST-001", "EV-TEST-002")
        with self.assertRaisesRegex(QueueError, "already exists|duplicate"):
            create_draft(self.root, snapshot, event)

    def test_duplicate_event_id_across_queue_fails_without_mutation(self):
        self.add()
        snapshot, event = valid_pair("WO-TEST-002", "EV-TEST-001")
        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*"))
        with self.assertRaisesRegex(QueueError, "duplicate event_id"):
            create_draft(self.root, snapshot, event)
        self.assertEqual(before, sorted(path.relative_to(self.root) for path in self.root.rglob("*")))

    def test_ordering_priority_then_time_then_id(self):
        self.add("WO-TEST-B", "EV-TEST-B", "2026-08-26T06:00:00Z", 50)
        self.add("WO-TEST-C", "EV-TEST-C", "2026-08-26T05:00:00Z", 80)
        self.add("WO-TEST-A", "EV-TEST-A", "2026-08-26T06:00:00Z", 50)
        ids = [item["work_order_id"] for item in ordered_snapshots(self.root)]
        self.assertEqual(ids, ["WO-TEST-C", "WO-TEST-A", "WO-TEST-B"])

    def test_authorized_owner_then_producer_transitions(self):
        self.add()
        self.assertEqual(transition(
            self.root, "WO-TEST-001", event_id="EV-TEST-002",
            next_state="READY", actor_id="owner", actor_role="STUDIO_OWNER",
            timestamp="2026-08-26T06:01:00Z", reason="Owner accepted intake.",
        ), "transitioned")
        self.assertEqual(transition(
            self.root, "WO-TEST-001", event_id="EV-TEST-003",
            next_state="CLAIMABLE", actor_id="PRODUCER-01", actor_role="PRODUCER-01",
            timestamp="2026-08-26T06:02:00Z", reason="Validated intake is claimable.",
        ), "transitioned")
        self.assertEqual(validate_queue(self.root), [])

    def test_transition_replay_exact_only(self):
        self.add()
        kwargs = dict(
            event_id="EV-TEST-002", next_state="READY", actor_id="owner",
            actor_role="STUDIO_OWNER", timestamp="2026-08-26T06:01:00Z",
            reason="Owner accepted intake.",
        )
        self.assertEqual(transition(self.root, "WO-TEST-001", **kwargs), "transitioned")
        before = sorted((path.relative_to(self.root), path.read_bytes())
                        for path in self.root.rglob("*.*"))
        self.assertEqual(transition(self.root, "WO-TEST-001", **kwargs), "replayed")
        with self.assertRaisesRegex(QueueError, "replay differs"):
            transition(self.root, "WO-TEST-001", **{**kwargs, "reason": "Changed"})
        after = sorted((path.relative_to(self.root), path.read_bytes())
                       for path in self.root.rglob("*.*"))
        self.assertEqual(before, after)

    def test_all_declared_active_transitions_and_roles(self):
        for index, ((prior, next_state), roles) in enumerate(ACTIVE_TRANSITIONS.items(), 1):
            snapshot, _ = valid_pair(f"WO-ROLE-{index:03d}", f"EV-ROLE-{index:03d}")
            snapshot["state"] = prior
            snapshot["updated_at"] = "2026-08-26T06:00:00Z"
            allowed = next(iter(roles))
            updated, event = build_transition(
                snapshot, event_id=f"EV-NEXT-{index:03d}", next_state=next_state,
                actor_id=allowed, actor_role=allowed,
                timestamp="2026-08-26T06:01:00Z", reason="Authorized test.",
            )
            self.assertEqual(updated["state"], next_state)
            self.assertEqual(event["actor_role"], allowed)

    def test_unauthorized_and_reserved_transitions_fail(self):
        snapshot, _ = valid_pair()
        cases = [
            ("READY", "PRODUCER-01"),
            ("CLAIMABLE", "STUDIO_OWNER"),
            ("CLAIMED", "PRODUCER-01"),
            ("QA_PENDING", "PRODUCER-01"),
            ("OWNER_PENDING", "STUDIO_OWNER"),
            ("DONE", "STUDIO_OWNER"),
        ]
        for index, (next_state, role) in enumerate(cases, 1):
            with self.subTest(next_state=next_state, role=role), self.assertRaises(QueueError):
                build_transition(
                    snapshot, event_id=f"EV-BAD-{index:03d}", next_state=next_state,
                    actor_id=role, actor_role=role,
                    timestamp="2026-08-26T06:01:00Z", reason="Must fail.",
                )

    def test_decreasing_transition_timestamp_fails_without_mutation(self):
        self.add()
        before = sorted((path.relative_to(self.root), path.read_bytes())
                        for path in self.root.rglob("*.*"))
        with self.assertRaisesRegex(QueueError, "timestamp"):
            transition(
                self.root, "WO-TEST-001", event_id="EV-TEST-002",
                next_state="READY", actor_id="owner", actor_role="STUDIO_OWNER",
                timestamp="2026-08-26T05:59:00Z", reason="Too early.",
            )
        after = sorted((path.relative_to(self.root), path.read_bytes())
                       for path in self.root.rglob("*.*"))
        self.assertEqual(before, after)

    def test_scope_objective_prohibition_and_budget_escalation_fail(self):
        before, _ = valid_pair()
        changes = {
            "permitted_paths": ["platform", "scripts"],
            "objective": "Expanded objective",
            "prohibited_actions": ["No network access"],
            "budget_ceiling": 1,
        }
        for field, value in changes.items():
            after = copy.deepcopy(before)
            after[field] = value
            with self.subTest(field=field), self.assertRaisesRegex(QueueError, field):
                validate_transition_change(before, after)

    def test_snapshot_history_mismatch_fails(self):
        snapshot, event = self.add()
        event_path = self.root / "events" / "WO-TEST-001.jsonl"
        changed = copy.deepcopy(event)
        changed["resulting_snapshot_digest"] = "sha256:" + "0" * 64
        event_path.write_text(json.dumps(changed) + "\n", encoding="utf-8")
        self.assertTrue(validate_queue(self.root))

    def test_cli_exit_codes_and_invalid_create_no_mutation(self):
        snapshot_path = Path(self.temporary.name) / "invalid.json"
        event_path = Path(self.temporary.name) / "event.json"
        snapshot_path.write_text(json.dumps(fixture("invalid-nonzero-budget.json")), encoding="utf-8")
        _, event = valid_pair("WO-007A-003", "EV-007A-003", "2026-08-26T05:02:00Z")
        event_path.write_text(json.dumps(event), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = main([
                "create-draft", "--queue-root", str(self.root),
                "--snapshot", str(snapshot_path), "--event", str(event_path),
            ])
        self.assertEqual(code, 1)
        self.assertFalse(self.root.exists())

    def test_cli_validate_and_list_do_not_mutate(self):
        self.add()
        before = sorted((path.relative_to(self.root), path.read_bytes())
                        for path in self.root.rglob("*.*"))
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(["validate", "--queue-root", str(self.root)]), 0)
            self.assertEqual(main(["list", "--queue-root", str(self.root)]), 0)
        after = sorted((path.relative_to(self.root), path.read_bytes())
                       for path in self.root.rglob("*.*"))
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
