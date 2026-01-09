# Deployment Checklist

## ✅ Backend (Railway) - COMPLETE

- [x] Code pushed to GitHub
- [x] Railway project connected
- [x] Root directory set to `backend`
- [x] Build successful
- [ ] **Environment variables added** ⬅️ DO THIS NEXT
- [ ] **Database initialized** ⬅️ DO THIS NEXT
- [ ] Service running and accessible

### Add Environment Variables in Railway:

1. Go to Railway dashboard → Your service → **Variables** tab
2. Add these variables:

```
SECRET_KEY=<generate-random-string>
```

Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

```
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

(Update this after deploying frontend)

```
UPLOAD_DIR=./uploads
CACHE_DIR=./cache
DEBUG=False
```

**Note:** `DATABASE_URL` is automatically provided by Railway - don't add it manually!

### Initialize Database:

After adding environment variables:

1. Railway dashboard → Your service → **Deploy Logs**
2. Click **"New Terminal"**
3. Run:
   ```bash
   cd backend
   python scripts/init_db.py
   ```

### Get Your Backend URL:

1. Railway dashboard → Your service
2. Click on the service URL (or go to Settings → Domains)
3. Copy the URL (e.g., `https://your-app.railway.app`)
4. Test it: `https://your-app.railway.app/api/health`
   - Should return: `{"status": "healthy"}`

---

## ⏳ Frontend (Vercel) - IN PROGRESS

- [x] Code pushed to GitHub
- [x] TypeScript errors fixed
- [ ] Vercel project connected
- [ ] Environment variables added
- [ ] Build successful
- [ ] Deployed and accessible

### Deploy Frontend to Vercel:

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click **"Add New Project"**
4. Import your GitHub repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add environment variable:
   ```
   VITE_API_URL=https://your-railway-app.railway.app
   ```
   (Use your Railway backend URL from above)
7. Click **"Deploy"**

### After Frontend Deployment:

1. Copy your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Go back to Railway
3. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ```
4. Railway will auto-redeploy

---

## 🎯 Final Steps

1. **Test Backend:**
   - Visit: `https://your-railway-app.railway.app/docs`
   - Should show FastAPI documentation

2. **Test Frontend:**
   - Visit: `https://your-vercel-app.vercel.app`
   - Should show login page

3. **Login:**
   - Username: `admin`
   - Password: `admin123`
   - **⚠️ Change this password after first login!**

4. **Upload a WSI file and test annotation tools**

---

## 🐛 Troubleshooting

### Backend not starting:
- Check Railway deploy logs
- Verify all environment variables are set
- Make sure database is initialized

### Frontend can't connect to backend:
- Verify `VITE_API_URL` is correct in Vercel
- Check `CORS_ORIGINS` includes your Vercel URL
- Ensure backend is running (check Railway dashboard)

### CORS errors:
- Make sure `CORS_ORIGINS` in Railway includes your Vercel URL
- No trailing slashes in URLs
- Use HTTPS URLs only

---

## 📝 Quick Reference

**Backend URL:** `https://your-railway-app.railway.app`  
**Frontend URL:** `https://your-vercel-app.vercel.app`  
**API Docs:** `https://your-railway-app.railway.app/docs`  
**Health Check:** `https://your-railway-app.railway.app/api/health`

---

**You're almost there!** 🚀
