# Database Migration and Setup Script for Hospital Management System (Windows)

Write-Host "🏥 Hospital Management System - Database Setup" -ForegroundColor Blue
Write-Host "==============================================" -ForegroundColor Blue

# Navigate to the Django project directory
Set-Location hospital_system

Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "🗄️ Setting up PostgreSQL database..." -ForegroundColor Yellow

# Check if PostgreSQL is installed
try {
    $null = Get-Command psql -ErrorAction Stop
    Write-Host "✅ PostgreSQL found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install PostgreSQL from: https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host "Make sure to add PostgreSQL bin directory to your PATH" -ForegroundColor Yellow
    exit 1
}

# Create database and user
Write-Host "Creating database and user..." -ForegroundColor Yellow

# Note: You may need to adjust the PostgreSQL connection parameters
# Based on your local setup (username, password, etc.)

Write-Host "🔄 Running Django migrations..." -ForegroundColor Yellow
python manage.py makemigrations
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error during makemigrations" -ForegroundColor Red
    exit 1
}

python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error during migration" -ForegroundColor Red
    exit 1
}

Write-Host "👤 Creating superuser (admin)..." -ForegroundColor Yellow
Write-Host "Please create an admin user for the system:" -ForegroundColor Cyan
python manage.py createsuperuser

Write-Host "🔧 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host "✅ Database setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server:" -ForegroundColor Cyan
Write-Host "python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "To start the frontend:" -ForegroundColor Cyan
Write-Host "cd ../frontend" -ForegroundColor White
Write-Host "streamlit run hospital_app.py" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Your Hospital Management System is ready!" -ForegroundColor Green
