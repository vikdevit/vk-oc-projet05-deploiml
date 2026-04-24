import json
#import hashlib
import psycopg2
import uuid

# =========================================================
# HASH EMPLOYEE
# =========================================================
#def generate_employee_hash(employee: dict):
#    """
#    Hash stable pour éviter doublons
#    """
#    raw = f"{employee.get('age')}_{employee.get('genre')}_{employee.get('revenu_mensuel')}_{employee.get('poste')}_{employee.get('departement')}_{employee.get('nombre_total_annees_experience')}"
#    return hashlib.sha256(raw.encode()).hexdigest()


# =========================================================
# INSERT EMPLOYEE
# =========================================================
def insert_employee(conn, employee: dict):

    employee = employee.copy()

    #  sécurité API
    employee.pop("id", None)

    #  hash obligatoire
    #employee_hash = generate_employee_hash(employee)
    #employee["employee_hash"] = employee_hash

    query = """
    INSERT INTO employees (
        age, genre, revenu_mensuel, statut_marital,
        departement, poste,
        nombre_experiences_precedentes,
        nombre_total_annees_experience,
        nombre_total_annees_dans_l_entreprise,
        nombre_total_annees_dans_le_poste_actuel,
        satisfaction_salarie_environnement,
        satisfaction_salarie_nature_travail,
        satisfaction_salarie_equipe,
        satisfaction_salarie_equilibre_pro_perso,
        note_evaluation_precedente,
        niveau_hierarchique_poste,
        note_evaluation_actuelle,
        heures_supplementaires,
        precedent_pourcentage_d_augmentation,
        nombre_participation_pee,
        nombre_de_formations_suivies,
        distance_domicile_travail,
        niveau_education,
        domaine_etude,
        frequence_deplacement,
        nombre_d_annees_depuis_la_derniere_promotion,
        nombre_d_annees_sous_le_responsable_actuel
    )
    VALUES (
        %(age)s, %(genre)s, %(revenu_mensuel)s, %(statut_marital)s,
        %(departement)s, %(poste)s,
        %(nombre_experiences_precedentes)s,
        %(nombre_total_annees_experience)s,
        %(nombre_total_annees_dans_l_entreprise)s,
        %(nombre_total_annees_dans_le_poste_actuel)s,
        %(satisfaction_salarie_environnement)s,
        %(satisfaction_salarie_nature_travail)s,
        %(satisfaction_salarie_equipe)s,
        %(satisfaction_salarie_equilibre_pro_perso)s,
        %(note_evaluation_precedente)s,
        %(niveau_hierarchique_poste)s,
        %(note_evaluation_actuelle)s,
        %(heures_supplementaires)s,
        %(precedent_pourcentage_d_augmentation)s,
        %(nombre_participation_pee)s,
        %(nombre_de_formations_suivies)s,
        %(distance_domicile_travail)s,
        %(niveau_education)s,
        %(domaine_etude)s,
        %(frequence_deplacement)s,
        %(nombre_d_annees_depuis_la_derniere_promotion)s,
        %(nombre_d_annees_sous_le_responsable_actuel)s
    )
    RETURNING id;
    """

    with conn.cursor() as cur:
        cur.execute(query, employee)
        employee_id = cur.fetchone()[0]
        conn.commit()

    return employee_id


# =========================================================
# INSERT FEATURES
# =========================================================
def insert_features(conn, employee_id: int, features: dict):

    features["employee_id"] = employee_id

    cols = list(features.keys())
    values = ", ".join([f"%({c})s" for c in cols])

    query = f"""
    INSERT INTO features ({",".join(cols)})
    VALUES ({values});
    """

    with conn.cursor() as cur:
        cur.execute(query, features)
        conn.commit()

# =========================================================
# INSERT PREDICTION
# =========================================================
def insert_prediction(conn, employee_id: int, prediction: dict):

    query = """
    INSERT INTO predictions (
        employee_id,
        prediction,
        probability,
        shap_values,
        input_features,
        model_version
    )
    VALUES (
        %(employee_id)s,
        %(prediction)s,
        %(probability)s,
        %(shap_values)s,
        %(input_features)s,
        %(model_version)s
    );
    """

    payload = {
        "employee_id": employee_id,
        "prediction": prediction["prediction"],
        "probability": prediction["probability"],
        "shap_values": json.dumps(prediction["explainability"]),
        "input_features": json.dumps(prediction["input"]),
        "model_version": "v1"
    }

    with conn.cursor() as cur:
        cur.execute(query, payload)
        conn.commit()

# =========================================================
# INSERT API_LOGS
# =========================================================
def log_api(conn, request_id, employee_id, step, status, message=None, payload=None):

    query = """
    INSERT INTO api_logs (request_id, employee_id, step, status, message, payload)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    # Conversion JSON
    payload_json = json.dumps(payload) if payload is not None else None

    with conn.cursor() as cur:
        cur.execute(query, (request_id, employee_id, step, status, message, payload_json))
        conn.commit()

