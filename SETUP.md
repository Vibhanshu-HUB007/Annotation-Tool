# Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- OpenSlide library (for WSI support)

### Installing OpenSlide

**Ubuntu/Debian:**
```bash
sudo apt-get install openslide-tools python3-openslide
```

**macOS:**
```bash
brew install openslide
```

**Windows:**
Download from: https://openslide.org/download/

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Default Credentials

After running `init_db.py`, you can login with:
- Username: `admin`
- Password: `admin123`

**Important:** Change the default password in production!

## Usage

1. Start both backend and frontend servers
2. Navigate to `http://localhost:3000`
3. Login with default credentials
4. Upload a WSI file from the dashboard
5. Click "View" to open the annotation viewer
6. Use the toolbar to select annotation tools
7. Draw annotations on the WSI
8. Save and export annotations

## Troubleshooting

### OpenSlide Installation Issues

If you encounter issues with OpenSlide:
- Ensure OpenSlide is properly installed and accessible
- Check that the Python bindings are installed: `pip install openslide-python`
- On Linux, you may need: `sudo apt-get install python3-openslide`

### Database Issues

If the database doesn't initialize:
- Check that SQLite is available (default) or PostgreSQL is configured
- Ensure write permissions in the project directory

### Port Conflicts

If ports 8000 or 3000 are in use:
- Backend: Change port in `uvicorn main:app --reload --port 8001`
- Frontend: Change port in `vite.config.ts` or use `npm run dev -- --port 3001`
