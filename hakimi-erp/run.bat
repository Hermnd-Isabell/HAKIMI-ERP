@echo off
echo ====================================================
echo   HAKIMI-ERP: UNIFIED STARTUP SCRIPT
echo ====================================================

:: Detect current directory
set BASE_DIR=%~dp0
cd /d %BASE_DIR%

echo [1/2] Starting Backend (FastAPI)...
start "HAKIMI-BACKEND" cmd /k "cd backend && (if exist venv\Scripts\activate (call venv\Scripts\activate) else (echo Virtual env not found, using global python)) && python main.py"

echo [2/2] Starting Frontend (Vue 3 / Vite)...
start "HAKIMI-FRONTEND" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================================
echo   Backend and Frontend are starting in separate windows.
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:5173
echo ====================================================
pause
