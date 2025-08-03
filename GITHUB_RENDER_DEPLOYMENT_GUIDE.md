# 🚀 Complete GitHub & Render Deployment Guide

## 📋 Pre-Deployment Checklist

Before starting, ensure you have:
- [ ] Azure OpenAI API credentials ready
- [ ] GitHub account
- [ ] Render account
- [ ] All project files committed locally

## 🔧 Step 1: Prepare Your Local Repository

### 1.1 Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit: Intelligent Document Query API"
```

### 1.2 Create .env.example file
```bash
# Create .env.example for reference
cat > .env.example << EOF
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
```

### 1.3 Test locally before deployment
```bash
# Test the application locally
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📤 Step 2: Push to GitHub

### 2.1 Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name: `intelligent-doc-query`
4. Description: `Intelligent Document Query API powered by Azure OpenAI`
5. Make it **Public** (for Render deployment)
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

### 2.2 Push Your Code
```bash
# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/intelligent-doc-query.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 2.3 Verify GitHub Repository
- Go to your GitHub repository
- Ensure all files are uploaded
- Check that `.env` is **NOT** in the repository (it should be in `.gitignore`)

## 🌐 Step 3: Deploy to Render

### 3.1 Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your GitHub repositories

### 3.2 Create New Web Service
1. Click "New +" button
2. Select "Web Service"
3. Connect your GitHub repository
4. Select the `intelligent-doc-query` repository

### 3.3 Configure the Service

**Basic Settings:**
- **Name**: `intelligent-doc-query`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: Leave empty (default)

**Build & Deploy Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3.4 Set Environment Variables

Click "Environment" tab and add these variables:

**Required Variables:**
```
AZURE_OPENAI_CHAT_API_KEY = your_actual_chat_api_key
AZURE_OPENAI_CHAT_ENDPOINT = your_actual_chat_endpoint
AZURE_OPENAI_EMBEDDING_API_KEY = your_actual_embedding_api_key
AZURE_OPENAI_EMBEDDING_ENDPOINT = your_actual_embedding_endpoint
```

**Optional Variables:**
```
AZURE_OPENAI_CHAT_DEPLOYMENT = gpt-4
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = text-embedding-3-large
TEAM_TOKEN = acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
```

### 3.5 Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete (usually 5-10 minutes)
3. Note your deployment URL (e.g., `https://intelligent-doc-query.onrender.com`)

## 🧪 Step 4: Test Your Deployment

### 4.1 Health Check
```bash
curl https://your-app-name.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "API is running successfully"
}
```

### 4.2 Test with Postman

**1. Health Check Request:**
- Method: `GET`
- URL: `https://your-app-name.onrender.com/api/v1/health`

**2. Main Query Request:**
- Method: `POST`
- URL: `https://your-app-name.onrender.com/api/v1/hackrx/run`
- Headers:
  ```
  Content-Type: application/json
  Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a
  ```
- Body (raw JSON):
  ```json
  {
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "questions": [
      "What is this document about?",
      "What are the main topics covered?"
    ]
  }
  ```

### 4.3 Test with cURL
```bash
# Health check
curl https://your-app-name.onrender.com/api/v1/health

# Test query
curl -X POST "https://your-app-name.onrender.com/api/v1/hackrx/run" \
  -H "Authorization: Bearer acee50b025067ece530801f7901433430fae46c00beae83921306b8503bfb39a" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "questions": ["What is this document about?"]
  }'
```

## 🔍 Step 5: Troubleshooting

### 5.1 Common Issues

**Issue: Build fails**
- Check that all files are committed to GitHub
- Verify `requirements.txt` exists and is valid
- Check Render logs for specific error messages

**Issue: Environment variables not set**
- Go to Render dashboard → Your service → Environment
- Add missing environment variables
- Redeploy the service

**Issue: Health check fails**
- Check if all Azure OpenAI credentials are correct
- Verify API endpoints are accessible
- Check Render logs for authentication errors

**Issue: API returns 401 Unauthorized**
- Verify the Bearer token is correct
- Check that `TEAM_TOKEN` environment variable is set

### 5.2 Check Logs
1. Go to Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Check for error messages

### 5.3 Redeploy if Needed
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select "Clear build cache & deploy"

## 📊 Step 6: Monitor Your Deployment

### 6.1 Render Dashboard
- Monitor service status
- Check response times
- View error logs

### 6.2 Health Monitoring
```bash
# Set up monitoring script
while true; do
  curl -s https://your-app-name.onrender.com/api/v1/health
  sleep 300  # Check every 5 minutes
done
```

### 6.3 Performance Monitoring
- Monitor Azure OpenAI API usage
- Check response times
- Monitor memory usage

## 🔄 Step 7: Continuous Deployment

### 7.1 Automatic Deployments
- Render automatically deploys when you push to `main` branch
- No additional configuration needed

### 7.2 Update Your Application
```bash
# Make changes locally
git add .
git commit -m "Update: description of changes"
git push origin main
# Render will automatically redeploy
```

## 🎯 Step 8: Production Checklist

- [ ] Health check endpoint working
- [ ] All environment variables set correctly
- [ ] API authentication working
- [ ] Document processing working
- [ ] Error handling working
- [ ] Logs accessible
- [ ] Performance acceptable
- [ ] SSL certificate working (automatic with Render)

## 📞 Support

If you encounter issues:

1. **Check Render Logs**: Go to your service → Logs
2. **Verify Environment Variables**: Ensure all Azure OpenAI credentials are correct
3. **Test Locally**: Ensure the app works locally before deploying
4. **Check GitHub**: Ensure all files are properly committed
5. **Contact Support**: Use Render's support if needed

## 🎉 Success!

Your Intelligent Document Query API is now deployed and ready to use!

**Your API URL**: `https://your-app-name.onrender.com`
**Documentation**: `https://your-app-name.onrender.com/docs`
**Health Check**: `https://your-app-name.onrender.com/api/v1/health`

---

**Remember**: Keep your Azure OpenAI API keys secure and never commit them to GitHub! 