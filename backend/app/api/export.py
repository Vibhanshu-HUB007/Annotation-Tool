"""
Export API routes for annotations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
import csv
import io

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.annotation import Annotation
from app.models.wsi import WSIFile

router = APIRouter()

@router.get("/wsi/{wsi_id}/coco")
async def export_coco(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export annotations in COCO JSON format"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    annotations = db.query(Annotation).filter(
        Annotation.wsi_file_id == wsi_id,
        Annotation.deleted_at.is_(None)
    ).all()
    
    # Build COCO format
    coco_data = {
        "info": {
            "description": f"Annotations for {wsi_file.original_filename}",
            "version": "1.0"
        },
        "images": [{
            "id": 1,
            "width": wsi_file.width or 0,
            "height": wsi_file.height or 0,
            "file_name": wsi_file.original_filename
        }],
        "annotations": [],
        "categories": []
    }
    
    # Extract unique categories
    categories_map = {}
    category_id = 1
    
    for ann in annotations:
        if ann.label not in categories_map:
            categories_map[ann.label] = category_id
            coco_data["categories"].append({
                "id": category_id,
                "name": ann.label,
                "supercategory": ann.label_hierarchy[0] if ann.label_hierarchy else "none"
            })
            category_id += 1
        
        # Convert GeoJSON to COCO segmentation format
        geometry = ann.geometry
        if geometry["type"] == "Polygon":
            # Flatten coordinates
            segmentation = []
            for ring in geometry["coordinates"]:
                flat = [coord for point in ring for coord in point]
                segmentation.append(flat)
        else:
            segmentation = []
        
        # Calculate bbox
        from shapely.geometry import shape
        geom = shape(geometry)
        bbox = list(geom.bounds)  # [minx, miny, maxx, maxy]
        bbox[2] -= bbox[0]  # width
        bbox[3] -= bbox[1]  # height
        bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
        
        coco_data["annotations"].append({
            "id": ann.id,
            "image_id": 1,
            "category_id": categories_map[ann.label],
            "segmentation": segmentation,
            "area": ann.area_um2 or 0,
            "bbox": bbox,
            "iscrowd": 0
        })
    
    return Response(
        content=json.dumps(coco_data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{wsi_file.original_filename}_coco.json"'}
    )

@router.get("/wsi/{wsi_id}/geojson")
async def export_geojson(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export annotations in GeoJSON format"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    annotations = db.query(Annotation).filter(
        Annotation.wsi_file_id == wsi_id,
        Annotation.deleted_at.is_(None)
    ).all()
    
    features = []
    for ann in annotations:
        feature = {
            "type": "Feature",
            "geometry": ann.geometry,
            "properties": {
                "id": ann.id,
                "label": ann.label,
                "label_hierarchy": ann.label_hierarchy,
                "color": ann.color,
                "opacity": ann.opacity,
                "description": ann.description,
                "confidence": ann.confidence,
                "is_ai_generated": ann.is_ai_generated,
                "layer_name": ann.layer_name,
                "area_um2": ann.area_um2,
                "perimeter_um": ann.perimeter_um,
                "creator_id": ann.creator_id,
                "created_at": ann.created_at.isoformat(),
                "updated_at": ann.updated_at.isoformat()
            }
        }
        features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return Response(
        content=json.dumps(geojson, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{wsi_file.original_filename}_annotations.geojson"'}
    )

@router.get("/wsi/{wsi_id}/csv")
async def export_csv(
    wsi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Export annotation summary as CSV"""
    wsi_file = db.query(WSIFile).filter(WSIFile.id == wsi_id).first()
    if not wsi_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="WSI file not found"
        )
    
    annotations = db.query(Annotation).filter(
        Annotation.wsi_file_id == wsi_id,
        Annotation.deleted_at.is_(None)
    ).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "ID", "Label", "Label Hierarchy", "Geometry Type",
        "Area (µm²)", "Perimeter (µm)", "Centroid X", "Centroid Y",
        "Confidence", "AI Generated", "Layer", "Description",
        "Creator ID", "Created At", "Updated At"
    ])
    
    # Rows
    for ann in annotations:
        writer.writerow([
            ann.id,
            ann.label,
            " > ".join(ann.label_hierarchy) if ann.label_hierarchy else "",
            ann.geometry_type,
            ann.area_um2 or "",
            ann.perimeter_um or "",
            ann.centroid_x or "",
            ann.centroid_y or "",
            ann.confidence or "",
            ann.is_ai_generated,
            ann.layer_name,
            ann.description or "",
            ann.creator_id,
            ann.created_at.isoformat(),
            ann.updated_at.isoformat()
        ])
    
    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{wsi_file.original_filename}_annotations.csv"'}
    )
