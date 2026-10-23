---
name: data-security
description: How we protect data through its whole lifecycle, covering data inventory and classification (personal, sensitive, payment, Aadhaar, health), encryption in transit and at rest, KMS and field-level encryption, password hashing, access control and production data access, masking and synthetic data for dev, retention and deletion, log redaction, backups, data residency in India, third-party sharing and breach response. Use whenever designing tables or storage for personal or sensitive data, handling PII, payments, Aadhaar, health or financial data, setting up encryption or key management, copying production data, writing retention or deletion jobs, sharing data with vendors or AI providers, or responding to a data leak.
metadata:
  status: seed
  version: 0.1.0
  last-reviewed: 2026-10-23
  owners: []
  tags: [security, data, privacy, compliance]
---

# Data security

`security` covers attacks on the application. This skill covers the
**data itself**: know what you hold, keep as little as possible, protect what
you keep, and be able to prove it.

## 1. Inventory and classify (before you store anything new)

| Class | Examples | Minimum controls |
|---|---|---|
| Public | Marketing pages, public catalogue | Integrity only |
| Internal | Configs, internal docs | Auth required |
| Confidential / personal | Name, email, phone, address, order history, chat messages | Encryption at rest, access control, retention limit, masked in logs |
| Restricted / sensitive | Passwords, bank/card/payment data, health, biometrics, Aadhaar, government IDs, precise location, children's data | All of the above + field-level encryption or tokenization, need-to-know access, access logging, stricter retention |

Keep a short data map per product (`docs/data-map.md`): field, class,
purpose, where stored, who can access, retention, shared with whom. It's the
backbone for privacy notices, DPDP requests and incident scoping.

## 2. Don't hold it if you can avoid it

- **Cards:** never store card numbers or CVV. Use gateway tokenization
  (Razorpay/Stripe), which also keeps you out of most PCI DSS scope. RBI
  rules forbid merchants storing card numbers.
- **Aadhaar:** avoid collecting it. If legally required, store it only in an
  Aadhaar Data Vault (tokenised, encrypted) and display masked (last 4 digits).
- **Analytics and AI prompts:** send IDs or pseudonymous keys, not raw PII.
- **Minimise fields:** every field needs a stated purpose.

## 3. Protect what you keep

- **In transit:** TLS 1.2+ everywhere (1.3 preferred), including
  service-to-service and DB connections; HSTS on web.
- **At rest:** managed disk/DB/bucket encryption (on by default in our
  clouds; verify). For restricted fields, **field-level encryption** with
  keys in KMS (AWS KMS / Cloud KMS) using envelope encryption. Rotate keys;
  never put keys in code or the same DB as the data.
- **Passwords:** Argon2id (or bcrypt/scrypt; Django's default PBKDF2 with
  current iteration counts is acceptable). Never reversible encryption.
- **Search on encrypted fields:** store a keyed hash (HMAC) alongside for
  equality lookups (e.g. phone number), not plaintext.
- **Access:** least privilege per service account; tenant isolation (`saas`,
  Supabase RLS, Firebase rules); **no standing human access to production
  data**: time-boxed, approved, logged break-glass access.
- **Files:** private buckets; short-lived signed URLs; malware scan on
  upload; strip EXIF/location from user images where not needed.

## 4. Use and share safely

- **Dev/staging:** seed with synthetic or masked data. Never copy raw
  production PII into lower environments or laptops.
- **Logs and error trackers:** redact PII and secrets at the logger (phone,
  email, tokens, OTPs, card fragments); never log request bodies of
  auth/payment endpoints.
- **Vendors and AI providers:** a data processing agreement, check where
  they store data, and send only what's needed. Record each sharing in the
  data map.
- **Exports:** bulk exports need permission, are logged, and expire.

## 5. Retain, delete, back up

- A **retention period per data class** (e.g. delete inactive leads after
  N months, keep invoices as tax law requires) enforced by scheduled jobs,
  not good intentions.
- **Deletion requests:** delete or anonymise across DB, search index,
  caches, analytics and files; backups age out on their schedule.
- **Backups:** encrypted, access-restricted, one copy isolated or immutable,
  and **restore-tested** regularly.

## 6. Residency (India)

- CERT-In requires ICT logs for 180 days **in India**; RBI requires payment
  system data in India. Prefer Mumbai/Delhi regions (`ap-south-1`,
  `asia-south1`/`asia-south2`) for primary data and logs.
- DPDP allows cross-border transfers except to countries the government
  restricts. Track where each vendor processes data.

## 7. Breach response (data-specific)

Contain (revoke keys/tokens, close access) → scope using the data map (which
classes, how many people) → preserve evidence and logs → notify:
**CERT-In within 6 hours**, and from 2027-05-13 the **Data Protection
Board** (immediate + detailed within 72 hours) and affected people
(`india-it-compliance`) → fix the root cause → retro.

## Sources

- `research/2026-10-23-marketing-india-compliance.md`; general practice
  (OWASP ASVS data protection, PCI DSS) from prior knowledge.
