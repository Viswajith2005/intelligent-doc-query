# Intelligent Document Query - Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Intelligent Document Query API to various platforms. The application is a FastAPI-based service that processes document queries using Azure OpenAI services.

## Prerequisites

### Required Environment Variables
Create a `.env` file in the project root with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_CHAT_API_KEY=your_chat_api_key_here
AZURE_OPENAI_CHAT_ENDPOINT=https://your-resource.openai.azure.com/

AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_EMBEDDING_API_KEY=your_embedding_api_key_here
AZURE_OPENAI_EMBEDDING_ENDPOINT=https://your-resource.openai.azure.com/

# Optional: Team Token for API Authentication
TEAM_TOKEN=acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
```

### System Requirements
- Python 3.11 or higher
- Docker (for containerized deployment)
- Git

## Deployment Options

### 1. Local Development Deployment

#### Option A: Direct Python Execution
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (create .env file)
# Copy the .env template above and fill in your Azure OpenAI credentials

# 5. Run the application
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option B: Using Docker Compose (Recommended for Development)
```bash
# 1. Build and run with Docker Compose
docker-compose up --build

# 2. Access the application
# API: http://localhost:8000
# Documentation: http://localhost:8000/docs
```

### 2. Production Deployment

#### Option A: Docker Deployment

1. **Build the Docker Image**
```bash
docker build -t intelligent-doc-query:latest .
```

2. **Run the Container**
```bash
docker run -d \
  --name doc-query-app \
  -p 8000:8000 \
  --env-file .env \
  intelligent-doc-query:latest
```

3. **Verify Deployment**
```bash
# Check if container is running
docker ps

# Test the API
curl http://localhost:8000/api/v1/health
```

#### Option B: Azure Container Instances

1. **Build and Push to Azure Container Registry**
```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name doc-query-rg --location eastus

# Create container registry
az acr create --resource-group doc-query-rg --name docqueryregistry --sku Basic

# Login to ACR
az acr login --name docqueryregistry

# Build and push image
docker build -t docqueryregistry.azurecr.io/intelligent-doc-query:latest .
docker push docqueryregistry.azurecr.io/intelligent-doc-query:latest
```

2. **Deploy to Azure Container Instances**
```bash
az container create \
  --resource-group doc-query-rg \
  --name doc-query-container \
  --image docqueryregistry.azurecr.io/intelligent-doc-query:latest \
  --dns-name-label doc-query-app \
  --ports 8000 \
  --environment-variables \
    AZURE_OPENAI_CHAT_API_KEY=your_key \
    AZURE_OPENAI_CHAT_ENDPOINT=your_endpoint \
    AZURE_OPENAI_EMBEDDING_API_KEY=your_key \
    AZURE_OPENAI_EMBEDDING_ENDPOINT=your_endpoint
```

#### Option C: Azure App Service

1. **Prepare for Azure App Service**
```bash
# Create a startup command file
echo "uvicorn app.main:app --host 0.0.0.0 --port 8000" > startup.sh
```

2. **Deploy using Azure CLI**
```bash
# Create App Service plan
az appservice plan create --name doc-query-plan --resource-group doc-query-rg --sku B1

# Create web app
az webapp create --name doc-query-app --resource-group doc-query-rg --plan doc-query-plan --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set --name doc-query-app --resource-group doc-query-rg --settings \
  AZURE_OPENAI_CHAT_API_KEY=your_key \
  AZURE_OPENAI_CHAT_ENDPOINT=your_endpoint \
  AZURE_OPENAI_EMBEDDING_API_KEY=your_key \
  AZURE_OPENAI_EMBEDDING_ENDPOINT=your_endpoint

# Deploy from local directory
az webapp deployment source config-local-git --name doc-query-app --resource-group doc-query-rg
```

#### Option D: Fly.io Deployment

1. **Install Fly CLI**
```bash
# Download and install Fly CLI from https://fly.io/docs/hands-on/install-flyctl/
```

2. **Deploy to Fly.io**
```bash
# Login to Fly
fly auth login

# Launch the app
fly launch

# Set secrets
fly secrets set AZURE_OPENAI_CHAT_API_KEY=your_key
fly secrets set AZURE_OPENAI_CHAT_ENDPOINT=your_endpoint
fly secrets set AZURE_OPENAI_EMBEDDING_API_KEY=your_key
fly secrets set AZURE_OPENAI_EMBEDDING_ENDPOINT=your_endpoint

# Deploy
fly deploy
```

### 3. Kubernetes Deployment

1. **Create Kubernetes Manifests**

Create `k8s-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intelligent-doc-query
spec:
  replicas: 3
  selector:
    matchLabels:
      app: intelligent-doc-query
  template:
    metadata:
      labels:
        app: intelligent-doc-query
    spec:
      containers:
      - name: app
        image: intelligent-doc-query:latest
        ports:
        - containerPort: 8000
        env:
        - name: AZURE_OPENAI_CHAT_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-openai-secret
              key: chat-api-key
        - name: AZURE_OPENAI_CHAT_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: azure-openai-secret
              key: chat-endpoint
        - name: AZURE_OPENAI_EMBEDDING_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-openai-secret
              key: embedding-api-key
        - name: AZURE_OPENAI_EMBEDDING_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: azure-openai-secret
              key: embedding-endpoint
---
apiVersion: v1
kind: Service
metadata:
  name: intelligent-doc-query-service
spec:
  selector:
    app: intelligent-doc-query
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

2. **Deploy to Kubernetes**
```bash
# Create secrets
kubectl create secret generic azure-openai-secret \
  --from-literal=chat-api-key=your_key \
  --from-literal=chat-endpoint=your_endpoint \
  --from-literal=embedding-api-key=your_key \
  --from-literal=embedding-endpoint=your_endpoint

# Apply deployment
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

## API Endpoints

### Health Check
- **GET** `/api/v1/health` - Health check endpoint

### Main Query Endpoint
- **POST** `/api/v1/hackrx/run` - Process document queries
  - Requires Bearer token authentication
  - Request body: `{"documents": "url", "questions": ["question1", "question2"]}`

### Legacy Endpoint
- **POST** `/query/` - Legacy document query endpoint (for testing)

## Testing the Deployment

### 1. Health Check
```bash
curl http://your-deployment-url/api/v1/health
```

### 2. API Documentation
Visit `http://your-deployment-url/docs` for interactive API documentation.

### 3. Test Query
```bash
curl -X POST "http://your-deployment-url/api/v1/hackrx/run" \
  -H "Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/sample-document.pdf",
    "questions": ["What is the main topic of this document?"]
  }'
```

## Monitoring and Logging

### 1. Application Logs
```bash
# Docker logs
docker logs doc-query-app

# Kubernetes logs
kubectl logs -l app=intelligent-doc-query
```

### 2. Health Monitoring
- Monitor the `/api/v1/health` endpoint
- Set up alerts for response time and error rates

## Troubleshooting

### Common Issues

1. **Environment Variables Not Set**
   - Ensure all required environment variables are properly configured
   - Check `.env` file or deployment platform's environment variable settings

2. **Azure OpenAI API Issues**
   - Verify API keys and endpoints are correct
   - Check Azure OpenAI service status
   - Ensure proper network connectivity

3. **Memory Issues**
   - The application uses sentence transformers which can be memory-intensive
   - Consider increasing container memory limits for production deployments

4. **Port Conflicts**
   - Ensure port 8000 is available or change the port in deployment configuration

### Debug Mode
For debugging, run the application with debug logging:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## Security Considerations

1. **API Key Management**
   - Use secure secret management in production
   - Rotate API keys regularly
   - Never commit API keys to version control

2. **Network Security**
   - Use HTTPS in production
   - Configure proper firewall rules
   - Consider using a reverse proxy (nginx) for additional security

3. **Authentication**
   - The application uses Bearer token authentication
   - Consider implementing additional security measures for production use

## Performance Optimization

1. **Resource Allocation**
   - Allocate sufficient CPU and memory for the application
   - Monitor resource usage and scale accordingly

2. **Caching**
   - Consider implementing Redis for caching embeddings
   - Cache frequently accessed documents

3. **Load Balancing**
   - Use multiple instances behind a load balancer
   - Configure health checks and auto-scaling

## Cost Optimization

1. **Azure OpenAI Usage**
   - Monitor API usage and costs
   - Consider using different model tiers based on requirements
   - Implement request rate limiting

2. **Infrastructure Costs**
   - Choose appropriate instance sizes
   - Use spot instances where possible
   - Implement auto-scaling based on demand

## Support and Maintenance

1. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Update Docker images regularly

2. **Backup and Recovery**
   - Implement backup strategies for configuration
   - Document recovery procedures
   - Test disaster recovery scenarios

---

For additional support or questions, refer to the project documentation or create an issue in the repository. 