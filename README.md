# 🦞 LeadClaw

**Autonomous AI-powered sales and lead generation engine for Helms AI**

*"Pinch the leads, close the deals"*

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Helms-AI/leadclaw)

---

## Overview

LeadClaw is a fully autonomous sales engine that:
- 🔍 **Discovers** potential customers through web research and data enrichment
- 📧 **Engages** prospects with personalized email sequences
- 📊 **Qualifies** leads automatically based on behavior and fit
- 🚨 **Hands off** hot leads to humans when they're ready to buy

## Tech Stack

| Layer | Technology | Cost |
|-------|------------|------|
| **Backend** | Vercel Serverless (Python) | Free tier |
| **Database** | Neon PostgreSQL | Free tier |
| **Frontend** | Static HTML/JS | Free |
| **Email Send** | SendGrid API | Free tier (100/day) |
| **Email Monitor** | IMAP | Your email provider |
| **Scheduling** | Vercel Cron | Free tier |
| **Enrichment** | Apollo.io API | Optional |

**Total cost: $0/month** on free tiers 🎉

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         VERCEL                                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   /api/*     │  │  /api/cron/* │  │   /public    │           │
│  │  REST APIs   │  │  Scheduled   │  │  Dashboard   │           │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘           │
│         └─────────────────┴─────────────────┘                    │
│                           │                                      │
│                           ▼                                      │
│              ┌─────────────────────────┐                         │
│              │   Neon PostgreSQL       │                         │
│              └─────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         SendGrid       IMAP      Apollo.io
         (send)       (replies)   (enrich)
```

## Features

### MVP (v1.0)
- [x] Vercel + Neon architecture
- [x] Lead data model & CRUD API
- [x] Pipeline kanban dashboard
- [x] Email sending (SendGrid)
- [x] Email reply monitoring (IMAP)
- [x] Multi-step sequence automation
- [x] Lead scoring algorithm
- [x] Hot lead handoff notifications
- [ ] Apollo.io enrichment integration

### Cron Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| `/api/cron/sequences` | Every 2 hours | Send scheduled sequence emails |
| `/api/cron/inbox` | Every 15 min | Check for email replies |
| `/api/cron/scoring` | Daily 6am | Recalculate scores, trigger handoffs |

## Quick Start

### 1. Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Helms-AI/leadclaw)

### 2. Create Neon Database

1. Go to [neon.tech](https://neon.tech)
2. Create a free project
3. Copy the connection string

### 3. Configure Environment Variables

In Vercel project settings, add:

```
DATABASE_URL=postgresql://...  (from Neon)
SENDGRID_API_KEY=...           (from SendGrid)
IMAP_HOST=imap.gmail.com
IMAP_USER=your@email.com
IMAP_PASSWORD=app-password
```

### 4. Initialize Database

```bash
# Run locally or via Vercel CLI
python -c "from api.db import init_db; init_db()"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api` | GET | Health check & info |
| `/api/leads` | GET, POST | List/create leads |
| `/api/leads/{id}` | GET, PUT, DELETE | Lead CRUD |
| `/api/pipeline` | GET | Kanban view data |
| `/api/stats` | GET | Dashboard statistics |

## Local Development

```bash
# Clone
git clone https://github.com/Helms-AI/leadclaw.git
cd leadclaw

# Install Vercel CLI
npm i -g vercel

# Link to project
vercel link

# Pull env vars
vercel env pull

# Run locally
vercel dev
```

## Project Structure

```
leadclaw/
├── api/                    # Vercel serverless functions
│   ├── index.py            # Health check
│   ├── leads.py            # Leads CRUD
│   ├── pipeline.py         # Kanban data
│   ├── stats.py            # Analytics
│   ├── db.py               # Neon connection
│   ├── models.py           # SQLAlchemy models
│   ├── cron/               # Scheduled jobs
│   │   ├── sequences.py    # Email sequences
│   │   ├── inbox.py        # Reply monitoring
│   │   └── scoring.py      # Lead scoring
│   └── services/           # Business logic
│       ├── email.py        # SendGrid
│       ├── scoring.py      # Score calculation
│       └── handoff.py      # Hot lead alerts
├── public/                 # Static frontend
│   └── index.html          # Dashboard
├── vercel.json             # Vercel config + crons
├── requirements.txt        # Python deps
└── docs/                   # Documentation
```

## Communication

- **[Issues](https://github.com/Helms-AI/leadclaw/issues)** — Bug reports, feature requests
- **[Discussions](https://github.com/Helms-AI/leadclaw/discussions)** — Strategy, ideas, Q&A
- **[Wiki](https://github.com/Helms-AI/leadclaw/wiki)** — Documentation, playbooks
- **[Project Board](https://github.com/Helms-AI/leadclaw/projects)** — Task tracking

## Blockers (Need From Ryan)

- [ ] **SendGrid API Key** — For email sending
- [ ] **IMAP Credentials** — For reply monitoring
- [ ] **Apollo.io API Key** — For lead enrichment (optional)
- [ ] **Vercel Account** — Or invite Kade to team

## License

MIT — See [LICENSE](LICENSE)

---

**Built with 🦞 by [Helms AI](https://helms.ai)**
