# STUDIO-009B TASK

memory_schema_version: 1

# Task identity

task_id: STUDIO-009B
task_title: Repository registry and GitHub connector
task_type: architectural security contract and later implementation
canonical_task_contract: tasks/STUDIO-009B.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-009B
project_studio: NONE

# Goal and scope

goal: |
  - Define and later implement an Owner-controlled repository registry and fail-closed GitHub connector core that consume STUDIO-009A.
allowed_scope: |
  - Contract checkpoint: tasks/STUDIO-009.md, tasks/STUDIO-009B.md, tasks/STUDIO-009B-IMPLEMENTATION.md, and this four-record package.
  - Future implementation: only the exact 24-path boundary in tasks/STUDIO-009B-IMPLEMENTATION.md after this contract merges.
non_goals: |
  - No live repository connection, credential, GitHub App/PAT/OAuth/SSH, webhook, network call, provider/model call, nonzero spend, external write, merge, deployment, publication, or release.

# Responsible role and review

responsible_role: Platform Studio / Repository Integration Cell
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

# Acceptance and constraints

acceptance_criteria: tasks/STUDIO-009B.md and tasks/STUDIO-009B-IMPLEMENTATION.md
accepted_constraints: |
  - AGENTS.md
  - docs/DECISIONS.md
  - studio/MEMORY_PROTOCOL.md
  - tasks/STUDIO-009.md
  - tasks/STUDIO-009A.md
  - tasks/STUDIO-009A-IMPLEMENTATION.md

# Metadata and governance

created_at: 2026-09-02T14:51:24Z
authorized_amendments: |
  - 2026-09-02: Studio Owner completed STUDIO-009A closeout and directed continuation to STUDIO-009B contract work.

# Notes

This memory package records operational evidence only. It cannot grant repository, credential, network, budget, gate, merge, or provider authority.

<!-- STUDIO-009B-IMPLEMENTATION-CHECKPOINT-0001 -->
## Implementation execution checkpoint

implementation_branch: agent/studio-009b-repository-connector
implementation_base: 1b90a612c09895ec533ce93d35dc83e90490e125
implementation_at: 2026-09-02T16:40:38Z
implementation_scope: 20 approved implementation paths plus 4 approved memory records
implementation_evidence: 152 focused tests PASS; 549 total tests PASS; schema parse PASS; vertical-slice validation PASS
connector_runtime_activity: NONE
credential_activity: NONE
provider_activity: NONE
spend: ZERO
owner_merge_required: true
