---
layout: default
title: Email Templates
---

# Email Templates

LeadClaw uses Jinja2 templates for email personalization.

## Available Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{first_name}}` | Lead's first name | John |
| `{{last_name}}` | Lead's last name | Smith |
| `{{company}}` | Company name | Acme Inc |
| `{{title}}` | Job title | VP of Operations |
| `{{industry}}` | Company industry | SaaS |
| `{{pain_point}}` | Detected pain point | manual processes |
| `{{case_study}}` | Relevant case study link | [link] |
| `{{cta_link}}` | Tracked call-to-action link | [link] |
| `{{unsubscribe_link}}` | Opt-out link | [link] |

## Default Sequence

### Email 1: Initial Outreach (Day 0)

```
Subject: Quick question about {{company}}'s operations

Hi {{first_name}},

I noticed {{company}} is growing fast in the {{industry}} space — congrats!

Quick question: how much time does your team spend on repetitive tasks that could be automated?

We help companies like yours save 10-40 hours/week with AI automation. Would a quick chat be useful?

Best,
[Signature]

{{unsubscribe_link}}
```

### Email 2: Follow-up (Day 3)

```
Subject: Re: Quick question about {{company}}'s operations

Hi {{first_name}},

Following up on my last note. 

I wanted to share a quick case study: [Similar Company] automated their [process] and saved 25 hours/week.

Would something like this be valuable for {{company}}?

Happy to show you how it works — just reply and we'll set up a quick call.

Best,
[Signature]
```

### Email 3: Value Add (Day 7)

```
Subject: Thought you might find this useful

Hi {{first_name}},

I put together a quick guide on "5 Processes Every {{industry}} Company Should Automate."

{{cta_link}}

No strings attached — just thought it might be helpful as you scale.

Let me know if you have any questions!

Best,
[Signature]
```

### Email 4: Break-up (Day 14)

```
Subject: Should I close your file?

Hi {{first_name}},

I haven't heard back, so I'll assume the timing isn't right.

No worries at all — I'll close out your file for now.

If things change and you want to explore automation for {{company}}, just reply to this email. I'll be here.

Best,
[Signature]
```

## Creating Custom Templates

Templates are stored in `templates/emails/`. Create new templates:

```bash
templates/emails/
├── sequences/
│   ├── default/
│   │   ├── email_1.html
│   │   ├── email_2.html
│   │   ├── email_3.html
│   │   └── email_4.html
│   └── enterprise/
│       └── ...
└── transactional/
    ├── demo_confirmation.html
    └── meeting_reminder.html
```

## Best Practices

1. **Keep it short** — Under 150 words for cold emails
2. **Personalize** — Use variables, reference their company
3. **One CTA** — Don't overwhelm with options
4. **Mobile-friendly** — Most emails read on phones
5. **Test deliverability** — Check spam scores before sending

---

[← Back to Home](../)
