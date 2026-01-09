#!/bin/bash

# Script to initialize the database with default admin user

echo "=========================================="
echo "Initializing Database"
echo "=========================================="
echo ""

echo "Checking if backend container is running..."
if ! sudo docker compose ps | grep -q "annotation-tool-backend-1.*Up"; then
    echo "❌ Backend container is not running!"
    echo "Start it with: sudo docker compose up -d"
    exit 1
fi

echo "✅ Backend container is running"
echo ""

echo "Initializing database..."
echo "This will create:"
echo "  - Default admin user (username: admin, password: admin123)"
echo "  - Default label schema"
echo ""

sudo docker compose exec backend python scripts/init_db.py

echo ""
echo "=========================================="
echo "Database initialization complete!"
echo "=========================================="
echo ""
echo "You can now login with:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
