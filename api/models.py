"""
LeadClaw Data Models (SQLAlchemy + Neon PostgreSQL)
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Float, 
    Boolean, ForeignKey, Enum as SQLEnum, JSON
)
from sqlalchemy.orm import relationship
from api.db import Base


class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    ENGAGED = "engaged"
    QUALIFIED = "qualified"
    HOT = "hot"
    CONVERTED = "converted"
    LOST = "lost"
    UNSUBSCRIBED = "unsubscribed"


class Lead(Base):
    """Core lead entity"""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Contact info
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(50))
    
    # Company info
    company_name = Column(String(255))
    company_domain = Column(String(255))
    job_title = Column(String(255))
    industry = Column(String(100))
    company_size = Column(String(50))  # e.g., "11-50", "51-200"
    
    # Location
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    timezone = Column(String(50))
    
    # Lead management
    status = Column(SQLEnum(LeadStatus), default=LeadStatus.NEW, index=True)
    score = Column(Float, default=0.0, index=True)
    source = Column(String(100))  # e.g., "apollo", "website", "referral"
    
    # Enrichment data (JSON blob for flexibility)
    enrichment_data = Column(JSON, default=dict)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted_at = Column(DateTime)
    last_replied_at = Column(DateTime)
    
    # Relationships
    activities = relationship("Activity", back_populates="lead", cascade="all, delete-orphan")
    sequence_enrollments = relationship("SequenceEnrollment", back_populates="lead")

    @property
    def full_name(self) -> str:
        parts = [self.first_name, self.last_name]
        return " ".join(p for p in parts if p) or self.email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "phone": self.phone,
            "company_name": self.company_name,
            "company_domain": self.company_domain,
            "job_title": self.job_title,
            "industry": self.industry,
            "company_size": self.company_size,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "status": self.status.value if self.status else None,
            "score": self.score,
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_contacted_at": self.last_contacted_at.isoformat() if self.last_contacted_at else None,
            "last_replied_at": self.last_replied_at.isoformat() if self.last_replied_at else None,
        }


class ActivityType(str, Enum):
    EMAIL_SENT = "email_sent"
    EMAIL_OPENED = "email_opened"
    EMAIL_CLICKED = "email_clicked"
    EMAIL_REPLIED = "email_replied"
    EMAIL_BOUNCED = "email_bounced"
    STATUS_CHANGE = "status_change"
    SCORE_CHANGE = "score_change"
    NOTE_ADDED = "note_added"
    HANDOFF = "handoff"


class Activity(Base):
    """Activity log for leads"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False, index=True)
    
    type = Column(SQLEnum(ActivityType), nullable=False)
    description = Column(Text)
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    lead = relationship("Lead", back_populates="activities")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "type": self.type.value,
            "description": self.description,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class EmailTemplate(Base):
    """Email templates for sequences"""
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body_html = Column(Text, nullable=False)
    body_text = Column(Text)
    
    # Template variables (JSON schema)
    variables = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "subject": self.subject,
            "body_html": self.body_html,
            "body_text": self.body_text,
            "variables": self.variables,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Sequence(Base):
    """Email sequences (multi-step campaigns)"""
    __tablename__ = "sequences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    steps = relationship("SequenceStep", back_populates="sequence", order_by="SequenceStep.order")
    enrollments = relationship("SequenceEnrollment", back_populates="sequence")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_active": self.is_active,
            "steps": [s.to_dict() for s in self.steps],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class SequenceStep(Base):
    """Individual steps in a sequence"""
    __tablename__ = "sequence_steps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sequence_id = Column(Integer, ForeignKey("sequences.id"), nullable=False)
    
    order = Column(Integer, nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"))
    delay_days = Column(Integer, default=0)  # Days after previous step
    delay_hours = Column(Integer, default=0)
    
    # Conditions (JSON for flexibility)
    conditions = Column(JSON, default=dict)
    
    sequence = relationship("Sequence", back_populates="steps")
    template = relationship("EmailTemplate")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "sequence_id": self.sequence_id,
            "order": self.order,
            "template_id": self.template_id,
            "delay_days": self.delay_days,
            "delay_hours": self.delay_hours,
            "conditions": self.conditions,
        }


class SequenceEnrollment(Base):
    """Track leads enrolled in sequences"""
    __tablename__ = "sequence_enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    sequence_id = Column(Integer, ForeignKey("sequences.id"), nullable=False)
    
    current_step = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    completed_at = Column(DateTime)
    
    # Track when next email should be sent
    next_send_at = Column(DateTime, index=True)
    
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    
    lead = relationship("Lead", back_populates="sequence_enrollments")
    sequence = relationship("Sequence", back_populates="enrollments")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "lead_id": self.lead_id,
            "sequence_id": self.sequence_id,
            "current_step": self.current_step,
            "is_active": self.is_active,
            "next_send_at": self.next_send_at.isoformat() if self.next_send_at else None,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
        }
