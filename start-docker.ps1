# Hospital Management System - Docker Startup Script for Windows

Write-Host "🐳 Starting Hospital Management System with Docker..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if docker-compose is available
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ docker-compose not found. Please install Docker Compose." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Building and starting containers..." -ForegroundColor Yellow

# Build and start all services
docker-compose up --build -d

Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if services are running
Write-Host "🔍 Checking service status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "✅ Hospital Management System is starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Service URLs:" -ForegroundColor Cyan
Write-Host "   🌐 Frontend (Streamlit): http://localhost:8501" -ForegroundColor White
Write-Host "   🔧 Backend API: http://localhost:8000/api" -ForegroundColor White
Write-Host "   👑 Django Admin: http://localhost:8000/admin" -ForegroundColor White
Write-Host "   🗄️  Database: localhost:5432" -ForegroundColor White
Write-Host "   🌐 Nginx Proxy: http://localhost:80 (if enabled)" -ForegroundColor White
Write-Host ""
Write-Host "📝 To view logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow
Write-Host "🔄 To restart: docker-compose restart" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  Note: It may take a few minutes for all services to be fully ready." -ForegroundColor Magenta
