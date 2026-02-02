# CLAUDE.md - LeadClaw Agent Instructions

This file provides guidance to Claude Code and OpenClaw agents working on this repository.

## Project Overview

LeadClaw is an autonomous sales and lead generation engine for Helms AI. It discovers prospects, engages them with email sequences, qualifies them automatically, and hands off hot leads to humans.

## Architecture

### Backend (Flask)
```
server/
├── app.py               # Main Flask application
├── models.py            # SQLAlchemy models (Lead, Interaction, Task, Sequence)
├── routes/
│   ├── leads.py         # Lead CRUD endpoints
│   ├── pipeline.py      # Pipeline stage management
│   ├── emails.py        # Email sending/receiving
│   ├── sequences.py     # Automation sequences
│   └── analytics.py     # Reporting endpoints
└── services/
    ├── discovery.py     # Lead finding (web scraping, Apollo)
    ├── enrichment.py    # Lead enrichment (Apollo, Clearbit)
    ├── email.py         # SendGrid integration
    ├── inbox.py         # IMAP reply monitoring
    ├── scoring.py       # Lead qualification algorithm
    └── handoff.py       # Notification to sales team
```

### Frontend (Lit + Preact Signals)
```
web/
├── index.html           # SPA entry
├── js/
│   ├── app.js           # Bootstrap
│   ├── store/           # Preact Signals state
│   ├── services/        # API clients
│   └── components/
│       ├── atoms/       # Basic elements
│       ├── molecules/   # Combinations
│       ├── organisms/   # Complex sections
│       └── layout/      # Page structure
└── css/
    └── dashboard.css    # Styles
```

## Data Models

### Lead
```python
class Lead:
    id: str (UUID)
    created_at: datetime
    updated_at: datetime
    
    # Contact
    first_name: str
    last_name: str
    email: str
    phone: str | None
    linkedin: str | None
    
    # Company
    company: str
    title: str
    company_size: str | None
    industry: str | None
    website: str | None
    
    # Pipeline
    stage: str  # new, contacted, engaged, qualified, opportunity, closed_won, closed_lost
    score: int  # 0-100
    source: str  # web_search, apollo, referral, inbound, linkedin
    
    # Assignment
    assigned_to: str | None  # 'kade' or 'ryan'
    handoff_requested: bool
    handoff_at: datetime | None
    
    # Sequences
    active_sequence_id: str | None
    sequence_step: int
    last_contacted_at: datetime | None
    next_contact_at: datetime | None
```

### Interaction
```python
class Interaction:
    id: str
    lead_id: str
    type: str  # email_sent, email_received, email_opened, link_clicked, call, note
    direction: str  # outbound, inbound
    subject: str | None
    content: str
    metadata: dict  # opens, clicks, etc.
    created_at: datetime
    created_by: str  # 'kade' or 'ryan'
```

### Sequence
```python
class Sequence:
    id: str
    name: str
    steps: list[SequenceStep]
    active: bool

class SequenceStep:
    day_offset: int
    template_id: str
    condition: str | None  # e.g., "not_replied"
```

## API Endpoints

### Leads
- `GET /api/leads` — List leads with filters
- `POST /api/leads` — Create lead
- `GET /api/leads/:id` — Get lead details
- `PATCH /api/leads/:id` — Update lead
- `DELETE /api/leads/:id` — Delete lead
- `POST /api/leads/:id/handoff` — Request handoff to Ryan

### Pipeline
- `GET /api/pipeline` — Get pipeline stages with counts
- `PATCH /api/leads/:id/stage` — Move lead to stage

### Emails
- `POST /api/emails/send` — Send email
- `GET /api/emails/inbox` — Check for replies
- `GET /api/leads/:id/emails` — Get email thread

### Sequences
- `GET /api/sequences` — List sequences
- `POST /api/sequences` — Create sequence
- `POST /api/leads/:id/enroll` — Enroll in sequence
- `POST /api/leads/:id/unenroll` — Remove from sequence

### Analytics
- `GET /api/analytics/overview` — Dashboard stats
- `GET /api/analytics/funnel` — Conversion funnel
- `GET /api/analytics/sequences` — Sequence performance

## Scoring Algorithm

```python
def calculate_score(lead: Lead) -> int:
    score = 0
    
    # Company fit (0-30)
    if lead.company_size in ['11-50', '51-200']:
        score += 20
    elif lead.company_size in ['201-500']:
        score += 30
    
    # Title fit (0-25)
    if 'CEO' in lead.title or 'Founder' in lead.title:
        score += 25
    elif 'VP' in lead.title or 'Director' in lead.title:
        score += 20
    elif 'Manager' in lead.title:
        score += 10
    
    # Engagement (0-30)
    if lead.email_opened:
        score += 10
    if lead.link_clicked:
        score += 15
    if lead.replied:
        score += 30
    
    # Recency (0-15)
    if lead.last_activity_within_days(7):
        score += 15
    elif lead.last_activity_within_days(30):
        score += 10
    
    return min(score, 100)
```

## Handoff Protocol

Leads are handed off to Ryan when:
1. Score exceeds 80
2. Positive reply detected
3. Demo/call request received
4. Manual handoff requested

Handoff notification includes:
- Lead details and company info
- Full email thread
- Engagement timeline
- Recommended talking points
- One-click link to LeadClaw

## Email Templates

Templates use Jinja2 with variables:
- `{{first_name}}` — Lead's first name
- `{{company}}` — Company name
- `{{pain_point}}` — Detected pain point
- `{{case_study}}` — Relevant case study
- `{{cta_link}}` — Tracked CTA link

## Environment Variables

```
# Required
SENDGRID_API_KEY=
APOLLO_API_KEY=
IMAP_HOST=
IMAP_USER=
IMAP_PASSWORD=
FROM_EMAIL=

# Optional
DATABASE_URL=sqlite:///data/leadclaw.db
OPENAI_API_KEY=  # For AI personalization
TELEGRAM_BOT_TOKEN=  # For handoff notifications
TELEGRAM_CHAT_ID=
```

## Development Workflow

1. Create feature branch: `git checkout -b feature/description`
2. Make changes
3. Test locally
4. Commit with clear message
5. Push and create PR
6. Get review
7. Merge to develop/main

## Critical Rules

🚨 **NEVER delete this repository**
🚨 **NEVER delete main, develop, or release branches**
✅ **Feature branches can be deleted after merge**

## Integration with OpenClaw

LeadClaw integrates with OpenClaw for:
- Cron jobs (lead discovery, sequence processing)
- Notifications (handoff alerts via Telegram)
- Memory (storing findings, learned patterns)
- Sub-agents (parallel research tasks)
