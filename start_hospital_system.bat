# 🚀 How to Run the Complete Hospital Management System

This guide provides step-by-step instructions to run the entire Hospital Management System project, including both the Django backend and Streamlit frontend.

## 📋 Prerequisites

Before starting, ensure you have:
- **Python 3.11+** installed
- **Git** (if cloning from repository)
- **PostgreSQL** (optional, for production)
- **Docker** (optional, for containerized deployment)

## 🔧 Method 1: Development Setup (Recommended for Testing)

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system
```

### Step 2: Set Up Virtual Environment
```bash
# Create virtual environment (if not already created)
python -m venv envir

# Activate virtual environment
# On Windows:
envir\Scripts\activate
# On macOS/Linux:
source envir/bin/activate
```

### Step 3: Install Backend Dependencies
```bash
cd hospital_system
pip install -r requirements.txt
```

### Step 4: Set Up Database (Development)
```bash
# Run migrations using SQLite (for development)
python manage.py migrate --settings=hospital_system.settings_local

# Create superuser account
python manage.py createsuperuser --settings=hospital_system.settings_local
```

### Step 5: Start Django Backend
```bash
# Start Django development server
python manage.py runserver --settings=hospital_system.settings_local
```
**✅ Backend will be running at: http://localhost:8000**

### Step 6: Install Frontend Dependencies (New Terminal)
Open a new terminal/command prompt and:
```bash
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\frontend

# Activate virtual environment again
..\envir\Scripts\activate

# Install frontend requirements
pip install -r requirements.txt
```

### Step 7: Start Streamlit Frontend
```bash
# Start Streamlit application
streamlit run hospital_app.py
```
**✅ Frontend will be running at: http://localhost:8501**

## 🐳 Method 2: Docker Deployment (Production-like)

### Step 1: Navigate to Hospital System Directory
```bash
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\hospital_system
```

### Step 2: Create .env File (if not exists)
Ensure your `.env` file has:
```env
SECRET_KEY=django-insecure-v@5z@wckggbyg*lk6&vc8u4(_$s5!pa(%)c!=b190i&m^z7ie3
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
DB_NAME=hospital_db
DB_USER=hospital_user
DB_PASSWORD=hospital_pass
DB_HOST=db
DB_PORT=5432
```

### Step 3: Run with Docker Compose
```bash
# Build and start all services
docker-compose -f docker-compose.prod.yml up --build

# Or run in background
docker-compose -f docker-compose.prod.yml up --build -d
```

This will start:
- **PostgreSQL Database** on port 5432
- **Django Backend** on port 8000
- **Streamlit Frontend** on port 8501

## 📱 Quick Start Script (Windows)

I'll create a batch script to automate the entire process:

<function_calls>
<invoke name="create_file">
<parameter name="content">@echo off
echo ==================================================
echo 🏥 Hospital Management System - Quick Start
echo ==================================================

cd /d "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system"

echo.
echo 📦 Setting up virtual environment...
if not exist "envir" (
    python -m venv envir
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 🔧 Activating virtual environment...
call envir\Scripts\activate

echo.
echo 📥 Installing backend dependencies...
cd hospital_system
pip install -r requirements.txt

echo.
echo 🗄️ Setting up database...
python manage.py migrate --settings=hospital_system.settings_local

echo.
echo 📥 Installing frontend dependencies...
cd ..\frontend
pip install -r requirements.txt

echo.
echo 🚀 Starting services...
echo.
echo Starting Django backend in new window...
start "Django Backend" cmd /k "cd /d %cd%\..\hospital_system && ..\envir\Scripts\activate && ..\envir\Scripts\python.exe manage.py runserver --settings=hospital_system.settings_local"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Streamlit frontend in new window...
start "Streamlit Frontend" cmd /k "cd /d %cd% && ..\envir\Scripts\activate && ..\envir\Scripts\streamlit.exe run hospital_app.py"

echo.
echo ✅ Services are starting!
echo.
echo 🌐 Access your application at:
echo   - Backend API: http://localhost:8000
echo   - Frontend UI: http://localhost:8501
echo   - Admin Panel: http://localhost:8000/admin
echo.
echo Press any key to exit...
pause > nul
