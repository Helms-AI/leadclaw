"""
Cron Job: Monitor Email Inbox for Replies

Runs every 15 minutes to check for replies.
Vercel cron: */15 * * * *
"""
from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
from imapclient import IMAPClient
import email
from email.header import decode_header
from api.db import get_db
from api.models import Lead, LeadStatus, Activity, ActivityType
from api.services.scoring import should_handoff
from api.services.handoff import notify_handoff, log_handoff

IMAP_HOST = os.environ.get("IMAP_HOST")
IMAP_USER = os.environ.get("IMAP_USER")
IMAP_PASSWORD = os.environ.get("IMAP_PASSWORD")


def decode_subject(subject):
    """Decode email subject header"""
    if not subject:
        return ""
    decoded = decode_header(subject)
    result = ""
    for part, encoding in decoded:
        if isinstance(part, bytes):
            result += part.decode(encoding or "utf-8", errors="replace")
        else:
            result += part
    return result


def extract_email_address(from_header):
    """Extract email address from From header"""
    if "<" in from_header and ">" in from_header:
        return from_header.split("<")[1].split(">")[0].lower()
    return from_header.lower().strip()


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Check inbox for replies from leads"""
        now = datetime.utcnow()
        results = {
            "checked": False,
            "new_replies": 0,
            "leads_updated": [],
            "timestamp": now.isoformat()
        }
        
        if not all([IMAP_HOST, IMAP_USER, IMAP_PASSWORD]):
            results["error"] = "IMAP credentials not configured"
            self._send_json(results)
            return
        
        try:
            # Connect to IMAP
            with IMAPClient(IMAP_HOST) as client:
                client.login(IMAP_USER, IMAP_PASSWORD)
                client.select_folder("INBOX")
                results["checked"] = True
                
                # Search for recent unseen messages
                messages = client.search(["UNSEEN", "SINCE", now.date()])
                
                if not messages:
                    self._send_json(results)
                    return
                
                # Fetch messages
                fetched = client.fetch(messages, ["ENVELOPE", "RFC822.HEADER"])
                
                with get_db() as db:
                    for msg_id, data in fetched.items():
                        envelope = data[b"ENVELOPE"]
                        from_addr = envelope.from_[0] if envelope.from_ else None
                        
                        if not from_addr:
                            continue
                        
                        # Build email address
                        sender_email = f"{from_addr.mailbox.decode()}@{from_addr.host.decode()}".lower()
                        subject = envelope.subject.decode() if envelope.subject else ""
                        
                        # Check if sender is a lead
                        lead = db.query(Lead).filter(Lead.email == sender_email).first()
                        
                        if lead:
                            results["new_replies"] += 1
                            results["leads_updated"].append({
                                "id": lead.id,
                                "email": lead.email,
                                "subject": subject
                            })
                            
                            # Update lead
                            lead.last_replied_at = now
                            old_status = lead.status
                            
                            # Upgrade status
                            if lead.status in [LeadStatus.NEW, LeadStatus.CONTACTED]:
                                lead.status = LeadStatus.ENGAGED
                            
                            # Add 30 points for reply
                            lead.score = min(100, lead.score + 30)
                            
                            # Log activity
                            activity = Activity(
                                lead_id=lead.id,
                                type=ActivityType.EMAIL_REPLIED,
                                description=f"Lead replied: {subject[:100]}",
                                metadata={
                                    "subject": subject,
                                    "old_status": old_status.value
                                }
                            )
                            db.add(activity)
                            
                            # Check for handoff
                            if should_handoff(lead):
                                reason = f"Lead replied to email: {subject[:50]}"
                                notification = notify_handoff(lead, reason)
                                log_handoff(db, lead, reason, notification)
                            
                            # Mark message as seen
                            client.add_flags(msg_id, [b"\\Seen"])
                
                self._send_json(results)
                
        except Exception as e:
            results["error"] = str(e)
            self._send_json(results, 500)
