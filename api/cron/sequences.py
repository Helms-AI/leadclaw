"""
Cron Job: Process Email Sequences

Runs every 2 hours to send scheduled sequence emails.
Vercel cron: 0 */2 * * *
"""
from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
from api.db import get_db
from api.models import (
    Lead, LeadStatus, SequenceEnrollment, SequenceStep, 
    Activity, ActivityType
)
from api.services.email import send_email, personalize_email
from api.services.scoring import calculate_lead_score


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Process pending sequence emails"""
        now = datetime.utcnow()
        results = {
            "processed": 0,
            "sent": 0,
            "skipped": 0,
            "errors": [],
            "timestamp": now.isoformat()
        }
        
        try:
            with get_db() as db:
                # Find enrollments due for next email
                pending = db.query(SequenceEnrollment).filter(
                    SequenceEnrollment.is_active == True,
                    SequenceEnrollment.next_send_at <= now
                ).limit(50).all()
                
                for enrollment in pending:
                    results["processed"] += 1
                    
                    lead = enrollment.lead
                    sequence = enrollment.sequence
                    
                    # Skip if lead is not contactable
                    if lead.status in [LeadStatus.CONVERTED, LeadStatus.LOST, 
                                       LeadStatus.UNSUBSCRIBED]:
                        enrollment.is_active = False
                        results["skipped"] += 1
                        continue
                    
                    # Skip if lead already replied (remove from sequence)
                    if lead.last_replied_at:
                        enrollment.is_active = False
                        enrollment.completed_at = now
                        results["skipped"] += 1
                        continue
                    
                    # Get current step
                    step = db.query(SequenceStep).filter(
                        SequenceStep.sequence_id == sequence.id,
                        SequenceStep.order == enrollment.current_step
                    ).first()
                    
                    if not step or not step.template:
                        # Sequence complete
                        enrollment.is_active = False
                        enrollment.completed_at = now
                        results["skipped"] += 1
                        continue
                    
                    # Personalize and send email
                    subject, body = personalize_email(step.template, lead)
                    send_result = send_email(lead.email, subject, body)
                    
                    if send_result["success"]:
                        results["sent"] += 1
                        
                        # Log activity
                        activity = Activity(
                            lead_id=lead.id,
                            type=ActivityType.EMAIL_SENT,
                            description=f"Sequence email sent: {sequence.name} - Step {step.order + 1}",
                            metadata={
                                "sequence_id": sequence.id,
                                "step": step.order,
                                "subject": subject,
                                "message_id": send_result.get("message_id")
                            }
                        )
                        db.add(activity)
                        
                        # Update lead
                        lead.last_contacted_at = now
                        if lead.status == LeadStatus.NEW:
                            lead.status = LeadStatus.CONTACTED
                        
                        # Move to next step
                        next_step = db.query(SequenceStep).filter(
                            SequenceStep.sequence_id == sequence.id,
                            SequenceStep.order == enrollment.current_step + 1
                        ).first()
                        
                        if next_step:
                            enrollment.current_step += 1
                            # Calculate next send time
                            delay_hours = (next_step.delay_days * 24) + next_step.delay_hours
                            enrollment.next_send_at = datetime.utcnow() + timedelta(hours=delay_hours)
                        else:
                            # Sequence complete
                            enrollment.is_active = False
                            enrollment.completed_at = now
                    else:
                        results["errors"].append({
                            "lead_id": lead.id,
                            "email": lead.email,
                            "error": send_result.get("error")
                        })
                
                self._send_json(results)
        except Exception as e:
            results["errors"].append(str(e))
            self._send_json(results, 500)


# Import at end to avoid circular
from datetime import timedelta
