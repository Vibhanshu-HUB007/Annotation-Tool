"""
Annotation API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.annotation import Annotation
from app.models.wsi import WSIFile
from app.schemas.annotation import (
    AnnotationCreate, AnnotationUpdate, AnnotationResponse,
    AnnotationBatchCreate
)

router = APIRouter()

def calculate_annotation_metrics(geometry: dict, mpp_x: float = None, mpp_y: float = None):
    """Calculate area, perimeter, and centroid from geometry"""
    try:
        geom = shape(geometry)
        area_pixels = geom.area
        perimeter_pixels = geom.length
        
        # Convert to microns if MPP available
        if mpp_x and mpp_y:
            area_um2 = area_pixels * mpp_x * mpp_y
            perimeter_um = perimeter_pixels * ((mpp_x + mpp_y) / 2)
        else:
            area_um2 = None
            perimeter_um = None
        
        centroid = geom.centroid
        
        return {
            "area_um2": area_um2,
            "perimeter_um": perimeter_um,
            "centroid_x": centroid.x,
            "centroid_y": centroid.y
        }
    except Exception:
        return {
            "area_um2": None,
            "perimeter_um": None,
            "centroid_x": None,
            "centroid_y": None
        }

@router.post("/", response_model=AnnotationResponse, status_code=status.HTTP_201_CREATED)
async def create_annotation(
    annotation: AnnotationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new annotation"""
    # Verify WSI file exists
    wsi_file = db.query(WSIFile).filter(WSIFile.id == annotation.wsi_file_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    # Calculate metrics
    metrics = calculate_annotation_metrics(
        annotation.geometry,
        wsi_file.mpp_x,
        wsi_file.mpp_y
    )
    
    # Create annotation
    db_annotation = Annotation(
        **annotation.dict(),
        creator_id=current_user.id,
        **metrics
    )
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    return db_annotation

@router.post("/batch", response_model=List[AnnotationResponse], status_code=status.HTTP_201_CREATED)
async def create_annotations_batch(
    batch: AnnotationBatchCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create multiple annotations at once"""
    # Verify WSI file exists
    wsi_file = db.query(WSIFile).filter(WSIFile.id == batch.wsi_file_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    db_annotations = []
    for annotation_data in batch.annotations:
        metrics = calculate_annotation_metrics(
            annotation_data.geometry,
            wsi_file.mpp_x,
            wsi_file.mpp_y
        )
        db_annotation = Annotation(
            **annotation_data.dict(),
            wsi_file_id=batch.wsi_file_id,
            creator_id=current_user.id,
            **metrics
        )
        db.add(db_annotation)
        db_annotations.append(db_annotation)
    
    db.commit()
    for ann in db_annotations:
        db.refresh(ann)
    return db_annotations

@router.get("/wsi/{wsi_id}", response_model=List[AnnotationResponse])
async def get_annotations_by_wsi(
    wsi_id: int,
    layer_name: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all annotations for a WSI file"""
    query = db.query(Annotation).filter(
        Annotation.wsi_file_id == wsi_id,
        Annotation.deleted_at.is_(None)
    )
    
    if layer_name:
        query = query.filter(Annotation.layer_name == layer_name)
    
    annotations = query.all()
    return annotations

@router.get("/{annotation_id}", response_model=AnnotationResponse)
async def get_annotation(
    annotation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific annotation"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation or annotation.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    return annotation

@router.put("/{annotation_id}", response_model=AnnotationResponse)
async def update_annotation(
    annotation_id: int,
    annotation_update: AnnotationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an annotation"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation or annotation.deleted_at:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Check permissions
    if annotation.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this annotation"
        )
    
    # Update fields
    update_data = annotation_update.dict(exclude_unset=True)
    if "geometry" in update_data:
        # Recalculate metrics if geometry changed
        wsi_file = annotation.wsi_file
        metrics = calculate_annotation_metrics(
            update_data["geometry"],
            wsi_file.mpp_x,
            wsi_file.mpp_y
        )
        update_data.update(metrics)
    
    for field, value in update_data.items():
        setattr(annotation, field, value)
    
    # Increment version
    annotation.version += 1
    
    db.commit()
    db.refresh(annotation)
    return annotation

@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(
    annotation_id: int,
    hard_delete: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an annotation (soft delete by default)"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Check permissions
    if annotation.creator_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this annotation"
        )
    
    if hard_delete:
        db.delete(annotation)
    else:
        from datetime import datetime
        annotation.deleted_at = datetime.utcnow()
    
    db.commit()
    return None
