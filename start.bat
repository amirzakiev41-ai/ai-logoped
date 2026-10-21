
@echo off
cd /d "%~dp0"

echo Starting backend...
start "Backend" cmd /k "cd /d backend && .venv\Scripts\python.exe -m uvicorn main:app --reload --app-dir src"

echo Starting frontend...
start "Frontend" cmd /k "npm.cmd run dev"

echo Both servers are starting...
