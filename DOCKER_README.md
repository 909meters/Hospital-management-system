# Hospital Management System - Docker Documentation

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose
- At least 4GB of available RAM

### Start the System
```bash
# Development mode (with hot reload)
docker-compose -f docker-compose.dev.yml up --build

# Production mode (background)
docker-compose up --build -d

# Using PowerShell scripts (Windows)
.\start-docker-dev.ps1    # Development
.\start-docker.ps1        # Production
```

### Service URLs
After starting:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin
- **Database**: localhost:5432

### Test Users
- **testuser** (Patient): test123
- **testdoctor** (Doctor): test123  
- **testadmin** (Admin): test123

## Configuration

### Environment Variables
Key environment variables can be customized in `.env.docker`:
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)

### Database Configuration
The PostgreSQL database is configured with:
- Database: `hospital_db`
- User: `hospital_user`
- Password: `hospital_pass123`
- Port: `5432`

## Docker Commands

### Basic Operations
```bash
# Build and start all services
docker-compose up --build -d

# View running containers
docker-compose ps

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes (⚠️ deletes data)
docker-compose down -v
```

### Development Commands
```bash
# Start in development mode
docker-compose -f docker-compose.dev.yml up

# Rebuild specific service
docker-compose build backend

# Execute commands in running container
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend bash
```

### Database Operations
```bash
# Access PostgreSQL database
docker-compose exec db psql -U hospital_user -d hospital_db

# Create database backup
docker-compose exec db pg_dump -U hospital_user hospital_db > backup.sql

# Restore database backup
docker-compose exec -T db psql -U hospital_user -d hospital_db < backup.sql
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   # Stop the service using the port or change port in docker-compose.yml
   ```

2. **Database connection issues**
   ```bash
   # Check if database is running
   docker-compose ps db
   # View database logs
   docker-compose logs db
   ```

3. **Frontend can't connect to backend**
   - Ensure backend is running: `docker-compose ps backend`
   - Check API_BASE_URL in frontend environment

4. **Permission issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Debugging

1. **View container logs**
   ```bash
   docker-compose logs -f [service_name]
   ```

2. **Access container shell**
   ```bash
   docker-compose exec [service_name] bash
   ```

3. **Check container resource usage**
   ```bash
   docker stats
   ```

## Production Deployment

### Security Considerations
1. Change default passwords in `.env.docker`
2. Set `DEBUG=False` in production
3. Configure proper `ALLOWED_HOSTS`
4. Use HTTPS with proper SSL certificates
5. Configure firewall rules

### Performance Optimization
1. Use production WSGI server (Gunicorn is included)
2. Configure Nginx for static file serving
3. Set up database connection pooling
4. Configure proper logging

### Backup Strategy
1. Regular database backups
2. Volume backups for persistent data
3. Configuration backup

## Monitoring

### Health Checks
All services include health checks:
- Backend: HTTP check on `/api/health/`
- Frontend: HTTP check on `/_stcore/health`
- Database: PostgreSQL connection check

### Logs
Logs are available via:
```bash
docker-compose logs -f [service_name]
```

## Scaling

### Horizontal Scaling
```bash
# Scale backend service
docker-compose up -d --scale backend=3

# Scale with load balancer
# (requires Nginx configuration)
```

## Support
For issues and questions:
1. Check the logs: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Check the main documentation: `README.md`
