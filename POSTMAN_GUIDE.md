# Hospital Management System API Guide for Postman

## Setting up Environment in Postman

### 1. Creating Environment
1. Open Postman
2. Click on "Environments" in the left panel
3. Click "Create Environment"
4. Name it "Hospital System"
5. Add the following variables:
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: (leave empty, will be filled automatically)

### 2. Getting Authentication Token

#### Endpoint: POST `/api/auth/login/`
**Description**: Get authentication token

**Headers**:
```
Content-Type: application/json
```

**Body (JSON)**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Example Response**:
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "username": "doctor_ivanov",
    "email": "ivanov@hospital.com",
    "role": "doctor",
    "first_name": "Ivan",
    "last_name": "Ivanov"
}
```

#### Automatic Token Saving
In the "Tests" section, add the following script to automatically save the token:
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set("token", response.token);
    console.log("Token saved:", response.token);
}
```

### 3. Setting up Authorization for Other Requests

For all protected endpoints, add to Headers:
```
Authorization: Token {{token}}
```

## Main API Endpoints

### Authentication

#### 1. Login
- **POST** `{{base_url}}/api/auth/login/`
- **Body**: `{"username": "user", "password": "pass"}`

#### 2. Logout
- **POST** `{{base_url}}/api/auth/logout/`
- **Headers**: `Authorization: Token {{token}}`

#### 3. User Profile
- **GET** `{{base_url}}/api/auth/profile/`
- **Headers**: `Authorization: Token {{token}}`

### Patients

#### 1. Patient List
- **GET** `{{base_url}}/api/patients/`
- **Headers**: `Authorization: Token {{token}}`

#### 2. Create Patient
- **POST** `{{base_url}}/api/patients/`
- **Headers**: `Authorization: Token {{token}}`
- **Body**:
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1985-03-15",
    "phone_number": "+1 (555) 123-45-67",
    "email": "john.doe@email.com",
    "address": "123 Main St, New York, NY 10001"
}
```

#### 3. Get Specific Patient
- **GET** `{{base_url}}/api/patients/{id}/`
- **Headers**: `Authorization: Token {{token}}`

#### 4. Update Patient
- **PUT** `{{base_url}}/api/patients/{id}/`
- **Headers**: `Authorization: Token {{token}}`

#### 5. Delete Patient
- **DELETE** `{{base_url}}/api/patients/{id}/`
- **Headers**: `Authorization: Token {{token}}`

### Users

#### 1. User List
- **GET** `{{base_url}}/api/users/`
- **Headers**: `Authorization: Token {{token}}`

#### 2. Create User
- **POST** `{{base_url}}/api/users/`
- **Headers**: `Authorization: Token {{token}}`
- **Body**:
```json
{
    "username": "new_doctor",
    "email": "doctor@hospital.com",
    "password": "secure_password",
    "first_name": "Anna",
    "last_name": "Smith",
    "role": "doctor"
}
```

### Scheduling

#### 1. Appointment List
- **GET** `{{base_url}}/api/scheduling/appointments/`
- **Headers**: `Authorization: Token {{token}}`

#### 2. Create Appointment
- **POST** `{{base_url}}/api/scheduling/appointments/`
- **Headers**: `Authorization: Token {{token}}`
- **Body**:
```json
{
    "patient": 1,
    "doctor": 2,
    "appointment_date": "2025-08-25",
    "appointment_time": "14:30:00",
    "notes": "Regular checkup"
}
```

## Filtering and Search

### Patients
- By first name: `{{base_url}}/api/patients/?first_name=John`
- By last name: `{{base_url}}/api/patients/?last_name=Doe`
- By phone: `{{base_url}}/api/patients/?phone_number=+1555`

### Appointments
- By date: `{{base_url}}/api/scheduling/appointments/?appointment_date=2025-08-25`
- By doctor: `{{base_url}}/api/scheduling/appointments/?doctor=2`
- By patient: `{{base_url}}/api/scheduling/appointments/?patient=1`

## Response Codes

- `200 OK` - Successful request
- `201 Created` - Resource created
- `400 Bad Request` - Data error
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Examples

### Invalid Authentication Data
```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```

### Missing Token
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token
```json
{
    "detail": "Invalid token."
}
```

## Useful Django Commands

To create tokens for existing users:
```bash
python manage.py create_tokens
```

To create superuser:
```bash
python manage.py createsuperuser
```

To apply migrations:
```bash
python manage.py migrate
```
