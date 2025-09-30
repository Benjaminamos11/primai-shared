"""Premium query and quote models"""
from sqlalchemy import Column, String, ForeignKey, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID
from shared.models.base import BaseModel


class PremiumQuery(BaseModel):
    """Premium calculation query"""
    
    __tablename__ = "premium_queries"
    
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True)
    insurance_type = Column(String, nullable=False)
    query_data = Column(JSON, nullable=False)
    result_data = Column(JSON, default=dict)
    status = Column(String, default="pending")


class Quote(BaseModel):
    """Insurance quote"""
    
    __tablename__ = "quotes"
    
    premium_query_id = Column(UUID(as_uuid=True), ForeignKey("premium_queries.id"), nullable=False, index=True)
    insurer_id = Column(UUID(as_uuid=True), ForeignKey("insurers.id"), nullable=True, index=True)
    product_name = Column(String, nullable=False)
    annual_premium = Column(Numeric(10, 2), nullable=False)
    coverage_details = Column(JSON, default=dict)
    quote_data = Column(JSON, default=dict)
    status = Column(String, default="draft")
