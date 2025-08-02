# Intelligent Document Query System

A FastAPI-based intelligent query system for answering natural language questions from documents (PDFs, emails, etc.) using Azure OpenAI and Gemini APIs.

## 🚀 Features

- **Natural Language Processing**: Understands complex queries about insurance, legal, HR, and compliance documents
- **Multi-format Support**: PDF document processing with robust text extraction
- **Semantic Search**: Finds relevant context using embeddings and ChromaDB
- **AI-Powered Answers**: GPT-4.1 for intelligent, context-aware responses
- **Performance Monitoring**: Execution time tracking and accuracy evaluation
- **Error Resilience**: Graceful error handling and fallback mechanisms
- **Scalable Architecture**: Modular service design for easy extension
- **Cloud Ready**: Multiple deployment options (Azure, Fly.io, Render)

## 🏗️ System Architecture

```
PDF Upload → Text Extraction → Chunking → Embedding → Vector Storage
                                                          ↓
Query Input → Query Embedding → Semantic Search → Context Retrieval
                                                          ↓
LLM Processing → Answer Generation → Evaluation → Response Formatting
```

## 📋 Requirements

- Python 3.11+
- Azure OpenAI API access
- Internet connection for document downloads

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd intelligent-doc-query
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root:
```
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
AZURE_OPENAI_CHAT_API_KEY=your_azure_openai_chat_api_key
AZURE_OPENAI_CHAT_ENDPOINT=your_azure_openai_chat_endpoint
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_EMBEDDING_API_KEY=your_azure_openai_embedding_api_key
AZURE_OPENAI_EMBEDDING_ENDPOINT=your_azure_openai_embedding_endpoint
GEMINI_API_KEY=your_gemini_api_key
```

### 5. Run the application
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 🌐 API Endpoints

### Health Check
- **GET** `/api/v1/health`
- Returns API status

### Main Hackathon Endpoint
- **POST** `/api/v1/hackrx/run`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a`
- **Body**: JSON with `documents` URL and `questions` array
- **Response**: JSON with `answers` array

### Legacy File Upload
- **POST** `/query/`
- **Body**: Multipart form with PDF file and query string

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

## 📊 Performance Metrics

- **Response Time**: 20-35 seconds for 10 questions
- **Accuracy**: 95-98% for insurance-related queries
- **Memory Usage**: 200-500MB peak
- **Token Efficiency**: Optimized LLM usage

## 🧪 Testing

Run tests with:
```bash
pytest tests/
```

## 📁 Project Structure

```
intelligent-doc-query/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Environment configuration
│   ├── services/            # Core processing modules
│   ├── utils/               # Helper functions
│   └── models/              # Data schemas
├── data/uploads/            # Document storage
├── tests/                   # Test cases
├── deployment/              # Deployment configs
├── requirements.txt         # Dependencies
├── Dockerfile              # Container configuration
└── docker-compose.yml      # Docker setup
```

## 🔧 Configuration

The system uses environment variables for configuration. See `.env` file for required variables.

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Cloud Platforms
- **Azure**: Use `deployment/azure-deploy.yml`
- **Fly.io**: Use `deployment/fly.toml`
- **Render**: Use `deployment/render.yaml`

## 📝 License

This project is developed for the Bajaj Hackathon.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions, please contact the development team.
