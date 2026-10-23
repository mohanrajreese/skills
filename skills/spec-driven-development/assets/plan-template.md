# Plan NNN: <feature name>

Spec: ./spec.md · Constitution check: <pass / exceptions with reason>

## Approach
Short description of the solution and why it beats the alternatives considered.

## Stack and components
Layers touched (web / API / mobile / DB / integrations). New technology? Link the ADR.

## Data model and migrations
Tables/collections, fields, indexes, RLS/rules; migration safety notes (see postgres skill).

## Interfaces
API endpoints / server actions / events / webhooks with request and response shapes.

## Security and privacy
Threats (top 3), authz checks, personal data handled, secrets.

## Cost and limits
New per-unit costs (LLM tokens, WhatsApp messages, payments), quotas, guardrails.

## Test strategy
Unit / integration / e2e coverage per acceptance criterion.

## Risks and mitigations
| Risk | Likelihood | Impact | Mitigation |

## Rollout
Feature flag, migration order, backfill, monitoring, rollback.
