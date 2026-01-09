"""
WSI file schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class WSIFileBase(BaseModel):
    filename: str
    original_filename: str
    file_format: str

class WSIFileCreate(WSIFileBase):
    file_path: str
    file_size: int
    study_instance_uid: Optional[str] = None
    patient_id: Optional[str] = None
    study_date: Optional[datetime] = None

class WSIFileResponse(WSIFileBase):
    id: int
    file_path: str
    file_size: int
    width: Optional[int] = None
    height: Optional[int] = None
    mpp_x: Optional[float] = None
    mpp_y: Optional[float] = None
    magnification: Optional[float] = None
    levels: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    study_instance_uid: Optional[str] = None
    patient_id: Optional[str] = None
    study_date: Optional[datetime] = None
    is_processed: bool
    processing_status: str
    uploader_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WSITileRequest(BaseModel):
    wsi_id: int
    level: int
    x: int
    y: int
    format: str = "jpeg"
