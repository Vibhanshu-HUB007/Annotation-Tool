# Oral Cytology WSI Annotation Tool

A professional-grade web-based annotation tool for Oral Cytology Whole Slide Imaging (WSI), designed for research and clinical decision support in Oral Potentially Malignant Disorders (OPMDs) and Oral Squamous Cell Carcinoma (OSCC).

## Features

### 🖼️ WSI Viewing
- Multi-resolution pyramid support for deep zoom
- Smooth pan & zoom (OpenSeadragon-based)
- Magnification labels (10×, 20×, 40×)
- Scale bar (µm)
- Tile-based loading for optimal performance
- Supported formats: `.svs`, `.tiff`, `.ndpi`, `.mrxs`, `.jpg`, `.png`

### ✏️ Annotation Tools
- **Manual Annotation**: Freehand pencil, polygon, rectangle, ellipse, point markers
- **Editing**: Eraser (partial & full ROI), move/resize, undo/redo
- **Labels**: Text labels inside ROI, color-coded classes, transparency control
- **Layers**: Enable/disable per layer, lock/unlock annotations

### 🧾 Label Schema Management
- Custom JSON-based label schemas
- Editable class names & colors
- Hierarchical label structure
- Export/import for dataset standardization

### 🤖 AI-Assisted Annotation
- Auto-suggest ROIs using pretrained models
- Active learning loop (user correction → model refinement)
- Heatmap overlay (risk probability)
- Tile-level → slide-level risk aggregation
- Confidence scores per annotation

### 💾 Data Export
- COCO JSON format
- GeoJSON format
- QuPath .geojson compatibility
- Image + mask pairs
- Tile-level datasets
- CSV summary (ROI counts, area, class)

### 👥 User Management
- Role-based access (Admin, Pathologist, Researcher)
- Case-wise annotation tracking
- Audit trail (who annotated what & when)
- Annotation versioning

## Architecture

```
Annotation-Tool/
├── backend/          # FastAPI server
├── frontend/         # React application
├── shared/           # Shared types and utilities
└── docs/             # Documentation
```

## Quick Start

### 🚀 Deploy to Web (Recommended)

**Deploy in 5 minutes using free hosting services:**

1. **Push to GitHub** (if not already done)
2. **Deploy Backend** to [Railway](https://railway.app) or [Render](https://render.com)
3. **Deploy Frontend** to [Vercel](https://vercel.com) or [Netlify](https://netlify.com)

See **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** for step-by-step instructions.

**Benefits:**
- ✅ No need to start servers manually
- ✅ Auto-deploys on every GitHub push
- ✅ Free hosting (with generous limits)
- ✅ HTTPS enabled automatically
- ✅ Accessible from anywhere

### Local Development

#### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (optional, SQLite for development)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py  # Initialize database
uvicorn main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

**Default Login:**
- Username: `admin`
- Password: `admin123`

## Domain-Specific Annotations

The tool supports annotation of:
- Dysplastic epithelial cells
- Keratin pearls
- Nuclear pleomorphism regions
- Increased N:C ratio cells
- Hyperchromatic nuclei
- Mitotic figures
- Inflammatory infiltrates
- Stromal invasion areas
- Normal vs abnormal epithelium
- Background artifacts (blood, debris, folds)

## 📚 Documentation

- **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** - 5-minute deployment guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Comprehensive deployment instructions
- **[SETUP.md](./SETUP.md)** - Local development setup
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture details
- **[NOTES.md](./NOTES.md)** - Implementation notes and future enhancements

## 🚀 Quick Deploy

Want to host this on the web? Follow the **[QUICK_DEPLOY.md](./QUICK_DEPLOY.md)** guide to deploy in 5 minutes using free hosting services (Railway + Vercel).

**Benefits:**
- No need to start servers manually
- Auto-deploys on every GitHub push
- Free hosting with HTTPS
- Accessible from anywhere

## License

MIT License

## Contact

For questions or support, please open an issue.
