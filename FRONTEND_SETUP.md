# Frontend Configuration for Render Backend

## Step 1: Update Frontend Environment Variables

### For Local Development

Create or update `.env.local` in the `frontend` directory:

```bash
VITE_API_URL=https://annotation-tool-v7mu.onrender.com/api
```

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://annotation-tool-v7mu.onrender.com/api`
   - **Environment**: Production, Preview, Development (select all)
4. Redeploy your frontend

### For Netlify Deployment

1. Go to your Netlify site dashboard
2. Navigate to **Site settings** → **Environment variables**
3. Add:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://annotation-tool-v7mu.onrender.com/api`
   - **Scopes**: All scopes (Production, Deploy previews, Branch deploys)
4. Redeploy your site

## Step 2: Update CORS Settings

Make sure your backend CORS settings include your frontend URL:

1. Go to Render dashboard → Your backend service → Environment
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend.netlify.app
   ```
3. Redeploy backend

## Step 3: Test the Connection

1. Open your frontend in browser
2. Open browser DevTools → Network tab
3. Try to login or make an API call
4. Verify requests are going to: `https://annotation-tool-v7mu.onrender.com/api/...`

## Troubleshooting

### CORS Errors

If you see CORS errors:
1. Verify `CORS_ORIGINS` includes your exact frontend URL (with https://)
2. Check backend logs for CORS-related errors
3. Ensure frontend is using the correct API URL

### Connection Timeout

If requests timeout:
1. Render free tier spins down after inactivity
2. First request may take 30-60 seconds to wake up
3. Consider upgrading to paid tier for always-on service

### 401 Unauthorized

If you get 401 errors:
1. Verify you're sending the Authorization header
2. Check token is being stored correctly
3. Ensure token hasn't expired
