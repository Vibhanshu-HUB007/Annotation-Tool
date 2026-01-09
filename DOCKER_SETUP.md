# Docker Compose Setup - Quick Start

## Step 1: Fix Docker Permissions (One-time setup)

You need to add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Then **log out and log back in** (or restart your terminal) for the changes to take effect.

**OR** use `sudo` for now (less secure but works immediately):
```bash
sudo docker compose build
sudo docker compose up
```

## Step 2: Build and Start Services

Once permissions are fixed:

```bash
cd /media/vibhanshu92/Data/Annotation-Tool

# Build the images (first time only, takes 5-10 minutes)
docker compose build

# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

## Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Change these immediately after first login!**

## Useful Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db

# Restart a service
docker compose restart backend

# Rebuild after code changes
docker compose up -d --build

# Stop and remove everything (including volumes)
docker compose down -v
```

## Troubleshooting

### Permission Denied Error
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Port Already in Use
```bash
# Check what's using the port
sudo lsof -i :8000
sudo lsof -i :3000

# Or change ports in docker-compose.yml
```

### Database Connection Error
- Wait 30 seconds after starting for database to initialize
- Check logs: `docker compose logs db`

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` in docker-compose.yml
- Check CORS settings in backend
- Check backend logs: `docker compose logs backend`
