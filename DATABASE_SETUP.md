# Database Setup Guide for Render.com

## Step 1: Create PostgreSQL Database on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `annotation-tool-db` (or your preferred name)
   - **Database**: `annotation_tool` (or your preferred name)
   - **User**: Leave default or set custom
   - **Region**: Same as your backend service
   - **PostgreSQL Version**: 16 (recommended)
   - **Plan**: Free tier is fine for development
4. Click **"Create Database"**
5. Wait for the database to be provisioned (takes 1-2 minutes)

## Step 2: Get Database Connection String

1. Once the database is created, click on it
2. Go to **"Connections"** tab
3. Copy the **"Internal Database URL"** (for services in the same account)
   - Format: `postgresql://user:password@host:port/dbname`
   - Example: `postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/annotation_tool`

## Step 3: Add Environment Variables to Backend Service

1. Go to your backend service on Render
2. Click on **"Environment"** tab
3. Add the following environment variables:

### Required Variables:

```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
CORS_ORIGINS=https://your-frontend-url.vercel.app,https://your-frontend-url.netlify.app
```

### Optional Variables (with defaults):

```bash
DEBUG=False
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10737418240
```

## Step 4: Redeploy Backend

1. After adding environment variables, Render will automatically redeploy
2. Check the logs to ensure:
   - Database connection is successful
   - Tables are created
   - Default admin user is created

## Step 5: Verify Database Initialization

1. Check the deployment logs for:
   ```
   Created default admin user (username: admin, password: admin123)
   Created default label schema
   Database initialized successfully
   ```

2. Test the API:
   - Health: `https://your-backend.onrender.com/api/health`
   - Docs: `https://your-backend.onrender.com/docs`
   - Login: `POST https://your-backend.onrender.com/api/auth/login`
     - Username: `admin`
     - Password: `admin123`

## Default Admin Credentials

⚠️ **IMPORTANT**: Change these in production!

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

## Troubleshooting

### Database Connection Errors

If you see connection errors:
1. Verify `DATABASE_URL` is correct
2. Check database is running (green status in Render dashboard)
3. Ensure database and backend are in the same region
4. For external connections, use "External Database URL" instead

### Migration Issues

If tables aren't created:
1. Check logs for SQL errors
2. Verify database user has CREATE permissions
3. Try manually running migrations (if using Alembic)

### Initialization Errors

If initialization fails:
1. Check if admin user already exists
2. Verify database connection is working
3. Check logs for specific error messages
