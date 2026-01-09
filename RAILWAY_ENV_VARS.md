# Railway Environment Variables Setup

## Required Environment Variables

After your Railway deployment builds successfully, add these environment variables:

### In Railway Dashboard:
1. Go to your service
2. Click on **"Variables"** tab
3. Add each variable:

```
SECRET_KEY=<generate-a-random-string>
```

To generate a secret key, you can use:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use any random string like: `your-super-secret-key-change-in-production-12345`

```
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

Replace with your actual frontend URL after deploying to Vercel.

```
UPLOAD_DIR=./uploads
CACHE_DIR=./cache
DEBUG=False
```

### Database (Auto-created by Railway)

Railway will automatically create a PostgreSQL database and provide `DATABASE_URL`. You don't need to set this manually - Railway does it automatically!

## Initialize Database

After deployment, run this command in Railway:

1. Go to your service → **"Deploy Logs"**
2. Click **"New Terminal"**
3. Run:
   ```bash
   cd backend
   python scripts/init_db.py
   ```

Or use Railway CLI:
```bash
railway run python backend/scripts/init_db.py
```

## Check Deployment

1. Go to Railway dashboard
2. Your service should show a URL like: `https://your-app.railway.app`
3. Visit: `https://your-app.railway.app/api/health`
   - Should return: `{"status": "healthy"}`
4. Visit: `https://your-app.railway.app/docs`
   - Should show FastAPI documentation

## Troubleshooting

If the app doesn't start:
- Check "Deploy Logs" for errors
- Verify all environment variables are set
- Make sure database is initialized
- Check that the service is running (not paused)
