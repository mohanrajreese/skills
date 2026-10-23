# Marketing, Meta platform, data security and Indian IT law baseline

Questions:
1. What changed recently in Meta's ads platform (Marketing API, Advantage+,
   Conversions API) that integrations must follow?
2. Which Indian laws and rules govern our products' data, content, security
   incidents and marketing, and what are their current timelines?

Checked 2026-10-23. Tags as in the other notes: **[registry]**,
**[primary]**, **[secondary]**. **This is engineering research, not legal
advice.** Confirm legal points with counsel and the official Gazette text.

## Meta (Facebook / Instagram) marketing

- Marketing API v26 announced 2026-07-29. Restrictions applying to **all**
  API versions (including unversioned calls) from **2026-10-27**: poll ad
  creation blocked, Messenger Stories placement value removed, a Web+App
  campaign rule. Source: developers.facebook.com blog "Introducing Graph API
  v26 and Marketing API v26" (via search). [primary]
- **Legacy Advantage+ shopping/app campaign (ASC/AAC) API paths retired:**
  can't be created or updated via the Marketing API from v25, extended to all
  versions by 2026-05-19; remaining ASC/AAC campaigns scheduled to be paused
  around September 2026. Campaigns become "Advantage+" through three levers
  (Advantage+ campaign budget, audience, placements). Source: Meta
  developer blog 2026-02-13 (via search) + ppc.land. [primary/secondary]
- SDKs: `facebook-business` (PyPI) 26.0.2 (2026-09-21);
  `facebook-nodejs-business-sdk` 24.0.1 (2025-11-21, lagging the API).
  [registry]

## Indian IT law and rules

- **IT Act 2000** (amended 2008) remains the base law. The proposed
  **Digital India Act** has not been enacted; no public draft confirmed.
  [secondary]
- **DPDP Act 2023 + Rules 2025:** Rules notified 2025-11-13; Board provisions
  in force; most obligations (fiduciary duties, rights, breach notification)
  and the **IT Act amendments** apply from **2027-05-13**, when Section 44(2)
  omits **IT Act Section 43A** and rule-making power 87(2)(ob), ending the
  **SPDI Rules 2011**. Until then SPDI Rules apply. Breach notification
  (Rule 7): intimation to the Board without delay, detailed report within
  72 hours (extendable on request), plus notice to each affected person.
  Source: law-firm commentary (KPMG, Acuity Law, KSK), multiple consistent.
  [secondary]
- **CERT-In Directions (28 April 2022, under Section 70B(6)):** report
  specified cyber incidents within **6 hours** of noticing; keep ICT
  system logs **180 days within India**; sync clocks to NIC/NPL NTP;
  designate a point of contact; data centre/VPS/cloud/VPN providers keep
  subscriber KYC for 5 years. No replacement regime found as of 2026.
  [secondary, consistent]
- **IT (Intermediary Guidelines and Digital Media Ethics Code) Rules 2021**
  amendments:
  - G.S.R. 775(E), 2025-10-22, effective **2025-11-15**: Rule 3(1)(d)
    takedown intimations only from officers of Joint Secretary rank or above
    (police: DIG or above); periodic review of notices. [secondary,
    consistent news]
  - G.S.R. 120(E), notified 2026-02-10, effective **2026-02-20**:
    "synthetically generated information" brought into due diligence;
    platforms enabling synthetic content must label it clearly and
    prominently, embed persistent metadata/provenance where feasible, and
    prevent label removal; SSMIs need user declarations; **removal within 3
    hours** for court/government-flagged unlawful content (was 36 hours) and
    **2 hours** for non-consensual intimate imagery complaints. A further
    draft on continuous labels is unconfirmed. Source: AMS Shardul
    legislative update, Mondaq, iPleaders (via search). [secondary,
    consistent]
- **TRAI TCCCPR 2018, amended 2025-02-12:** 140-series numbers for
  promotional calls; new 1600-series for service/transactional calls
  (mandated phase-wise, BFSI first from a 2025-11-19 direction); ordinary
  10-digit numbers barred for telemarketing; service messages limited to
  existing customers (inferred consent) or explicit consent; escalating
  penalties (15-day bar, then 1-year disconnection and blacklisting). Header
  suffixes `-P/-S/-T/-G` and a 90-day re-consent bar are from secondary
  sources only. Source: TRAI PR No. 11 of 2025 (via search), JSA. [primary/
  secondary]

## From prior knowledge (before 2026-06), not re-verified here

- IT Act sections and penalties: 43, 43A, 66, 66C, 66D, 66E, 67/67A/67B,
  69, 69A, 69B, 70B, 72A, 79, 85.
- IT Rules 2021 baseline duties: grievance officer, acknowledgement in
  24 hours, resolution in 15 days, 72-hour handling of certain removal
  complaints, 180-day retention of removed content and user records,
  additional SSMI duties (≥ 5 million users).
- CCPA Guidelines for Prevention and Regulation of Dark Patterns (2023-11-30):
  13 specified dark patterns. Consumer Protection (E-Commerce) Rules 2020.
- RBI payment data localisation (2018), card-on-file tokenization (from
  2022-10-01: merchants may not store card numbers), UIDAI Aadhaar Data
  Vault requirement, PCI DSS v4.0.1.
- Bharatiya Nyaya Sanhita 2023 replaced the IPC from 2024-07-01; national
  cybercrime helpline 1930 and cybercrime.gov.in.
- Gmail/Yahoo bulk-sender rules (2024): SPF, DKIM, DMARC, one-click
  unsubscribe, low spam rates. ASCI influencer disclosure guidelines.
- Meta Pixel + Conversions API deduplication via shared `event_id`, hashed
  customer parameters, Click-to-WhatsApp free entry point window, Lead Ads
  webhooks, Special Ad Categories.

## Open questions

- Official Gazette text for G.S.R. 120(E) labelling specifics.
- Current phase deadlines for 1600-series adoption outside BFSI.
- Whether any CERT-In directions were revised in 2026.
