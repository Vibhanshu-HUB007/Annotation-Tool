"""
Label schema API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.label_schema import LabelSchema
from app.schemas.label_schema import LabelSchemaCreate, LabelSchemaUpdate, LabelSchemaResponse

router = APIRouter()

@router.post("/", response_model=LabelSchemaResponse, status_code=status.HTTP_201_CREATED)
async def create_label_schema(
    schema: LabelSchemaCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new label schema"""
    # Check if name already exists
    existing = db.query(LabelSchema).filter(LabelSchema.name == schema.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Label schema with this name already exists"
        )
    
    # If setting as default, unset other defaults
    if schema.is_default:
        db.query(LabelSchema).filter(LabelSchema.is_default == True).update({"is_default": False})
    
    db_schema = LabelSchema(
        **schema.dict(),
        creator_id=current_user.id
    )
    db.add(db_schema)
    db.commit()
    db.refresh(db_schema)
    return db_schema

@router.get("/", response_model=List[LabelSchemaResponse])
async def list_label_schemas(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all label schemas"""
    query = db.query(LabelSchema)
    if active_only:
        query = query.filter(LabelSchema.is_active == True)
    schemas = query.all()
    return schemas

@router.get("/default", response_model=LabelSchemaResponse)
async def get_default_schema(
    db: Session = Depends(get_db)
):
    """Get the default label schema"""
    schema = db.query(LabelSchema).filter(LabelSchema.is_default == True).first()
    if not schema:
        # Return oral cytology default schema
        return get_oral_cytology_default_schema()
    return schema

@router.get("/{schema_id}", response_model=LabelSchemaResponse)
async def get_label_schema(
    schema_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific label schema"""
    schema = db.query(LabelSchema).filter(LabelSchema.id == schema_id).first()
    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label schema not found"
        )
    return schema

@router.put("/{schema_id}", response_model=LabelSchemaResponse)
async def update_label_schema(
    schema_id: int,
    schema_update: LabelSchemaUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a label schema"""
    schema = db.query(LabelSchema).filter(LabelSchema.id == schema_id).first()
    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label schema not found"
        )
    
    # Check permissions (admin or creator)
    if schema.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this schema"
        )
    
    update_data = schema_update.dict(exclude_unset=True)
    
    # If setting as default, unset other defaults
    if update_data.get("is_default") == True:
        db.query(LabelSchema).filter(
            LabelSchema.is_default == True,
            LabelSchema.id != schema_id
        ).update({"is_default": False})
    
    for field, value in update_data.items():
        setattr(schema, field, value)
    
    db.commit()
    db.refresh(schema)
    return schema

@router.delete("/{schema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label_schema(
    schema_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a label schema"""
    schema = db.query(LabelSchema).filter(LabelSchema.id == schema_id).first()
    if not schema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label schema not found"
        )
    
    # Check permissions
    if schema.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this schema"
        )
    
    db.delete(schema)
    db.commit()
    return None

def get_oral_cytology_default_schema():
    """Get the default oral cytology label schema"""
    return {
        "id": 0,
        "name": "Oral Cytology Default",
        "description": "Default label schema for oral cytology annotations",
        "version": "1.0.0",
        "schema_definition": {
            "classes": [
                {
                    "name": "Malignant",
                    "color": "#FF0000",
                    "description": "Malignant cells and structures",
                    "children": [
                        {
                            "name": "OSCC",
                            "color": "#CC0000",
                            "description": "Oral Squamous Cell Carcinoma"
                        },
                        {
                            "name": "Severe Dysplasia",
                            "color": "#FF6666",
                            "description": "Severe dysplastic changes"
                        }
                    ]
                },
                {
                    "name": "Dysplastic Epithelial Cells",
                    "color": "#FF8800",
                    "description": "Dysplastic epithelial cells"
                },
                {
                    "name": "Keratin Pearls",
                    "color": "#FFAA00",
                    "description": "Keratin pearl formations"
                },
                {
                    "name": "Nuclear Pleomorphism",
                    "color": "#FFCC00",
                    "description": "Regions with nuclear pleomorphism"
                },
                {
                    "name": "Increased N:C Ratio",
                    "color": "#FFFF00",
                    "description": "Cells with increased nuclear to cytoplasmic ratio"
                },
                {
                    "name": "Hyperchromatic Nuclei",
                    "color": "#8800FF",
                    "description": "Hyperchromatic nuclei"
                },
                {
                    "name": "Mitotic Figures",
                    "color": "#AA00FF",
                    "description": "Mitotic figures"
                },
                {
                    "name": "Inflammatory Infiltrates",
                    "color": "#00AAFF",
                    "description": "Inflammatory cell infiltrates"
                },
                {
                    "name": "Stromal Invasion",
                    "color": "#FF0088",
                    "description": "Stromal invasion areas"
                },
                {
                    "name": "Normal Epithelium",
                    "color": "#00FF00",
                    "description": "Normal epithelial tissue"
                },
                {
                    "name": "Artifacts",
                    "color": "#888888",
                    "description": "Background artifacts",
                    "children": [
                        {
                            "name": "Blood",
                            "color": "#AA0000",
                            "description": "Blood artifacts"
                        },
                        {
                            "name": "Debris",
                            "color": "#666666",
                            "description": "Debris artifacts"
                        },
                        {
                            "name": "Folds",
                            "color": "#444444",
                            "description": "Tissue folds"
                        }
                    ]
                }
            ]
        },
        "is_default": True,
        "is_active": True
    }
