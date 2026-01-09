"""
WSI processing utilities
"""

# Optional openslide import (requires system libraries)
try:
    import openslide
    HAS_OPENSLIDE = True
except ImportError:
    HAS_OPENSLIDE = False
    openslide = None

from PIL import Image
import io
from pathlib import Path

def process_wsi_file(file_path: str):
    """Process a WSI file and extract metadata"""
    if not HAS_OPENSLIDE:
        raise ImportError("OpenSlide library not available. Install openslide-python and system libraries.")
    slide = openslide.OpenSlide(file_path)
    try:
        metadata = {
            "dimensions": slide.dimensions,
            "level_count": slide.level_count,
            "level_dimensions": slide.level_dimensions,
            "level_downsamples": slide.level_downsamples,
            "properties": dict(slide.properties)
        }
        return metadata
    finally:
        slide.close()

def get_wsi_tile(file_path: str, level: int, x: int, y: int, tile_size: int = 256, format: str = "jpeg"):
    """Extract a tile from a WSI file"""
    if not HAS_OPENSLIDE:
        raise ImportError("OpenSlide library not available. Install openslide-python and system libraries.")
    slide = openslide.OpenSlide(file_path)
    try:
        # Get tile
        tile = slide.read_region((x, y), level, (tile_size, tile_size))
        
        # Convert RGBA to RGB
        if tile.mode == "RGBA":
            # Create white background
            rgb_tile = Image.new("RGB", tile.size, (255, 255, 255))
            rgb_tile.paste(tile, mask=tile.split()[3])  # Use alpha channel as mask
        else:
            rgb_tile = tile.convert("RGB")
        
        # Convert to bytes
        output = io.BytesIO()
        rgb_tile.save(output, format=format.upper(), quality=85)
        output.seek(0)
        return output.getvalue()
    finally:
        slide.close()

def get_wsi_info(file_path: str):
    """Get basic information about a WSI file"""
    if not HAS_OPENSLIDE:
        raise ImportError("OpenSlide library not available. Install openslide-python and system libraries.")
    slide = openslide.OpenSlide(file_path)
    try:
        return {
            "width": slide.dimensions[0],
            "height": slide.dimensions[1],
            "levels": slide.level_count,
            "level_dimensions": slide.level_dimensions,
            "mpp_x": float(slide.properties.get(openslide.PROPERTY_NAME_MPP_X, 0)),
            "mpp_y": float(slide.properties.get(openslide.PROPERTY_NAME_MPP_Y, 0)),
            "magnification": float(slide.properties.get(openslide.PROPERTY_NAME_OBJECTIVE_POWER, 0))
        }
    finally:
        slide.close()
