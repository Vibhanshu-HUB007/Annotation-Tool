"""
Annotation schemas
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class AnnotationBase(BaseModel):
    geometry: Dict[str, Any]  # GeoJSON geometry
    geometry_type: str
    label: str
    label_hierarchy: Optional[List[str]] = None
    color: Optional[str] = None
    opacity: float = 0.7
    description: Optional[str] = None
    layer_name: str = "default"
    is_locked: bool = False
    is_visible: bool = True

class AnnotationCreate(AnnotationBase):
    wsi_file_id: int
    confidence: Optional[float] = None
    is_ai_generated: bool = False
    ai_model_version: Optional[str] = None

class AnnotationUpdate(BaseModel):
    geometry: Optional[Dict[str, Any]] = None
    geometry_type: Optional[str] = None
    label: Optional[str] = None
    label_hierarchy: Optional[List[str]] = None
    color: Optional[str] = None
    opacity: Optional[float] = None
    description: Optional[str] = None
    layer_name: Optional[str] = None
    is_locked: Optional[bool] = None
    is_visible: Optional[bool] = None
    confidence: Optional[float] = None

class AnnotationResponse(AnnotationBase):
    id: int
    wsi_file_id: int
    confidence: Optional[float] = None
    is_ai_generated: bool
    ai_model_version: Optional[str] = None
    area_um2: Optional[float] = None
    perimeter_um: Optional[float] = None
    centroid_x: Optional[float] = None
    centroid_y: Optional[float] = None
    version: int
    parent_annotation_id: Optional[int] = None
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnnotationBatchCreate(BaseModel):
    wsi_file_id: int
    annotations: List[AnnotationCreate]
