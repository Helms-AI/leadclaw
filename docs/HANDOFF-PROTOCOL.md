# 🤝 Handoff Protocol

This document defines how Kade and Ryan communicate and hand off tasks using GitHub.

## Overview

All handoffs happen through GitHub Issues with specific labels:

| Label | Meaning |
|-------|---------|
| `handoff: to-ryan` 🚨 | Kade needs Ryan's input, decision, or action |
| `handoff: to-kade` 🦞 | Ryan is handing a task back to Kade |
| `handoff: waiting` ⏳ | Waiting for response from the other party |
| `handoff: complete` ✅ | Handoff resolved, ready to close |

## When Kade Hands Off to Ryan

### Triggers
- **API keys needed** — Can't proceed without credentials
- **Human conversation required** — Lead wants to talk to a person
- **Decision needed** — Strategy question requiring Ryan's input
- **External action required** — Something only Ryan can do
- **Hot lead detected** — Score > 80 or positive reply

### Process
1. Kade creates issue with `[HANDOFF]` prefix
2. Applies label `handoff: to-ryan`
3. Provides full context:
   - What's needed
   - Why it's needed
   - Deadline/urgency
   - Related issues/links
4. Adds label `handoff: waiting`

### Example
```markdown
Title: [HANDOFF] Need SendGrid API key to proceed

## Direction
- [x] 🚨 Kade → Ryan

## Summary
Blocked on email automation - need SendGrid API key.

## Context
Issues #3, #4, #5 all depend on email functionality.
Can't test sequences without ability to send.

## Requested Action
1. Sign up at sendgrid.com (free tier works)
2. Create API key with "Mail Send" permission
3. Paste key in comment below

## Deadline
- [x] ASAP (blocking Week 1 deliverables)
```

## When Ryan Hands Off to Kade

### Triggers
- **New task assignment** — Something Kade should work on
- **Responding to Kade's handoff** — Providing requested info
- **Strategic direction** — New priority or focus area
- **Bug report** — Something that needs fixing
- **Feature request** — New capability needed

### Process
1. Ryan creates issue with `[HANDOFF]` prefix (or comments on existing)
2. Applies label `handoff: to-kade`
3. Provides clear instructions:
   - What to do
   - Acceptance criteria
   - Priority level
4. Kade picks up within 30 minutes (via cron monitor)

### Example (Responding to Kade)
```markdown
## Response

Here's the SendGrid API key:
`SG.xxxxxxxxxxxxx`

Also created sales@helmsai.com for sending.
IMAP credentials:
- Host: imap.gmail.com
- User: sales@helmsai.com
- Password: [app password]

Removing `handoff: to-ryan`, adding `handoff: to-kade`.
```

### Example (New Task)
```markdown
Title: [HANDOFF] Prioritize fintech companies in outreach

## Direction
- [x] 🦞 Ryan → Kade

## Summary
Shift ICP focus to fintech companies - higher willingness to pay.

## Requested Action
1. Update ICP documentation in Wiki
2. Research top 50 fintech companies (Series A-C)
3. Prioritize these in discovery workflow
4. Create fintech-specific email template

## Deadline
- [x] This week
```

## Completing a Handoff

When the handoff is resolved:
1. Recipient comments with completion status
2. Add label `handoff: complete`
3. Remove other handoff labels
4. Close the issue

## Monitoring

Kade checks for handoffs every 30 minutes via cron job:
```bash
gh issue list --repo Helms-AI/leadclaw --label "handoff: to-kade" --state open
```

Ryan can check pending handoffs:
```bash
gh issue list --repo Helms-AI/leadclaw --label "handoff: to-ryan" --state open
```

## Quick Reference

### Kade Needs Ryan
```bash
# Create handoff issue
gh issue create --repo Helms-AI/leadclaw \
  --title "[HANDOFF] <summary>" \
  --label "handoff: to-ryan" \
  --label "handoff: waiting"
```

### Ryan Responds
1. Comment on the issue
2. Change label from `to-ryan` to `to-kade`
3. Remove `waiting` label

### Complete Handoff
```bash
# Mark complete and close
gh issue edit <number> --add-label "handoff: complete" --remove-label "handoff: to-ryan" --remove-label "handoff: to-kade"
gh issue close <number>
```

---

**The goal: Async collaboration that doesn't block either party for long.**
