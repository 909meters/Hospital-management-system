# Hospital Management System - Complete Setup and Documentation

## 🏥 Project Overview

This is a complete Hospital Management System with Django REST API backend and a Streamlit low-code frontend. The system provides comprehensive patient management, appointment scheduling, medical records, and user management capabilities.

This project is created for the course Software Architecture under the program "Computer Science and Information Technology" in University Ca'Foscari.

## 🚀 Features Implemented

### Backend (Django REST API)
- **Authentication & Authorization**: Token-based authentication with role-based access control
- **User Management**: Custom user model with roles (admin, doctor, nurse, receptionist)
- **Patient Management**: Complete patient CRUD operations with medical records
- **Appointment Scheduling**: Full appointment management system
- **Medical Records**: Patient medical history and records management
- **API Documentation**: RESTful API with proper endpoints

### Frontend (Streamlit Low-Code)
- **Modern UI**: Clean, responsive interface using Streamlit
- **Dashboard**: Overview with key metrics and recent activity
- **Patient Management**: Add, view, search, and manage patients
- **Appointment System**: Schedule and manage appointments
- **Medical Records**: View and add medical records
- **User Management**: Admin interface for user management
- **Role-based Access**: Different access levels based on user roles

### Database
- **Development**: SQLite (ready to use)
- **Production**: PostgreSQL (configured with environment variables)
- **Migrations**: All models properly migrated

### Deployment
- **Docker Support**: Complete Docker and Docker Compose configuration
- **Environment Configuration**: Proper environment variable management
- **Production Ready**: Gunicorn, static file handling, security settings

## 📋 Quick Start Guide

### Prerequisites
- Python 3.11+
- Git
- (Optional) PostgreSQL for production
- (Optional) Docker for containerized deployment

### 1. Clone and Setup
```bash
git clone <your-repo>
cd Hospital-management-system
```

### 2. Backend Setup
```bash
cd hospital_system

# Create virtual environment
python -m venv envir
# On Windows:
envir\Scripts\activate
# On macOS/Linux:
source envir/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (SQLite for development)
python manage.py migrate --settings=hospital_system.settings_local

# Create superuser
python manage.py createsuperuser --settings=hospital_system.settings_local

# Start Django server
python manage.py runserver --settings=hospital_system.settings_local
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install frontend dependencies
pip install -r requirements.txt

# Start Streamlit app
streamlit run hospital_app.py
```

### 4. Access the System
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:8501
- **Django Admin**: http://localhost:8000/admin
- **API Browser**: http://localhost:8000/api

## 🔧 Configuration

### Environment Variables (.env file)
```env
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# PostgreSQL Database (for production)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hospital_db
DB_USER=hospital_user
DB_PASSWORD=hospital_pass
DB_HOST=localhost
DB_PORT=5432
```

### PostgreSQL Setup (Production)
1. Install PostgreSQL
2. Create database and user:
```sql
CREATE DATABASE hospital_db;
CREATE USER hospital_user WITH PASSWORD 'hospital_pass';
GRANT ALL PRIVILEGES ON DATABASE hospital_db TO hospital_user;
```
3. Update .env file with PostgreSQL settings
4. Run migrations: `python manage.py migrate`

## 🐳 Docker Deployment

### Development
```bash
cd hospital_system
docker-compose up --build
```

### Production
```bash
cd hospital_system
docker-compose -f docker-compose.prod.yml up --build
```

## 📱 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

### Patients
- `GET /api/patients/` - List patients
- `POST /api/patients/` - Create patient
- `GET /api/patients/{id}/` - Get patient details
- `PUT /api/patients/{id}/` - Update patient
- `DELETE /api/patients/{id}/` - Delete patient

### Appointments
- `GET /api/appointments/` - List appointments
- `POST /api/appointments/` - Create appointment
- `GET /api/appointments/{id}/` - Get appointment details
- `PUT /api/appointments/{id}/` - Update appointment
- `DELETE /api/appointments/{id}/` - Delete appointment

### Medical Records
- `GET /api/medical-records/` - List medical records
- `POST /api/medical-records/` - Create medical record
- `GET /api/patients/{id}/medical-records/` - Patient's medical records

### Users
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create user (admin only)
- `GET /api/users/{id}/` - Get user details

## 👥 User Roles and Permissions

### Admin
- Full access to all features
- User management
- System configuration

### Doctor
- Patient management
- Medical records
- Appointments
- View user information

### Nurse
- Patient management
- Appointments
- Limited medical records access

### Receptionist
- Patient registration
- Appointment scheduling
- Basic patient information

## 🔒 Security Features

- **Authentication**: Token-based authentication
- **Authorization**: Role-based access control
- **CORS**: Configured for frontend access
- **Input Validation**: Comprehensive data validation
- **Security Headers**: Production security settings
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Automatic escaping and validation

## 📊 Testing

### API Testing
Use the provided Postman collection or test with curl:
```bash
# Get auth token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# Use token for authenticated requests
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Token your-token-here"
```

### Frontend Testing
1. Open http://localhost:8501
2. Login with your admin credentials
3. Test all features through the UI

## 📈 Monitoring and Logs

### Django Logs
- Development: Console output
- Production: File logging in `django.log`

### Streamlit Logs
- Console output with detailed error information

## 🔄 Backup and Maintenance

### Database Backup
```bash
# SQLite backup
cp db_dev.sqlite3 backup_$(date +%Y%m%d).sqlite3

# PostgreSQL backup
pg_dump hospital_db > backup_$(date +%Y%m%d).sql
```

### Regular Maintenance
- Update dependencies regularly
- Monitor logs for errors
- Backup database regularly
- Review user access permissions

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**
   - Change port: `python manage.py runserver 8001`
   - Or: `streamlit run hospital_app.py --server.port 8502`

2. **Database connection error**
   - Check PostgreSQL is running
   - Verify connection settings in .env
   - Use SQLite for development

3. **Frontend can't connect to API**
   - Check API_BASE_URL in frontend
   - Verify CORS settings in Django
   - Ensure Django server is running

4. **Permission denied errors**
   - Check user roles and permissions
   - Verify authentication token
   - Review API endpoint permissions

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs for error details
3. Verify configuration settings
4. Check API documentation

## 🎯 Future Enhancements

Potential improvements:
- **Real-time notifications** using WebSockets
- **Advanced reporting** with charts and analytics
- **Mobile app** using React Native or Flutter
- **Integration** with external medical systems
- **AI features** for diagnosis assistance
- **Telemedicine** capabilities
- **Electronic Health Records** (EHR) integration

## 📝 License

This project is available for educational and commercial use. Please review the specific license terms for your use case.

---

**🏥 Hospital Management System** - Built with Django REST Framework and Streamlit for modern, scalable healthcare management.