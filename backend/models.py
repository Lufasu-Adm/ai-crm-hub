from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    source = Column(String, default="web_form")
    status = Column(String, default="New") 
    lead_score = Column(Integer, default=0)
    ai_category = Column(String, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)