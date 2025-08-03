# Quick Deployment Reference

## 🚀 Fastest Way to Deploy

### 1. Setup Environment Variables
Create a `.env` file in the project root:
```env
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_CHAT_API_KEY=your_chat_api_key_here
AZURE_OPENAI_CHAT_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_EMBEDDING_API_KEY=your_embedding_api_key_here
AZURE_OPENAI_EMBEDDING_ENDPOINT=https://your-resource.openai.azure.com/
TEAM_TOKEN=acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
```

### 2. Deploy Using Scripts

#### Windows:
```cmd
deploy.bat docker-compose
```

#### Linux/Mac:
```bash
./deploy.sh docker-compose
```

### 3. Access Your Application
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🔧 Manual Deployment Options

### Local Python Development
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker (Production Ready)
```bash
docker build -t intelligent-doc-query:latest .
docker run -d --name doc-query-app -p 8000:8000 --env-file .env intelligent-doc-query:latest
```

### Docker Compose (Recommended)
```bash
docker-compose up --build -d
```

## 🧪 Test Your Deployment

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Test Query
```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/sample-document.pdf",
    "questions": ["What is the main topic of this document?"]
  }'
```

## 📋 Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Docker installed (for containerized deployment)
- [ ] Azure OpenAI API credentials configured
- [ ] `.env` file created with proper credentials
- [ ] Port 8000 available

## 🚨 Common Issues

1. **Port 8000 in use**: Change port in deployment command
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **Docker not running**: Start Docker Desktop
4. **Invalid API keys**: Check your Azure OpenAI configuration

## 📖 Full Documentation
See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions including:
- Azure Container Instances
- Azure App Service
- Kubernetes
- Fly.io
- Production optimization
- Security considerations 