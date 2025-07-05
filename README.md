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
- **📝 Summary Generation**: Automatic response synthesis

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

## 📦 Endpoints de la API

### Endpoints Básicos
- `POST /questions/` — Enviar una nueva pregunta
- `GET /questions/` — Obtener historial de preguntas
- `GET /responses/by-question/{id}` — Obtener respuestas de una pregunta
- `GET /summaries/by-question/{id}` — Obtener resumen
- `GET /similarities/by-question/{id}` — Obtener similitud textual
- `GET /semantic-similarities/by-question/{id}` — Obtener similitud semántica
- `GET /contradictions/by-question/{id}` — Detección de contradicciones NLI
- `GET /sentiments/by-question/{id}` — Análisis de sentimiento
- `GET /named-entities/by-question/{id}` — Entidades nombradas

### 🚀 Endpoints de Análisis Avanzado
- `POST /advanced-analysis/analyze-responses` — Análisis completo de respuestas
- `POST /advanced-analysis/compare-intelligently` — Comparación inteligente
- `POST /advanced-analysis/quality-assessment` — Evaluación de calidad
- `POST /advanced-analysis/consensus-analysis` — Análisis de consenso
- `POST /advanced-analysis/divergence-analysis` — Análisis de divergencias
- `GET /advanced-analysis/recommendations/{question_id}` — Recomendaciones
- `GET /advanced-analysis/detailed-comparison/{question_id}` — Comparación detallada

---

## 🎯 Casos de Uso

### 📊 Análisis Comparativo de IA
- Comparar respuestas de múltiples modelos de IA
- Identificar fortalezas y debilidades de cada modelo
- Detectar sesgos y enfoques diferentes

### 🔍 Evaluación de Calidad
- Medir la legibilidad y concisión de las respuestas
- Evaluar la estructura y organización del contenido
- Analizar el uso de vocabulario y términos técnicos

### 🎯 Detección de Consenso y Divergencia
- Identificar puntos de acuerdo entre diferentes IA
- Detectar contradicciones y enfoques únicos
- Generar recomendaciones basadas en el análisis

### 📈 Investigación y Desarrollo
- Evaluar el rendimiento de diferentes modelos de IA
- Identificar áreas de mejora para cada modelo
- Generar insights para el desarrollo de IA

---

## 🔧 Configuración Avanzada

### Personalización de Modelos
Puedes configurar qué modelos de IA usar editando `backend/services/IAManager.py`:

```python
self.ias = {
    "ChatGPT": IAFactory.create_ia("ChatGPT", os.getenv("OPENAI_API_KEY")),
    "Claude": IAFactory.create_ia("Claude", os.getenv("ANTHROPIC_API_KEY")),
    # Agregar o quitar modelos según necesites
}
```

### Métricas de Calidad Personalizadas
Modifica los pesos de las métricas en `backend/services/AdvancedResponseAnalyzer.py`:

```python
def _calculate_quality_score(self, metrics: Dict) -> float:
    # Personalizar los pesos según tus necesidades
    score = 0.0
    
    # Readability (25%)
    if metrics.get("readability", {}).get("flesch_score", 0) > 60:
        score += 0.25
    
    # Conciseness (20%)
    if metrics.get("conciseness", {}).get("content_word_ratio", 0) > 0.6:
        score += 0.20
    
    # ... más métricas
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🆘 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la documentación de la API en `/docs`
- Consulta los logs de Docker para debugging