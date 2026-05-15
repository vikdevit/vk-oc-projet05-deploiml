from app.db.database_neon import get_connection

# ==========
# EMPLOYEES 
# ==========
CREATE_EMPLOYEES_TABLE = """
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    age INT,
    genre VARCHAR,
    revenu_mensuel INT,
    statut_marital VARCHAR,
    departement VARCHAR,
    poste VARCHAR,
    nombre_experiences_precedentes INT,
    nombre_total_annees_experience INT,
    nombre_total_annees_dans_l_entreprise INT,
    nombre_total_annees_dans_le_poste_actuel INT,
    satisfaction_salarie_environnement INT,
    satisfaction_salarie_nature_travail INT,
    satisfaction_salarie_equipe INT,
    satisfaction_salarie_equilibre_pro_perso INT,
    note_evaluation_precedente INT,
    niveau_hierarchique_poste INT,
    note_evaluation_actuelle INT,
    heures_supplementaires VARCHAR,
    precedent_pourcentage_d_augmentation INT,
    a_quitte_l_entreprise VARCHAR,
    nombre_participation_pee INT,
    nombre_de_formations_suivies INT,
    distance_domicile_travail INT,
    niveau_education INT,
    domaine_etude VARCHAR,
    frequence_deplacement VARCHAR,
    nombre_d_annees_depuis_la_derniere_promotion INT,
    nombre_d_annees_sous_le_responsable_actuel INT
);
"""

# =========
# FEATURES 
# =========
CREATE_FEATURES_TABLE ="""
CREATE TABLE IF NOT EXISTS features (
    id SERIAL PRIMARY KEY,

    employee_id INT UNIQUE REFERENCES employees(id) ON DELETE CASCADE,

    -- numeric
    satisfaction_moyenne FLOAT,
    ratio_salaire_experience FLOAT,
    anciennete_ratio FLOAT,
    anciennete_sous_responsable_ratio FLOAT,
    niveau_poste_vs_revenu FLOAT,
    distance_domicile_travail FLOAT,
    nombre_de_formations_suivies INT,
    nombre_d_annees_depuis_la_derniere_promotion INT,

    -- behavioral
    stagnation INT,
    stress INT,
    mobilite INT,
    low_satisfaction INT,

    -- categorical (poste)
    poste_assistant_de_direction INT,
    poste_cadre_commercial INT,
    poste_consultant INT,
    poste_directeur_technique INT,
    poste_manager INT,
    poste_representant_commercial INT,
    poste_senior_manager INT,
    poste_tech_lead INT,
    poste_other INT,

    -- departement
    departement_commercial INT,
    departement_consulting INT,
    departement_other INT,

    -- domaine
    domaine_etude_autre INT,
    domaine_etude_entrepreunariat INT,
    domaine_etude_infra_et_cloud INT,
    domaine_etude_marketing INT,
    domaine_etude_transformation_digitale INT,
    domaine_etude_other INT,

    -- genre
    genre_f INT,
    genre_m INT,

    -- heures sup
    heures_supplementaires_non INT,
    heures_supplementaires_oui INT,

    -- déplacement
    frequence_deplacement_aucun INT,
    frequence_deplacement_frequent INT,
    frequence_deplacement_occasionnel INT,

    -- education
    niveau_education_1 INT,
    niveau_education_2 INT,
    niveau_education_3 INT,
    niveau_education_4 INT,
    niveau_education_other INT
);
"""

# ============
# PREDICTIONS 
# ============
CREATE_PREDICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,

    employee_id INT NOT NULL
        REFERENCES employees(id)
        ON DELETE CASCADE,

    prediction INT,
    probability FLOAT,

    shap_values JSONB,
    input_features JSONB,

    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
"""

# =========
# API_LOGS
# =========
CREATE_API_LOGS_TABLE = """
CREATE TABLE api_logs (
    id SERIAL PRIMARY KEY,
    request_id UUID,
    employee_id INT,
    step VARCHAR(50),
    status VARCHAR(20),
    message TEXT,
    payload JSONB,
    created_at TIMESTAMP DEFAULT now()
);
"""
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(CREATE_EMPLOYEES_TABLE)
    cur.execute(CREATE_FEATURES_TABLE)
    cur.execute(CREATE_PREDICTIONS_TABLE)
    cur.execute(CREATE_API_LOGS_TABLE)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Tables créées sur Neon DB uniquement")


if __name__ == "__main__":
    create_tables()
