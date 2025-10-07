from sqlalchemy import JSON, Column, String

from shared.models.base import BaseModel


class FunnelEvent(BaseModel):
    """Funnel event model for tracking user journey."""

    __tablename__ = "funnel_events"

    # Event identification
    event_type = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    lead_id = Column(String, nullable=True)

    # Event payload
    payload = Column(JSON, nullable=True)

    # Context data
    geo_data = Column(JSON, nullable=True)  # {country, region, city, plz}
    locale = Column(String, nullable=True)
    utm_source = Column(String, nullable=True)
    utm_medium = Column(String, nullable=True)
    utm_campaign = Column(String, nullable=True)
    utm_term = Column(String, nullable=True)
    utm_content = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    browser = Column(String, nullable=True)
    os = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    ip_hash = Column(String, nullable=True)
