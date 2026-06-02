# Prefect Cloud Redeployment Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Prefect Cloud Redeployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "[1/2] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please ensure venv exists in snowflake-mcp-server directory" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/2] Deploying flows to Prefect Cloud..." -ForegroundColor Yellow
python deployment.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Deployment failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Redeployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://app.prefect.cloud/" -ForegroundColor White
Write-Host "2. Click 'Deployments' in the left sidebar" -ForegroundColor White
Write-Host "3. Select a deployment (e.g., 'get-customers')" -ForegroundColor White
Write-Host "4. Click 'Run' to test" -ForegroundColor White
Write-Host ""
Write-Host "Your flows should now successfully connect to Snowflake!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"

# Made with Bob
