@echo off
echo ========================================
echo PES Pakistan Web Application Setup
echo ========================================
echo.

echo [1/5] Creating Python virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment. Please ensure Python 3.10+ is installed.
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b 1
)

echo [4/5] Setting up frontend...
cd ..\pes-frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies. Please ensure Node.js is installed.
    pause
    exit /b 1
)

echo [5/5] Building frontend...
call npm run build
if errorlevel 1 (
    echo ERROR: Failed to build frontend.
    pause
    exit /b 1
)

echo Copying frontend files to Flask static directory...
xcopy /E /I /Y dist\* ..\pes-app\src\static\

cd ..\pes-app

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the application:
echo 1. Run: python src/main.py
echo 2. Open browser to: http://localhost:5000
echo 3. Login with: admin@pes.com / admin123
echo.
echo Press any key to start the application now...
pause > nul

echo Starting PES Pakistan Web Application...
python src/main.py

