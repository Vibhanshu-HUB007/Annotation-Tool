# Deploy Backend to Render.com (Free, No Size Limits)

## Why Render.com?

- ✅ **No 4GB image size limit** (unlike Railway)
- ✅ **Free PostgreSQL database** included
- ✅ **Free tier available**
- ✅ **Auto-deploys from GitHub**
- ✅ **Easy setup**

## Step-by-Step Setup

### 1. Sign Up

1. Go to [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (recommended)

### 2. Create Web Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Click **"Connect account"** if not connected to GitHub
4. Select your repository: `Vibhanshu-HUB007/Annotation-Tool`

### 3. Configure Service

**Basic Settings:**
- **Name**: `oral-cytology-api` (or any name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: `backend` ⚠️ **IMPORTANT!**

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements-minimal.txt
  ```
- **Start Command**: 
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (deploys on every push)

### 4. Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"**:

```
SECRET_KEY=<generate-random-string>
```

Generate with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

```
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

(Update after deploying frontend)

```
UPLOAD_DIR=./uploads
CACHE_DIR=./cache
DEBUG=False
```

### 5. Create PostgreSQL Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Name: `oral-cytology-db`
4. Click **"Create Database"**
5. Copy the **Internal Database URL**
6. Go back to your Web Service
7. Add environment variable:
   ```
   DATABASE_URL=<paste-internal-database-url>
   ```

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will start building (takes 5-10 minutes)
3. Wait for "Live" status

### 7. Initialize Database

1. Go to your service → **"Shell"** tab
2. Or use Render's terminal
3. Run:
   ```bash
   cd backend
   python scripts/init_db.py
   ```

### 8. Get Your Backend URL

1. Your service will have a URL like: `https://oral-cytology-api.onrender.com`
2. Test it: `https://oral-cytology-api.onrender.com/api/health`
3. API docs: `https://oral-cytology-api.onrender.com/docs`

### 9. Update Frontend

1. Go to Vercel dashboard
2. Your project → **Settings** → **Environment Variables**
3. Update `VITE_API_URL`:
   ```
   VITE_API_URL=https://oral-cytology-api.onrender.com
   ```
4. Redeploy frontend

### 10. Update CORS

1. Go back to Render
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=["https://your-vercel-app.vercel.app"]
   ```
3. Render will auto-redeploy

## Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes** of inactivity
- **First request after spin-down takes ~30 seconds** (wake-up time)
- **750 hours/month free** (enough for development/testing)

### To Keep Service Awake (Optional)

You can use a free service like [UptimeRobot](https://uptimerobot.com) to ping your service every 5 minutes.

## Troubleshooting

**Build fails:**
- Check build logs in Render dashboard
- Verify Root Directory is set to `backend`
- Make sure `requirements-minimal.txt` exists

**Service won't start:**
- Check environment variables are set
- Verify `DATABASE_URL` is correct
- Check service logs

**Database connection errors:**
- Make sure PostgreSQL is created
- Use **Internal Database URL** (not External)
- Verify `DATABASE_URL` environment variable

## Success!

Once deployed:
- ✅ Backend: `https://your-app.onrender.com`
- ✅ Frontend: `https://your-app.vercel.app`
- ✅ No size limits!
- ✅ Free hosting!

---

**Need help?** Check Render's docs: https://render.com/docs
