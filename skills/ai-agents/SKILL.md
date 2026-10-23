---
name: ai-agents
description: How we design and build AI features and agents into our products, covering when an agent is warranted versus a single LLM call or workflow, choosing between the Claude API with tools, the Tool Runner, Managed Agents and the Claude Agent SDK, model choice, tool and MCP server design, guardrails against prompt injection and excessive agency, human approval, cost and loop limits, evals, and observability. Use whenever building a chatbot, copilot, RAG, extraction pipeline, autonomous or multi-step agent, MCP server, or AI feature in a web, mobile, WhatsApp or Shopify product, or when choosing an LLM or agent framework. Load the claude-api skill too before writing Claude API code.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [ai, agents, llm, mcp]
---

# AI agents

Start with the simplest thing that works: one call, then a workflow, then an
agent. Agents earn their cost only when the task is open-ended **and**
mistakes can be caught and undone.

## Before you start

1. Run `ai-feasibility` if nobody has yet checked fit, accuracy needs and cost.
2. Check the project for an existing LLM provider or framework (Anthropic
   SDK, Vercel `ai`, OpenAI, LangChain, Genkit). Follow it; don't add a
   second one.
3. **Before writing Claude API code, load the `claude-api` skill.** Its
   API details are authoritative and current; this skill covers design, not
   SDK syntax.

## Pick the tier

| Tier | Use for | Build with |
|---|---|---|
| Single call | Classify, extract, summarise, draft, answer from given context | Claude API (structured outputs for JSON) |
| Workflow | Fixed multi-step pipeline; code decides the steps | Claude API + tools; your code orchestrates |
| Agent | Open-ended, model chooses steps and tools | Tool Runner (your tools, your infra), **Managed Agents** (Anthropic hosts loop + sandbox; scheduled or long-running), or **Claude Agent SDK** (Claude Code harness with file/bash tools, self-hosted) |

An agent is justified only if all four hold: the task is complex, the value
justifies the cost and latency, the model is capable at it, and errors are
recoverable (tests, review, rollback).

## Defaults (checked 2026-10-23)

- Model: `claude-opus-5-5` by default; `claude-sonnet-5-5` or
  `claude-haiku-5-5` for high-volume sub-steps once evals show quality
  holds. Use the exact IDs; check the `claude-api` skill for the current list.
- Thinking: adaptive; tune `effort` per route instead of switching models
  first.
- Prompt caching on stable system prompts and tool definitions.
- Structured outputs or strict tools for anything code consumes.
- Mobile apps (Flutter) and browsers **never** call the LLM directly with a
  key; route through our backend, which adds auth, limits and logging.

## Tools and MCP

- Few, well-named tools with clear descriptions and strict schemas; return
  concise, structured results and helpful errors (`is_error: true`).
- Expose internal systems as an **MCP server** when more than one agent or
  client will use them. MCP spec **2026-07-28** is current (stateless: no
  session handshake). Use the official SDKs (`@modelcontextprotocol/sdk`,
  Python `mcp`) and authenticate every server.
- Tools that change the world (send WhatsApp, refund via Razorpay, edit
  Shopify orders, delete data) need **human approval** or tight
  allow-lists, idempotency keys and audit logs.

## Guardrails (OWASP GenAI LLM Top 10 2026)

- **Prompt injection:** treat user text, documents, web pages, emails and
  tool results as untrusted data. Never let them grant permissions. Keep
  operator instructions in system/operator channels.
- **Excessive agency:** least-privilege tools, scoped credentials per
  tenant, approval gates for irreversible actions.
- **Unbounded consumption:** per-user/org token, cost and step limits;
  timeouts; kill switch.
- **Output handling:** validate before executing, rendering (XSS) or
  storing model output.
- **Sensitive data:** minimise personal data in prompts; check the
  provider's data terms against DPDP/GDPR duties.

## Evals and observability

- Build a small eval set from real examples **before** tuning prompts:
  inputs, expected outputs or a rubric, pass threshold. Re-run on every
  prompt, model or tool change (the `claude-api` skill has eval guides).
- Log per request: model, tokens in/out, cache hits, latency, tool calls,
  cost, outcome. Watch cost per *completed task*, not per call.

## Changed recently (checked 2026-10-23)

- Current Claude models: Opus 5.5 (default), Sonnet 5.5, Haiku 5.5, Fable 5.1
  (most capable). Older code can break: assistant **prefill is rejected**,
  forced `tool_choice` (`any`/`tool`) returns 400 on Opus 5.5 / Sonnet 5.5 /
  Fable 5.1, `budget_tokens` thinking is replaced by adaptive thinking +
  effort, and `temperature`/`top_p`/`top_k` are rejected from API version
  2026-10-21. Use `claude-api`'s `migrate` flow for old code.
- WhatsApp bans general-purpose AI assistants on the Business API; business
  support bots are fine (see `whatsapp-integration`).

## Sources

- `research/2026-10-23-product-platform-baseline.md` → AI agents section
  (claude-api skill, registries, MCP spec repo, OWASP GenAI).
