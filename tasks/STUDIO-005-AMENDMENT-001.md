# STUDIO-005 Amendment 001 — Windows-compatible save roundtrip test

## 1. Amendment identity

- `amendment_id`: `STUDIO-005-AMENDMENT-001`
- `parent_contract`: `tasks/STUDIO-005.md`
- `parent_contract_commit`: `531235536db678ec93c1f8a11ed4e31bbb0bfeff`
- `approval_date`: `2026-08-12`
- `approved_by`: `Studio Owner`
- `approval_status`: `OWNER_APPROVED`
- `durability_before_commit`: `WORKTREE_ONLY`

The Studio Owner selected Option A in the active STUDIO-005 recovery workflow: repair the existing save-roundtrip test for Windows compatibility and run the complete suite without installing WSL or skipping a test. This file is the durable repository record of that bounded authorization once committed.

## 2. Trigger and evidence

The STUDIO-005 validators and all 15 Project Studio validator tests passed under Python 3.13.15 on Windows. The complete suite then ran 54 tests and reported one error:

- failing test: `tests/test_rules_prototype.py::RulesTests::test_save_roundtrip`
- failing operation: `prototype/rules/save_system.py` called `os.replace(tmp, path)`
- observed result: `PermissionError: [WinError 5] Access is denied`
- suite result before amendment: 53 passed, 1 error

The test held the destination `NamedTemporaryFile` open while `save()` attempted to replace it. Python documents that reopening a still-open named temporary file differs on Windows and requires specific delete-sharing conditions. It separately documents that `TemporaryDirectory` securely creates a directory and cleans it up when its context ends. The repaired fixture therefore uses a path inside a managed temporary directory and never keeps the destination handle open.

Authoritative references:

- Python `NamedTemporaryFile`: https://docs.python.org/3/library/tempfile.html#tempfile.NamedTemporaryFile
- Python `os.replace`: https://docs.python.org/3/library/os.html#os.replace

## 3. Authorized scope extension

This amendment adds exactly two paths to the 14 implementation paths already authorized by the parent contract, producing an amended implementation scope of exactly 16 paths:

1. `tasks/STUDIO-005-AMENDMENT-001.md`
2. `tests/test_rules_prototype.py`

The first path records this authorization. The second path may receive only the bounded change in Section 4. All original 14 paths may be updated only as necessary to record this amendment, the 16-path scope, checkpoints, validator coverage, and final check state.

No other file may be created, modified, deleted, renamed, or moved.

## 4. Authorized test repair

Only `RulesTests.test_save_roundtrip` and the import list required by that test may change in `tests/test_rules_prototype.py`.

The repaired test must:

1. create a managed `TemporaryDirectory`;
2. derive a save path inside it with `os.path.join`;
3. call `save()` twice so the second call still exercises replacement of an existing, closed destination;
4. load the resulting file and compare the complete state dictionary;
5. rely on the temporary directory context for cleanup.

The amendment does not authorize any change to `prototype/rules/save_system.py`, other production code, gameplay values, quest content, data, or GDD material.

## 5. Preserved authority boundaries

- `tasks/STUDIO-005.md` remains byte-for-byte unchanged at blob `cf09f87461f78500e380a68600fae53df7dc1d02`.
- V22 and V23 remain immutable, co-equal, Owner-created working drafts.
- Neither V22 nor V23 gains precedence, including for `MQ01A–MQ01D` or `DOC01`.
- `official_integrated_gdd` remains `NOT_YET_DESIGNATED`.
- No external capability, WSL distribution, engine, language, framework, model, provider, router, database, or dependency is selected, installed, or adopted by this amendment.
- The Python runtime already installed by the Studio Owner is an execution precondition, not a technology-selection decision for the game.

## 6. Acceptance criteria

The amended recovery may reach `HANDOFF` only if all of the following pass without test skipping:

1. exact branch, HEAD, parent, contract blob, and original test blob preflight;
2. exact reconciliation of the existing 14-file `BLOCKED` snapshot;
3. exact 16-path amended scope;
4. immutable V22 and V23 blob checks;
5. Project Studio validator;
6. evidence-register validator;
7. Project Studio validator unit tests, including amendment and patch negative cases;
8. complete `unittest` discovery suite on Windows;
9. working-tree and staged whitespace checks;
10. zero staged files and no commit, push, Pull Request, merge, or branch deletion.

Any failure leaves a repository-visible `BLOCKED` checkpoint. It may not be reported as a pass.

## 7. Supersession rule

This amendment supersedes the parent contract only where the parent contract limits implementation to 14 paths or forbids modifying `tests/test_rules_prototype.py`. Every other term of `tasks/STUDIO-005.md` remains binding. The contract-only commit remains immutable evidence of the original approval; this amendment must not rewrite it.
