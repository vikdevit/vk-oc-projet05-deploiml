from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# -------------------------------------------------
# 1. Valeur hors limites (conint)
# -------------------------------------------------
def test_invalid_range():
    payload = {
        "employees": [{
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

            # ❌ valeur invalide volontairement
            "satisfaction_salarie_environnement": 999,

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
        }]
    }

    response = client.post("/predict_test", json=payload)

    assert response.status_code == 422


# -------------------------------------------------
# 2. Enum invalide (Literal)
# -------------------------------------------------
def test_invalid_enum():
    payload = {
        "employees": [{
            "age": 30,
            "genre": "X",  # ❌ invalide
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
        }]
    }

    response = client.post("/predict_test", json=payload)

    assert response.status_code == 422
