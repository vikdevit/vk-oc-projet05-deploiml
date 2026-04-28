import os
import psycopg2
from dotenv import load_dotenv
from app.core.config import settings

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


def get_connection():
    """
    Retourne une connexion PostgreSQL
    (désactivée en mode Hugging Face)
    """
    # HF MODE pas de DB
    if settings.environment == "hf":
        raise RuntimeError("Database disabled in Hugging Face mode")


    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
