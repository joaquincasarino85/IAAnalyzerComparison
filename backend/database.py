import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db():
    """Espera a que PostgreSQL esté disponible antes de conectarse."""
    max_retries = 10
    retries = 0

    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            conn.close()
            print("✅ PostgreSQL está listo.")
            return
        except psycopg2.OperationalError:
            print(f"⏳ Esperando a PostgreSQL... ({retries + 1}/{max_retries})")
            time.sleep(2)
            retries += 1

    print("🚨 No se pudo conectar a PostgreSQL.")
    exit(1)  # Termina el programa si no se puede conectar


def create_database():
    """Crea la base de datos si no existe."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Crear la base de datos si no existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
        if not cur.fetchone():
            print(f"⚠️  La base de datos '{DB_NAME}' no existe. Creándola...")
            cur.execute(f"CREATE DATABASE {DB_NAME} OWNER {DB_USER};")
            print(f"✅  Base de datos '{DB_NAME}' creada con éxito.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"🚨 Error creando la base de datos: {e}")
        exit(1)

def init_models():
    from backend.models import question, response, similarity, summary  # Importá todos los modelos que definen tablas
    Base.metadata.create_all(bind=engine)



# Esperar a que PostgreSQL esté listo antes de crear la base de datos
wait_for_db()
create_database()
init_models()