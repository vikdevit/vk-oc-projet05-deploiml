import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")


def create_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        print("✅ DB créée")
    except psycopg2.errors.DuplicateDatabase:
        print("ℹ️ DB existe déjà")

    cur.close()
    conn.close()


if __name__ == "__main__":
    create_database()
