"""
Label schema model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class LabelSchema(Base):
    __tablename__ = "label_schemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    version = Column(String, default="1.0.0")
    
    # Schema definition (hierarchical structure)
    schema_definition = Column(JSON, nullable=False)  # Full schema JSON
    
    # Default schema for oral cytology
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Creator
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
