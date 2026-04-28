import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = os.getenv("POSTGRES_PORT", "5432")


def load_data():
    df = pd.read_json("data/raw/employees.json")
    df = df.drop(columns=["satisfaction_moyenne", "satisfaction_bin"], errors="ignore")
    return df


def insert_employees():

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )

    cur = conn.cursor()
    df = load_data()

    columns = [
        "age","genre","revenu_mensuel","statut_marital",
        "departement","poste","nombre_experiences_precedentes",
        "nombre_total_annees_experience","nombre_total_annees_dans_l_entreprise",
        "nombre_total_annees_dans_le_poste_actuel",
        "satisfaction_salarie_environnement",
        "satisfaction_salarie_nature_travail",
        "satisfaction_salarie_equipe",
        "satisfaction_salarie_equilibre_pro_perso",
        "note_evaluation_precedente",
        "niveau_hierarchique_poste",
        "note_evaluation_actuelle",
        "heures_supplementaires",
        "precedent_pourcentage_d_augmentation",
        "a_quitte_l_entreprise",
        "nombre_participation_pee",
        "nombre_de_formations_suivies",
        "distance_domicile_travail",
        "niveau_education",
        "domaine_etude",
        "frequence_deplacement",
        "nombre_d_annees_depuis_la_derniere_promotion",
        "nombre_d_annees_sous_le_responsable_actuel"
    ]
# 🔥 récupération existants (clé métier simple)
    cur.execute("""
        SELECT age, genre, revenu_mensuel, poste, departement
        FROM employees
    """)
    existing = set(cur.fetchall())

    data_to_insert = []

    for _, row in df.iterrows():
        key = (
            row["age"],
            row["genre"],
            row["revenu_mensuel"],
            row["poste"],
            row["departement"]
        )

        if key not in existing:
            data_to_insert.append(tuple(row[c] for c in columns))
            existing.add(key)

    cur.execute("SELECT COUNT(*) FROM employees")
    before = cur.fetchone()[0]

    query = f"""
    INSERT INTO employees ({",".join(columns)})
    VALUES %s
    """

    execute_values(cur, query, data_to_insert)

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM employees")
    after = cur.fetchone()[0]

    cur.close()
    conn.close()

    print("====================================")
    print(f"📊 Dataset total        : {len(df)}")
    print(f"✅ Nouveaux insérés     : {after - before}")
    print(f"⚠️  Doublons ignorés    : {len(df) - (after - before)}")
    print("====================================")


if __name__ == "__main__":
    insert_employees()
