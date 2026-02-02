---
layout: default
title: Lead Scoring
---

# Lead Scoring Algorithm

LeadClaw automatically scores leads from 0-100 based on fit and engagement.

## Scoring Components

### Company Fit (0-30 points)

| Company Size | Points |
|--------------|--------|
| 1-10 employees | 5 |
| 11-50 employees | 15 |
| 51-200 employees | 25 |
| 201-500 employees | 30 |
| 500+ employees | 20 |

*Sweet spot is 51-500 — big enough to pay, small enough to decide fast.*

### Title/Role Fit (0-25 points)

| Title | Points |
|-------|--------|
| CEO, Founder, Owner | 25 |
| VP, Director | 20 |
| Manager | 15 |
| Individual Contributor | 5 |

### Engagement Score (0-30 points)

| Action | Points |
|--------|--------|
| Email opened | +5 |
| Link clicked | +10 |
| Multiple opens | +5 |
| Replied (any) | +15 |
| Replied (positive) | +30 |
| Replied (negative) | -10 |

### Recency (0-15 points)

| Last Activity | Points |
|---------------|--------|
| Within 24 hours | 15 |
| Within 7 days | 10 |
| Within 30 days | 5 |
| Over 30 days | 0 |

## Score Thresholds

| Score | Classification | Action |
|-------|----------------|--------|
| 0-25 | Cold | Continue nurture sequence |
| 26-50 | Warming | Increase touchpoints |
| 51-75 | Engaged | Personalized follow-up |
| 76-89 | Hot | Priority attention |
| 90-100 | 🔥 On Fire | **Immediate handoff to Ryan** |

## Automatic Actions

### Score > 80
- Stop automated sequences
- Send handoff notification
- Create follow-up task
- Flag for human review

### Positive Reply Detected
- Immediate +30 points
- Auto-classify sentiment
- Trigger handoff if score > 80
- Log interaction

### Negative Reply Detected
- Mark as "Not Interested"
- Stop all sequences
- Remove from future campaigns
- Respect opt-out

## Customization

Edit scoring weights in `server/services/scoring.py`:

```python
SCORING_CONFIG = {
    'company_size': {
        '1-10': 5,
        '11-50': 15,
        '51-200': 25,
        '201-500': 30,
        '500+': 20
    },
    'title_keywords': {
        'ceo': 25,
        'founder': 25,
        'vp': 20,
        'director': 20,
        'manager': 15
    },
    'engagement': {
        'email_opened': 5,
        'link_clicked': 10,
        'replied_positive': 30,
        'replied_negative': -10
    },
    'handoff_threshold': 80
}
```

## Score History

LeadClaw tracks score changes over time:

```json
{
  "lead_id": "abc123",
  "current_score": 72,
  "history": [
    {"date": "2026-02-01", "score": 25, "reason": "Initial score"},
    {"date": "2026-02-02", "score": 30, "reason": "Email opened"},
    {"date": "2026-02-03", "score": 45, "reason": "Link clicked"},
    {"date": "2026-02-05", "score": 72, "reason": "Reply received"}
  ]
}
```

---

[← Back to Home](../)
