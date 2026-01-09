# Free Hosting Alternatives (No Image Size Limits)

Since Railway has a 4GB limit, here are free alternatives:

## Option 1: Render.com (Recommended)

**Pros:**
- Free tier available
- No strict image size limits
- PostgreSQL included
- Easy GitHub integration
- Auto-deploys on push

**Setup:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. New → Web Service
4. Connect your repository
5. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements-minimal.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Create PostgreSQL database in Render dashboard

**Note:** Render spins down after 15 min of inactivity (free tier), but wakes up on first request.

---

## Option 2: Fly.io

**Pros:**
- Free tier with generous limits
- No image size limits
- Global edge network
- Docker-based

**Setup:**
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Sign up: `fly auth signup`
3. In your project: `fly launch`
4. Follow prompts

---

## Option 3: PythonAnywhere

**Pros:**
- Free tier available
- Python-focused
- No Docker needed

**Limitations:**
- Free tier has restrictions
- Manual deployment

---

## Option 4: Optimize Current Setup

### Use Minimal Requirements

I've created `requirements-minimal.txt` that removes:
- PyTorch (2.1GB+)
- OpenCV (large)
- OpenSlide (requires system libs)

**To use minimal requirements:**

1. In Railway, update build command to:
   ```
   pip install -r requirements-minimal.txt
   ```

2. Or use the Dockerfile I created (multi-stage build, smaller image)

### Make ML Libraries Optional

The AI features can be added later. The core annotation tool works without them.

---

## Option 5: Split Deployment

- **Backend (Core)**: Render/Fly.io (lightweight, no ML)
- **AI Service**: Separate service (only when needed)
- **Frontend**: Vercel (already working!)

---

## Recommended: Render.com

**Why Render:**
- ✅ No 4GB limit
- ✅ Free PostgreSQL
- ✅ Easy setup
- ✅ Auto-deploy from GitHub
- ✅ Good documentation

**Quick Start:**
1. Sign up at render.com
2. New Web Service
3. Connect GitHub repo
4. Set Root Directory: `backend`
5. Use `requirements-minimal.txt`
6. Deploy!

---

## Current Status

- ✅ Frontend: Deployed on Vercel (working!)
- ⚠️ Backend: Railway (image too large)
- 🔄 Solution: Use Render.com or minimal requirements

---

## Next Steps

1. **Try Render.com** (easiest, no limits)
2. **Or** use `requirements-minimal.txt` on Railway
3. **Or** use the Dockerfile for smaller image

Let me know which option you prefer!
