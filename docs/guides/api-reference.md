---
layout: default
title: API Reference
---

# API Reference

LeadClaw exposes a REST API for all operations.

**Base URL:** `http://localhost:24283/api`

## Authentication

Currently local-only. Future: API key authentication.

---

## Leads

### List Leads

```http
GET /api/leads
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `stage` | string | Filter by pipeline stage |
| `source` | string | Filter by lead source |
| `min_score` | integer | Minimum score filter |
| `max_score` | integer | Maximum score filter |
| `search` | string | Search name, company, email |
| `limit` | integer | Results per page (default: 50) |
| `offset` | integer | Pagination offset |

**Response:**

```json
{
  "leads": [
    {
      "id": "abc123",
      "first_name": "John",
      "last_name": "Smith",
      "email": "john@acme.com",
      "company": "Acme Inc",
      "title": "VP Operations",
      "stage": "contacted",
      "score": 45,
      "created_at": "2026-02-01T10:00:00Z"
    }
  ],
  "total": 150,
  "limit": 50,
  "offset": 0
}
```

### Create Lead

```http
POST /api/leads
```

**Body:**

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@acme.com",
  "company": "Acme Inc",
  "title": "VP Operations",
  "source": "web_search"
}
```

### Get Lead

```http
GET /api/leads/:id
```

### Update Lead

```http
PATCH /api/leads/:id
```

### Delete Lead

```http
DELETE /api/leads/:id
```

---

## Pipeline

### Get Pipeline Overview

```http
GET /api/pipeline
```

**Response:**

```json
{
  "stages": [
    {"name": "new", "count": 45, "value": 0},
    {"name": "contacted", "count": 30, "value": 0},
    {"name": "engaged", "count": 15, "value": 0},
    {"name": "qualified", "count": 8, "value": 24000},
    {"name": "opportunity", "count": 3, "value": 15000}
  ],
  "total_leads": 101,
  "total_value": 39000
}
```

### Move Lead Stage

```http
PATCH /api/leads/:id/stage
```

**Body:**

```json
{
  "stage": "qualified"
}
```

---

## Emails

### Send Email

```http
POST /api/emails/send
```

**Body:**

```json
{
  "lead_id": "abc123",
  "template": "initial_outreach",
  "variables": {
    "custom_var": "value"
  }
}
```

### Get Email Thread

```http
GET /api/leads/:id/emails
```

---

## Sequences

### List Sequences

```http
GET /api/sequences
```

### Enroll Lead

```http
POST /api/leads/:id/enroll
```

**Body:**

```json
{
  "sequence_id": "default"
}
```

### Unenroll Lead

```http
POST /api/leads/:id/unenroll
```

---

## Analytics

### Overview Stats

```http
GET /api/analytics/overview
```

**Response:**

```json
{
  "period": "7d",
  "leads_created": 45,
  "emails_sent": 120,
  "emails_opened": 48,
  "emails_replied": 12,
  "open_rate": 0.40,
  "reply_rate": 0.10,
  "handoffs": 3
}
```

### Funnel Data

```http
GET /api/analytics/funnel
```

---

## Handoffs

### Request Handoff

```http
POST /api/leads/:id/handoff
```

**Body:**

```json
{
  "reason": "Positive reply - wants demo",
  "priority": "high"
}
```

---

## Webhooks

### Incoming Webhook (for integrations)

```http
POST /api/webhooks/inbound
```

---

[← Back to Home](../)
