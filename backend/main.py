"""
Oral Cytology WSI Annotation Tool - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

from app.api import auth, annotations, wsi, labels, users, export, ai
from app.core.config import settings
from app.core.database import engine, Base
from app.core.security import get_current_user
from app.scripts.init_db import init_database

# Create database tables and initialize with default data
Base.metadata.create_all(bind=engine)
try:
    init_database()
except Exception as e:
    # Log error but don't fail startup if database is already initialized
    print(f"Database initialization note: {e}")

app = FastAPI(
    title="Oral Cytology WSI Annotation Tool API",
    description="Backend API for WSI annotation tool",
    version="1.0.0"
)

# CORS middleware
# In production, allow specific origins; in dev, allow all
cors_origins = settings.CORS_ORIGINS if not settings.DEBUG else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for WSI tiles
uploads_dir = Path(settings.UPLOAD_DIR)
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(wsi.router, prefix="/api/wsi", tags=["WSI"])
app.include_router(annotations.router, prefix="/api/annotations", tags=["Annotations"])
app.include_router(labels.router, prefix="/api/labels", tags=["Label Schemas"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI-Assisted"])

@app.get("/")
async def root():
    return {
        "message": "Oral Cytology WSI Annotation Tool API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
