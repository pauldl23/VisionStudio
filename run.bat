@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo    VisionStudio | Premium Launcher
echo ==========================================
echo.

:: Clear Port 8501 to prevent conflicts with old apps
echo Cleaning up environment...
powershell -Command "Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -ErrorAction SilentlyContinue | Stop-Process -Force"

:: Find Python
set "PY_CMD=python"
python --version >nul 2>&1
if errorlevel 1 (
    set "PY_CMD=py"
    py --version >nul 2>&1
    if errorlevel 1 (
        set "PY_CMD=python3"
        python3 --version >nul 2>&1
        if errorlevel 1 (
            echo [ERROR] Python not found. Please install Python.
            pause
            exit /b 1
        )
    )
)

echo Using: !PY_CMD!
echo.

echo Checking requirements...
!PY_CMD! -m pip install streamlit pandas scikit-learn plotly joblib -q

echo Starting Dashboard...
!PY_CMD! -m streamlit run app.py --server.port 8501
pause
