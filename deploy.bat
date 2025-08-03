@echo off
setlocal enabledelayedexpansion

REM Intelligent Document Query - Deployment Script for Windows
REM This script automates the deployment process for different environments

echo [INFO] Intelligent Document Query - Deployment Script
echo [INFO] =============================================

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo [INFO] Creating .env template...
    (
        echo # Azure OpenAI Configuration
        echo AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
        echo AZURE_OPENAI_CHAT_API_KEY=your_chat_api_key_here
        echo AZURE_OPENAI_CHAT_ENDPOINT=https://your-resource.openai.azure.com/
        echo.
        echo AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
        echo AZURE_OPENAI_EMBEDDING_API_KEY=your_embedding_api_key_here
        echo AZURE_OPENAI_EMBEDDING_ENDPOINT=https://your-resource.openai.azure.com/
        echo.
        echo # Optional: Team Token for API Authentication
        echo TEAM_TOKEN=acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
    ) > .env
    echo [WARNING] Please edit .env file with your actual Azure OpenAI credentials before deploying!
    pause
    exit /b 1
)

REM Parse command line arguments
if "%1"=="" goto show_help
if "%1"=="help" goto show_help
if "%1"=="local-python" goto deploy_local_python
if "%1"=="docker" goto deploy_docker
if "%1"=="docker-compose" goto deploy_docker_compose
if "%1"=="azure" goto deploy_azure
goto show_help

:deploy_local_python
echo [INFO] Deploying locally with Python...
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
echo [INFO] Installing dependencies...
pip install -r requirements.txt
echo [INFO] Starting the application...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
goto end

:deploy_docker
echo [INFO] Deploying with Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)
echo [INFO] Building Docker image...
docker build -t intelligent-doc-query:latest .
echo [INFO] Stopping existing container if running...
docker stop doc-query-app >nul 2>&1
docker rm doc-query-app >nul 2>&1
echo [INFO] Starting container...
docker run -d --name doc-query-app -p 8000:8000 --env-file .env intelligent-doc-query:latest
echo [SUCCESS] Docker deployment completed!
echo [INFO] Application is running at: http://localhost:8000
echo [INFO] API Documentation: http://localhost:8000/docs
goto end

:deploy_docker_compose
echo [INFO] Deploying with Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)
echo [INFO] Building and starting services...
docker-compose up --build -d
echo [SUCCESS] Docker Compose deployment completed!
echo [INFO] Application is running at: http://localhost:8000
echo [INFO] API Documentation: http://localhost:8000/docs
goto end

:deploy_azure
echo [INFO] Deploying to Azure Container Instances...
az --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Azure CLI is not installed. Please install Azure CLI first.
    pause
    exit /b 1
)
echo [INFO] Checking Azure login status...
az account show >nul 2>&1
if errorlevel 1 (
    echo [INFO] Logging in to Azure...
    az login
)
echo [INFO] Creating resource group...
az group create --name doc-query-rg --location eastus
echo [INFO] Creating Azure Container Registry...
az acr create --resource-group doc-query-rg --name docqueryregistry --sku Basic
echo [INFO] Logging in to ACR...
az acr login --name docqueryregistry
echo [INFO] Building and pushing Docker image...
docker build -t docqueryregistry.azurecr.io/intelligent-doc-query:latest .
docker push docqueryregistry.azurecr.io/intelligent-doc-query:latest
echo [INFO] Deploying to Azure Container Instances...
az container create --resource-group doc-query-rg --name doc-query-container --image docqueryregistry.azurecr.io/intelligent-doc-query:latest --dns-name-label doc-query-app --ports 8000 --environment-variables AZURE_OPENAI_CHAT_API_KEY=%AZURE_OPENAI_CHAT_API_KEY% AZURE_OPENAI_CHAT_ENDPOINT=%AZURE_OPENAI_CHAT_ENDPOINT% AZURE_OPENAI_EMBEDDING_API_KEY=%AZURE_OPENAI_EMBEDDING_API_KEY% AZURE_OPENAI_EMBEDDING_ENDPOINT=%AZURE_OPENAI_EMBEDDING_ENDPOINT%
echo [SUCCESS] Azure deployment completed!
echo [INFO] Application URL: http://doc-query-app.eastus.azurecontainer.io
goto end

:show_help
echo Intelligent Document Query - Deployment Script
echo.
echo Usage: %0 [OPTION]
echo.
echo Options:
echo   local-python    Deploy locally using Python and virtual environment
echo   docker          Deploy using Docker
echo   docker-compose  Deploy using Docker Compose (recommended for development)
echo   azure           Deploy to Azure Container Instances
echo   help            Show this help message
echo.
echo Examples:
echo   %0 local-python
echo   %0 docker-compose
echo   %0 azure
goto end

:end
pause 