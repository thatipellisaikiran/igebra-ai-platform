@echo off
echo ===================================================
echo Running GapFinder AI - Automated Test Suite
echo ===================================================
python "%~dp0backend\run_tests.py"
echo.
echo ===================================================
echo Running GapFinder AI - End-to-End Pipeline Check
echo ===================================================
python "%~dp0backend\test_pipeline.py"
pause

