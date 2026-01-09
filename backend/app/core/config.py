"""
Application configuration
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Oral Cytology WSI Annotation Tool"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite:///./annotation_tool.db"
    
    # CORS - Add your frontend URLs here (comma-separated)
    # For production, specify exact URLs like:
    # ["https://your-app.vercel.app", "https://your-app.netlify.app"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024 * 1024  # 10GB
    ALLOWED_EXTENSIONS: List[str] = [".svs", ".tiff", ".tif", ".ndpi", ".mrxs", ".jpg", ".jpeg", ".png"]
    
    # WSI Processing
    TILE_SIZE: int = 256
    MAX_ZOOM_LEVEL: int = 10
    CACHE_DIR: str = "./cache"
    
    # AI/ML
    AI_MODEL_PATH: str = "./models"
    GPU_ENABLED: bool = False
    BATCH_SIZE: int = 4
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Create necessary directories
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.CACHE_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.AI_MODEL_PATH).mkdir(parents=True, exist_ok=True)
