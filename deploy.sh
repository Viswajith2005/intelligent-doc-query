#!/bin/bash

# Intelligent Document Query - Deployment Script
# This script automates the deployment process for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        print_status "Creating .env template..."
        cat > .env << EOF
# Azure OpenAI Configuration
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_CHAT_API_KEY=your_chat_api_key_here
AZURE_OPENAI_CHAT_ENDPOINT=https://your-resource.openai.azure.com/

AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_EMBEDDING_API_KEY=your_embedding_api_key_here
AZURE_OPENAI_EMBEDDING_ENDPOINT=https://your-resource.openai.azure.com/

# Optional: Team Token for API Authentication
TEAM_TOKEN=acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
EOF
        print_warning "Please edit .env file with your actual Azure OpenAI credentials before deploying!"
        exit 1
    fi
}

# Function to deploy locally with Python
deploy_local_python() {
    print_status "Deploying locally with Python..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    print_status "Installing dependencies..."
    pip install -r requirements.txt
    
    # Run the application
    print_status "Starting the application..."
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    # Check if Docker is installed
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Build Docker image
    print_status "Building Docker image..."
    docker build -t intelligent-doc-query:latest .
    
    # Stop existing container if running
    if docker ps -q --filter "name=doc-query-app" | grep -q .; then
        print_status "Stopping existing container..."
        docker stop doc-query-app
        docker rm doc-query-app
    fi
    
    # Run new container
    print_status "Starting container..."
    docker run -d \
        --name doc-query-app \
        -p 8000:8000 \
        --env-file .env \
        intelligent-doc-query:latest
    
    print_success "Docker deployment completed!"
    print_status "Application is running at: http://localhost:8000"
    print_status "API Documentation: http://localhost:8000/docs"
}

# Function to deploy with Docker Compose
deploy_docker_compose() {
    print_status "Deploying with Docker Compose..."
    
    # Check if Docker Compose is installed
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Build and run with Docker Compose
    print_status "Building and starting services..."
    docker-compose up --build -d
    
    print_success "Docker Compose deployment completed!"
    print_status "Application is running at: http://localhost:8000"
    print_status "API Documentation: http://localhost:8000/docs"
}

# Function to deploy to Azure Container Instances
deploy_azure() {
    print_status "Deploying to Azure Container Instances..."
    
    # Check if Azure CLI is installed
    if ! command_exists az; then
        print_error "Azure CLI is not installed. Please install Azure CLI first."
        exit 1
    fi
    
    # Check if logged in to Azure
    if ! az account show >/dev/null 2>&1; then
        print_status "Logging in to Azure..."
        az login
    fi
    
    # Set variables
    RESOURCE_GROUP="doc-query-rg"
    LOCATION="eastus"
    ACR_NAME="docqueryregistry"
    CONTAINER_NAME="doc-query-container"
    
    # Create resource group
    print_status "Creating resource group..."
    az group create --name $RESOURCE_GROUP --location $LOCATION
    
    # Create container registry
    print_status "Creating Azure Container Registry..."
    az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
    
    # Login to ACR
    print_status "Logging in to ACR..."
    az acr login --name $ACR_NAME
    
    # Build and push image
    print_status "Building and pushing Docker image..."
    docker build -t $ACR_NAME.azurecr.io/intelligent-doc-query:latest .
    docker push $ACR_NAME.azurecr.io/intelligent-doc-query:latest
    
    # Deploy to Azure Container Instances
    print_status "Deploying to Azure Container Instances..."
    az container create \
        --resource-group $RESOURCE_GROUP \
        --name $CONTAINER_NAME \
        --image $ACR_NAME.azurecr.io/intelligent-doc-query:latest \
        --dns-name-label doc-query-app \
        --ports 8000 \
        --environment-variables \
            AZURE_OPENAI_CHAT_API_KEY=$(grep AZURE_OPENAI_CHAT_API_KEY .env | cut -d '=' -f2) \
            AZURE_OPENAI_CHAT_ENDPOINT=$(grep AZURE_OPENAI_CHAT_ENDPOINT .env | cut -d '=' -f2) \
            AZURE_OPENAI_EMBEDDING_API_KEY=$(grep AZURE_OPENAI_EMBEDDING_API_KEY .env | cut -d '=' -f2) \
            AZURE_OPENAI_EMBEDDING_ENDPOINT=$(grep AZURE_OPENAI_EMBEDDING_ENDPOINT .env | cut -d '=' -f2)
    
    print_success "Azure deployment completed!"
    print_status "Application URL: http://doc-query-app.eastus.azurecontainer.io"
}

# Function to show help
show_help() {
    echo "Intelligent Document Query - Deployment Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  local-python    Deploy locally using Python and virtual environment"
    echo "  docker          Deploy using Docker"
    echo "  docker-compose  Deploy using Docker Compose (recommended for development)"
    echo "  azure           Deploy to Azure Container Instances"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 local-python"
    echo "  $0 docker-compose"
    echo "  $0 azure"
}

# Main script
main() {
    print_status "Intelligent Document Query - Deployment Script"
    print_status "============================================="
    
    # Check environment file
    check_env_file
    
    # Parse command line arguments
    case "${1:-help}" in
        "local-python")
            deploy_local_python
            ;;
        "docker")
            deploy_docker
            ;;
        "docker-compose")
            deploy_docker_compose
            ;;
        "azure")
            deploy_azure
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@" 