"""
API routes
"""

from app.api import auth, annotations, wsi, labels, users, export, ai

__all__ = ["auth", "annotations", "wsi", "labels", "users", "export", "ai"]
