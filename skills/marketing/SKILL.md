---
name: marketing
description: How we market our products and our clients' businesses, covering positioning and messaging, ideal customer profiles, channel choice for Indian SMB, D2C and SaaS (WhatsApp, Meta and Google ads, SEO and content, email, Shopify App Store, partnerships, referrals), funnel metrics and unit economics, tracking plans with UTMs and server-side events, landing pages, experiments, and Indian marketing compliance (TRAI DLT and 140/1600 series, WhatsApp opt-in, DPDP consent, email sender rules, ASCI disclosures, dark patterns). Use whenever planning a launch or campaign, writing positioning or ad copy briefs, choosing marketing channels, setting up analytics or attribution, building landing pages, or checking marketing messages for compliance. For Facebook and Instagram specifics use meta-marketing.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [marketing, growth, analytics, india]
---

# Marketing

Marketing that works is specific (one customer, one problem, one promise),
measured (every channel has a number), and lawful (consent first).
Engineering matters here too: broken tracking means decisions made blind.

## 1. Positioning (before any campaign)

Write one page:

```markdown
For <ideal customer> who <problem/trigger>, <product> is a <category>
that <key benefit>. Unlike <main alternative>, we <differentiator>.
Proof: <numbers, testimonials, logos>.   Objections + answers: …
```

Make the ICP concrete: industry, size, location/language, the moment they
start looking, who decides and who pays.

## 2. Pick 1–2 channels to start, not everything

| Channel | Works best for | Notes |
|---|---|---|
| WhatsApp (opt-in lists, Click-to-WhatsApp ads) | India B2C/D2C, SMB owners | Highest engagement; template rules and costs (`whatsapp-integration`) |
| Meta ads (FB/IG) | D2C, consumer apps, local businesses | `meta-marketing` for Pixel/CAPI, catalogs, Advantage+ |
| Google Search ads | High-intent searches ("billing software for clinics") | Expensive keywords; landing page quality matters |
| SEO + content | B2B SaaS, long-term | Slow; compounding; pick topics from real customer questions |
| Shopify App Store listing | Shopify apps | Listing copy, screenshots, reviews, category ranking |
| Email | Retention, B2B nurture | Needs authenticated sending and consent |
| Partnerships / referrals / communities | SMB SaaS in India | Accountants, agencies, trade associations, referral credits |

## 3. Measure the funnel

- Funnel: impressions → clicks → signups/leads → activated → paying →
  retained/expanded. Track conversion between each step.
- Unit economics per channel: **CAC**, payback months, **LTV:CAC** (aim
  ≥ 3), ROAS for e-commerce. Compare with `pricing` and
  `cloud-cost-planning`.
- **Tracking plan** in the repo: event names (`signup_completed`,
  `order_placed`), properties, which tool receives them. Fire key
  conversions **server-side** too (more reliable than browser-only).
- **UTM convention:** lowercase, fixed vocab: `utm_source=meta|google|whatsapp|newsletter`,
  `utm_medium=paid_social|cpc|message|email`, `utm_campaign=<yyyy-mm>-<name>`.
  Persist first-touch and last-touch UTMs on the user/lead record.
- Never put PII (email, phone) in URLs or analytics event properties.

## 4. Landing pages and experiments

- One page per audience/offer: headline = the promise, proof above the fold,
  one primary CTA, fast on mid-range Android over 4G, Indian formats (₹,
  lakh/crore where natural, vernacular if the ICP needs it).
- Experiments: one variable, a pre-stated metric, enough traffic for the
  difference you care about; stop on the plan, not on a lucky day.

## 5. Compliance (India-first)

- **SMS/calls (TRAI TCCCPR):** register headers and templates on DLT;
  promotional calls only from **140-series**, service/transactional from
  **1600-series** (phased); no telemarketing from ordinary 10-digit numbers;
  honour opt-outs. Violations escalate to number bans and blacklisting.
- **WhatsApp:** explicit opt-in, approved templates, easy opt-out
  (`whatsapp-integration`).
- **Consent and data (DPDP):** collect marketing consent separately from
  service consent, record it, make withdrawal easy. Core obligations apply
  from 2027-05-13; build it now (`data-security`).
- **Email:** SPF, DKIM and DMARC on sending domains, one-click unsubscribe,
  low complaint rates (major inbox providers enforce this for bulk senders).
- **Advertising standards:** truthful, provable claims; ASCI rules; influencer
  posts disclosed (#ad / "Paid partnership").
- **No dark patterns** (CCPA 2023): fake urgency/scarcity, hidden charges,
  pre-ticked add-ons, hard-to-cancel subscriptions (`india-it-compliance`).

## Campaign brief format

```markdown
# Campaign: <name> (<dates>)
Goal + metric: <e.g. 200 trial signups at CAC ≤ ₹800>
Audience: …   Offer: …   Channels + budget split: …
Message: headline, 3 proof points, CTA
Tracking: UTMs, events, dashboard link
Compliance check: consent, DLT/templates, claims substantiated, no dark patterns
Review date and decision rule: <scale / fix / stop>
```

## Sources

- `research/2026-10-23-marketing-india-compliance.md` (TRAI 2025 amendment,
  DPDP timeline; prior-knowledge items listed there).
