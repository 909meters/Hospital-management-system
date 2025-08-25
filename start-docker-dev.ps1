# Hospital Management System - Docker Development Mode

Write-Host "🐳 Starting Hospital Management System in Development Mode..." -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "📦 Building and starting containers in development mode..." -ForegroundColor Yellow

# Build and start development services
docker-compose -f docker-compose.dev.yml up --build

Write-Host ""
Write-Host "🛑 To stop development containers:" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C or run: docker-compose -f docker-compose.dev.yml down" -ForegroundColor White
