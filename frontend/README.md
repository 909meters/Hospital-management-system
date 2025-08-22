# Hospital Management System - Frontend

This is a Streamlit-based low-code frontend for the Hospital Management System API.

## 🚀 Quick Start

### Option 1: Use the Automated Scripts (Easiest)

**Windows Batch Script:**
```bash
# Navigate to project root and run:
start_hospital_system.bat
```

**PowerShell Script:**
```powershell
# Navigate to project root and run:
.\start_hospital_system.ps1
```

### Option 2: Manual Setup

1. **Ensure the Django backend is running on `http://localhost:8000`**

2. **Navigate to frontend directory:**
```bash
cd c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\frontend
```

3. **Activate virtual environment:**
```bash
# Windows:
..\envir\Scripts\activate
# macOS/Linux:
source ../envir/bin/activate
```

4. **Install the frontend requirements:**
```bash
pip install -r requirements.txt
```

5. **Run the Streamlit application:**
```bash
streamlit run hospital_app.py
```

6. **Open your browser to `http://localhost:8501`**

## 🔗 Service URLs

Once both services are running:
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **API Browser**: http://localhost:8000/api

## ✨ Features

- **User Authentication**: Login with username/password
- **Dashboard Overview**: View key metrics and recent activity
- **Patient Management**: Add, view, and search patients
- **Appointment Scheduling**: Schedule and manage appointments
- **Medical Records**: View and add medical records for patients
- **User Management**: Admin-only user management interface

## Default Login Credentials

The system should be set up with default admin credentials. If not, create a superuser in Django:

```bash
cd hospital_system
python manage.py createsuperuser
```

## Configuration

- **API_BASE_URL**: Set in `hospital_app.py` to point to your Django API
- **Authentication**: Uses Django Token Authentication
- **CORS**: Ensure Django backend allows requests from Streamlit (localhost:8501)

## Usage

1. **Login**: Use your Django user credentials
2. **Navigation**: Use the sidebar to navigate between different sections
3. **Patients**: Add new patients or search existing ones
4. **Appointments**: Schedule appointments and view existing ones
5. **Medical Records**: Add and view medical records for patients
6. **Users**: Admin users can manage system users

## Features by Role

- **Admin**: Full access to all features including user management
- **Doctor**: Access to patients, appointments, and medical records
- **Nurse**: Access to patients and appointments
- **Receptionist**: Access to patients and appointment scheduling

## Troubleshooting

- Ensure Django backend is running and accessible
- Check that CORS is properly configured in Django settings
- Verify API endpoints are working using Django admin or API browser
- Check browser console for any JavaScript errors
