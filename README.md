1 - RUN docker compose up --build
2 - Set a .env file with folowing information:

OPENAI_API_KEY=XXXXX
SUMMARY_API_KEY=XXXX
GEMINI_API_KEY=YYYY

POSTGRES_DB=ianalyzer
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_HOST=ia_db
POSTGRES_PORT=5432