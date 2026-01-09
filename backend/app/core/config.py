"""
Application configuration
"""

from pydantic_settings import BaseSettings
from typing import List, Union
import os
from pathlib import Path
import json

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Oral Cytology WSI Annotation Tool"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite:///./annotation_tool.db"
    
    # CORS - Accepts comma-separated string or JSON array
    # Examples:
    # - "https://app1.vercel.app,https://app2.netlify.app" (comma-separated)
    # - '["https://app1.vercel.app","https://app2.netlify.app"]' (JSON array)
    # - "*" (allow all - development only)
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS to a list, handling both string and list formats"""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        
        # If it's a string, try to parse as JSON first, then as comma-separated
        cors_str = str(self.CORS_ORIGINS).strip()
        
        # If it's "*", return ["*"]
        if cors_str == "*":
            return ["*"]
        
        # Try to parse as JSON array
        try:
            parsed = json.loads(cors_str)
            if isinstance(parsed, list):
                return [str(origin) for origin in parsed]
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Parse as comma-separated string
        origins = [origin.strip() for origin in cors_str.split(",") if origin.strip()]
        return origins if origins else ["*"]
    
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
