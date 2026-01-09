"""
WSI file model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class WSIFile(Base):
    __tablename__ = "wsi_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_format = Column(String, nullable=False)  # .svs, .tiff, etc.
    
    # WSI metadata
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    mpp_x = Column(Float, nullable=True)  # microns per pixel X
    mpp_y = Column(Float, nullable=True)  # microns per pixel Y
    magnification = Column(Float, nullable=True)  # e.g., 20.0, 40.0
    levels = Column(Integer, nullable=True)  # pyramid levels
    wsi_metadata = Column(JSON, nullable=True)  # Additional metadata (renamed from 'metadata' - reserved in SQLAlchemy)
    
    # Study information
    study_instance_uid = Column(String, nullable=True)
    patient_id = Column(String, nullable=True)
    study_date = Column(DateTime, nullable=True)
    
    # Status
    is_processed = Column(Boolean, default=False)
    processing_status = Column(String, default="pending")  # pending, processing, completed, error
    
    # Relationships
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploader = relationship("User", back_populates="wsi_files")
    annotations = relationship("Annotation", back_populates="wsi_file", cascade="all, delete-orphan")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
