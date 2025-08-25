# Hospital Management System - Technical Specifications

## 🎯 Project Overview

**Course**: Software Architecture  
**Program**: Computer Science and Information Technology  
**University**: Ca'Foscari Venice  
**Project Type**: Backend-oriented software solution

## 📋 Requirements Compliance Matrix

| Requirement Category | Specification | Implementation Status | Technical Details |
|---------------------|---------------|----------------------|-------------------|
| **Patient Management** | CRUD operations for EMR | ✅ Complete | Django models + REST API |
| **Authentication** | Role-based access control | ✅ Complete | Token auth + permissions |
| **Schedule Management** | Appointments + staff scheduling | ✅ Complete | Appointment model + API |
| **Search & Filter** | Multi-criteria search | ✅ Complete | Django filters + pagination |
| **Security** | HIPAA-equivalent protection | ✅ Complete | Role permissions + CORS |
| **Reliability** | Data integrity + backups | ✅ Complete | PostgreSQL + Docker volumes |
| **Deployability** | Docker containerization | ✅ Complete | Multi-container setup |
| **Scalability** | 50→500+ concurrent users | ✅ Complete | Horizontal scaling ready |

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Hospital Management System               │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer (Streamlit - Low-code Solution)            │
│  ├── Patient Interface    ├── Doctor Interface             │
│  ├── Admin Interface      └── Role-based Navigation        │
├─────────────────────────────────────────────────────────────┤
│  API Layer (Django REST Framework)                         │
│  ├── Authentication       ├── Patient Management          │
│  ├── Medical Records      ├── Appointment Scheduling       │
│  ├── User Management      └── Search & Filtering           │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer (Django Models & Services)           │
│  ├── User Roles          ├── Patient Records              │
│  ├── Medical History     ├── Appointment Logic            │
│  └── Permission System   └── Data Validation              │
├─────────────────────────────────────────────────────────────┤
│  Data Layer (PostgreSQL)                                   │
│  ├── User Management     ├── Patient Records              │
│  ├── Medical Records     ├── Appointments                 │
│  └── Audit Logs         └── System Configuration          │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Docker)                             │
│  ├── Application Container  ├── Database Container        │
│  ├── Web Server Container   └── Reverse Proxy (Nginx)     │
└─────────────────────────────────────────────────────────────┘
```

## 👥 User Role Implementation

### Patient Role
- **Capabilities**: View personal medical records, book appointments, manage profile
- **Restrictions**: Cannot access other patients' data, cannot create new patients
- **Implementation**: Role-based permissions in Django + UI restrictions

### Doctor/Nurse Role  
- **Capabilities**: Full patient management, create medical records, view schedules
- **Restrictions**: Cannot perform administrative functions, limited user management
- **Implementation**: Custom permissions class + role checking

### Administrative Staff Role
- **Capabilities**: Full system access, user management, system configuration
- **Restrictions**: None (super admin privileges)
- **Implementation**: Django admin + custom admin interface

## 📊 Performance & Load Specifications

### Current Capacity (MVP)
- **Database**: PostgreSQL optimized for 100+ concurrent connections
- **API**: Django REST Framework with pagination (20 items/page)
- **Frontend**: Streamlit with efficient API calls and caching

### Scalability Implementation
- **Horizontal Scaling**: Docker Compose supports service replication
- **Load Balancing**: Nginx reverse proxy configuration included
- **Database**: PostgreSQL connection pooling ready
- **Caching**: Redis integration prepared for future implementation

### Monitoring & Reliability
- **Health Checks**: All containers include health monitoring
- **Logging**: Structured logging for all components
- **Backup**: Automated database backups via Docker volumes
- **Recovery**: Container restart policies implemented

## 🔐 Security Implementation

### Authentication & Authorization
```python
# Token-based authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Role-based permissions
class CanViewPatients(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['DOCTOR', 'ADMIN']
```

### Data Protection
- **CORS**: Configured for secure cross-origin requests
- **SQL Injection**: Django ORM automatic protection
- **XSS Protection**: Template auto-escaping enabled
- **Input Validation**: Serializer-based validation

## 🚀 Deployment Architecture

### Development Environment
```yaml
services:
  db: postgres:15-alpine
  backend: django + development server
  frontend: streamlit development mode
```

### Production Environment  
```yaml
services:
  db: postgres:15-alpine + persistent volumes
  backend: django + gunicorn + static files
  frontend: streamlit + production config
  nginx: reverse proxy + load balancer
```

## 🏛️ Architecture Characteristics for Hospital Management System (MVP)

### 1. 🔐 Security
**Reasoning**: Handling personal medical data requires compliance with HIPAA or equivalent standards. Role-based access control ensures only authorized personnel can access specific records.

**Quantification**:
- **Data encryption**: AES-256 for storage, TLS 1.3 for transit
- **Zero tolerance**: 0 security breaches allowed
- **Access control enforcement**: ≤ 100 ms per request
- **Implementation**: Token-based authentication, role-based permissions, CORS protection

### 2. 🔧 Reliability  
**Reasoning**: Medical records and schedules must be consistently available to avoid operational disruption. Backup and recovery mechanisms are crucial.

**Quantification**:
- **Uptime**: 99.9% per month
- **Automated database backups**: Every 12 hours via Docker volumes
- **Recovery Time Objective (RTO)**: ≤ 1 hour
- **Implementation**: PostgreSQL ACID compliance, container health checks, restart policies

### 3. 🚀 Deployability
**Reasoning**: Docker-based deployment enables fast setup in hospital IT environments with varying infrastructure.

**Quantification**:
- **Deployment time**: ≤ 10 minutes for full stack
- **Environment replication**: Identical staging & production via docker-compose
- **Rollback capability**: ≤ 5 minutes with container versioning
- **Implementation**: Multi-container Docker setup, automated scripts, environment variables

### 4. 📈 Scalability
**Reasoning**: The system should handle a growing number of concurrent users without degradation, especially in larger hospitals or during emergencies.

**Quantification**:
- **MVP capacity**: Up to 50 concurrent users
- **Target scalability**: Up to 500 concurrent users with < 20% performance drop
- **Horizontal scaling**: Docker swarm/Kubernetes ready
- **Implementation**: Stateless API design, load balancing with Nginx, database connection pooling

### 5. ⚡ Performance
**Reasoning**: Quick response times are critical for usability, especially for search and record retrieval.

**Quantification**:
- **CRUD operations**: ≤ 200 ms response time under normal load
- **Search queries**: ≤ 500 ms for up to 100k records
- **Server CPU usage**: < 70% at peak load
- **Implementation**: Database indexing, pagination, efficient API design, caching ready

### 6. 🧩 Modularity
**Reasoning**: Clear separation between patient management, scheduling, and authentication modules allows independent development and testing.

**Quantification**:
- **Module separation**: Each feature as separate Django app (users, patients, scheduling)
- **Change isolation**: 80% of changes isolated to single module without affecting others
- **API independence**: RESTful endpoints with clear boundaries
- **Implementation**: Django app structure, dependency injection, clean interfaces

### 7. 🧪 Testability
**Reasoning**: Automated tests are needed for quick iteration and safe deployment.

**Quantification**:
- **Unit test coverage**: ≥ 80% for core business logic
- **Test suite execution**: ≤ 5 minutes for full test run
- **API testing**: Comprehensive Postman collection included
- **Implementation**: Django TestCase framework, API testing tools, mock data generation

## 📈 Future Enhancements

### Phase 2 Features
- Real-time notifications (WebSocket)
- Advanced reporting and analytics
- Mobile application (React Native)
- Integration with external medical systems

### Scalability Improvements
- Redis caching layer
- Microservices architecture
- Kubernetes deployment
- Auto-scaling based on load

## 🧪 Quality Assurance

### Testing Strategy
- **Unit Tests**: Django models and API endpoints
- **Integration Tests**: Full user workflows
- **Load Testing**: Concurrent user simulation
- **Security Testing**: Authentication and authorization

### Code Quality
- **Type Hints**: Python type annotations
- **Documentation**: Comprehensive API documentation
- **Code Style**: PEP 8 compliance
- **Version Control**: Git with semantic commits

## 📚 Documentation

- **[`README.md`](README.md)**: Project overview and quick start
- **[`DOCKER_README.md`](DOCKER_README.md)**: Deployment instructions
- **API Documentation**: Postman collection included
- **Code Comments**: Inline documentation for complex logic
