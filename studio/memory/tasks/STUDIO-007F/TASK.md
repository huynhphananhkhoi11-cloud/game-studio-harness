# STUDIO-007F Task Memory

## Objective

Implement a provider-neutral request/result boundary with only deterministic `MANUAL` and `FAKE` adapters in v1.0.

## Authorization

The contract merged through PR #31 at `3e678e8beb480e8d1aaa1c0aa8a85baccfbb64b8`. Implementation is authorized only on `agent/studio-007f-provider-adapter`.

## Implementation scope

- nineteen new documentation, schema, fixture, validator, and test paths listed in `tasks/STUDIO-007F-IMPLEMENTATION.md`;
- four materially updated STUDIO-007F memory paths;
- maximum 23 changed paths.

## Safety boundary

- standard library, caller-supplied time, safe references, and immutable evidence only;
- only `MANUAL` result normalization and deterministic `FAKE` simulation;
- zero monetary usage;
- no provider, model, endpoint, account, credential, network, subprocess, Git mutation, execution, gate approval, merge, publication, or deployment.

## Completion boundary

Implementation remains unmerged until Rules CI, independent QA, independent Review and Integration, and the Studio Owner accept one immutable head. A separate closeout Pull Request is still required.
