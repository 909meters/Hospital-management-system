# 🚀 Quick Start Guide - Hospital Management System

## Method 1: Automated Setup (Recommended)

### Windows Users:
```bash
# Double-click or run from command prompt:
start_hospital_system.bat
```

### PowerShell Users:
```powershell
# Run from PowerShell:
.\start_hospital_system.ps1
```

## Method 2: Manual Setup

### Step 1: Backend Setup
```bash
# Navigate to project
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system

# Activate virtual environment
envir\Scripts\activate

# Go to backend directory
cd hospital_system

# Install dependencies (if not done)
pip install -r requirements.txt

# Run migrations (if not done)
python manage.py migrate --settings=hospital_system.settings_local

# Start Django server
python manage.py runserver --settings=hospital_system.settings_local
```

### Step 2: Frontend Setup (New Terminal)
```bash
# Navigate to frontend
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\frontend

# Activate virtual environment
..\envir\Scripts\activate

# Install dependencies (if not done)
pip install -r requirements.txt

# Start Streamlit
streamlit run hospital_app.py
```

## 🌐 Access Points

Once running, access:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## 👤 Available Login Credentials

The system has these users available:
- **Username**: `testuser` / **Password**: `test123` (Doctor role)
- **Username**: `admin` / **Password**: `[your-admin-password]` (Admin role)
- **Username**: `doctor1` / **Password**: `[set-in-admin]` (Doctor role)
- **Username**: `patient1` / **Password**: `[set-in-admin]` (Patient role)

### 🔧 Create/Reset User Passwords

If you need to reset passwords or create new users:

1. **Via Django Admin**:
   - Go to http://localhost:8000/admin
   - Login with admin credentials
   - Navigate to Users → Add/Edit users

2. **Via Django Shell**:
```bash
cd hospital_system
python manage.py shell --settings=hospital_system.settings_local

# In the shell:
from users.models import CustomUser
user = CustomUser.objects.get(username='admin')
user.set_password('newpassword')
user.save()
```

## 🆘 Troubleshooting

**Port already in use?**
- Backend: `python manage.py runserver 8001`
- Frontend: `streamlit run hospital_app.py --server.port 8502`

**Can't connect to API?**
- Ensure Django backend is running first
- Check if ports 8000 and 8501 are available
- Verify API URL in frontend (should be `http://127.0.0.1:8000/api`)

**Invalid credentials error?**
- Use the test credentials: `testuser` / `test123`
- Or reset admin password via Django admin
- Check available users in Django admin panel

**Connection refused error?**
- Make sure Django server is running on http://127.0.0.1:8000
- Test API directly: Open `frontend/test_system.html` in browser
- Check firewall settings if needed

**Streamlit won't start?**
- Skip email prompt by pressing Enter
- Use full path to streamlit.exe if needed
- Check if all frontend dependencies are installed
