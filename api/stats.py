"""
LeadClaw API - Statistics & Analytics
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timedelta
from sqlalchemy import func
from api.db import get_db
from api.models import Lead, LeadStatus, Activity, ActivityType


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Get dashboard statistics"""
        try:
            with get_db() as db:
                now = datetime.utcnow()
                week_ago = now - timedelta(days=7)
                month_ago = now - timedelta(days=30)
                
                # Lead counts by status
                status_counts = {}
                for status in LeadStatus:
                    count = db.query(Lead).filter(Lead.status == status).count()
                    status_counts[status.value] = count
                
                # Total leads
                total_leads = sum(status_counts.values())
                
                # New leads this week
                new_this_week = db.query(Lead).filter(
                    Lead.created_at >= week_ago
                ).count()
                
                # Leads by source
                source_counts = db.query(
                    Lead.source, func.count(Lead.id)
                ).group_by(Lead.source).all()
                
                # Activity counts this week
                emails_sent = db.query(Activity).filter(
                    Activity.type == ActivityType.EMAIL_SENT,
                    Activity.created_at >= week_ago
                ).count()
                
                emails_replied = db.query(Activity).filter(
                    Activity.type == ActivityType.EMAIL_REPLIED,
                    Activity.created_at >= week_ago
                ).count()
                
                # Score distribution
                score_ranges = {
                    "cold (0-25)": db.query(Lead).filter(Lead.score < 25).count(),
                    "warm (25-50)": db.query(Lead).filter(Lead.score >= 25, Lead.score < 50).count(),
                    "hot (50-75)": db.query(Lead).filter(Lead.score >= 50, Lead.score < 75).count(),
                    "burning (75+)": db.query(Lead).filter(Lead.score >= 75).count(),
                }
                
                # Conversion rate (hot + converted / total)
                converted = status_counts.get("converted", 0) + status_counts.get("hot", 0)
                conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
                
                # Reply rate
                reply_rate = (emails_replied / emails_sent * 100) if emails_sent > 0 else 0
                
                self._send_json({
                    "overview": {
                        "total_leads": total_leads,
                        "new_this_week": new_this_week,
                        "hot_leads": status_counts.get("hot", 0),
                        "conversion_rate": round(conversion_rate, 1),
                        "reply_rate": round(reply_rate, 1)
                    },
                    "by_status": status_counts,
                    "by_source": dict(source_counts),
                    "score_distribution": score_ranges,
                    "activity": {
                        "emails_sent_this_week": emails_sent,
                        "replies_this_week": emails_replied
                    },
                    "generated_at": now.isoformat()
                })
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
