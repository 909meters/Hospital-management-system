#!/bin/bash

echo "🐳 Starting Hospital Management System with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "📦 Building and starting containers..."

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Hospital Management System is starting up!"
echo ""
echo "📋 Service URLs:"
echo "   🌐 Frontend (Streamlit): http://localhost:8501"
echo "   🔧 Backend API: http://localhost:8000/api"
echo "   👑 Django Admin: http://localhost:8000/admin"
echo "   🗄️  Database: localhost:5432"
echo "   🌐 Nginx Proxy: http://localhost:80 (if enabled)"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "⚠️  Note: It may take a few minutes for all services to be fully ready."
