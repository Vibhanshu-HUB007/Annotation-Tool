# ✅ Docker Compose Setup Complete!

## Services Running

Your annotation tool is now running with Docker Compose:

- ✅ **Backend API**: Running on port 8000
- ✅ **Frontend**: Running on port 3000  
- ✅ **PostgreSQL Database**: Running (internal)

## Access Your Application

### Web Interface
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Default Login Credentials

⚠️ **IMPORTANT**: Change these after first login!

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

## Useful Commands

### Check Service Status
```bash
sudo docker compose ps
```

### View Logs
```bash
# All services
sudo docker compose logs -f

# Specific service
sudo docker compose logs -f backend
sudo docker compose logs -f frontend
sudo docker compose logs -f db
```

### Stop Services
```bash
sudo docker compose down
```

### Restart Services
```bash
sudo docker compose restart
# Or restart specific service
sudo docker compose restart backend
```

### Start Services (after stopping)
```bash
sudo docker compose up -d
```

### Rebuild After Code Changes
```bash
sudo docker compose up -d --build
```

### Remove Everything (including data)
```bash
sudo docker compose down -v
```

## Next Steps

1. **Open your browser** and go to: http://localhost:3000
2. **Login** with admin/admin123
3. **Change the password** immediately
4. **Test uploading** a WSI file or image
5. **Create annotations** to test the tool

## Troubleshooting

### Can't Access Frontend
- Check if service is running: `sudo docker compose ps`
- Check logs: `sudo docker compose logs frontend`
- Verify port 3000 is not in use: `sudo lsof -i :3000`

### Can't Access Backend
- Wait 30 seconds for backend to fully start
- Check logs: `sudo docker compose logs backend`
- Test health endpoint: `curl http://localhost:8000/api/health`

### Database Connection Issues
- Wait for database to initialize (30-60 seconds)
- Check database logs: `sudo docker compose logs db`
- Verify database is running: `sudo docker compose ps db`

### Login Not Working
- Check backend logs for errors
- Verify database was initialized (should see "Created default admin user" in logs)
- Try accessing API docs: http://localhost:8000/docs

## Data Persistence

Your data is stored in Docker volumes:
- **Database**: `annotation-tool_postgres_data` volume
- **Uploads**: `./backend/uploads` directory (mapped to container)
- **Cache**: `./backend/cache` directory (mapped to container)

To backup:
```bash
# Backup database
sudo docker compose exec db pg_dump -U postgres annotation_tool > backup.sql

# Backup uploads
tar -czf uploads_backup.tar.gz backend/uploads/
```

## Performance Tips

- First request may be slow (services starting up)
- Database queries get faster after warm-up
- Large WSI files may take time to process
- Check system resources: `docker stats`

## Success! 🎉

Your annotation tool is now running locally on your server!
