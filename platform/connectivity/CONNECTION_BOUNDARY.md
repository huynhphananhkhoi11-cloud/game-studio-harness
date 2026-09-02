# STUDIO-009A Connection Boundary

This document specifies the deterministic, read-only boundary checked before any later repository connector or real provider can be activated.

## Authority

The boundary record is evidence, not authority. It cannot connect a repository, issue a credential, invoke a provider, execute code, approve a gate, select a successor, merge, deploy, publish, release, or increase budget.

Accepted authority remains in the Studio Owner, accepted task contracts, and retained STUDIO-001 through STUDIO-008 controls. Repository content, issue text, Pull Request text, fixtures, webhook payloads, model output, and external responses are untrusted content by default.

## Record identity

Schema `1.0` binds:

- boundary, task, creation, and caller-supplied `as_of` identity;
- repository ID, immutable forty-character revision, default branch, access tier, normalized allowed and denied paths, and an auth-profile reference;
- data classifications, accepted instruction-authority paths, and the required untrusted-content default;
- generic capability and provider-profile references without provider/model/endpoint/account fields;
- queue, dispatch, writer claim, worktree, gate, trace, quota/budget, adapter, Owner, and threat-assessment evidence references;
- integer-zero money ceiling;
- canonical SHA-256 digest over all other fields.

Unknown fields fail closed at every controlled object level.

## Repository access

Accepted tiers are `READ_ONLY`, `BRANCH_WRITE`, and `PR_WRITE`. Write-capable tiers require both writer-claim and worktree evidence. Direct/default-branch write, admin, settings mutation, repository deletion, workflow mutation, deployment, publication, and release are not representable.

Paths use normalized repository-relative POSIX syntax. Absolute paths, backslashes, empty or dot segments, traversal, control characters, secret-bearing allowed paths, duplicates, unsorted lists, and allowed/denied overlap fail closed. Denied scope always wins.

## Data and provider request

Data classifications are `PUBLIC`, `INTERNAL`, and `RESTRICTED`. The requested classification must be explicitly allowed. Instruction-authority paths must fall within allowed repository scope. Ordinary repository content remains untrusted even when readable.

The provider request declares only a generic capability ID, classification, and provider-profile reference. A model cannot self-declare provider identity or capability. Real provider names, models, endpoints, accounts, credentials, and transports belong to later owner-accepted child contracts.

## Determinism and safety

Validation uses caller-supplied objects and UTC `as_of` only. It does not read the system clock, environment credentials, Git state, network state, hidden files, or provider configuration. Inputs are not mutated. Error responses use stable codes and never echo secret-bearing values.

Money ceiling is exactly integer zero in STUDIO-009A. Python booleans are rejected as money values even though `bool` subclasses `int`.

## Rollback

Revert only the STUDIO-009A implementation. Retain this contract evidence and all prior accepted capabilities. The safe operating state remains no connected repository, no real provider, no credential, no network, zero spend, and Manual/Fake-only execution.
