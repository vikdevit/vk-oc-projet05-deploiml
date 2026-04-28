import pytest
import pandas as pd
from app.ml.feature_builder import FeatureBuilder

def test_feature_builder_basic():

    data = {
        "age": [30],
        "genre": ["m"],
        "revenu_mensuel": [3000],
        "nombre_total_annees_experience": [5],
        "nombre_total_annees_dans_l_entreprise": [3],
        "nombre_total_annees_dans_le_poste_actuel": [2],
        "nombre_d_annees_sous_le_responsable_actuel": [1],
        "satisfaction_salarie_environnement": [3],
        "satisfaction_salarie_nature_travail": [3],
        "satisfaction_salarie_equipe": [3],
        "satisfaction_salarie_equilibre_pro_perso": [3],
        "heures_supplementaires": ["non"],
        "frequence_deplacement": ["aucun"],
        "niveau_hierarchique_poste": [2],
        "poste": ["manager"],
        "departement": ["consulting"],
        "domaine_etude": ["marketing"],
        "niveau_education": [3],
        "nombre_d_annees_depuis_la_derniere_promotion": [1],
        "nombre_de_formations_suivies": [2],
        "distance_domicile_travail": [10] 
    }

    df = pd.DataFrame(data)

    fb = FeatureBuilder()
    result = fb.build(df)

    assert result.shape[0] == 1
    assert "satisfaction_moyenne" in result.columns
    assert "stress" in result.columns
