# STUDIO-006-AMENDMENT-001 - Candidate Register Validator Transition

## 1. Purpose

Authorize a bounded correction to the Project Studio validator and its tests so the repository can validate both the accepted STUDIO-005 baseline register and the contract-required STUDIO-006 evaluated register.

This amendment corrects an integration defect. It does not change candidate evidence, recommendations, installation state, adoption state, project authority, historical content, gameplay, or the STUDIO-006 evaluation conclusions.

## 2. Approval and identity

- Status: `APPROVED`
- Approved by: Studio Owner
- Approval date: `2026-08-16`
- Parent contract: `tasks/STUDIO-006.md`, revision `1.0`
- Parent contract merge: `0e2d7bab5c7c876338a246be16d46a8f1073b95c`
- Affected evaluation Pull Request: `#12`
- Affected evaluation head: `5f8b81058123600f5eb257e9fd32ca49655ceed7`
- Amendment contract branch: `agent/studio-006-amendment-001-contract`
- Planned implementation branch: `agent/studio-006-validator-transition`

The Studio Owner authorization is limited to the exact scope and behavior below. The amendment contract must be merged before implementation begins.

## 3. Deterministic defect evidence

GitHub Actions Rules CI ran the repository's ordinary 71-test suite against Pull Request #12 and failed five tests:

1. `test_cli_exit_code_for_valid_and_invalid_fixture`
2. `test_directly_negated_engine_selection_remains_valid`
3. `test_directly_negated_precedence_remains_valid`
4. `test_valid_structure_passes`
5. `test_windows_crlf_checkout_preserves_text_blob_identity`

Evidence:

- pull-request run: https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/actions/runs/31894266232
- push run: https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/actions/runs/31894263760
- failing step: `Unit tests`
- passing preceding step: `Validate data`
- observed result: `Ran 71 tests`; `FAILED (failures=5)`

The failure is deterministic:

- `scripts/validate_project_studio.py` requires every candidate to remain `UNASSESSED`, `NOT REVIEWED`, `NONE`, and `UNRESOLVED`;
- the approved parent contract requires every candidate to be evaluated, assigned an immutable reference, and given one non-binding recommendation;
- the validator counts every GitHub URL in a candidate section, so the required immutable commit URL is incorrectly treated as a duplicate canonical candidate URL;
- several tests copy the current repository register as their valid fixture, then apply the STUDIO-005-only assumptions to it.

## 4. Decision

The STUDIO-006 evaluated register is not reverted. The validator and tests must be extended to model the authorized state transition without weakening the STUDIO-005 baseline protections.

The register has exactly two valid whole-document modes:

1. `BASELINE_UNASSESSED` - all ten candidates retain the STUDIO-005 fields and safe values.
2. `EVALUATED` - all ten candidates satisfy the STUDIO-006 evaluated-state requirements below.

A mixed or partially transitioned register is invalid.

## 5. Exact implementation scope

After this amendment contract is merged, the implementation may modify exactly:

- `scripts/validate_project_studio.py`
- `tests/test_validate_project_studio.py`

No other file may be created, modified, deleted, renamed, or moved by the implementation Pull Request.

The following remain protected:

- `.github/workflows/rules-ci.yml`;
- `tasks/STUDIO-006.md` and this merged amendment contract;
- the seven files in Pull Request #12;
- GDD sources, MQ01 evidence, gameplay, prototype code/data, dependencies, repository configuration, and completed STUDIO-005 memory.

## 6. Required validator behavior

### 6.1 Shared identity and safety rules

Both valid modes must enforce:

- exactly ten ordered sections, `CANDIDATE-01` through `CANDIDATE-10`;
- exactly one explicit `URL` field per candidate;
- the exact canonical repository URL assigned to that candidate;
- exactly one non-empty bounded evaluation purpose;
- `installation: NOT INSTALLED` for every candidate;
- `adoption decision: NO DECISION` for every candidate;
- no installed, adopted, enabled, or authority-granting state.

Canonical URL uniqueness must be calculated from the explicit `URL` field only. An immutable commit URL is evidence, not a second canonical candidate URL.

### 6.2 Baseline mode

When every candidate has `assessment: UNASSESSED`, preserve the existing STUDIO-005 requirements:

- `license: NOT REVIEWED`;
- `security: NOT REVIEWED`;
- `pinned commit or tag: NONE`;
- `compatibility: UNRESOLVED`;
- existing canonical URL, purpose, installation, and adoption checks.

### 6.3 Evaluated mode

When every candidate has `assessment: EVALUATED`, require for every candidate:

- one full 40-lowercase-hex `evaluated reference`;
- one `immutable reference` equal to the canonical URL plus `/commit/` plus the evaluated reference;
- one non-empty license conclusion;
- one non-empty security conclusion;
- one non-empty compatibility conclusion;
- one recommendation from `ADOPT`, `ADAPT`, `REFERENCE`, `DEFER`, or `REJECT`;
- one report anchor under `studio/EXTERNAL_CAPABILITY_EVALUATION.md`;
- one non-empty evidence limitation;
- `installation: NOT INSTALLED`;
- `adoption decision: NO DECISION`.

The validator must reject missing evidence, malformed SHAs, mismatched immutable URLs, unsupported recommendations, unsafe states, duplicate canonical URLs, and mixed baseline/evaluated modes.

## 7. Required test behavior

The test suite must:

- retain a valid STUDIO-005 baseline fixture;
- add a valid STUDIO-006 evaluated fixture;
- prove both modes pass the validator;
- prove a mixed transition fails;
- prove malformed or mismatched immutable references fail;
- prove duplicate explicit canonical URL fields fail;
- prove immutable commit URLs do not create false canonical duplicates;
- preserve the existing precedence, engine-selection, source-hash, CRLF, production-immutability, checkpoint, and CLI regression coverage;
- stop depending on whichever candidate-register state happens to exist in the current repository when a test is intended to exercise unrelated behavior.

Test assertions must validate behavior and must not bypass or skip the candidate register.

## 8. Acceptance criteria

- [ ] This amendment contract is merged alone before implementation begins.
- [ ] The implementation Pull Request changes exactly the validator and its test file.
- [ ] The workflow file remains unchanged.
- [ ] The STUDIO-005 baseline register remains valid.
- [ ] The exact STUDIO-006 evaluated register at Pull Request #12 remains valid.
- [ ] Mixed and unsafe states remain invalid.
- [ ] All existing relevant tests pass and new transition tests pass.
- [ ] `python scripts/validate_project_studio.py --skip-git-scope` passes against both authorized fixtures.
- [ ] `python scripts/validate_evidence_register.py source/MQ01_evidence_register.csv` passes.
- [ ] `python -m unittest discover -s tests -p "test*.py" -v` passes.
- [ ] GitHub Actions Rules CI passes on push and pull-request events.
- [ ] Pull Request #12 remains Draft until the corrected validator is merged to `main` and all required gates are rerun.

## 9. Workflow after approval

1. Merge this contract-only amendment Pull Request.
2. Implement the validator transition on `agent/studio-006-validator-transition`.
3. Run baseline, evaluated, negative-transition, evidence-register, and complete unit-test checks.
4. Independently review and merge the validator-transition Pull Request.
5. Reconcile Pull Request #12 with the corrected `main` baseline.
6. Rerun Official QA, Review and Integration, and GitHub Actions against the new immutable integration target.
7. Studio Owner decides the final Pull Request #12 disposition only after every required check is green.

## 10. Rollback and non-goals

Rollback is the ordinary revert of the later validator-transition implementation commit. Reverting this contract alone does not modify code.

This amendment does not authorize:

- weakening, disabling, skipping, or deleting Rules CI;
- changing the GitHub Actions workflow;
- reverting candidates to an unassessed state;
- modifying candidate evidence or recommendations;
- installing, importing, vendoring, executing, enabling, or adopting a candidate;
- changing historical content, gameplay, project canon, dependencies, runtimes, models, providers, engines, or platforms;
- merging Pull Request #12 while required checks are failing.
