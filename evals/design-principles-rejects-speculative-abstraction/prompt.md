---
tags: [design-principles]
max_turns: 10
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

We only send order updates over WhatsApp today. A teammate proposes a NotificationChannel interface, a ChannelFactory, a plugin registry and a YAML config so we can add SMS, email and push later. Should we build that now? Give a recommendation.
