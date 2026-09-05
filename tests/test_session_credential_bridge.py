from __future__ import annotations

import copy
import inspect
import io
import unittest
from unittest import mock

from scripts import session_credential_bridge as bridge

AS_OF = "2026-09-05T01:00:00Z"
SECRET = "synthetic-secret-material-1234567890"

def valid_lease():
    value = {
        "schema_version": "1.0",
        "credential_lease_id": "credential-lease:" + "a" * 32,
        "credential_profile_id": bridge.CREDENTIAL_PROFILE_ID,
        "profile_digest": "sha256:" + "b" * 64,
        "subject_ref": bridge.SUBJECT_REF,
        "capability": bridge.CAPABILITY,
        "purpose": bridge.PURPOSE,
        "repository_record_digest": None,
        "operation_digest": None,
        "issued_at": "2026-09-05T00:59:00Z",
        "expires_at": "2026-09-05T01:10:00Z",
        "idempotency_key": "studio-009v-01-session",
        "canonical_digest": "",
    }
    value["canonical_digest"] = bridge.canonical_digest(value)
    return value

class SessionCredentialBridgeTests(unittest.TestCase):
    def assertCode(self, code, fn):
        with self.assertRaises(bridge.SessionCredentialError) as ctx:
            fn()
        self.assertEqual(ctx.exception.code, code)
        self.assertNotIn(SECRET, ctx.exception.safe_message)

    def test_01_source_has_no_ambient_secret_lookup(self):
        source = inspect.getsource(bridge)
        for token in ("os.environ", "getenv(", ".env", "keyring", "win32cred", "subprocess", "open("):
            self.assertNotIn(token, source)

    def test_02_valid_lease(self):
        result = bridge.validate_lease(valid_lease(), as_of=AS_OF)
        self.assertEqual(result["credential_profile_id"], bridge.CREDENTIAL_PROFILE_ID)

    def test_03_wrong_profile(self):
        value = valid_lease()
        value["credential_profile_id"] = "credential-profile:other"
        value["canonical_digest"] = bridge.canonical_digest(value)
        self.assertCode("LEASE_LINEAGE", lambda: bridge.validate_lease(value, as_of=AS_OF))

    def test_04_wrong_purpose(self):
        value = valid_lease()
        value["purpose"] = "OTHER_PURPOSE"
        value["canonical_digest"] = bridge.canonical_digest(value)
        self.assertCode("LEASE_LINEAGE", lambda: bridge.validate_lease(value, as_of=AS_OF))

    def test_05_expired_lease(self):
        self.assertCode("LEASE_TIME", lambda: bridge.validate_lease(valid_lease(), as_of="2026-09-05T01:11:00Z"))

    def test_06_future_lease(self):
        self.assertCode("LEASE_TIME", lambda: bridge.validate_lease(valid_lease(), as_of="2026-09-05T00:58:00Z"))

    def test_07_digest_mismatch(self):
        value = valid_lease()
        value["canonical_digest"] = "sha256:" + "0" * 64
        self.assertCode("LEASE_DIGEST", lambda: bridge.validate_lease(value, as_of=AS_OF))

    def test_08_secret_reaches_consumer_only(self):
        seen = []
        result = bridge.with_secret(
            valid_lease(), lambda secret: seen.append(secret) or {"ok": True},
            as_of=AS_OF, supplier=lambda: SECRET,
        )
        self.assertEqual(result, {"ok": True})
        self.assertEqual(seen, [SECRET])

    def test_09_secret_cannot_escape_result(self):
        self.assertCode(
            "SECRET_ESCAPE",
            lambda: bridge.with_secret(
                valid_lease(), lambda secret: {"leak": secret},
                as_of=AS_OF, supplier=lambda: SECRET,
            ),
        )

    def test_10_invalid_secret_supplier(self):
        self.assertCode(
            "INVALID_SECRET",
            lambda: bridge.with_secret(
                valid_lease(), lambda secret: {"ok": True},
                as_of=AS_OF, supplier=lambda: "short",
            ),
        )

    def test_11_noninteractive_requires_owner_input(self):
        with mock.patch.object(bridge.sys.stdin, "isatty", return_value=False):
            self.assertCode(
                "INTERACTIVE_REQUIRED",
                lambda: bridge.with_secret(
                    valid_lease(), lambda secret: {"ok": True}, as_of=AS_OF
                ),
            )

    def test_12_input_is_immutable(self):
        value = valid_lease()
        before = copy.deepcopy(value)
        bridge.validate_lease(value, as_of=AS_OF)
        self.assertEqual(value, before)
