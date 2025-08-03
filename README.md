# Intelligent Document Query API

A FastAPI-based intelligent document query system powered by Azure OpenAI services. This application processes documents and answers questions using advanced LLM capabilities.

## 🚀 Features

- **Document Processing**: Supports PDF document upload and processing
- **Intelligent Querying**: Uses Azure OpenAI GPT-4 for intelligent question answering
- **Vector Search**: Implements semantic search using embeddings
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **Authentication**: Bearer token-based API security
- **Health Monitoring**: Built-in health check endpoints

## 📋 Prerequisites

- Python 3.11+
- Azure OpenAI API credentials
- Docker (for containerized deployment)

## 🔧 Environment Variables

Create a `.env` file in the project root:

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

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd intelligent-doc-query
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the .env template and fill in your Azure OpenAI credentials
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/v1/health

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   docker build -t intelligent-doc-query .
   docker run -d --name doc-query-app -p 8000:8000 --env-file .env intelligent-doc-query
   ```

2. **Or use Docker Compose**
   ```bash
   docker-compose up --build -d
   ```

## 📚 API Endpoints

### Health Check
- **GET** `/api/v1/health` - Health check endpoint

### Main Query Endpoint
- **POST** `/api/v1/hackrx/run` - Process document queries
  - Requires Bearer token authentication
  - Request body: `{"documents": "url", "questions": ["question1", "question2"]}`

### Legacy Endpoint
- **POST** `/query/` - Legacy document query endpoint (for testing)

## 🧪 Testing

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

## 🚀 Deployment

### Render Deployment

1. **Fork/Clone this repository to your GitHub account**

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login
   - Click "New +" → "Web Service"

3. **Configure the service**
   - **Name**: `intelligent-doc-query`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - `AZURE_OPENAI_CHAT_API_KEY`: Your Azure OpenAI chat API key
   - `AZURE_OPENAI_CHAT_ENDPOINT`: Your Azure OpenAI chat endpoint
   - `AZURE_OPENAI_EMBEDDING_API_KEY`: Your Azure OpenAI embedding API key
   - `AZURE_OPENAI_EMBEDDING_ENDPOINT`: Your Azure OpenAI embedding endpoint
   - `AZURE_OPENAI_CHAT_DEPLOYMENT`: `gpt-4`
   - `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`: `text-embedding-3-large`
   - `TEAM_TOKEN`: `acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### GitHub Actions (Optional)

The repository includes GitHub Actions for automated testing and deployment.

## 📁 Project Structure

```
intelligent-doc-query/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── data/
│   └── uploads/             # Uploaded files
├── tests/                   # Test files
├── deployment/              # Deployment configs
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose
├── requirements.txt        # Python dependencies
└── render.yaml            # Render configuration
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_CHAT_API_KEY` | Azure OpenAI Chat API Key | Yes |
| `AZURE_OPENAI_CHAT_ENDPOINT` | Azure OpenAI Chat Endpoint | Yes |
| `AZURE_OPENAI_EMBEDDING_API_KEY` | Azure OpenAI Embedding API Key | Yes |
| `AZURE_OPENAI_EMBEDDING_ENDPOINT` | Azure OpenAI Embedding Endpoint | Yes |
| `AZURE_OPENAI_CHAT_DEPLOYMENT` | Chat model deployment name | No (default: gpt-4) |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model deployment name | No (default: text-embedding-3-large) |
| `TEAM_TOKEN` | API authentication token | No (default: provided) |

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black app/
isort app/
```

### Type Checking
```bash
mypy app/
```

## 📊 Monitoring

- **Health Check**: Monitor `/api/v1/health` endpoint
- **Logs**: Check application logs for errors
- **Performance**: Monitor response times and memory usage

## 🔒 Security

- API uses Bearer token authentication
- Environment variables for sensitive data
- Input validation with Pydantic models
- Error handling without exposing sensitive information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation at `/docs` endpoint
2. Review the health check endpoint
3. Check application logs
4. Create an issue in the repository

---

**Note**: Make sure to configure your Azure OpenAI credentials before deploying or running the application.
