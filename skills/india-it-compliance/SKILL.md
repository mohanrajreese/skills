---
name: india-it-compliance
description: Engineering checklist for complying with Indian technology law and preventing violations, covering the IT Act 2000 sections that matter (43, 43A, 66C, 66D, 72A, 79, 85), SPDI Rules until the DPDP Act takes over in May 2027, CERT-In's 6-hour incident reporting and 180-day log rules, the IT Intermediary Rules 2021 with the 2025 and 2026 amendments (takedown timelines, AI and deepfake labelling), RBI data localisation and card tokenization, e-commerce rules and dark-pattern guidelines. Use whenever building or reviewing a product used in India, handling user data, user-generated content, AI-generated media, payments, marketplaces or security incidents, writing privacy policies, terms or grievance flows, or when someone mentions IT Act, CERT-In, intermediary rules, DPDP, SPDI or Indian cyber law.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [compliance, india, legal, security]
---

# India IT law compliance (engineering view)

Turns Indian tech law into **controls we build**. It is not legal advice:
use it to find what applies and to build preventions, then confirm with
counsel against the Gazette text.

## 1. Which rules apply to this product?

| If the product… | Applies |
|---|---|
| Collects any personal data | IT Act 43A + **SPDI Rules 2011** now; **DPDP Act 2023 + Rules 2025** core duties from **2027-05-13** (Section 43A is then omitted) |
| Runs any computer systems (everyone) | **CERT-In Directions 2022** (incidents, logs, clocks) |
| Hosts, transmits or lets users post content (chat, reviews, marketplace, social, UGC) | **IT Intermediary Rules 2021** + amendments (Section 79 safe harbour depends on them) |
| Lets users generate or edit images/video/audio with AI | 2026 amendment: **synthetic content labelling** |
| Takes payments / stores card or payment data | RBI: payment data localisation, card tokenization, e-mandates (`razorpay`) |
| Sells goods or services online, or is a marketplace | Consumer Protection (E-Commerce) Rules 2020, **CCPA dark-pattern guidelines 2023** |
| Sends SMS or calls for marketing/service | TRAI TCCCPR (`marketing`) |

## 2. IT Act sections and the prevention for each

| Section | What it covers | Prevention we build |
|---|---|---|
| 43 / 66 | Unauthorised access, data theft, damage; criminal if dishonest/fraudulent | Least privilege, MFA, audit logs, offboarding that revokes access same day |
| **43A** | Compensation if a company holding sensitive personal data is negligent with "reasonable security practices" (until 2027-05-13) | Documented security programme (ISO 27001-style), SPDI consent and privacy policy (`data-security`) |
| 66C | Identity theft (passwords, signatures, unique identifiers) | Hashed passwords, MFA, credential-stuffing protection, no shared accounts |
| 66D | Cheating by impersonation (phishing, fake support numbers) | Verified sender IDs, SPF/DKIM/DMARC, official support channels published, anti-phishing UX |
| 66E / 67 / 67A / 67B | Private images, obscene and child sexual abuse material | UGC moderation, fast removal paths, reporting, never store or forward CSAM |
| 69 / 69A / 69B | Lawful interception, blocking orders, traffic data | Process to receive and confidentially action government orders |
| 70B | CERT-In powers (the 2022 Directions) | Incident runbook (section 4) |
| **72A** | Disclosing personal data in breach of contract, without consent | Access controls on customer data, DPAs with vendors, staff confidentiality terms, export logging |
| **79** | Intermediary safe harbour, only with due diligence | Intermediary compliance (section 3) |
| 85 | Offences by companies: officers in charge can be liable | Named owners for each control; evidence of due diligence |

## 3. Intermediary duties (if users post or send content)

- Publish terms, privacy policy and user agreement; tell users what is
  prohibited, and remind them periodically.
- **Grievance officer** (resident in India) with a published contact;
  acknowledge complaints within 24 hours and resolve within 15 days.
- **Takedowns:** act on court orders or government notices. From
  2025-11-15 only senior officials (Joint Secretary / DIG and above) may
  issue Rule 3(1)(d) notices. From **2026-02-20**, court- or
  government-flagged unlawful content must come down within **3 hours**, and
  non-consensual intimate imagery within **2 hours** of a complaint. Build a
  takedown queue with timestamps, on-call ownership and an audit trail.
- **AI-generated media (from 2026-02-20):** if users can create or alter
  realistic audio/images/video, label it clearly, embed provenance metadata
  where feasible, and stop users from stripping labels. Large platforms
  (SSMIs, ≥ 5 million users) also need user declarations and more.
- Keep records of removed content and user registration data for 180 days
  (or longer when an investigation requires).

## 4. Security incidents (CERT-In Directions 2022)

- **Report specified incidents to CERT-In within 6 hours** of noticing:
  breaches, data leaks, unauthorised access, ransomware, compromise of
  critical systems, attacks on apps, and more. Prepare the form and contact in
  advance.
- **Keep logs of all ICT systems for 180 days, stored in India**:
  application, auth, firewall, DB audit, cloud audit logs (`aws`/`gcp`
  regions `ap-south-1` / `asia-south1`).
- **Sync clocks** to NIC/NPL NTP (or ensure cloud time sources trace to
  them) so logs line up.
- Name a **point of contact** for CERT-In.
- From 2027-05-13, also notify the **Data Protection Board** (immediate
  intimation + detailed report within 72 hours) and **each affected
  person** under DPDP.

## 5. Payments, commerce and consumer protection

- **RBI:** payment system data stored only in India (applies to payment
  operators and their partners); merchants must not store card numbers
  (use gateway tokenization); e-mandate rules for recurring debits.
- **E-commerce rules:** show seller details, total price, return/refund
  and cancellation terms, country of origin where required; grievance
  officer for consumers.
- **Dark patterns (CCPA 2023): never build** false urgency, basket
  sneaking, confirm-shaming, forced action, subscription traps (hard to
  cancel), interface interference, bait and switch, drip pricing, disguised
  ads, nagging, trick questions, SaaS billing traps or rogue malware.

## Prevention checklist (per release)

- [ ] Personal data inventory up to date; consent and notice text reviewed (`data-security`)
- [ ] Logs retained 180 days in India; clocks synced; CERT-In contact current
- [ ] Incident runbook includes the 6-hour CERT-In clock (and the DPDP Board from 2027-05-13)
- [ ] UGC/AI features: takedown queue meets the 3-hour/2-hour timelines; synthetic media labelled
- [ ] No dark patterns in signup, checkout, pricing or cancellation flows
- [ ] Payments: no card data stored; gateway tokenization; payment data in India
- [ ] Vendors with customer data have contracts covering confidentiality (Section 72A)

## Sources

- `research/2026-10-23-marketing-india-compliance.md` (law-firm and
  government-source summaries; items from prior knowledge listed
  separately). Re-check before relying on dates.
