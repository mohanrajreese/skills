---
name: domain-learning
description: Learn a new business domain quickly and turn it into reusable knowledge, covering glossary and core entities, actors and workflows, rules and regulators (RBI, SEBI, IRDAI, GSTN, TRAI, MeitY, FSSAI and others), India's digital public infrastructure and industry APIs (UPI, ONDC, Account Aggregator, DigiLocker, GST e-invoicing), competitors, open questions for subject experts, then a domain brief and seed skills. Use whenever starting a project in an unfamiliar industry or domain such as logistics, healthcare, insurance, lending, education, restaurants, real estate or GST and accounting, when a client describes processes we don't know, or when someone asks to "learn this domain", "understand this industry" or "make a skill for this domain".
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [meta, learning, domain, research]
---

# Domain learning

Code built without understanding the domain encodes the wrong rules. This
skill gets us to a working model of a new domain in hours, captures it so
the next project starts ahead, and grows domain skills over time.

## Steps

1. **Glossary first.** List the domain's terms with plain definitions and
   the synonyms customers use (e.g. logistics: AWB, RTO, NDR, COD, manifest).
   Ambiguous words cause most requirement bugs.
2. **Entities and relationships.** The nouns (order, shipment, policy,
   claim, patient, invoice) and how they relate. Sketch the core data model.
3. **Actors and workflows.** Who does what, in which order, today ("as-is"),
   including the paper/WhatsApp/Excel steps we might replace. Note pain points
   and where money and risk move.
4. **Rules and regulators.** Which laws, regulators and standards apply
   (India examples: RBI payments/lending, SEBI securities, IRDAI insurance,
   GSTN/CBIC tax and e-invoicing, TRAI messaging, MeitY IT/DPDP, FSSAI food,
   NMC/ABDM health). Note licences needed and what we must never do. Use
   `india-it-compliance` and `data-security` for cross-cutting ones.
5. **Existing rails and APIs.** Infrastructure we should plug into rather
   than rebuild: UPI, Account Aggregator, DigiLocker, ONDC, GST e-invoice/
   e-way bill, industry aggregators (shipping, labs, insurers). Check
   access requirements (licences, approvals, sandbox).
6. **Market map.** Main competitors and substitutes, what customers like or
   hate about them, and pricing norms (`pricing`).
7. **Questions for experts.** Write the list of unknowns, ask the client or
   a subject expert, and record the answers with dates.
8. **Capture:**
   - `research/YYYY-MM-DD-domain-<name>.md` with sourced facts
     (`skill-research` rules: primary sources, dated).
   - `docs/domains/<name>.md`: the **domain brief** (format below), kept
     current.
   - If the domain will recur, a seed skill via `skill-forge`
     (e.g. `logistics-india`), plus backlog lines for sub-topics.

## Domain brief format

```markdown
# Domain: <name> (updated <date>)
Glossary: term — meaning (synonyms)
Entities & relationships: …
Actors & key workflows (as-is → opportunities): …
Rules, regulators, licences; things we must never do: …
Rails / APIs to integrate: …
Competitors & pricing norms: …
Open questions (owner, date asked, answer): …
Sources: …
```

## Pitfalls

- Copying a competitor's data model without understanding why it's shaped
  that way.
- Treating regulatory points from blogs as settled; confirm with primary
  sources or counsel.
- Keeping domain knowledge only in chat or one person's head. If it isn't
  in the brief, it isn't learned.
