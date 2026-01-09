"""
Label schema schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class LabelClass(BaseModel):
    name: str
    color: str
    description: Optional[str] = None
    children: Optional[List["LabelClass"]] = None

LabelClass.model_rebuild()

class LabelSchemaBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: str = "1.0.0"
    schema_definition: Dict[str, Any]

class LabelSchemaCreate(LabelSchemaBase):
    is_default: bool = False

class LabelSchemaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    schema_definition: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None

class LabelSchemaResponse(LabelSchemaBase):
    id: int
    is_default: bool
    is_active: bool
    creator_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
