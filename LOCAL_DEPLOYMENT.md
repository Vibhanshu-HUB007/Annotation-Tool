# Local/Private Server Deployment Guide

This guide helps you deploy the annotation tool on your own server/machine for private use, not as a public web application.

## Option 1: Docker Compose (Recommended - Easiest)

### Prerequisites
- Docker and Docker Compose installed on your server
- At least 4GB RAM
- 10GB+ free disk space

### Quick Start

1. **Clone the repository** (if not already):
   ```bash
   git clone https://github.com/Vibhanshu-HUB007/Annotation-Tool.git
   cd Annotation-Tool
   ```

2. **Create environment file**:
   ```bash
   cd backend
   cp .env.example .env  # Or create .env manually
   ```

3. **Edit `.env` file**:
   ```bash
   # Database (SQLite for simplicity, or PostgreSQL)
   DATABASE_URL=sqlite:///./annotation_tool.db
   
   # Security
   SECRET_KEY=your-super-secret-key-change-this-min-32-chars
   
   # CORS - Allow local access only
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
   
   # Server settings
   DEBUG=True
   ```

4. **Create `docker-compose.yml`** in project root:
   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://postgres:postgres@db:5432/annotation_tool
         - SECRET_KEY=${SECRET_KEY:-change-this-secret-key}
         - CORS_ORIGINS=http://localhost:3000,http://localhost:5173
         - DEBUG=True
       volumes:
         - ./backend/uploads:/app/uploads
         - ./backend/cache:/app/cache
       depends_on:
         - db
       restart: unless-stopped

     db:
       image: postgres:16
       environment:
         - POSTGRES_USER=postgres
         - POSTGRES_PASSWORD=postgres
         - POSTGRES_DB=annotation_tool
       volumes:
         - postgres_data:/var/lib/postgresql/data
       restart: unless-stopped

     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - "3000:3000"
       environment:
         - VITE_API_URL=http://localhost:8000/api
       depends_on:
         - backend
       restart: unless-stopped

   volumes:
     postgres_data:
   ```

5. **Start everything**:
   ```bash
   docker-compose up -d
   ```

6. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

7. **Default admin credentials**:
   - Username: `admin`
   - Password: `admin123`

## Option 2: Manual Installation on Your Server

### Backend Setup

1. **Install Python 3.11+**:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip
   ```

2. **Install PostgreSQL** (optional, SQLite works too):
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

3. **Set up backend**:
   ```bash
   cd Annotation-Tool/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-minimal.txt
   ```

4. **Configure environment**:
   ```bash
   # Create .env file
   cat > .env << EOF
   DATABASE_URL=sqlite:///./annotation_tool.db
   SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
   CORS_ORIGINS=http://localhost:3000,http://localhost:5173
   DEBUG=True
   EOF
   ```

5. **Initialize database**:
   ```bash
   python scripts/init_db.py
   ```

6. **Start backend** (with systemd service):
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/annotation-backend.service
   ```

   Add this content:
   ```ini
   [Unit]
   Description=Annotation Tool Backend
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/Annotation-Tool/backend
   Environment="PATH=/path/to/Annotation-Tool/backend/venv/bin"
   ExecStart=/path/to/Annotation-Tool/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable annotation-backend
   sudo systemctl start annotation-backend
   ```

### Frontend Setup

1. **Install Node.js 18+**:
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt install -y nodejs
   ```

2. **Set up frontend**:
   ```bash
   cd Annotation-Tool/frontend
   npm install
   ```

3. **Configure API URL**:
   ```bash
   # Create .env.local
   echo "VITE_API_URL=http://localhost:8000/api" > .env.local
   ```

4. **Build and serve**:
   ```bash
   npm run build
   # Option 1: Use a simple server
   npx serve -s dist -l 3000
   
   # Option 2: Use nginx (see below)
   ```

### Nginx Setup (Optional - for production-like setup)

1. **Install nginx**:
   ```bash
   sudo apt install nginx
   ```

2. **Create nginx config**:
   ```bash
   sudo nano /etc/nginx/sites-available/annotation-tool
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name localhost;  # Or your server's IP/domain

       # Frontend
       location / {
           root /path/to/Annotation-Tool/frontend/dist;
           try_files $uri $uri/ /index.html;
       }

       # Backend API
       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

3. **Enable and restart**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/annotation-tool /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Option 3: Single Machine (Development Mode)

For quick testing on your local machine:

1. **Backend** (Terminal 1):
   ```bash
   cd Annotation-Tool/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-minimal.txt
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend** (Terminal 2):
   ```bash
   cd Annotation-Tool/frontend
   npm install
   echo "VITE_API_URL=http://localhost:8000/api" > .env.local
   npm run dev
   ```

3. **Access**: http://localhost:5173 (or whatever port Vite shows)

## Security for Private Deployment

### Firewall Setup

Only allow access from your local network:

```bash
# Ubuntu/Debian
sudo ufw allow from 192.168.1.0/24 to any port 8000
sudo ufw allow from 192.168.1.0/24 to any port 3000
sudo ufw enable
```

### Change Default Credentials

After first login, immediately:
1. Go to user settings
2. Change admin password
3. Create additional users if needed

### Network Access

- **Local only**: Bind to `127.0.0.1` instead of `0.0.0.0`
- **Local network**: Use your server's local IP (e.g., `192.168.1.100`)
- **VPN**: Set up VPN for remote access

## Troubleshooting

### Backend won't start
- Check logs: `journalctl -u annotation-backend -f`
- Verify database connection
- Check port 8000 is not in use: `sudo lsof -i :8000`

### Frontend can't connect
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend
- Verify backend is running

### Database errors
- For SQLite: Check file permissions
- For PostgreSQL: Verify connection string and user permissions

## Maintenance

### Update the application
```bash
cd Annotation-Tool
git pull
# Restart services
sudo systemctl restart annotation-backend
```

### Backup database
```bash
# SQLite
cp backend/annotation_tool.db backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump annotation_tool > backup_$(date +%Y%m%d).sql
```

### View logs
```bash
# Backend logs
journalctl -u annotation-backend -f

# Docker logs
docker-compose logs -f backend
```

## Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend accessible
- [ ] Can login with admin credentials
- [ ] Database initialized
- [ ] Can upload/test WSI files
- [ ] Firewall configured (if needed)
- [ ] Default password changed
