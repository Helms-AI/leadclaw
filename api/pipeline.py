"""
LeadClaw API - Pipeline View (Kanban data)
"""
from http.server import BaseHTTPRequestHandler
import json
from api.db import get_db
from api.models import Lead, LeadStatus


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        """Get leads grouped by status for pipeline/kanban view"""
        try:
            with get_db() as db:
                pipeline = {}
                
                for status in LeadStatus:
                    leads = db.query(Lead).filter(
                        Lead.status == status
                    ).order_by(Lead.score.desc()).limit(100).all()
                    
                    pipeline[status.value] = {
                        "status": status.value,
                        "count": len(leads),
                        "leads": [l.to_dict() for l in leads]
                    }
                
                # Calculate summary stats
                total_leads = db.query(Lead).count()
                hot_leads = db.query(Lead).filter(Lead.status == LeadStatus.HOT).count()
                avg_score = db.query(Lead).with_entities(
                    db.func.avg(Lead.score)
                ).scalar() or 0
                
                self._send_json({
                    "pipeline": pipeline,
                    "summary": {
                        "total_leads": total_leads,
                        "hot_leads": hot_leads,
                        "average_score": round(float(avg_score), 2)
                    }
                })
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
