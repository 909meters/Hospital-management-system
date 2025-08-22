#!/bin/bash
# Database Migration and Setup Script for Hospital Management System

echo "🏥 Hospital Management System - Database Setup"
echo "=============================================="

# Navigate to the Django project directory
cd hospital_system

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🗄️ Setting up PostgreSQL database..."

# Check if PostgreSQL is running
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL is not installed or not in PATH"
    echo "Please install PostgreSQL and ensure it's running"
    echo "For Windows: Download from https://www.postgresql.org/download/windows/"
    echo "For Mac: brew install postgresql"
    echo "For Ubuntu: sudo apt-get install postgresql postgresql-contrib"
    exit 1
fi

# Create database and user (if they don't exist)
echo "Creating database and user..."

# This assumes PostgreSQL is running and you have superuser access
# You may need to modify this based on your PostgreSQL setup
createdb hospital_db 2>/dev/null || echo "Database 'hospital_db' may already exist"

# Alternative using psql (uncomment if needed)
# psql -U postgres -c "CREATE DATABASE hospital_db;" 2>/dev/null || echo "Database may already exist"
# psql -U postgres -c "CREATE USER hospital_user WITH PASSWORD 'hospital_pass';" 2>/dev/null || echo "User may already exist"
# psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;" 2>/dev/null

echo "🔄 Running Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "👤 Creating superuser (admin)..."
echo "Please create an admin user for the system:"
python manage.py createsuperuser

echo "📊 Loading initial data (if any)..."
# Uncomment if you have fixtures
# python manage.py loaddata initial_data.json

echo "🔧 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Database setup complete!"
echo ""
echo "To start the development server:"
echo "python manage.py runserver"
echo ""
echo "To start the frontend:"
echo "cd ../frontend"
echo "streamlit run hospital_app.py"
echo ""
echo "🚀 Your Hospital Management System is ready!"
