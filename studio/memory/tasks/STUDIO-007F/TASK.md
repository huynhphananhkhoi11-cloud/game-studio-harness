# STUDIO-007F Task Memory

## Objective

Define and later implement a provider-neutral adapter boundary with only deterministic `manual` and `fake` adapters in v1.0.

## Current authorization

Contract-only work is authorized. Runtime implementation is not authorized until the contract Pull Request merges.

## Contract Pull Request scope

Exactly six paths:

- `tasks/STUDIO-007F.md`
- `tasks/STUDIO-007F-IMPLEMENTATION.md`
- the four files in `studio/memory/tasks/STUDIO-007F/`

## Accepted constraints

- zero cost and no real provider;
- no SDK, account, credential, secret, network, subprocess, Git mutation, merge, publication, or execution;
- exact request/result/capability allowlists;
- real providers require separate change control.

## Completion boundary

STUDIO-007F becomes COMPLETE only after contract merge, bounded implementation, Rules CI, independent QA, independent Review and Integration, Owner merge, and a separate merged closeout Pull Request.
