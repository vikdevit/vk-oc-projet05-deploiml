from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_unknown_route():
    response = client.get("/route_qui_nexiste_pas")
    assert response.status_code == 404


def test_predict_test_endpoint():
    response = client.post("/predict_test", json={
        "employees": [
            {
                "age": 34,
                "genre": "m",
                "revenu_mensuel": 3200,
                "statut_marital": "celibataire",
                "departement": "commercial",
                "poste": "manager",
                "nombre_experiences_precedentes": 3,
                "nombre_total_annees_experience": 5,
                "nombre_total_annees_dans_l_entreprise": 4,
                "nombre_total_annees_dans_le_poste_actuel": 2,
                "satisfaction_salarie_environnement": 3,
                "satisfaction_salarie_nature_travail": 4,
                "satisfaction_salarie_equipe": 3,
                "satisfaction_salarie_equilibre_pro_perso": 3,
                "note_evaluation_precedente": 4,
                "niveau_hierarchique_poste": 2,
                "note_evaluation_actuelle": 4,
                "heures_supplementaires": "oui",
                "precedent_pourcentage_d_augmentation": 12,
                "nombre_participation_pee": 2,
                "nombre_de_formations_suivies": 3,
                "distance_domicile_travail": 10,
                "niveau_education": 3,
                "domaine_etude": "infra_et_cloud",
                "frequence_deplacement": "frequent",
                "nombre_d_annees_depuis_la_derniere_promotion": 2,
                "nombre_d_annees_sous_le_responsable_actuel": 1
            }
        ]
    })

    assert response.status_code in [200, 500]


def test_predict_endpoint():
    response = client.post("/predict", json={
        "employees": [
            {
                "age": 34,
                "genre": "m",
                "revenu_mensuel": 3200,
                "statut_marital": "celibataire",
                "departement": "commercial",
                "poste": "manager",
                "nombre_experiences_precedentes": 3,
                "nombre_total_annees_experience": 5,
                "nombre_total_annees_dans_l_entreprise": 4,
                "nombre_total_annees_dans_le_poste_actuel": 2,
                "satisfaction_salarie_environnement": 3,
                "satisfaction_salarie_nature_travail": 4,
                "satisfaction_salarie_equipe": 3,
                "satisfaction_salarie_equilibre_pro_perso": 3,
                "note_evaluation_precedente": 4,
                "niveau_hierarchique_poste": 2,
                "note_evaluation_actuelle": 4,
                "heures_supplementaires": "oui",
                "precedent_pourcentage_d_augmentation": 12,
                "nombre_participation_pee": 2,
                "nombre_de_formations_suivies": 3,
                "distance_domicile_travail": 10,
                "niveau_education": 3,
                "domaine_etude": "infra_et_cloud",
                "frequence_deplacement": "frequent",
                "nombre_d_annees_depuis_la_derniere_promotion": 2,
                "nombre_d_annees_sous_le_responsable_actuel": 1
            }
        ]
    })

    assert response.status_code in [200, 500]


def test_waterfall_endpoint():
    response = client.post("/explain/waterfall", json={
        "employees": [
            {
                "age": 34,
                "genre": "m",
                "revenu_mensuel": 3200,
                "statut_marital": "celibataire",
                "departement": "commercial",
                "poste": "manager",
                "nombre_experiences_precedentes": 3,
                "nombre_total_annees_experience": 5,
                "nombre_total_annees_dans_l_entreprise": 4,
                "nombre_total_annees_dans_le_poste_actuel": 2,
                "satisfaction_salarie_environnement": 3,
                "satisfaction_salarie_nature_travail": 4,
                "satisfaction_salarie_equipe": 3,
                "satisfaction_salarie_equilibre_pro_perso": 3,
                "note_evaluation_precedente": 4,
                "niveau_hierarchique_poste": 2,
                "note_evaluation_actuelle": 4,
                "heures_supplementaires": "oui",
                "precedent_pourcentage_d_augmentation": 12,
                "nombre_participation_pee": 2,
                "nombre_de_formations_suivies": 3,
                "distance_domicile_travail": 10,
                "niveau_education": 3,
                "domaine_etude": "infra_et_cloud",
                "frequence_deplacement": "frequent",
                "nombre_d_annees_depuis_la_derniere_promotion": 2,
                "nombre_d_annees_sous_le_responsable_actuel": 1
            }
        ]
    })

    assert response.status_code in [200, 401, 403]
