---
type: llm
focus: last_message
weight: 1
---

The answer verifies the X-Razorpay-Signature header with HMAC-SHA256 computed over the raw request body using the webhook secret (not the API key secret), before trusting or parsing the payload.
