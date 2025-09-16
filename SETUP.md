# Installation and Setup Guide

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning repository)
- At least 4GB available RAM
- Available ports: 8501 (frontend), 8000 (backend), 5432 (database)

## Quick Start Deployment

### 1. Environment Preparation
Ensure Docker Desktop is operational before proceeding with deployment.

### 2. Application Deployment
```bash
# Deploy development environment
docker-compose -f docker-compose.dev.yml up -d

# Alternative: Windows PowerShell script
.\start-docker-dev.ps1
```

### 3. Application Access
- **Web Interface**: http://localhost:8501
- **API Endpoints**: http://localhost:8000/api/
- **Administrative Panel**: http://localhost:8000/admin/

### 4. Test User Credentials
- **Administrator**: username `admin`, password `admin123`
- **Healthcare Provider**: username `doctor1`, password `doctor123`  
- **Patient**: username `patient1`, password `patient123`

## Troubleshooting

### Service Recovery
```bash
# Stop and restart all services
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

### Port Conflicts
If ports are already in use:
```bash
# Identify conflicting processes
netstat -ano | findstr :8501
netstat -ano | findstr :8000

# Terminate conflicting processes or modify docker-compose port mappings
```

### Complete System Reset
For persistent issues requiring fresh deployment:
```bash
# Remove all containers and volumes
docker-compose -f docker-compose.dev.yml down -v
docker system prune -f

# Redeploy system
docker-compose -f docker-compose.dev.yml up -d --build
```

## Verification Steps

1. Confirm all containers are running: `docker-compose -f docker-compose.dev.yml ps`
2. Access web interface at http://localhost:8501
3. Verify API connectivity at http://localhost:8000/api/
4. Test authentication using provided credentials

---

**Note**: For production deployment, use `docker-compose.yml` instead of the development configuration.
