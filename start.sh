#!/bin/bash

# DefinitelyNotASpy - Startup Script

echo "🚀 Starting DefinitelyNotASpy services..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "✓ Created .env file. Please update it with your configuration."
fi

# Build and start services
echo "📦 Building services..."
docker-compose build

echo "🏃 Starting services..."
docker-compose up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📡 Service URLs:"
echo "  - Crawler API:     http://localhost:8080"
echo "  - Intel API:       http://localhost:8000"
echo "  - API Docs:        http://localhost:8000/docs"
echo "  - Neo4j Browser:   http://localhost:7474"
echo "  - Qdrant Dashboard: http://localhost:6333/dashboard"
echo ""
echo "📊 Check logs with: docker-compose logs -f"
echo "🛑 Stop services with: docker-compose down"
echo ""
