# TASK.md — memory package TASK template

memory_schema_version: 1

# Task identity

task_id: <TASK-ID>
task_title: <Short title>
task_type: <task type or handoff level>
canonical_task_contract: <path or identifier to canonical task contract>
memory_root: <repository-relative memory root for package>
package_path: <full repository-relative path to this package folder>
project_studio: <project_studio_id or NONE>

# Goal and scope

goal: |
  - <concise goal statement>
allowed_scope: |
  - <file or directory globs or explicit file list>
non_goals: |
  - <explicit non-goals>

# Responsible role and review

responsible_role: <logical role or Cell>
review_target: <review role or integration target>

# Acceptance and constraints

acceptance_criteria: <path or reference>
accepted_constraints: |
  - <reference to docs/DECISIONS.md or other accepted decisions>

# Metadata and governance

created_at: <ISO 8601 timestamp with tz>
authorized_amendments: |
  - <who/when/reference>

# Notes

This TASK.md is the stable execution index for a single memory package. It records the authorized scope and references the canonical task contract. It must not be used to broaden the canonical task contract or to record dynamic execution state (use STATE.md for current state). Any amendment to scope or acceptance must cite the authority that authorized the change and be appended to `authorized_amendments` with a timestamp and reference.