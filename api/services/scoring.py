"""
Lead Scoring Service
"""
from datetime import datetime, timedelta
from api.models import Lead, Activity, ActivityType


# Scoring weights (configurable)
SCORE_WEIGHTS = {
    # Engagement signals
    "email_opened": 5,
    "email_clicked": 15,
    "email_replied": 30,
    
    # Profile completeness
    "has_phone": 5,
    "has_company": 5,
    "has_title": 5,
    
    # Company fit (ICP match)
    "target_industry": 10,
    "target_company_size": 10,
    
    # Recency
    "contacted_this_week": 10,
    "replied_this_week": 20,
    
    # Negative signals
    "email_bounced": -50,
    "unsubscribed": -100,
}

# Target industries (ICP)
TARGET_INDUSTRIES = [
    "technology",
    "software",
    "saas",
    "professional services",
    "consulting",
    "finance",
    "healthcare",
]

# Target company sizes
TARGET_COMPANY_SIZES = [
    "11-50",
    "51-200",
    "201-500",
]


def calculate_lead_score(lead: Lead, activities: list[Activity]) -> float:
    """Calculate a lead's score based on profile and activities"""
    score = 0.0
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    
    # Profile completeness
    if lead.phone:
        score += SCORE_WEIGHTS["has_phone"]
    if lead.company_name:
        score += SCORE_WEIGHTS["has_company"]
    if lead.job_title:
        score += SCORE_WEIGHTS["has_title"]
    
    # ICP match
    if lead.industry and lead.industry.lower() in TARGET_INDUSTRIES:
        score += SCORE_WEIGHTS["target_industry"]
    if lead.company_size and lead.company_size in TARGET_COMPANY_SIZES:
        score += SCORE_WEIGHTS["target_company_size"]
    
    # Activity signals
    for activity in activities:
        if activity.type == ActivityType.EMAIL_OPENED:
            score += SCORE_WEIGHTS["email_opened"]
        elif activity.type == ActivityType.EMAIL_CLICKED:
            score += SCORE_WEIGHTS["email_clicked"]
        elif activity.type == ActivityType.EMAIL_REPLIED:
            score += SCORE_WEIGHTS["email_replied"]
            if activity.created_at and activity.created_at >= week_ago:
                score += SCORE_WEIGHTS["replied_this_week"]
        elif activity.type == ActivityType.EMAIL_BOUNCED:
            score += SCORE_WEIGHTS["email_bounced"]
    
    # Recency bonus
    if lead.last_contacted_at and lead.last_contacted_at >= week_ago:
        score += SCORE_WEIGHTS["contacted_this_week"]
    
    # Unsubscribed penalty
    if lead.status and lead.status.value == "unsubscribed":
        score += SCORE_WEIGHTS["unsubscribed"]
    
    # Clamp to 0-100
    return max(0, min(100, score))


def should_handoff(lead: Lead) -> bool:
    """Determine if a lead should be handed off to Ryan"""
    # Hot leads with recent replies
    if lead.score >= 70:
        return True
    
    # Explicit hot status
    if lead.status and lead.status.value == "hot":
        return True
    
    # Multiple replies
    if lead.last_replied_at:
        return True
    
    return False
