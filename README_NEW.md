# Hospital Management System

## Student Project - Software Architecture Course

This is my final project for Software Architecture at University Ca'Foscari. I built a web-based hospital management system to learn about API design, database relationships, and modern deployment practices.

**Time spent**: ~1 month  
**Main goal**: Learn how to build a real full-stack application

## The Problem I'm Solving

Hospitals have tons of paperwork and scheduling chaos. My system lets:
- **Patients**: View their records and book appointments
- **Doctors**: Manage patient records and schedules  
- **Admin**: Add new patients and oversee everything

## What I Built With

- **Backend**: Django (familiar from class) + PostgreSQL
- **Frontend**: Streamlit (quick to build, focuses on backend learning)
- **Deploy**: Docker (took forever to understand, but now it's magic!)
- **API**: REST endpoints with proper authentication

## How to Run It

See [`SETUP.md`](SETUP.md) for detailed instructions.

**TL;DR**: 
```bash
docker-compose -f docker-compose.dev.yml up -d
```
Then open http://localhost:8501

## Features That Work

- **User Authentication**: Different roles (admin/doctor/patient)
- **Patient Management**: Add, view, edit patient records
- **Appointments**: Book and manage appointments
- **Security**: Token-based API auth, role-based permissions
- **API**: RESTful endpoints tested with Postman

## How It Performed

- **Speed**: API responds in ~150ms
- **Load**: Tested with 50+ users simultaneously  
- **Deploy**: Sets up in under 5 minutes with Docker
- **Security**: Role-based access working properly

## What I Learned

- **API Design**: How to structure REST endpoints that make sense
- **Database**: PostgreSQL relationships and migrations
- **Security**: Authentication, authorization, input validation
- **Docker**: Container deployment (confusing at first!)
- **Architecture**: Separating frontend, API, and database layers

## Project Structure

```
├── hospital_system/     # Django backend (main logic)
├── frontend/           # Streamlit UI
├── docker-compose.yml  # Production deployment
├── SETUP.md           # How to run everything
└── PROJECT_NOTES.md   # My development notes
```

## What I'd Improve

- **Frontend**: Learn React for a better user interface
- **Testing**: Add more unit tests (I added them later, should've started with them)
- **Features**: Email notifications, mobile app
- **Performance**: Caching for better speed

## Documentation

- [`SETUP.md`](SETUP.md) - How to run the project
- [`PROJECT_NOTES.md`](PROJECT_NOTES.md) - My development notes and decisions
- `Hospital_System_API.postman_collection.json` - API testing collection

---

** Final thoughts**: This was my first real full-stack project with proper architecture. Started knowing almost nothing about APIs and Docker, now I have something that actually works and can be deployed anywhere. Pretty proud of what I learned in just one month!

**University Ca'Foscari | Computer Science | Software Architecture Course**
