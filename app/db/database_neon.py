import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("❌ DATABASE_URL manquant")

    if "localhost" in database_url or "127.0.0.1" in database_url:
        raise ValueError("❌ Connexion locale détectée — interdit, on utilise Neon uniquement")

    return psycopg2.connect(database_url, sslmode="require")
