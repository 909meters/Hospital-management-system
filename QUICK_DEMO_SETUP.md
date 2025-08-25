# 🚀 Quick Demo Setup

## Pre-Presentation Setup (5 minutes)

### 1. Start Docker Desktop
Ensure Docker Desktop is running on your system.

### 2. Navigate to Project Directory
```powershell
cd "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system"
```

### 3. Start the Hospital Management System
```powershell
# Development environment (recommended for demo)
docker-compose -f docker-compose.dev.yml up -d

# OR Production environment
docker-compose up -d
```

### 4. Verify Services Are Running
```powershell
docker-compose -f docker-compose.dev.yml ps
```

Expected output:
```
NAME       SERVICE     STATUS      PORTS
backend    backend     running     0.0.0.0:8000->8000/tcp
db         db          running     5432/tcp
frontend   frontend    running     0.0.0.0:8501->8501/tcp
```

### 5. Access the System
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### 6. Test Credentials
```
Admin User:
- Username: admin
- Password: admin123

Doctor User:  
- Username: doctor1
- Password: doctor123

Patient User:
- Username: patient1  
- Password: patient123
```

## Demo Flow (15 minutes)

### 1. Authentication Demo (3 minutes)
- Show login as different roles
- Demonstrate role-based access control
- Display user permissions

### 2. Patient Management (4 minutes)
- Create new patient record
- View patient list
- Update patient information
- Show search and filtering

### 3. Appointment Scheduling (3 minutes)
- Book new appointment
- View appointment calendar
- Update appointment status

### 4. API Documentation (2 minutes)
- Open Postman collection
- Demonstrate API endpoints
- Show response formats

### 5. Architecture Walkthrough (3 minutes)
- Display system architecture diagram
- Explain layered design
- Highlight security features

## Troubleshooting

### If Docker fails to start:
```powershell
# Check Docker status
docker version

# Restart Docker Desktop
# Use screenshots from PRESENTATION_MATERIALS.md
```

### If ports are in use:
```powershell
# Stop any existing containers
docker-compose -f docker-compose.dev.yml down

# Clean up
docker system prune
```

### If database issues:
```powershell
# Reset database
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

## Backup Demo Plan

If live demo fails, use:
1. Screenshots from `PRESENTATION_MATERIALS.md`
2. Architecture diagrams  
3. Code walkthrough in IDE
4. Postman collection demonstration

## Post-Demo Cleanup

```powershell
# Stop all services
docker-compose -f docker-compose.dev.yml down

# Optional: Clean up volumes
docker-compose -f docker-compose.dev.yml down -v
```

## Key Numbers to Remember

- **Response Time**: <200ms average
- **Concurrent Users**: 50+ tested
- **Uptime Target**: 99.9%
- **Test Coverage**: 81%
- **Deployment Time**: <5 minutes
- **Architecture Score**: 8.32/10
