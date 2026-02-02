---
layout: default
title: Getting Started
---

# Getting Started with LeadClaw

This guide will help you set up and run LeadClaw.

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Helms-AI/leadclaw.git
cd leadclaw
```

### 2. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

# Node dependencies (for frontend)
npm install
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
SENDGRID_API_KEY=your_key_here
APOLLO_API_KEY=your_key_here
IMAP_HOST=imap.gmail.com
IMAP_USER=your_email@domain.com
IMAP_PASSWORD=your_app_password
```

### 4. Initialize Database

```bash
python -m server.init_db
```

### 5. Run the Server

```bash
python -m server.app
```

The dashboard will be available at `http://localhost:24283`

## Next Steps

- [Configure Email Templates](./email-templates.html)
- [Set Up Lead Scoring](./lead-scoring.html)
- [API Reference](./api-reference.html)

---

[← Back to Home](../)
