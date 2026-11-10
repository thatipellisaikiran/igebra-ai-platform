@echo off
echo ===================================================
echo Starting GapFinder AI - FastAPI Backend Server
echo ===================================================
cd backend
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Virtual environment not found. Using system Python...
    python -m uvicorn app.main:app --reload --port 8000
) else (
    call venv\Scripts\activate.bat
    python -m uvicorn app.main:app --reload --port 8000
)
pause

