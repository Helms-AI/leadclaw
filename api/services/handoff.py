"""
Handoff Service - Notify Ryan when leads are hot
"""
import os
import json
import httpx
from datetime import datetime
from api.models import Lead, Activity, ActivityType

HANDOFF_WEBHOOK = os.environ.get("HANDOFF_WEBHOOK")
OPENCLAW_GATEWAY = os.environ.get("OPENCLAW_GATEWAY", "http://127.0.0.1:18789")
OPENCLAW_TOKEN = os.environ.get("OPENCLAW_TOKEN")


def notify_handoff(lead: Lead, reason: str) -> dict:
    """Notify Ryan about a hot lead"""
    
    message = f"""🔥 **HOT LEAD ALERT** 🔥

**{lead.full_name}** from **{lead.company_name or 'Unknown Company'}** is ready for handoff!

📧 **Email:** {lead.email}
💼 **Title:** {lead.job_title or 'N/A'}
🏢 **Industry:** {lead.industry or 'N/A'}
📊 **Score:** {lead.score}/100
📍 **Location:** {lead.city or ''} {lead.state or ''} {lead.country or ''}

**Why:** {reason}

---
View in dashboard: [LeadClaw Pipeline](/pipeline)
"""

    result = {"notified": False, "channels": []}
    
    # Try OpenClaw messaging (preferred)
    if OPENCLAW_TOKEN:
        try:
            response = httpx.post(
                f"{OPENCLAW_GATEWAY}/tools/invoke",
                headers={
                    "Authorization": f"Bearer {OPENCLAW_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "tool": "message",
                    "input": {
                        "action": "send",
                        "message": message
                    }
                },
                timeout=10
            )
            if response.status_code == 200:
                result["notified"] = True
                result["channels"].append("openclaw")
        except Exception as e:
            result["openclaw_error"] = str(e)
    
    # Try webhook fallback
    if HANDOFF_WEBHOOK:
        try:
            response = httpx.post(
                HANDOFF_WEBHOOK,
                json={
                    "lead_id": lead.id,
                    "email": lead.email,
                    "name": lead.full_name,
                    "company": lead.company_name,
                    "score": lead.score,
                    "reason": reason,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                },
                timeout=10
            )
            if response.status_code < 400:
                result["notified"] = True
                result["channels"].append("webhook")
        except Exception as e:
            result["webhook_error"] = str(e)
    
    return result


def log_handoff(db, lead: Lead, reason: str, notification_result: dict):
    """Log handoff activity"""
    activity = Activity(
        lead_id=lead.id,
        type=ActivityType.HANDOFF,
        description=f"Lead handed off: {reason}",
        metadata={
            "reason": reason,
            "score": lead.score,
            "notification": notification_result
        }
    )
    db.add(activity)
