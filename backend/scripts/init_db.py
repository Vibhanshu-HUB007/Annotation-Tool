"""
Initialize database with default data
"""

from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.label_schema import LabelSchema
from app.core.security import get_password_hash

def init_database():
    """Initialize database with default admin user and label schema"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create default admin user if not exists
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrator",
                role=UserRole.ADMIN
            )
            db.add(admin)
            print("Created default admin user (username: admin, password: admin123)")
        
        # Create default label schema if not exists
        default_schema = db.query(LabelSchema).filter(LabelSchema.name == "Oral Cytology Default").first()
        if not default_schema:
            default_schema = LabelSchema(
                name="Oral Cytology Default",
                description="Default label schema for oral cytology annotations",
                version="1.0.0",
                schema_definition={
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
                is_default=True,
                is_active=True
            )
            db.add(default_schema)
            print("Created default label schema")
        
        db.commit()
        print("Database initialized successfully")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
