# STUDIO-009D TASK

memory_schema_version: 1

task_id: STUDIO-009D
task_title: Provider onboarding framework
task_type: architectural provider-onboarding contract and later implementation
canonical_task_contract: tasks/STUDIO-009D.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-009D
project_studio: NONE

goal: |
  - Define and later implement a deterministic provider-neutral onboarding framework that every real `STUDIO-009P*` child must satisfy before connected activation.
allowed_scope: |
  - Contract checkpoint: tasks/STUDIO-009.md, tasks/STUDIO-009D.md, tasks/STUDIO-009D-IMPLEMENTATION.md, and this four-record package.
  - Future implementation: only the exact 25-path maximum boundary in tasks/STUDIO-009D-IMPLEMENTATION.md after this contract merges.
non_goals: |
  - No real provider approval, model call, endpoint probe, SDK/API/CLI, account discovery, credential resolution, live routing, connected execution, nonzero spend, external write, deployment, publication, or release.

responsible_role: Platform Studio / Provider Integration Cell
review_target: QA-01 and REVIEW-INTEGRATION-01, then Studio Owner

acceptance_criteria: tasks/STUDIO-009D.md and tasks/STUDIO-009D-IMPLEMENTATION.md
accepted_constraints: |
  - AGENTS.md
  - docs/DECISIONS.md
  - studio/MEMORY_PROTOCOL.md
  - tasks/STUDIO-009.md
  - tasks/STUDIO-007F.md
  - tasks/STUDIO-009A.md
  - tasks/STUDIO-009B.md
  - tasks/STUDIO-009C.md
  - platform/orchestration/PROVIDER_ADAPTER.md
  - platform/connectivity/CREDENTIAL_BROKER.md
  - platform/connectivity/SECRET_LIFECYCLE.md

created_at: 2026-09-03T07:49:07Z
authorized_amendments: |
  - 2026-09-03: Studio Owner completed STUDIO-009C closeout and directed continuation to STUDIO-009D contract work.

notes: |
  - This package grants no provider, credential, network, routing, budget, gate, merge, deployment, publication, or release authority.
<!-- STUDIO-009D-IMPLEMENTATION-CHECKPOINT-0001 -->
# STUDIO-009D implementation checkpoint

implementation_branch: agent/studio-009d-provider-onboarding
implementation_base: 5da4b292a5fe8ef9dcb75c1446fd0dae8ea40dc0
implementation_status: IMPLEMENTED - QA PENDING
implementation_paths: 21
memory_paths: 4
focused_tests: 323 PASS
total_tests: 720 PASS
new_009d_tests: 60 PASS
schemas: 5
fixtures: 10
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
secret_store_activity: NONE
connector_runtime_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO
checkpoint_at: 2026-09-03T08:41:46Z
exact_next_action: Open the implementation Pull Request, preserve the immutable head, then perform independent QA-01.
<!-- STUDIO-009D-IMPLEMENTATION-PR-CHECKPOINT-0002 -->
# Implementation Pull Request checkpoint

implementation_pr: https://github.com/huynhphananhkhoi11-cloud/game-studio-harness/pull/48
implementation_first_commit: 34eaf9efad80992ef2e1718810386f00d3f65361
pr_checkpoint_at: 2026-09-03T08:41:52Z
disposition: OPEN - QA and Review pending; Studio Owner merge decision remains separate