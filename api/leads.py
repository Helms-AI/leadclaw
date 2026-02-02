"""
LeadClaw API - Leads CRUD
"""
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from api.db import get_db
from api.models import Lead, LeadStatus, Activity, ActivityType


class handler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _get_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length:
            return json.loads(self.rfile.read(content_length))
        return {}

    def do_OPTIONS(self):
        self._send_json({})

    def do_GET(self):
        """List leads or get single lead"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        # Check for ID in path: /api/leads/123
        path_parts = parsed.path.strip("/").split("/")
        lead_id = int(path_parts[2]) if len(path_parts) > 2 and path_parts[2].isdigit() else None
        
        try:
            with get_db() as db:
                if lead_id:
                    # Get single lead
                    lead = db.query(Lead).filter(Lead.id == lead_id).first()
                    if not lead:
                        self._send_json({"error": "Lead not found"}, 404)
                        return
                    self._send_json(lead.to_dict())
                else:
                    # List leads with filters
                    query = db.query(Lead)
                    
                    # Filter by status
                    if "status" in params:
                        query = query.filter(Lead.status == params["status"][0])
                    
                    # Filter by minimum score
                    if "min_score" in params:
                        query = query.filter(Lead.score >= float(params["min_score"][0]))
                    
                    # Search by email/company
                    if "search" in params:
                        search = f"%{params['search'][0]}%"
                        query = query.filter(
                            (Lead.email.ilike(search)) | 
                            (Lead.company_name.ilike(search)) |
                            (Lead.first_name.ilike(search)) |
                            (Lead.last_name.ilike(search))
                        )
                    
                    # Pagination
                    limit = int(params.get("limit", [50])[0])
                    offset = int(params.get("offset", [0])[0])
                    
                    # Order by score descending (hot leads first)
                    query = query.order_by(Lead.score.desc())
                    
                    total = query.count()
                    leads = query.limit(limit).offset(offset).all()
                    
                    self._send_json({
                        "leads": [l.to_dict() for l in leads],
                        "total": total,
                        "limit": limit,
                        "offset": offset
                    })
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_POST(self):
        """Create a new lead"""
        try:
            data = self._get_body()
            
            if not data.get("email"):
                self._send_json({"error": "Email is required"}, 400)
                return
            
            with get_db() as db:
                # Check for duplicate
                existing = db.query(Lead).filter(Lead.email == data["email"]).first()
                if existing:
                    self._send_json({"error": "Lead with this email already exists", "lead": existing.to_dict()}, 409)
                    return
                
                lead = Lead(
                    email=data["email"],
                    first_name=data.get("first_name"),
                    last_name=data.get("last_name"),
                    phone=data.get("phone"),
                    company_name=data.get("company_name"),
                    company_domain=data.get("company_domain"),
                    job_title=data.get("job_title"),
                    industry=data.get("industry"),
                    company_size=data.get("company_size"),
                    city=data.get("city"),
                    state=data.get("state"),
                    country=data.get("country"),
                    timezone=data.get("timezone"),
                    source=data.get("source", "manual"),
                    status=LeadStatus(data.get("status", "new")),
                    score=data.get("score", 0.0),
                    enrichment_data=data.get("enrichment_data", {})
                )
                db.add(lead)
                db.flush()  # Get the ID
                
                # Log activity
                activity = Activity(
                    lead_id=lead.id,
                    type=ActivityType.STATUS_CHANGE,
                    description=f"Lead created with status: {lead.status.value}",
                    metadata={"source": lead.source}
                )
                db.add(activity)
                
                self._send_json(lead.to_dict(), 201)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_PUT(self):
        """Update a lead"""
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) < 3 or not path_parts[2].isdigit():
            self._send_json({"error": "Lead ID required in path"}, 400)
            return
        
        lead_id = int(path_parts[2])
        
        try:
            data = self._get_body()
            
            with get_db() as db:
                lead = db.query(Lead).filter(Lead.id == lead_id).first()
                if not lead:
                    self._send_json({"error": "Lead not found"}, 404)
                    return
                
                # Track status change
                old_status = lead.status
                
                # Update fields
                for field in ["first_name", "last_name", "phone", "company_name", 
                              "company_domain", "job_title", "industry", "company_size",
                              "city", "state", "country", "timezone", "source", "enrichment_data"]:
                    if field in data:
                        setattr(lead, field, data[field])
                
                if "status" in data:
                    lead.status = LeadStatus(data["status"])
                
                if "score" in data:
                    lead.score = float(data["score"])
                
                # Log status change
                if lead.status != old_status:
                    activity = Activity(
                        lead_id=lead.id,
                        type=ActivityType.STATUS_CHANGE,
                        description=f"Status changed: {old_status.value} → {lead.status.value}",
                        metadata={"old_status": old_status.value, "new_status": lead.status.value}
                    )
                    db.add(activity)
                
                self._send_json(lead.to_dict())
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_DELETE(self):
        """Delete a lead"""
        parsed = urlparse(self.path)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) < 3 or not path_parts[2].isdigit():
            self._send_json({"error": "Lead ID required in path"}, 400)
            return
        
        lead_id = int(path_parts[2])
        
        try:
            with get_db() as db:
                lead = db.query(Lead).filter(Lead.id == lead_id).first()
                if not lead:
                    self._send_json({"error": "Lead not found"}, 404)
                    return
                
                db.delete(lead)
                self._send_json({"deleted": True, "id": lead_id})
        except Exception as e:
            self._send_json({"error": str(e)}, 500)
