from fastapi import FastAPI
from backend.database import engine, Base
from backend.routes import questions, responses, summaries, similarities
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
