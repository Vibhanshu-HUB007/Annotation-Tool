"""
Annotation model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Annotation(Base):
    __tablename__ = "annotations"

    id = Column(Integer, primary_key=True, index=True)
    
    # WSI reference
    wsi_file_id = Column(Integer, ForeignKey("wsi_files.id"), nullable=False)
    wsi_file = relationship("WSIFile", back_populates="annotations")
    
    # Annotation geometry (GeoJSON format)
    geometry = Column(JSON, nullable=False)  # GeoJSON geometry object
    geometry_type = Column(String, nullable=False)  # Polygon, Point, LineString, etc.
    
    # Annotation properties
    label = Column(String, nullable=False)  # Class label
    label_hierarchy = Column(JSON, nullable=True)  # ["Malignant", "OSCC", "Severe dysplasia"]
    color = Column(String, nullable=True)  # Hex color code
    opacity = Column(Float, default=0.7)
    
    # Annotation metadata
    description = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)  # For AI annotations
    is_ai_generated = Column(Boolean, default=False)
    ai_model_version = Column(String, nullable=True)
    
    # Layer and visibility
    layer_name = Column(String, default="default")
    is_locked = Column(Boolean, default=False)
    is_visible = Column(Boolean, default=True)
    
    # Measurements (for cytology)
    area_um2 = Column(Float, nullable=True)  # Area in square microns
    perimeter_um = Column(Float, nullable=True)
    centroid_x = Column(Float, nullable=True)
    centroid_y = Column(Float, nullable=True)
    
    # Versioning and audit
    version = Column(Integer, default=1)
    parent_annotation_id = Column(Integer, ForeignKey("annotations.id"), nullable=True)
    parent_annotation = relationship("Annotation", remote_side=[id], backref="versions")
    
    # Creator
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", back_populates="annotations")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
