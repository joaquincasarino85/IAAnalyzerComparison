from fastapi import FastAPI
from database import engine, Base
from routes import questions, responses, summaries, similarities, sentiments, contradictions, named_entities, semantic_similarity, health
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar la aplicación
app = FastAPI(title="IAAnalyzerComparison API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes (ajústalo según tu necesidad)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Incluir las rutas
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(responses.router, prefix="/responses", tags=["Responses"])
app.include_router(summaries.router, prefix="/summaries", tags=["Summaries"])
app.include_router(similarities.router, prefix="/similarities", tags=["Similarities"])

app.include_router(sentiments.router, prefix="/sentiments", tags=["sentiments"])
app.include_router(contradictions.router, prefix="/contradictions", tags=["contradictions"])
app.include_router(named_entities.router, prefix="/named-entities", tags=["named_entities"])
app.include_router(semantic_similarity.router, prefix="/semantic-similarity", tags=["semantic_similarity"])
app.include_router(health.router)