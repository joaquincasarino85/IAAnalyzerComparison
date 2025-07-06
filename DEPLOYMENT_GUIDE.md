# 🚀 Railway Deployment Guide

## 📋 Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **API Keys**: Make sure you have all the required API keys:
   - OpenAI API Key
   - Anthropic API Key (Claude)
   - Google AI API Key (Gemini)
   - Cohere API Key
   - Perplexity API Key

## 🗄️ Step 1: Set up PostgreSQL Database

1. **Create Railway Project**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

2. **Add PostgreSQL Service**:
   - Click "New Service" → "Database" → "PostgreSQL"
   - Railway will automatically create a PostgreSQL database
   - Note the connection details (you'll need them later)

3. **Get Database URL**:
   - Go to your PostgreSQL service
   - Click "Connect" tab
   - Copy the "Postgres Connection URL"

## 🔧 Step 2: Deploy Backend

1. **Create Backend Service**:
   - In your Railway project, click "New Service"
   - Select "GitHub Repo"
   - Choose your repository
   - Railway will detect the Dockerfile and deploy

2. **Configure Environment Variables**:
   - Go to your backend service
   - Click "Variables" tab
   - Add the following variables:

```env
# Database
DATABASE_URL=your_postgres_connection_url_from_step_1

# AI API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_AI_API_KEY=your_google_ai_api_key
COHERE_API_KEY=your_cohere_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key

# App Settings
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-domain.railway.app
```

3. **Deploy Backend**:
   - Railway will automatically build and deploy your backend
   - Wait for the deployment to complete
   - Note the generated URL (e.g., `https://your-backend.railway.app`)

## 🎨 Step 3: Deploy Frontend

1. **Create Frontend Service**:
   - In your Railway project, click "New Service"
   - Select "GitHub Repo"
   - Choose your repository
   - Set the **Root Directory** to `react-frontend`

2. **Configure Frontend Environment**:
   - Go to your frontend service
   - Click "Variables" tab
   - Add the backend URL:

```env
VITE_API_URL=https://your-backend.railway.app
```

3. **Deploy Frontend**:
   - Railway will build and deploy your React app
   - Wait for deployment to complete
   - Note the frontend URL

## 🔗 Step 4: Connect Services

1. **Update CORS Settings**:
   - In your backend service variables, update:
   ```env
   CORS_ORIGINS=https://your-frontend-domain.railway.app
   ```

2. **Update Frontend API URL**:
   - In your frontend service variables, ensure:
   ```env
   VITE_API_URL=https://your-backend-domain.railway.app
   ```

## 🧪 Step 5: Test Your Deployment

1. **Test Backend**:
   - Visit `https://your-backend.railway.app/health`
   - Should return a health status

2. **Test Frontend**:
   - Visit your frontend URL
   - Try submitting a question
   - Check if it connects to the backend

## 🔧 Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check Railway logs for error messages
   - Ensure all dependencies are in requirements.txt
   - Verify Dockerfile syntax

2. **Database Connection Issues**:
   - Verify DATABASE_URL is correct
   - Check if PostgreSQL service is running
   - Ensure database migrations run

3. **CORS Errors**:
   - Update CORS_ORIGINS with correct frontend URL
   - Restart backend service after variable changes

4. **API Key Issues**:
   - Verify all API keys are valid
   - Check API key permissions
   - Ensure keys are properly formatted

### Useful Commands:

```bash
# Check Railway CLI (optional)
npm install -g @railway/cli
railway login
railway status

# View logs
railway logs

# Redeploy
railway up
```

## 📊 Monitoring

1. **Railway Dashboard**:
   - Monitor service health
   - View logs in real-time
   - Check resource usage

2. **Custom Domain** (Optional):
   - Go to your service settings
   - Add custom domain
   - Configure DNS records

## 💰 Cost Optimization

- Railway offers free tier with limitations
- Monitor usage in Railway dashboard
- Consider upgrading for production use

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your main branch. To disable:
- Go to service settings
- Toggle "Auto Deploy" off

---

## 🎉 Success!

Your IAAnalyzerComparator is now deployed on Railway! 

**Next Steps:**
1. Test all AI integrations
2. Monitor performance
3. Set up custom domain (optional)
4. Configure monitoring alerts 