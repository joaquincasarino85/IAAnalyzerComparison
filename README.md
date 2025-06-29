# 📊 IAAnalyzerComparison

IAAnalyzerComparison is a web application that allows users to ask a question and receive responses from multiple AI models. It performs advanced NLP analysis on the answers, including similarity comparisons, contradiction detection, named entity recognition, sentiment analysis, and summary generation.

## 🚀 Features

- Ask any open-ended question related to markets or general topics.
- Compare responses from multiple AI models (e.g., ChatGPT, Gemini, etc.).
- Automatically stores all questions and answers in a PostgreSQL database.
- Computes:
  - 🔁 Textual similarity between AI responses
  - 🧠 Semantic similarity using transformer embeddings
  - ⚔️ Natural Language Inference (NLI) to detect contradictions
  - 🧾 Named Entity Recognition (NER)
  - ❤️ Sentiment Analysis
  - 📝 Summarization of all answers

## 🧱 Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: Vanilla JS + HTML + CSS
- **AI & NLP**: Hugging Face Transformers (BERT, RoBERTa, DistilBERT, etc.)
- **Deployment**: Docker + Docker Compose

---

## 🐳 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/joaquincasarino85/IAAnalyzerComparison
cd IAAnalyzerComparison

2. Run with Docker Compose
docker-compose up --build
This will:

Build the FastAPI backend (ia_backend)
Launch a PostgreSQL database (ia_db)
Start pgAdmin (ia_pgadmin)
Serve the frontend (index.html) via FastAPI
Once running, access the app at:

http://localhost:8000
PgAdmin is available at:

http://localhost:5050
Use the credentials set in docker-compose.yml to log in.

📦 API Endpoints

Some key API endpoints include:

POST /questions/ — Submit a new question
GET /questions/ — Retrieve history of asked questions
GET /responses/by-question/{id} — Get responses for a question
GET /summaries/by-question/{id} — Get summary
GET /similarities/by-question/{id} — Get textual similarity
GET /semantic-similarities/by-question/{id} — Get semantic similarity
GET /contradictions/by-question/{id} — Get NLI contradiction detection
GET /sentiments/by-question/{id} — Get sentiment analysis
GET /named-entities/by-question/{id} — Get named entities