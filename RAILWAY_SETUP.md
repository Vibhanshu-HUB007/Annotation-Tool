# Railway Deployment Setup

## Issue
Railway's Railpack can't detect the project because it's a monorepo with both `backend/` and `frontend/` directories.

## Solution: Configure Root Directory in Railway

### Option 1: Set Root Directory in Railway Dashboard (Recommended)

1. Go to your Railway project dashboard
2. Click on your service
3. Go to **Settings** tab
4. Scroll to **"Root Directory"**
5. Set it to: `backend`
6. Click **Save**
7. Railway will redeploy automatically

### Option 2: Use the railway.json Configuration

The `railway.json` file in the root should help, but Railway might still need the root directory set.

### Option 3: Create a Start Script

If the above doesn't work, create a `start.sh` in the root:

```bash
#!/bin/bash
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Then in Railway settings, set:
- **Start Command**: `bash start.sh`

## Environment Variables Needed

Make sure to add these in Railway:

```
SECRET_KEY=<generate-random-string>
DATABASE_URL=<railway-will-provide-this>
CORS_ORIGINS=["https://your-frontend.vercel.app"]
UPLOAD_DIR=./uploads
CACHE_DIR=./cache
DEBUG=False
```

## Initialize Database

After deployment, run:

```bash
railway run python backend/scripts/init_db.py
```

Or use Railway's terminal:
1. Go to your service
2. Click "Deploy Logs"
3. Click "New Terminal"
4. Run: `cd backend && python scripts/init_db.py`

## Quick Fix

**Easiest solution**: In Railway dashboard → Your Service → Settings → Set **Root Directory** to `backend`

This tells Railway to treat the `backend/` folder as the project root.
