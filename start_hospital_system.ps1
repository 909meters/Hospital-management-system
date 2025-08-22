# Hospital Management System - PowerShell Startup Script

Write-Host "==================================================" -ForegroundColor Blue
Write-Host "🏥 Hospital Management System - Quick Start" -ForegroundColor Blue
Write-Host "==================================================" -ForegroundColor Blue

$projectPath = "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system"
Set-Location $projectPath

Write-Host ""
Write-Host "📦 Setting up virtual environment..." -ForegroundColor Yellow

if (-not (Test-Path "envir")) {
    python -m venv envir
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "$projectPath\envir\Scripts\Activate.ps1"

Write-Host ""
Write-Host "📥 Installing backend dependencies..." -ForegroundColor Yellow
Set-Location "$projectPath\hospital_system"
pip install -r requirements.txt

Write-Host ""
Write-Host "🗄️ Setting up database..." -ForegroundColor Yellow
python manage.py migrate --settings=hospital_system.settings_local

Write-Host ""
Write-Host "📥 Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location "$projectPath\frontend"
pip install -r requirements.txt

Write-Host ""
Write-Host "🚀 Starting services..." -ForegroundColor Yellow

Write-Host ""
Write-Host "Starting Django backend..." -ForegroundColor Cyan
$backendJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\hospital_system"
    & "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\envir\Scripts\python.exe" manage.py runserver --settings=hospital_system.settings_local
}

Write-Host "Waiting 5 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep 5

Write-Host ""
Write-Host "Starting Streamlit frontend..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\frontend"
    & "c:\Users\kuatk\PythonProjects\software_architecture\Project\Hospital-management-system\envir\Scripts\streamlit.exe" run hospital_app.py
}

Write-Host ""
Write-Host "✅ Services are starting!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Access your application at:" -ForegroundColor Cyan
Write-Host "  - Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  - Frontend UI: http://localhost:8501" -ForegroundColor White
Write-Host "  - Admin Panel: http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
Write-Host "  - Backend Job ID: $($backendJob.Id)" -ForegroundColor White
Write-Host "  - Frontend Job ID: $($frontendJob.Id)" -ForegroundColor White
Write-Host ""
Write-Host "💡 To stop services, use:" -ForegroundColor Yellow
Write-Host "  Stop-Job $($backendJob.Id); Stop-Job $($frontendJob.Id)" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to continue monitoring or Ctrl+C to exit..." -ForegroundColor Gray
Read-Host

# Keep monitoring jobs
while ($true) {
    $backendState = (Get-Job $backendJob.Id).State
    $frontendState = (Get-Job $frontendJob.Id).State
    
    Write-Host "Backend: $backendState | Frontend: $frontendState" -ForegroundColor Green
    
    if ($backendState -eq "Failed" -or $frontendState -eq "Failed") {
        Write-Host "One or more services failed. Check the logs." -ForegroundColor Red
        break
    }
    
    Start-Sleep 10
}
