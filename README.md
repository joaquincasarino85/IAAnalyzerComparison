# 🤖 IAAnalyzerComparator - Intelligent AI Response Analysis

IAAnalyzerComparator is an advanced web application that allows users to ask questions and receive responses from multiple AI models. It performs sophisticated NLP analysis, intelligent comparisons, and quality assessments to provide deep insights into responses from different AI agents.

## 🚀 Key Features

### 🤖 AI Integrations
- **ChatGPT** (OpenAI) - Conversational and detailed responses
- **Claude** (Anthropic) - Deep analysis and reasoning
- **Gemini** (Google) - Balanced and well-structured responses
- **Mistral** - Technical and precise responses
- **Cohere** - Command-based responses
- **Perplexity** - Responses with sources and references

### 📊 Advanced Response Analysis
- **🔍 Quality Analysis**: Automatic evaluation of readability, conciseness, and structure
- **📈 Quality Metrics**: Overall quality score based on multiple criteria
- **🎯 Consensus Analysis**: Detection of agreement points between different AIs
- **⚡ Divergence Analysis**: Identification of contradictions and unique approaches
- **📋 Intelligent Comparison**: Detailed analysis between AI pairs
- **💡 Recommendations**: Automatic improvement suggestions

### 🧠 Sophisticated NLP Analysis
- **🔁 Textual Similarity**: Direct content comparison
- **🧠 Semantic Similarity**: Meaning analysis using embeddings
- **⚔️ Contradiction Detection**: NLI to identify inconsistencies
- **🧾 Named Entity Recognition**: Extraction of named entities
- **❤️ Sentiment Analysis**: Emotional evaluation of responses
- **📝 Summary Generation**: Automatic response synthesis (summary is generated in the same language as the question; language detection is automatic)

### 📊 Detailed Quality Metrics
- **📖 Readability**: Flesch score, sentence and word length
- **🎯 Conciseness**: Content word ratio, redundancy
- **🏗️ Structure**: Bullet points, logical connectors, paragraphs
- **📚 Vocabulary**: Lexical diversity, technical terms, richness
- **📊 Factual Indicators**: Evidence and certainty detection
- **🎭 Confidence Indicators**: Response confidence level

## 🧱 Technology Stack

### Backend
- **FastAPI** - Modern and fast REST API
- **SQLAlchemy** - ORM for database management
- **PostgreSQL** - Robust relational database
- **Docker** - Containerization and deployment

### AI and NLP
- **Hugging Face Transformers** - BERT, RoBERTa, DistilBERT models
- **Sentence Transformers** - Semantic embeddings
- **NLTK** - Natural language processing
- **NumPy** - Numerical computation
- **Anthropic** - Claude API
- **OpenAI** - ChatGPT API
- **Google Generative AI** - Gemini API
- **Cohere** - Cohere API
- **Mistral AI** - Mistral API

### Frontend
- **React + TypeScript** - Modern and responsive interface
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool
- **Chart.js** - Data visualizations

### Deployment
- **Docker Compose** - Service orchestration
- **Nginx** - Web server and reverse proxy
- **PgAdmin** - Database administration

---

## 🐳 Setup and Deployment

### 1. Clone the repository

```bash
git clone https://github.com/joaquincasarino85/IAAnalyzerComparator
cd IAAnalyzerComparator
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys for different AI services
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GEMINI_API_KEY=your_google_api_key
MISTRAL_API_KEY=your_mistral_api_key
COHERE_API_KEY=your_cohere_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key

# Database configuration
DATABASE_URL=postgresql://user:password@localhost/ia_analyzer
```

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

This will start:
- **FastAPI Backend** (port 8000)
- **PostgreSQL Database** (port 5432)
- **PgAdmin** (port 5050)
- **React Frontend** (port 3000)

### 4. Access the application

- **Main application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PgAdmin**: http://localhost:5050

---

## 📦 API Endpoints

### Basic Endpoints
- `POST /questions/` — Submit a new question
- `GET /questions/` — Get question history
- `GET /responses/by-question/{id}` — Get responses for a question
- `GET /summaries/by-question/{id}` — Get summary
- `GET /similarities/by-question/{id}` — Get textual similarity
- `GET /semantic-similarities/by-question/{id}` — Get semantic similarity
- `GET /contradictions/by-question/{id}` — NLI contradiction detection
- `GET /sentiments/by-question/{id}` — Sentiment analysis
- `GET /named-entities/by-question/{id}` — Named entities

### 🚀 Advanced Analysis Endpoints
- `POST /advanced-analysis/analyze-responses` — Complete response analysis
- `POST /advanced-analysis/compare-intelligently` — Intelligent comparison
- `POST /advanced-analysis/quality-assessment` — Quality evaluation
- `POST /advanced-analysis/consensus-analysis` — Consensus analysis
- `POST /advanced-analysis/divergence-analysis` — Divergence analysis
- `GET /advanced-analysis/recommendations/{question_id}` — Recommendations
- `GET /advanced-analysis/detailed-comparison/{question_id}` — Detailed comparison

---

## 🎯 Use Cases

### 📊 AI Comparative Analysis
- Compare responses from multiple AI models
- Identify strengths and weaknesses of each model
- Detect biases and different approaches

### 🔍 Quality Assessment
- Measure readability and conciseness of responses
- Evaluate structure and content organization
- Analyze vocabulary usage and technical terms

### 🎯 Consensus and Divergence Detection
- Identify agreement points between different AIs
- Detect contradictions and unique approaches
- Generate recommendations based on analysis

### 📈 Research and Development
- Evaluate performance of different AI models
- Identify improvement areas for each model
- Generate insights for AI development

---

## 🔧 Advanced Configuration

### Model Customization
You can configure which AI models to use by editing `backend/services/IAManager.py`:

```python
self.ias = {
    "ChatGPT": IAFactory.create_ia("ChatGPT", os.getenv("OPENAI_API_KEY")),
    "Claude": IAFactory.create_ia("Claude", os.getenv("ANTHROPIC_API_KEY")),
    # Add or remove models as needed
}
```

### Custom Quality Metrics
Modify metric weights in `backend/services/AdvancedResponseAnalyzer.py`:

```python
def _calculate_quality_score(self, metrics: Dict) -> float:
    # Customize weights according to your needs
    score = 0.0
    
    # Readability (25%)
    if metrics.get("readability", {}).get("flesch_score", 0) > 60:
        score += 0.25
    
    # Conciseness (20%)
    if metrics.get("conciseness", {}).get("content_word_ratio", 0) > 0.6:
        score += 0.20
    
    # ... more metrics
```

---

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🆘 Support

If you have problems or questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Consult Docker logs for debugging