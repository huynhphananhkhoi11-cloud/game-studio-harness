# STUDIO-009R-01 TASK

memory_schema_version: 1

task_id: STUDIO-009R-01
task_title: Progressive Live Activation Amendment
task_type: governance amendment and later offline live-validation framework
canonical_task_contract: tasks/STUDIO-009R-01.md
implementation_contract: tasks/STUDIO-009R-01-IMPLEMENTATION.md
memory_root: studio/memory/tasks
package_path: studio/memory/tasks/STUDIO-009R-01
project_studio: NONE

goal: |
  - Split provider-specific connected validation from final STUDIO-009F integrated acceptance.
  - Preserve Owner authority, zero-cost operation, provider-specific contracts, and fail-closed evidence.

allowed_scope: |
  - Contract/reconciliation only in the exact nine paths authorized by the STUDIO-009R-01 contract runner.
  - Later implementation is separately bounded by tasks/STUDIO-009R-01-IMPLEMENTATION.md and is not authorized until this contract PR merges.

non_goals: |
  - No credential resolution, provider/network/model call, routing, real tool execution, Unity/game repository work, deployment, publication, or spend.
  - No selection of P-03/P-04/P-05 provider/model identities.

responsible_role: Platform Studio / Connected Validation Governance Cell
review_target: Rules CI and Studio Owner contract merge; later independent QA and Review apply to implementation.

task_status: IMPLEMENTATION_READY_FOR_QA
contract_record_semantics: EFFECTIVE_WHEN_MERGED
money_ceiling: 0
provider_runtime_activity: NONE
network_activity: NONE
credential_runtime_activity: NONE
routing_activity: NONE
connected_execution_activity: NONE
spend: ZERO
next_phase_after_contract_merge: STUDIO-009R-01_IMPLEMENTATION_QA

implementation_contract_pr: 56
implementation_contract_head: b163e0ddc4007f12c749f4f3db438287a666782b
implementation_contract_merge: 6902b2a656b24a37b5a573867cab57d75a13feb9
implementation_branch: agent/studio-009r-01-implementation
implementation_scope_paths: 17
implementation_cumulative_pr_paths: 21
implementation_new_tests: 50
implementation_expected_focused_tests: 457
implementation_expected_total_tests: 854
implementation_runtime_activity: NONE
implementation_spend: ZERO
<!-- STUDIO-009R-01-IMPLEMENTATION-CHECKPOINT-0002 -->
