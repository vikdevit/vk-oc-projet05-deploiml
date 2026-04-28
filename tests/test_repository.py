import pytest
from app.db.repository import insert_employee
import app.db.repository as repo

def test_repository_loaded():
    assert hasattr(repo, "__file__")

@pytest.mark.db
def test_insert_employee(db_conn):

    employee = {
        "age": 30,
        "genre": "m",
        "revenu_mensuel": 3000,
        "statut_marital": "celibataire",
        "departement": "consulting",
        "poste": "manager",
        "nombre_experiences_precedentes": 1,
        "nombre_total_annees_experience": 5,
        "nombre_total_annees_dans_l_entreprise": 3,
        "nombre_total_annees_dans_le_poste_actuel": 2,
        "satisfaction_salarie_environnement": 3,
        "satisfaction_salarie_nature_travail": 3,
        "satisfaction_salarie_equipe": 3,
        "satisfaction_salarie_equilibre_pro_perso": 3,
        "note_evaluation_precedente": 3,
        "niveau_hierarchique_poste": 2,
        "note_evaluation_actuelle": 3,
        "heures_supplementaires": "non",
        "precedent_pourcentage_d_augmentation": 15,
        "nombre_participation_pee": 1,
        "nombre_de_formations_suivies": 2,
        "distance_domicile_travail": 10,
        "niveau_education": 3,
        "domaine_etude": "marketing",
        "frequence_deplacement": "aucun",
        "nombre_d_annees_depuis_la_derniere_promotion": 1,
        "nombre_d_annees_sous_le_responsable_actuel": 1
    }

    emp_id = insert_employee(db_conn, employee)

    assert emp_id is not None
