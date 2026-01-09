"""
WSI file management API routes
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
import shutil
import os
from PIL import Image
import openslide

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.wsi import WSIFile
from app.schemas.wsi import WSIFileResponse, WSITileRequest
from app.utils.wsi_processor import process_wsi_file, get_wsi_tile

router = APIRouter()

@router.post("/upload", response_model=WSIFileResponse, status_code=status.HTTP_201_CREATED)
async def upload_wsi(
    file: UploadFile = File(...),
    study_instance_uid: str = None,
    patient_id: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a WSI file"""
    # Validate file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_ext} not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Save file
    upload_dir = Path(settings.UPLOAD_DIR)
    file_path = upload_dir / f"{current_user.id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = file_path.stat().st_size
    
    # Process WSI metadata
    try:
        if file_ext in [".svs", ".tiff", ".tif", ".ndpi", ".mrxs"]:
            slide = openslide.OpenSlide(str(file_path))
            width, height = slide.dimensions
            mpp_x = float(slide.properties.get(openslide.PROPERTY_NAME_MPP_X, 0))
            mpp_y = float(slide.properties.get(openslide.PROPERTY_NAME_MPP_Y, 0))
            levels = slide.level_count
            magnification = float(slide.properties.get(openslide.PROPERTY_NAME_OBJECTIVE_POWER, 0))
            metadata = dict(slide.properties)
            slide.close()
        else:
            # Regular image
            img = Image.open(file_path)
            width, height = img.size
            mpp_x = mpp_y = None
            levels = 1
            magnification = None
            metadata = {}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing WSI file: {str(e)}"
        )
    
    # Create database record
    db_wsi = WSIFile(
        filename=file_path.name,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        file_format=file_ext,
        width=width,
        height=height,
        mpp_x=mpp_x,
        mpp_y=mpp_y,
        magnification=magnification,
        levels=levels,
        wsi_metadata=metadata,
        study_instance_uid=study_instance_uid,
        patient_id=patient_id,
        uploader_id=current_user.id
    )
    db.add(db_wsi)
    db.commit()
    db.refresh(db_wsi)
    
    # Process WSI in background (tile generation, etc.)
    # This would typically be done in a background task
    
    return db_wsi

@router.get("/", response_model=List[WSIFileResponse])
async def list_wsi_files(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List all WSI files"""
    wsi_files = db.query(WSIFile).offset(skip).limit(limit).all()
    return wsi_files

@router.get("/{wsi_id}", response_model=WSIFileResponse)
async def get_wsi_file(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific WSI file"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    return wsi_file

@router.get("/{wsi_id}/tile-source")
async def get_tile_source(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get OpenSeadragon tile source configuration"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    # For OpenSeadragon, we'll use a custom tile source function
    # that calls our tile endpoint
    tile_source = {
        "type": "custom",
        "tileSource": {
            "getTileUrl": f"/api/wsi/{wsi_id}/tile",
            "width": wsi_file.width or 0,
            "height": wsi_file.height or 0,
            "tileSize": 256,
            "tileOverlap": 0,
            "minLevel": 0,
            "maxLevel": wsi_file.levels or 0,
        }
    }
    return tile_source

@router.get("/{wsi_id}/tile")
async def get_tile(
    wsi_id: int,
    level: int,
    x: int,
    y: int,
    format: str = "jpeg",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a tile from a WSI file"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    try:
        tile_data = get_wsi_tile(wsi_file.file_path, level, x, y, format)
        from fastapi.responses import Response
        return Response(content=tile_data, media_type=f"image/{format}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting tile: {str(e)}"
        )

@router.delete("/{wsi_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wsi_file(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a WSI file"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    # Check permissions (admin or owner)
    if current_user.role != "admin" and wsi_file.uploader_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this file"
        )
    
    # Delete file from filesystem
    if os.path.exists(wsi_file.file_path):
        os.remove(wsi_file.file_path)
    
    db.delete(wsi_file)
    db.commit()
    return None
