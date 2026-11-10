@echo off
echo ===================================================
echo Starting GapFinder AI - React Frontend
echo ===================================================
cd frontend
if not exist "node_modules\" (
    echo [INFO] Installing node dependencies...
    call npm install
)
call npm run dev
pause

