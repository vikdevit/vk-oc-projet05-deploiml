import pandas as pd
import numpy as np


# =========================================================
# CONFIG FEATURES (source unique de vérité)
# =========================================================
class FeatureConfig:

    numeric_features = [
        "satisfaction_moyenne",
        "ratio_salaire_experience",
        "anciennete_ratio",
        "anciennete_sous_responsable_ratio",
        "niveau_poste_vs_revenu",
        "distance_domicile_travail",
        "nombre_de_formations_suivies",
        "nombre_d_annees_depuis_la_derniere_promotion"
    ]

    behavioral_features = [
        "stagnation",
        "stress",
        "mobilite",
        "low_satisfaction"
    ]

    categorical_prefixes = [
        "poste_",
        "departement_",
        "domaine_etude_",
        "genre_",
        "heures_supplementaires_",
        "frequence_deplacement_",
        "niveau_education_"
    ]

    @classmethod
    def get_final_features(cls, df):
        categorical_features = [
            col for col in df.columns
            if any(col.startswith(prefix) for prefix in cls.categorical_prefixes)
        ]

        return cls.numeric_features + cls.behavioral_features + categorical_features


# =========================================================
# FEATURE BUILDER
# =========================================================
class FeatureBuilder:

    def build(self, df_joint: pd.DataFrame) -> pd.DataFrame:

        df_mod = df_joint.copy()

        # --------------------
        # DROP FEATURES BRUTES NON UTILISÉES
        # --------------------
        drop_cols = [
            "id",
            "nombre_d_annees_sous_le_responsable_actuel",
            "nombre_total_annees_experience",
            "nombre_total_annees_dans_l_entreprise",
            "nombre_total_annees_dans_le_poste_actuel",
            "revenu_mensuel"
        ]
        # df_mod = df_mod.drop(columns=drop_cols)
        df_mod = df_mod.drop(columns=drop_cols, errors="ignore")

        # --------------------
        # FEATURES NUMÉRIQUES DÉRIVÉES
        # --------------------
        df_mod["ratio_salaire_experience"] = (
            df_joint["revenu_mensuel"] /
            (df_joint["nombre_total_annees_experience"] + 1)
        )

        df_mod["anciennete_ratio"] = (
            df_joint["nombre_total_annees_dans_l_entreprise"] /
            (df_joint["nombre_total_annees_experience"] + 1)
        )

        df_mod["anciennete_sous_responsable_ratio"] = (
            df_joint["nombre_d_annees_sous_le_responsable_actuel"] /
            (df_joint["nombre_total_annees_dans_le_poste_actuel"] + 1)
        )

        df_mod["niveau_poste_vs_revenu"] = (
            df_joint["revenu_mensuel"] /
            (df_joint["niveau_hierarchique_poste"] + 1e-6)
        )

        # --------------------
        # SATISFACTION
        # --------------------
        satisfaction_cols = [
            "satisfaction_salarie_environnement",
            "satisfaction_salarie_nature_travail",
            "satisfaction_salarie_equipe",
            "satisfaction_salarie_equilibre_pro_perso"
        ]

        df_mod["satisfaction_moyenne"] = df_joint[satisfaction_cols].mean(axis=1)

        df_mod["satisfaction_bin"] = pd.cut(
            df_mod["satisfaction_moyenne"],
            bins=10
        )

        # --------------------
        # FEATURES COMPORTEMENTALES
        # --------------------
        df_mod["stagnation"] = (
            df_joint["nombre_d_annees_depuis_la_derniere_promotion"] > 3
        ).astype(int)

        df_mod["stress"] = (
            (df_joint["heures_supplementaires"] == "oui") &
            (df_mod["satisfaction_moyenne"] < 3)
        ).astype(int)

        df_mod["mobilite"] = (
            df_joint["frequence_deplacement"] != "aucun"
        ).astype(int)

        df_mod["low_satisfaction"] = (
            df_mod["satisfaction_moyenne"] < 2.5
        ).astype(int)

        # =====================================================
        # ENCODING MANUEL (CATÉGORIELS → BOOLS)
        # =====================================================

        def create_col(condition):
            return condition.astype(int)

        # --------------------
        # POSTE
        # --------------------
        postes_valides = [
            "assistant_de_direction",
            "cadre_commercial",
            "consultant",
            "directeur_technique",
            "manager",
            "representant_commercial",
            "senior_manager",
            "tech_lead"
        ]

        for p in postes_valides:
            df_mod[f"poste_{p}"] = create_col(df_joint["poste"] == p)

        df_mod["poste_other"] = create_col(~df_joint["poste"].isin(postes_valides))

        # --------------------
        # DEPARTEMENT
        # --------------------
        df_mod["departement_commercial"] = create_col(df_joint["departement"] == "commercial")
        df_mod["departement_consulting"] = create_col(df_joint["departement"] == "consulting")
        df_mod["departement_other"] = create_col(
            ~df_joint["departement"].isin(["commercial", "consulting"])
        )

        # --------------------
        # DOMAINE ETUDE
        # --------------------
        domaines_valides = [
            "autre",
            "entrepreunariat",
            "infra_et_cloud",
            "marketing",
            "transformation_digitale"
        ]

        for d in domaines_valides:
            df_mod[f"domaine_etude_{d}"] = create_col(df_joint["domaine_etude"] == d)

        df_mod["domaine_etude_other"] = create_col(
            ~df_joint["domaine_etude"].isin(domaines_valides)
        )

        # --------------------
        # GENRE
        # --------------------
        df_mod["genre_f"] = create_col(df_joint["genre"] == "f")
        df_mod["genre_m"] = create_col(df_joint["genre"] == "m")

        # --------------------
        # HEURES SUP
        # --------------------
        df_mod["heures_supplementaires_non"] = create_col(df_joint["heures_supplementaires"] == "non")
        df_mod["heures_supplementaires_oui"] = create_col(df_joint["heures_supplementaires"] == "oui")

        # --------------------
        # DEPLACEMENT
        # --------------------
        df_mod["frequence_deplacement_aucun"] = create_col(df_joint["frequence_deplacement"] == "aucun")
        df_mod["frequence_deplacement_frequent"] = create_col(df_joint["frequence_deplacement"] == "frequent")
        df_mod["frequence_deplacement_occasionnel"] = create_col(df_joint["frequence_deplacement"] == "occasionnel")

        # --------------------
        # EDUCATION
        # --------------------
        for i in [1, 2, 3, 4]:
            df_mod[f"niveau_education_{i}"] = create_col(df_joint["niveau_education"] == i)

        df_mod["niveau_education_other"] = create_col(
            ~df_joint["niveau_education"].isin([1, 2, 3, 4])
        )

        return df_mod
