@echo off
echo ========================================
echo Prefect Cloud Redeployment Script
echo ========================================
echo.

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please ensure venv exists in snowflake-mcp-server directory
    pause
    exit /b 1
)

echo [2/3] Uploading secrets to Prefect Cloud...
echo.
echo Please choose an option:
echo 1. Upload secrets from .env file
echo 2. List existing secrets
echo 3. Skip secret upload
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Uploading secrets...
    python -c "import asyncio; from setup_secrets import setup_secrets; asyncio.run(setup_secrets())"
    if errorlevel 1 (
        echo ERROR: Failed to upload secrets
        pause
        exit /b 1
    )
    echo.
    echo ✅ Secrets uploaded successfully!
) else if "%choice%"=="2" (
    echo.
    echo Listing existing secrets...
    python -c "import asyncio; from setup_secrets import list_secrets; asyncio.run(list_secrets())"
    echo.
    pause
) else (
    echo.
    echo Skipping secret upload...
)

echo.
echo [3/3] Deploying flows to Prefect Cloud...
python deployment.py

if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Redeployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://app.prefect.cloud/
echo 2. Click "Deployments" in the left sidebar
echo 3. Select a deployment (e.g., "get-customers")
echo 4. Click "Run" to test
echo.
echo Your flows should now successfully connect to Snowflake!
echo.
pause

@REM Made with Bob
