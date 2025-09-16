# 🚀 How to Run My Project

## Quick Start (5 minutes)

### 1. Make sure Docker is running
Open Docker Desktop and wait for it to start.

### 2. Run everything
```bash
# Start everything with one command
docker-compose -f docker-compose.dev.yml up -d

# Or use the script (Windows)
.\start-docker-dev.ps1
```

### 3. Open the app
- **Main App**: http://localhost:8501
- **API**: http://localhost:8000/api/

### 4. Test accounts
- **Admin**: admin / admin123
- **Doctor**: doctor1 / doctor123  
- **Patient**: patient1 / patient123

## If something breaks

```bash
# Stop and restart
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

That's it! 🎉
