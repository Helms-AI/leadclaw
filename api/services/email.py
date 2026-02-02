"""
Email Service - SendGrid integration
"""
import os
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Template

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "sales@helmsai.com")
FROM_NAME = os.environ.get("FROM_NAME", "Kade @ Helms AI")


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
) -> dict:
    """Send an email via SendGrid"""
    if not SENDGRID_API_KEY:
        return {"success": False, "error": "SENDGRID_API_KEY not configured"}
    
    try:
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        
        if text_content:
            message.add_content(Content("text/plain", text_content))
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        return {
            "success": True,
            "status_code": response.status_code,
            "message_id": response.headers.get("X-Message-Id")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def render_template(template_html: str, variables: dict) -> str:
    """Render a Jinja2 template with variables"""
    template = Template(template_html)
    return template.render(**variables)


def personalize_email(template, lead) -> tuple[str, str]:
    """Personalize an email template for a specific lead"""
    variables = {
        "first_name": lead.first_name or "there",
        "last_name": lead.last_name or "",
        "full_name": lead.full_name,
        "email": lead.email,
        "company_name": lead.company_name or "your company",
        "job_title": lead.job_title or "",
        "industry": lead.industry or "",
    }
    
    subject = render_template(template.subject, variables)
    body = render_template(template.body_html, variables)
    
    return subject, body
