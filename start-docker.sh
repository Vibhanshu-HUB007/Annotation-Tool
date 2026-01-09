#!/bin/bash

# Docker Compose Setup Script for Annotation Tool
# Run this script to start the application

set -e

echo "=========================================="
echo "Annotation Tool - Docker Compose Setup"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker compose is available
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
elif docker-compose version &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo "✅ Docker Compose found: $($DOCKER_COMPOSE version | head -1)"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cat > .env << 'EOF'
SECRET_KEY=fKDSYLZ9N2u67XDBamvDqr-kfhZ6BApLqf703QWMgWc
DATABASE_URL=postgresql://postgres:postgres@db:5432/annotation_tool
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000
DEBUG=True
EOF
    echo "✅ Created .env file"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p backend/uploads backend/cache backend/models
echo "✅ Directories created"
echo ""

# Check if user is in docker group
if groups | grep -q docker; then
    echo "✅ User is in docker group - no sudo needed"
    USE_SUDO=""
else
    echo "⚠️  User not in docker group - will use sudo"
    echo "   (To fix: sudo usermod -aG docker $USER, then log out/in)"
    USE_SUDO="sudo"
fi
echo ""

# Build images
echo "🔨 Building Docker images (this may take 5-10 minutes)..."
$USE_SUDO $DOCKER_COMPOSE build
echo "✅ Build complete!"
echo ""

# Start services
echo "🚀 Starting services..."
$USE_SUDO $DOCKER_COMPOSE up -d
echo "✅ Services started!"
echo ""

# Wait a bit for services to initialize
echo "⏳ Waiting for services to initialize (30 seconds)..."
sleep 30

# Check status
echo ""
echo "📊 Service Status:"
$USE_SUDO $DOCKER_COMPOSE ps
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "🌐 Access your application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🔑 Default Login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "📝 Useful commands:"
echo "   View logs:    $USE_SUDO $DOCKER_COMPOSE logs -f"
echo "   Stop:        $USE_SUDO $DOCKER_COMPOSE down"
echo "   Restart:      $USE_SUDO $DOCKER_COMPOSE restart"
echo ""
