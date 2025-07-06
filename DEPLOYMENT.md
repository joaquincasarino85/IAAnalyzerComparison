# 🚀 Deployment Guide - IAAnalyzerComparator

## 🆓 Free Hosting Options

### 1. **Railway** (Recommended) ⭐⭐⭐⭐⭐
**Free tier**: $5 credit/month (sufficient for development)

#### Quick Setup:
1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy automatically** with Docker

#### Steps:
```bash
# 1. Push your code to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Go to Railway Dashboard
# 3. Click "New Project" → "Deploy from GitHub repo"
# 4. Select your repository
# 5. Railway will automatically detect Dockerfile and deploy
```

#### Environment Variables in Railway:
- Go to your project → Variables tab
- Add all your API keys:
  ```
  OPENAI_API_KEY=your_key
  GEMINI_API_KEY=your_key
  MISTRAL_API_KEY=your_key
  COHERE_API_KEY=your_key
  PERPLEXITY_API_KEY=your_key
  DATABASE_URL=postgresql://...
  ```

### 2. **Render** ⭐⭐⭐⭐
**Free tier**: 750 hours/month (enough for 24/7)

#### Setup:
1. **Sign up** at [render.com](https://render.com)
2. **New Web Service** → Connect GitHub
3. **Build Command**: `pip install -r backend/requirements.txt`
4. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. **Vercel** (Frontend Only) ⭐⭐⭐⭐
**Free tier**: Unlimited

#### Setup:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd react-frontend
vercel

# Or connect GitHub for auto-deploy
```

## 🐳 Docker Deployment

### Local Testing:
```bash
# Build image
docker build -t ia-analyzer .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e GEMINI_API_KEY=your_key \
  ia-analyzer
```

### Production Docker Compose:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - MISTRAL_API_KEY=${MISTRAL_API_KEY}
      - COHERE_API_KEY=${COHERE_API_KEY}
      - PERPLEXITY_API_KEY=${PERPLEXITY_API_KEY}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=ia_analyzer
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔧 Environment Variables

Create a `.env` file for local development:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/ia_analyzer

# AI API Keys
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
MISTRAL_API_KEY=sk-...
COHERE_API_KEY=sk-...
PERPLEXITY_API_KEY=pplx-...

# Optional: Claude
ANTHROPIC_API_KEY=sk-ant-...
```

## 📊 Database Setup

### Railway PostgreSQL:
1. **Add PostgreSQL** service in Railway
2. **Copy connection string** to environment variables
3. **Database will be created automatically**

### Local PostgreSQL:
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb ia_analyzer
sudo -u postgres createuser user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ia_analyzer TO user;"
```

## 🚀 Deployment Checklist

### Before Deploying:
- [ ] All API keys configured
- [ ] Database connection string ready
- [ ] Code pushed to GitHub
- [ ] Dockerfile tested locally
- [ ] Environment variables documented

### After Deploying:
- [ ] Health check endpoint working
- [ ] API endpoints responding
- [ ] Database migrations applied
- [ ] SSL certificate active
- [ ] Custom domain configured (optional)

## 🔍 Troubleshooting

### Common Issues:

1. **Port Issues**:
   ```bash
   # Railway uses $PORT environment variable
   # Make sure your app uses: os.getenv('PORT', '8000')
   ```

2. **Database Connection**:
   ```bash
   # Check DATABASE_URL format
   # Should be: postgresql://user:password@host:port/database
   ```

3. **API Key Errors**:
   ```bash
   # Verify all API keys are set in environment variables
   # Check API key formats and permissions
   ```

4. **Build Failures**:
   ```bash
   # Check Dockerfile syntax
   # Verify all dependencies in requirements.txt
   # Test build locally first
   ```

## 📈 Scaling Options

### When you outgrow free tier:

1. **Railway**: Upgrade to paid plan ($5-20/month)
2. **Render**: Upgrade to paid plan ($7/month)
3. **AWS**: Use AWS Free Tier, then pay-as-you-go
4. **Google Cloud**: Use free tier, then pay-as-you-go
5. **DigitalOcean**: $5-10/month for droplets

## 🎯 Recommended Workflow

1. **Start with Railway** (easiest)
2. **Test thoroughly** with free tier
3. **Monitor usage** and performance
4. **Scale up** when needed
5. **Consider multiple regions** for global users

## 📞 Support

- **Railway**: [Discord](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **Vercel**: [Documentation](https://vercel.com/docs)

---

**Happy Deploying! 🚀** 