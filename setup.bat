@echo off
setlocal

echo ========================================
echo PES Pakistan Backend Setup
echo ========================================

echo [1/3] Creating Python virtual environment...
python -m venv .venv
if errorlevel 1 exit /b 1

echo [2/3] Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 exit /b 1

echo [3/3] Installing pinned Python dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

echo.
echo Setup completed.
echo.
echo Before starting, configure SECRET_KEY with at least 32 random characters.
echo To create the first administrator, optionally configure all three variables:
echo   PES_BOOTSTRAP_ADMIN_EMAIL
 echo   PES_BOOTSTRAP_ADMIN_PASSWORD
 echo   PES_BOOTSTRAP_ADMIN_NAME
 echo Remove the bootstrap variables after the administrator is created.
echo.
echo Run verification:
echo   python -m unittest discover -s tests -v
 echo   python scripts\security_check.py
 echo.
echo Start locally:
echo   python src\main.py

endlocal
