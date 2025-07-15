@echo off
setlocal

:: Check if python is installed
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed.
    goto run_script
)

echo Python not found. Downloading and installing...

:: Set temp download path
set "PY_INSTALLER=%TEMP%\python_installer.exe"

:: Download latest Python installer (Windows x64)
curl -o "%PY_INSTALLER%" https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe

:: Install silently with Add to PATH
"%PY_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Clean up
del "%PY_INSTALLER%"

:: Wait for install to finish
echo Waiting for Python installation to complete...

:checkpython
timeout /t 2 >nul
python --version >nul 2>&1
if errorlevel 1 (
    goto checkpython
)

echo clearing screen..
timeout /t 3 >nul
cls

:run_script
echo Running run.py...
python assets/run.py

pause
