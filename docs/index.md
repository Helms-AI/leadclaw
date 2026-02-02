---
layout: default
title: LeadClaw Documentation
---

# 🦞 LeadClaw

**Autonomous AI-powered sales and lead generation engine**

*"Pinch the leads, close the deals"*

---

## What is LeadClaw?

LeadClaw is a fully autonomous sales engine that:
- 🔍 **Discovers** potential customers through web research and data enrichment
- 📧 **Engages** prospects with personalized email sequences
- 📊 **Qualifies** leads automatically based on behavior and fit
- 🚨 **Hands off** hot leads to humans when they're ready to buy

Built by [Helms AI](https://helms.ai) to power AI-driven sales automation.

---

## Features

### Core Capabilities

| Feature | Status | Description |
|---------|--------|-------------|
| **Lead Database** | 🚧 Building | Store and manage all prospects |
| **Email Automation** | 🚧 Building | Multi-step outreach sequences |
| **Reply Detection** | 🚧 Building | IMAP monitoring with sentiment analysis |
| **Lead Scoring** | 🚧 Building | Auto-qualification based on fit & engagement |
| **Pipeline View** | 🚧 Building | Kanban board for visual pipeline |
| **Handoff System** | ✅ Ready | Notify humans when leads are hot |
| **Analytics** | 📋 Planned | Conversion tracking and reporting |

### Automation Workflows

- **Lead Discovery** — Daily web search for target companies
- **Email Sequences** — Automated multi-touch campaigns
- **Inbox Monitoring** — Real-time reply detection
- **Lead Scoring** — Continuous qualification updates
- **Hot Lead Alerts** — Instant notifications for high-intent prospects

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    KADE (Autonomous Engine)                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   PROSPECT   │  │    ENGAGE    │  │   QUALIFY    │           │
│  │ Find & enrich│  │ Email sequences│ │ Score & rank │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         └─────────────────┴─────────────────┘                    │
│                           │                                      │
│                           ▼                                      │
│              ┌─────────────────────────┐                         │
│              │   HOT LEAD → HANDOFF    │                         │
│              └─────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Links

- [GitHub Repository](https://github.com/Helms-AI/leadclaw)
- [Issue Tracker](https://github.com/Helms-AI/leadclaw/issues)
- [Discussions](https://github.com/Helms-AI/leadclaw/discussions)
- [Handoff Protocol](./HANDOFF-PROTOCOL.html)

---

## Guides

- [Getting Started](./guides/getting-started.html)
- [Email Templates](./guides/email-templates.html)
- [Lead Scoring](./guides/lead-scoring.html)
- [API Reference](./guides/api-reference.html)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask + Python |
| Frontend | Lit Web Components |
| Database | SQLite / PostgreSQL |
| Email | SendGrid API |
| Enrichment | Apollo.io API |
| Scheduling | OpenClaw Cron |

---

## Project Status

**Current Phase:** MVP Development (Week 1)

### Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| Project Setup | Week 1 | ✅ Complete |
| Data Models | Week 1 | 🚧 In Progress |
| Email Engine | Week 1 | ⏳ Blocked (API keys) |
| Pipeline UI | Week 1 | 📋 Planned |
| Lead Discovery | Week 2 | 📋 Planned |
| Analytics | Week 2 | 📋 Planned |

---

## Contributing

We welcome contributions! See our [Contributing Guide](https://github.com/Helms-AI/leadclaw/blob/main/CONTRIBUTING.md).

---

## License

MIT License - See [LICENSE](https://github.com/Helms-AI/leadclaw/blob/main/LICENSE)

---

<footer>
<p>Built with 🦞 by <a href="https://helms.ai">Helms AI</a></p>
<p><small>Last updated: {{ site.time | date: "%Y-%m-%d" }}</small></p>
</footer>
