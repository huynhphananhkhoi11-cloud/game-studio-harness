# Cloudflare Workers AI provider child - STUDIO-009P-02

This directory is an offline/synthetic implementation of the merged STUDIO-009P-02 contract.

Provider: Cloudflare Workers AI
Exact model: `@cf/nvidia/nemotron-3-120b-a12b`
Provider profile state: `DISABLED`
Model state: `DECLARED`
Money ceiling: `0`
Connected authority: `NONE`

The implementation validates deterministic provider/model/account-reference/transport/data/quota/budget metadata and normalizes synthetic requests, responses, errors, quota evidence, and local tool requests.

It does not discover a Cloudflare account, resolve an Account ID, create or resolve an API token, construct live HTTP transport, call Workers AI, enable AI Gateway or billing, use storage services, execute tools, route work, or spend money.

Real connected activation remains gated by STUDIO-009F. Future routing/failover remains governed by STUDIO-009E.
