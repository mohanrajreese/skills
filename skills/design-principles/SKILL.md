---
name: design-principles
description: Apply KISS, YAGNI, DRY with the rule of three, SOLID, separation of concerns and Kent Beck's rules of simple design pragmatically, and actively prevent overengineering such as speculative abstractions, needless layers, premature optimization, gold-plating and framework-building, while not underengineering things that are expensive to retrofit. Use whenever designing a module, service or feature, reviewing a plan or diff for complexity, deciding whether to add an abstraction, interface, pattern, config option, dependency or service, when someone asks "is this overengineered", "keep it simple", "do we need this", mentions KISS, YAGNI or SOLID, or when an AI agent's output adds layers nobody asked for.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [engineering, design, principles, simplicity]
---

# Design principles and overengineering prevention

The goal is code that is easy to understand and cheap to change. The
principles below are tools for that goal, not laws. When they pull in
different directions, **readability and ease of change win.**

## The principles, applied

| Principle | What it means for us | Typical violation |
|---|---|---|
| **KISS** | The simplest design that meets today's requirements. Boring, obvious code beats clever code. | A generic engine where three `if` branches would do |
| **YAGNI** | Build for requirements that exist now, not ones we imagine. Adding it later is usually cheaper than carrying it. | Config flags, plugin systems or "multi-provider" support with one provider |
| **DRY (rule of three)** | One source of truth for each piece of *knowledge* (a business rule, a price, a schema). Tolerate similar-looking code until the third repeat; the wrong abstraction costs more than duplication. | Merging two code paths that only look alike, then piling flags on to split them again |
| **Separation of concerns** | UI ↔ state ↔ domain ↔ data access ↔ external integrations stay separate (see the stack skills' layering). | Razorpay calls inside a React component; SQL in templates |
| **Beck's simple design** | In order: passes the tests, reveals intention, no duplication, fewest elements. | Extra classes "for structure" that add nothing |

### SOLID, pragmatically

- **S: Single responsibility.** A module has one reason to change. Split
  when two *different* stakeholders change the same file for different
  reasons, not just because it got long.
- **O: Open/closed.** Make code easy to extend *once a second variant
  actually exists*. Don't add extension points in advance.
- **L: Liskov substitution.** If something implements an interface or
  subclass, it must honour the whole contract: no surprise exceptions, no
  ignored methods.
- **I: Interface segregation.** Small interfaces, defined where they are
  *used* (idiomatic in Go; same idea for TS types and Python Protocols).
- **D: Dependency inversion.** Depend on abstractions **at boundaries**:
  payment gateway, WhatsApp client, LLM client, clock, email. Fakes then
  make tests easy. Don't put an interface in front of every internal class.

Prefer composition over inheritance. Prefer functions and data over class
hierarchies when there's no state to encapsulate.

## Overengineering prevention

**Before adding any abstraction, layer, pattern, config option, dependency
or service, answer these:**

1. Which requirement *today* needs it? (Name the ticket or acceptance
   criterion.)
2. What breaks, or gets painful, if we don't add it?
3. How hard would it be to add later, when needed?
4. Does it make the code easier for a newcomer to read?

If the answers are "none, nothing, easy, no" → **don't add it.**

**Red flags:**

- An interface or abstract class with one implementation and no testing need.
- Factory, strategy, plugin or registry for a single case.
- A "framework", base class or generic utility built before three real
  uses.
- Config options or feature flags nobody has asked to change.
- Microservices, event buses, CQRS, Kubernetes or a message queue for a
  product with a few thousand users and one team.
- Caching, sharding or async rewrites without a measured bottleneck
  (premature optimisation).
- Wrapping the ORM or framework "in case we switch". We won't, and the
  wrapper leaks.
- New dependencies for something the standard library does in a few lines.
- Deep inheritance, layers that only forward calls, DTO-to-DTO mapping chains.
- "Future-proof", "flexible" or "generic" used as the justification.

**Pushback with AI agents:** coding agents add layers, options and
defensive code by default. Instruct: *"Implement the minimal change that
satisfies the acceptance criteria. No new abstractions, config options or
dependencies unless a current requirement needs them."* Then review the
diff for the red flags.

## …but don't underengineer

Some things are cheap now and expensive later. Do these from the start:

- Input validation, authorization checks, error handling, tests for core
  behaviour.
- Data foundations: `org_id` on tenant data, proper keys, `timestamptz`,
  integer money, safe migrations (`saas`, `postgres`).
- Idempotency for webhooks and payments; audit logs for money and admin
  actions.
- Versioning for *public* APIs and webhooks other people consume.
- Seams (dependency inversion) around external services, for testing.

## Using this in reviews

For a plan or diff, list: what could be removed or simplified without
losing a requirement; which abstractions lack a second use; which
"cheap now, expensive later" items are missing. Suggest the smaller design
concretely, e.g. "replace the `NotifierFactory` + 3 classes with one
`send_whatsapp()` function until a second channel exists".

## Sources

- `research/2026-10-23-engineering-principles.md`.
