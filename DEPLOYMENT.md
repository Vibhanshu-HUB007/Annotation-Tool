# Deployment Guide

This guide will help you deploy the Oral Cytology WSI Annotation Tool to the web using GitHub and free hosting services.

## Deployment Options

### Option 1: Railway (Backend) + Vercel (Frontend) - Recommended

**Railway** offers free tier with PostgreSQL and easy GitHub integration.
**Vercel** offers free hosting for frontend with automatic deployments.

### Option 2: Render (Backend) + Netlify (Frontend)

**Render** offers free tier with PostgreSQL.
**Netlify** offers free hosting for frontend.

---

## Step-by-Step Deployment

### Part 1: Deploy Backend to Railway

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/annotation-tool.git
   git push -u origin main
   ```

2. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Create a New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Railway will detect it's a Python project

4. **Configure Backend**
   - Railway will auto-detect the backend folder
   - Add environment variables:
     - `SECRET_KEY`: Generate a random secret key
     - `DATABASE_URL`: Railway will auto-create PostgreSQL, use that URL
     - `CORS_ORIGINS`: Add your frontend URL (you'll get this after deploying frontend)
     - `UPLOAD_DIR`: `./uploads`
     - `CACHE_DIR`: `./cache`

5. **Set Root Directory**
   - In Railway project settings, set "Root Directory" to `backend`

6. **Initialize Database**
   - Railway will run the app, but you need to initialize the database
   - Go to Railway dashboard → your service → "Deploy Logs"
   - Click "New Terminal" or use Railway CLI:
     ```bash
     railway run python scripts/init_db.py
     ```

7. **Get Backend URL**
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Save this URL for frontend configuration

### Part 2: Deploy Frontend to Vercel

1. **Sign up for Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Vite
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

3. **Add Environment Variables**
   - `VITE_API_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)

4. **Update API Proxy**
   - Edit `frontend/vercel.json`
   - Replace `your-backend-url.railway.app` with your actual Railway URL

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - You'll get a URL like: `https://your-app.vercel.app`

6. **Update Backend CORS**
   - Go back to Railway
   - Update `CORS_ORIGINS` environment variable to include your Vercel URL
   - Redeploy backend

### Alternative: Deploy to Render

#### Backend on Render

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `oral-cytology-api`
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt && python scripts/init_db.py`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Root Directory**: `backend`

3. **Add Environment Variables**
   - `SECRET_KEY`: Generate a random secret key
   - `DATABASE_URL`: Create a PostgreSQL database in Render and use its URL
   - `CORS_ORIGINS`: Your frontend URL
   - `UPLOAD_DIR`: `./uploads`
   - `CACHE_DIR`: `./cache`

4. **Create PostgreSQL Database**
   - In Render dashboard, create a new PostgreSQL database
   - Use the connection string as `DATABASE_URL`

#### Frontend on Netlify

1. **Sign up for Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign up with GitHub

2. **Add New Site**
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub and select your repository
   - Configure:
     - **Base directory**: `frontend`
     - **Build command**: `npm run build`
     - **Publish directory**: `dist`

3. **Add Environment Variables**
   - `VITE_API_URL`: Your Render backend URL

4. **Update netlify.toml**
   - Edit `frontend/netlify.toml`
   - Replace `your-backend-url.railway.app` with your Render URL

5. **Deploy**
   - Netlify will automatically deploy on every push to main branch

---

## Post-Deployment Steps

### 1. Update CORS Settings

After deploying frontend, update backend CORS to include frontend URL:

**Railway:**
- Go to your service → Variables
- Update `CORS_ORIGINS` to include your frontend URL

**Render:**
- Go to your service → Environment
- Update `CORS_ORIGINS`

### 2. Initialize Database

Run the database initialization script:

**Railway:**
```bash
railway run python scripts/init_db.py
```

**Render:**
- Use the Shell in Render dashboard
- Or SSH into the service and run:
```bash
python scripts/init_db.py
```

### 3. Test the Application

1. Visit your frontend URL
2. Login with default credentials:
   - Username: `admin`
   - Password: `admin123`
3. Upload a WSI file
4. Test annotation tools

### 4. Set Up Custom Domain (Optional)

Both Vercel and Netlify support custom domains:
- Add your domain in the platform settings
- Update DNS records as instructed
- Update `CORS_ORIGINS` in backend to include your custom domain

---

## Environment Variables Reference

### Backend

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
CORS_ORIGINS=["https://your-frontend.vercel.app"]
UPLOAD_DIR=./uploads
CACHE_DIR=./cache
DEBUG=False
```

### Frontend

```env
VITE_API_URL=https://your-backend.railway.app
```

---

## Troubleshooting

### Backend Issues

**Database connection errors:**
- Check `DATABASE_URL` is correct
- Ensure PostgreSQL is running (Railway/Render)
- Run `python scripts/init_db.py` to initialize

**CORS errors:**
- Verify `CORS_ORIGINS` includes your frontend URL
- Check for trailing slashes
- Ensure HTTPS URLs are used

**File upload errors:**
- Check `UPLOAD_DIR` exists and is writable
- Verify file size limits

### Frontend Issues

**API connection errors:**
- Verify `VITE_API_URL` is correct
- Check backend is running
- Verify CORS settings in backend

**Build errors:**
- Check Node.js version (should be 18+)
- Clear `node_modules` and reinstall
- Check for TypeScript errors

---

## Continuous Deployment

Both platforms support automatic deployments:
- **Railway/Render**: Auto-deploys on push to main branch
- **Vercel/Netlify**: Auto-deploys on push to main branch

No need to manually deploy after initial setup!

---

## Free Tier Limits

### Railway
- $5 free credit monthly
- 500 hours of usage
- 512MB RAM, 1GB storage

### Render
- Free tier available
- Spins down after 15 minutes of inactivity
- 512MB RAM

### Vercel
- Unlimited deployments
- 100GB bandwidth
- No time limits

### Netlify
- 100GB bandwidth
- 300 build minutes/month
- No time limits

---

## Security Notes

1. **Change default admin password** after first login
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS** (automatic on all platforms)
4. **Set DEBUG=False** in production
5. **Regularly update dependencies**

---

## Support

If you encounter issues:
1. Check deployment logs in your platform dashboard
2. Verify environment variables are set correctly
3. Check that both backend and frontend are deployed
4. Review the troubleshooting section above
