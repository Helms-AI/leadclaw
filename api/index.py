"""
LeadClaw API - Health Check & Info
"""
from http.server import BaseHTTPRequestHandler
import json
from api.db import health_check


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        db_status = health_check()
        
        response = {
            "name": "LeadClaw API",
            "version": "1.0.0",
            "status": "running",
            "database": db_status,
            "endpoints": {
                "leads": "/api/leads",
                "sequences": "/api/sequences",
                "templates": "/api/templates",
                "pipeline": "/api/pipeline",
                "stats": "/api/stats"
            }
        }
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())
