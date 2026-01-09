# Quick Setup Guide - Complete Database & Frontend Configuration

## ✅ Your Backend is Already Deployed!

**Backend URL**: `https://annotation-tool-v7mu.onrender.com`

## Step 1: Create PostgreSQL Database (5 minutes)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `annotation-tool-db`
   - **Database**: `annotation_tool`
   - **Region**: Same as your backend (check your backend service region)
   - **PostgreSQL Version**: 16
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait 1-2 minutes for provisioning

## Step 2: Get Database Connection String

1. Click on your new database
2. Go to **"Connections"** tab
3. Copy the **"Internal Database URL"**
   - It looks like: `postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/annotation_tool`

## Step 3: Add Environment Variables to Backend

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your backend service (it should be named something like `annotation-tool-v7mu` or similar)
3. In the left sidebar, click **"Environment"** (or look for the **"Environment"** tab at the top)
4. You'll see three sections:
   - **Environment Variables** ← Click on this one!
   - Secret Files
   - Linked Environment Groups
5. Click on **"Environment Variables"** section
6. You'll see a button that says **"Add Environment Variable"** (usually a blue button)
7. Click it and add each variable one by one:

### Required Variables:

**Variable 1: DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: Paste the Internal Database URL you copied from Step 2
- Click **"Save and Deploy"** (this will save the variable and restart your service)

**Variable 2: SECRET_KEY**
- Click **"Add Environment Variable"** again
- **Key**: `SECRET_KEY`
- **Value**: `WxVt6bWR83RJrCMVepgv1wuxgRQd83_4wE5wDzIVzP0`
- Click **"Save and Deploy"**

**Variable 3: CORS_ORIGINS**
- Click **"Add Environment Variable"** again
- **Key**: `CORS_ORIGINS`
- **Value**: 
  - If you have a frontend URL: `https://your-frontend.vercel.app` (replace with your actual URL)
  - If you have multiple frontends: `https://app1.vercel.app,https://app2.netlify.app` (comma-separated, no spaces)
  - If you don't have a frontend yet: `*` (allows all origins - only for development)
- Click **"Save and Deploy"**

> **Note**: You can enter CORS_ORIGINS as:
> - A single URL: `https://your-app.vercel.app`
> - Multiple URLs (comma-separated): `https://app1.vercel.app,https://app2.netlify.app`
> - Wildcard (dev only): `*`

> **Note**: You'll see three options when saving:
> - **"Save"** - Just saves, doesn't restart (not recommended)
> - **"Save and Deploy"** ← **Choose this one!** (saves and restarts to pick up new variables)
> - **"Save, Rebuild and Deploy"** - Full rebuild (not necessary for env vars, but works too)

### Optional (but recommended):

```bash
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

4. Click **"Save Changes"** - Render will auto-redeploy

## Step 4: Wait for Redeployment

1. Go to **"Events"** tab in your backend service
2. Wait for deployment to complete (2-3 minutes)
3. Check logs for:
   ```
   Created default admin user (username: admin, password: admin123)
   Database initialized successfully
   ```

## Step 5: Test Your Backend

1. **Health Check**: https://annotation-tool-v7mu.onrender.com/api/health
2. **API Docs**: https://annotation-tool-v7mu.onrender.com/docs
3. **Test Login**:
   - URL: `POST https://annotation-tool-v7mu.onrender.com/api/auth/login`
   - Body: `{"username": "admin", "password": "admin123"}`

## Step 6: Configure Frontend

### If using Vercel:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your frontend project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://annotation-tool-v7mu.onrender.com/api`
   - **Environments**: Production, Preview, Development (all)
5. Click **"Save"**
6. Go to **Deployments** → Click **"..."** → **Redeploy**

### If using Netlify:

1. Go to [Netlify Dashboard](https://app.netlify.com)
2. Select your site
3. Go to **Site settings** → **Environment variables**
4. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://annotation-tool-v7mu.onrender.com/api`
   - **Scopes**: All scopes
5. Click **"Save"**
6. Go to **Deploys** → **Trigger deploy** → **Deploy site**

## Step 7: Update Backend CORS (if needed)

1. Go back to Render → Your backend service → Environment
2. Update `CORS_ORIGINS` to include your frontend URL:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
   ```
3. Save (auto-redeploys)

## Step 8: Test Everything

1. Open your frontend URL
2. Try to login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Check browser console for any errors
4. Check Network tab to verify API calls are going to Render backend

## Default Admin Credentials

⚠️ **CHANGE THESE IN PRODUCTION!**

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

## Troubleshooting

### Database Connection Error
- Verify `DATABASE_URL` is correct (use Internal Database URL)
- Check database is running (green status)
- Ensure database and backend are in same region

### CORS Errors
- Verify `CORS_ORIGINS` includes your exact frontend URL
- Include `https://` in the URL
- No trailing slashes

### Frontend Can't Connect
- Verify `VITE_API_URL` is set correctly
- Check browser console for errors
- Verify backend is running (check Render logs)

### Slow First Request
- Render free tier spins down after 15 min inactivity
- First request takes ~30 seconds to wake up
- This is normal for free tier

## Success Checklist

- [ ] PostgreSQL database created
- [ ] `DATABASE_URL` environment variable set
- [ ] `SECRET_KEY` environment variable set
- [ ] Backend redeployed successfully
- [ ] Database initialized (check logs)
- [ ] Frontend `VITE_API_URL` configured
- [ ] Frontend redeployed
- [ ] Can login with admin credentials
- [ ] API calls working from frontend

## Need Help?

- Check `DATABASE_SETUP.md` for detailed database setup
- Check `FRONTEND_SETUP.md` for detailed frontend setup
- Check Render logs for errors
- Check browser console for frontend errors
