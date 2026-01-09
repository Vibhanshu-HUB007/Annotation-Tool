# Quick Deployment Guide

## Fastest Way to Deploy (5 minutes)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/annotation-tool.git
git push -u origin main
```

### Step 2: Deploy Backend (Railway - 2 minutes)

1. Go to [railway.app](https://railway.app) → Sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. In project settings:
   - Set **Root Directory** to `backend`
   - Add environment variable:
     - `SECRET_KEY`: Click "Generate" (or use a random string)
5. Railway will auto-deploy
6. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### Step 3: Deploy Frontend (Vercel - 2 minutes)

1. Go to [vercel.com](https://vercel.com) → Sign up with GitHub
2. Click "Add New Project" → Import your GitHub repo
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add environment variable:
   - `VITE_API_URL`: Your Railway URL from Step 2
5. Click "Deploy"
6. Copy your Vercel URL (e.g., `https://your-app.vercel.app`)

### Step 4: Update CORS (1 minute)

1. Go back to Railway dashboard
2. Your service → Variables
3. Add/Update `CORS_ORIGINS`:
   ```
   https://your-app.vercel.app
   ```
4. Railway will auto-redeploy

### Step 5: Initialize Database

1. In Railway dashboard → Your service → "Deploy Logs"
2. Click "New Terminal"
3. Run:
   ```bash
   python scripts/init_db.py
   ```

### Done! 🎉

Visit your Vercel URL and login with:
- Username: `admin`
- Password: `admin123`

---

## Alternative: Render + Netlify

### Backend on Render

1. [render.com](https://render.com) → Sign up with GitHub
2. "New +" → "Web Service" → Connect repo
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (same as Railway)
5. Create PostgreSQL database in Render dashboard
6. Use PostgreSQL URL as `DATABASE_URL`

### Frontend on Netlify

1. [netlify.com](https://netlify.com) → Sign up with GitHub
2. "Add new site" → "Import an existing project"
3. Settings:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
4. Add environment variable:
   - `VITE_API_URL`: Your Render backend URL

---

## Troubleshooting

**Backend won't start:**
- Check Railway/Render logs
- Verify `DATABASE_URL` is set
- Run `python scripts/init_db.py` in terminal

**Frontend can't connect to backend:**
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Ensure backend URL uses HTTPS

**CORS errors:**
- Add frontend URL to `CORS_ORIGINS` in backend
- Redeploy backend after changing CORS

---

## That's it!

Your app is now live and will auto-deploy on every GitHub push! 🚀
