import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")


DROP_ALL = """
DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS features CASCADE;
DROP TABLE IF EXISTS api_logs CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
"""


def reset_database():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    cur = conn.cursor()

    print("🧹 Suppression complète des tables...")

    cur.execute(DROP_ALL)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Toutes les tables supprimées")


if __name__ == "__main__":
    reset_database()
