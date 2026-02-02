# CLAUDE.md - LeadClaw Agent Instructions

## Project Overview

LeadClaw is an autonomous sales and lead generation engine built on **Vercel + Neon** (free tier stack).

**Primary Agent:** Kade (OpenClaw)
**Human Owner:** Ryan (closes deals)

## Architecture

- **Backend:** Vercel Serverless Python Functions (`/api/*`)
- **Database:** Neon PostgreSQL (serverless, auto-scaling)
- **Frontend:** Static HTML/JS in `/public/`
- **Cron Jobs:** Vercel Cron (defined in `vercel.json`)

## Key Files

| File | Purpose |
|------|---------|
| `api/models.py` | SQLAlchemy models (Lead, Activity, Sequence, etc.) |
| `api/db.py` | Neon database connection |
| `api/leads.py` | Leads CRUD API |
| `api/services/scoring.py` | Lead scoring algorithm |
| `api/services/handoff.py` | Hot lead notification |
| `api/cron/*.py` | Scheduled automation jobs |
| `public/index.html` | Dashboard UI |
| `vercel.json` | Deployment config + cron schedules |

## Commands

```bash
# Local development
vercel dev

# Deploy
vercel --prod

# Initialize database
python -c "from api.db import init_db; init_db()"

# Test API
curl http://localhost:3000/api
curl http://localhost:3000/api/leads
```

## Environment Variables

Required in Vercel project settings:

- `DATABASE_URL` — Neon PostgreSQL connection string
- `SENDGRID_API_KEY` — For email sending
- `IMAP_HOST`, `IMAP_USER`, `IMAP_PASSWORD` — For reply monitoring
- `APOLLO_API_KEY` — For enrichment (optional)
- `OPENCLAW_TOKEN` — For handoff notifications (optional)

## Data Models

### Lead Status Flow
```
new → contacted → engaged → qualified → hot → converted
                                    ↘ lost
                                    ↘ unsubscribed
```

### Lead Scoring
- Profile completeness: +5 each (phone, company, title)
- ICP match: +10 each (target industry, company size)
- Engagement: +5 open, +15 click, +30 reply
- Recency bonuses: +10-20
- Negative: -50 bounce, -100 unsubscribe

### Handoff Triggers
- Score >= 70
- Status = "hot"
- Lead replied to email

## Coding Guidelines

1. **Vercel Functions:** Each file in `/api/` is a separate function. Use `handler` class pattern.
2. **Database:** Always use `with get_db() as db:` context manager
3. **Error Handling:** Return JSON `{"error": "message"}` with appropriate status
4. **CORS:** Add `Access-Control-Allow-Origin: *` to all responses
5. **Cron Jobs:** Must handle GET requests, return JSON status

## GitHub Workflow

- Use Issues for tasks
- Link commits to issues with `#123`
- PR for significant changes
- Keep Ryan informed of hot leads via handoff system

## Contact

- **Kade:** OpenClaw main session
- **Ryan:** Handoff notifications, strategic decisions
