from app.db.database_neon import get_connection

DROP_ALL = """
DROP TABLE IF EXISTS logs CASCADE;
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS features CASCADE;
DROP TABLE IF EXISTS api_logs CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
"""


def reset_database():
    
    conn = get_connection()

    cur = conn.cursor()

    print("Suppression complète des tables sur Neon DB...")

    cur.execute(DROP_ALL)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Toutes les tables supprimées sur Neon DB")


if __name__ == "__main__":
    reset_database()
