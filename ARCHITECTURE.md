# Architecture Documentation

## System Overview

The Oral Cytology WSI Annotation Tool is a full-stack web application designed for annotating Whole Slide Images (WSI) of oral cytology samples. The system consists of a FastAPI backend and a React frontend with OpenSeadragon for WSI viewing.

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens
- **WSI Processing**: OpenSlide

### Directory Structure
```
backend/
├── app/
│   ├── api/           # API route handlers
│   ├── core/          # Core configuration (database, security, config)
│   ├── models/        # SQLAlchemy database models
│   ├── schemas/       # Pydantic schemas for validation
│   └── utils/         # Utility functions (WSI processing)
├── scripts/           # Database initialization scripts
└── main.py            # Application entry point
```

### Key Components

#### 1. Database Models
- **User**: User accounts with role-based access
- **WSIFile**: WSI file metadata and processing status
- **Annotation**: Annotation geometry, labels, and metadata
- **LabelSchema**: Hierarchical label definitions

#### 2. API Routes
- `/api/auth`: Authentication (login, register)
- `/api/users`: User management
- `/api/wsi`: WSI file upload and management
- `/api/annotations`: Annotation CRUD operations
- `/api/labels`: Label schema management
- `/api/export`: Export annotations (COCO, GeoJSON, CSV)
- `/api/ai`: AI-assisted annotation endpoints

#### 3. WSI Processing
- Tile extraction using OpenSlide
- Multi-resolution pyramid support
- Metadata extraction (MPP, magnification, dimensions)

## Frontend Architecture

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **WSI Viewer**: OpenSeadragon
- **State Management**: Zustand
- **HTTP Client**: Axios with React Query
- **UI Library**: Material-UI
- **Annotation Overlay**: Fabric.js

### Directory Structure
```
frontend/
├── src/
│   ├── api/           # API client and endpoints
│   ├── components/    # React components
│   ├── pages/         # Page components
│   ├── store/         # Zustand state stores
│   └── types/         # TypeScript type definitions
└── public/            # Static assets
```

### Key Components

#### 1. WSI Viewer (`WSIViewer.tsx`)
- OpenSeadragon integration
- Multi-resolution tile loading
- Viewport synchronization

#### 2. Annotation Overlay (`AnnotationOverlay.tsx`)
- Fabric.js canvas overlay
- Real-time annotation rendering
- Coordinate transformation (WSI → viewport)

#### 3. Annotation Tools (`AnnotationToolbar.tsx`)
- Tool selection (freehand, polygon, rectangle, point, eraser)
- Save and export functionality

#### 4. State Management
- **authStore**: User authentication state
- **annotationStore**: Annotation state and viewport

## Data Flow

### Annotation Creation Flow
1. User selects annotation tool and label
2. User draws annotation on WSI viewer
3. Frontend captures geometry (GeoJSON format)
4. POST request to `/api/annotations`
5. Backend validates and stores annotation
6. Backend calculates metrics (area, perimeter, centroid)
7. Response returned to frontend
8. Annotation overlay updated

### WSI Viewing Flow
1. User selects WSI file from dashboard
2. Frontend requests WSI metadata from `/api/wsi/{id}`
3. OpenSeadragon initialized with tile source
4. Tiles requested from `/api/wsi/{id}/tile?level=x&x=y&y=z`
5. Backend extracts tiles using OpenSlide
6. Tiles served to viewer
7. Annotations loaded and overlaid

## Annotation Format

### GeoJSON Structure
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[x1, y1], [x2, y2], ...]]
  },
  "properties": {
    "label": "Dysplastic Epithelial Cells",
    "label_hierarchy": ["Malignant", "OSCC"],
    "color": "#FF8800",
    "opacity": 0.7,
    "confidence": 0.95
  }
}
```

### Label Schema Structure
```json
{
  "classes": [
    {
      "name": "Malignant",
      "color": "#FF0000",
      "children": [
        {"name": "OSCC", "color": "#CC0000"}
      ]
    }
  ]
}
```

## Security

### Authentication
- JWT-based authentication
- Token stored in localStorage (frontend)
- Token expiration: 24 hours (configurable)

### Authorization
- Role-based access control (Admin, Pathologist, Researcher)
- Resource-level permissions (users can only edit their own annotations)

### Data Protection
- File upload size limits
- File type validation
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (React's built-in escaping)

## Performance Considerations

### WSI Tile Caching
- Tiles can be cached on the server
- Client-side caching via OpenSeadragon

### Database Optimization
- Indexed foreign keys
- Soft deletes for annotations (versioning support)

### Frontend Optimization
- React Query for data caching
- Lazy loading of components
- Canvas-based annotation rendering (Fabric.js)

## Future Enhancements

### AI Integration
- Tile-level inference pipeline
- Slide-level risk aggregation
- Active learning loop
- Model versioning

### Advanced Features
- Multi-user collaborative annotation
- Annotation review workflow
- Measurement tools (ruler, area calculator)
- Image comparison (side-by-side)

## Deployment

### Backend
- Production: Use PostgreSQL instead of SQLite
- Set `DEBUG=False` in production
- Use environment variables for secrets
- Configure CORS for production domain

### Frontend
- Build: `npm run build`
- Serve static files via nginx or similar
- Configure API proxy

### WSI Storage
- Consider object storage (S3, etc.) for large files
- Implement tile pre-generation for faster loading
