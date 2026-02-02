# 🦞 LeadClaw

**Autonomous AI-powered sales and lead generation engine for Helms AI**

*"Pinch the leads, close the deals"*

---

## Overview

LeadClaw is a fully autonomous sales engine that:
- 🔍 **Discovers** potential customers through web research and data enrichment
- 📧 **Engages** prospects with personalized email sequences
- 📊 **Qualifies** leads automatically based on behavior and fit
- 🚨 **Hands off** hot leads to humans when they're ready to buy

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

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask + Python |
| Frontend | Lit Web Components + Preact Signals |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Email | SendGrid API |
| Enrichment | Apollo.io API |
| Scheduling | OpenClaw Cron |

## Features

### MVP (v1.0)
- [ ] Lead database with CRUD API
- [ ] Email sending engine (SendGrid)
- [ ] Email reply monitoring (IMAP)
- [ ] Multi-step sequence automation
- [ ] Lead scoring algorithm
- [ ] Pipeline kanban view
- [ ] Handoff notification system
- [ ] Activity timeline

### Future
- [ ] LinkedIn integration
- [ ] Website visitor tracking
- [ ] AI-powered email personalization
- [ ] Referral tracking
- [ ] Revenue attribution

## Quick Start

```bash
# Clone
git clone https://github.com/Helms-AI/leadclaw.git
cd leadclaw

# Install dependencies
pip install -r requirements.txt
npm install

# Configure
cp .env.example .env
# Add your API keys

# Run
python -m server.app
```

## Project Structure

```
leadclaw/
├── server/              # Flask backend
│   ├── app.py           # Main application
│   ├── models.py        # SQLAlchemy models
│   ├── routes/          # API endpoints
│   └── services/        # Business logic
├── web/                 # Lit frontend
│   ├── index.html
│   ├── js/components/
│   └── css/
├── templates/           # Email templates
├── scripts/             # Automation scripts
├── docs/                # Documentation
└── data/                # Database (gitignored)
```

## Communication

- **Issues** — Bug reports, feature requests
- **Discussions** — Strategy, ideas, Q&A
- **Wiki** — Documentation, playbooks
- **Project Board** — Task tracking

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT — See [LICENSE](LICENSE)

---

**Built with 🦞 by [Helms AI](https://helms.ai)**
