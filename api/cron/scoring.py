"""
Cron Job: Recalculate Lead Scores & Trigger Handoffs

Runs daily at 6am to score all leads and notify on hot ones.
Vercel cron: 0 6 * * *
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from api.db import get_db
from api.models import Lead, LeadStatus, Activity, ActivityType
from api.services.scoring import calculate_lead_score, should_handoff
from api.services.handoff import notify_handoff, log_handoff


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Recalculate all lead scores"""
        now = datetime.utcnow()
        results = {
            "scored": 0,
            "upgraded_to_hot": 0,
            "handoffs_triggered": 0,
            "timestamp": now.isoformat()
        }
        
        try:
            with get_db() as db:
                # Get all active leads
                leads = db.query(Lead).filter(
                    Lead.status.notin_([
                        LeadStatus.CONVERTED, 
                        LeadStatus.LOST, 
                        LeadStatus.UNSUBSCRIBED
                    ])
                ).all()
                
                for lead in leads:
                    old_score = lead.score
                    old_status = lead.status
                    
                    # Get activities for scoring
                    activities = db.query(Activity).filter(
                        Activity.lead_id == lead.id
                    ).all()
                    
                    # Calculate new score
                    new_score = calculate_lead_score(lead, activities)
                    lead.score = new_score
                    results["scored"] += 1
                    
                    # Log score change if significant
                    if abs(new_score - old_score) >= 5:
                        activity = Activity(
                            lead_id=lead.id,
                            type=ActivityType.SCORE_CHANGE,
                            description=f"Score changed: {old_score:.0f} → {new_score:.0f}",
                            metadata={
                                "old_score": old_score,
                                "new_score": new_score
                            }
                        )
                        db.add(activity)
                    
                    # Check for status upgrade
                    if new_score >= 50 and old_status in [LeadStatus.NEW, LeadStatus.CONTACTED]:
                        lead.status = LeadStatus.ENGAGED
                    
                    if new_score >= 70 and old_status != LeadStatus.HOT:
                        lead.status = LeadStatus.HOT
                        results["upgraded_to_hot"] += 1
                        
                        # Trigger handoff
                        if should_handoff(lead):
                            reason = f"Lead score reached {new_score:.0f}/100"
                            notification = notify_handoff(lead, reason)
                            log_handoff(db, lead, reason, notification)
                            results["handoffs_triggered"] += 1
                
                self._send_json(results)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
