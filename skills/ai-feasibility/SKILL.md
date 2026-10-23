---
name: ai-feasibility
description: Assess whether a feature is a good fit for AI or LLMs and whether it is compatible with our stack, data and policies, before building it. Covers task fit, accuracy needed versus cost of errors, data and privacy, latency, per-request and monthly cost estimates, model choice, SDK and platform compatibility (Flutter, WhatsApp, Shopify, AWS Bedrock, Vertex), an eval plan with go/no-go thresholds, and fallbacks. Use whenever someone asks "can we use AI for X", "is this feasible with AI", "which model should we use", "how much will the AI cost", or proposes an AI, chatbot, agent or automation feature.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [ai, feasibility, planning]
---

# AI feasibility and compatibility

Answers three questions with evidence: **Can a model do this well enough?
Can we afford it at scale? Can we ship it within our stack, data rules and
platform policies?** Produces a scorecard with a go / spike / no-go verdict.

## Steps

1. **Restate the job** as input → output, e.g. "WhatsApp message in
   Hinglish → order intent + items (JSON)". Who sees the output, and what
   happens if it's wrong?
2. **Task fit.** Strong fits: extraction, classification, summarisation,
   drafting, search over our own content, conversational support within a
   narrow domain, code generation with tests. Weak fits: exact arithmetic or
   accounting (use code), decisions with legal/financial liability without
   review, facts the model can't access. Mostly deterministic jobs belong in
   rules, not an LLM.
3. **Accuracy vs cost of error.** Define the bar (e.g. ≥95% correct
   extractions on our eval) and the failure handling: human review queue,
   confidence threshold, undo, or fall back to non-AI flow.
4. **Data and privacy.** What personal or confidential data goes into
   prompts? Is it allowed under our terms, DPDP/GDPR duties and the
   provider's data terms? Can it be minimised or masked? Data residency
   needs may point to Claude on AWS Bedrock or Google Vertex.
5. **Compatibility with our stack.**
   - Official Anthropic SDKs exist for Python, TypeScript, Go and others;
     **Flutter/Dart has none**, so call through our backend (never ship API
     keys in apps).
   - WhatsApp: business-specific bots are allowed, general-purpose AI
     assistants aren't (`whatsapp-integration`).
   - Shopify: run AI in the app backend; respect API rate limits.
   - Serverless timeouts vs long model turns: stream, or use background jobs.
6. **Latency.** Interactive (under ~2–5 s to first token), async (seconds
   to minutes) or batch (hours, ~50% cheaper via batch APIs)? Pick the UX to
   match.
7. **Cost estimate** (prices from the provider's pricing page, dated):
   ```text
   cost/request = input_tokens × input_price + output_tokens × output_price
                  (cached input billed at the lower cache-read rate)
   monthly      = cost/request × requests/user/month × active users
   ```
   Example at prices checked 2026-10-23 (Claude Haiku 5.5 $0.10 / $0.50 per
   MTok; Sonnet 5.5 $2 / $10; Opus 5.5 $4 / $20): 2,000 in + 300 out tokens
   ≈ $0.00035 on Haiku 5.5, $0.007 on Sonnet 5.5, $0.014 on Opus 5.5. Then
   compare per-user AI cost with the plan price (`pricing`).
8. **Model choice.** Start with the most capable sensible model to prove
   feasibility, then step down (effort first, then model) while the eval
   still passes.
9. **Eval plan.** 20–50 real, labelled examples (including hard and
   adversarial ones), a scoring method, and the go/no-go threshold. A quick
   spike against the eval beats debate.
10. **Write the scorecard** and hand off: go → `ai-agents` +
    `spec-driven-development`; spike → time-boxed experiment; no-go →
    non-AI alternative.

## Scorecard format

```markdown
# AI feasibility: <feature> (<date>)
Job: <input → output>        Users/volume: <…>
| Dimension | Finding | Risk (L/M/H) |
| Task fit | | |
| Accuracy bar & error handling | | |
| Data & privacy | | |
| Stack & platform compatibility | | |
| Latency & UX | | |
| Cost (per request / per month / % of plan price) | | |
| Model choice | | |
Eval plan: <dataset, metric, threshold>
Verdict: GO / SPIKE (what, how long) / NO-GO (alternative)
```

## Sources

- Model prices and capabilities: the `claude-api` skill (cached
  2026-10-06) and `research/2026-10-23-product-platform-baseline.md`.
  Re-check prices before quoting them to anyone.
