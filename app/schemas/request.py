from pydantic import BaseModel, Field, conint, confloat
from typing import List, Literal, Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class Employee(BaseModel):
    id: Optional[int] = None

    age: int
    genre: Literal["m", "f"]

    revenu_mensuel: int

    statut_marital: Literal["celibataire", "mariee", "divorcee"]

    departement: Literal["commercial", "consulting", "ressources_humaines"]

    poste: Literal[
        "cadre_commercial",
        "assistant_de_direction",
        "consultant",
        "tech_lead",
        "manager",
        "senior_manager",
        "representant_commercial",
        "directeur_technique",
        "ressources_humaines"
    ]

    nombre_experiences_precedentes: int

    nombre_total_annees_experience: int
    nombre_total_annees_dans_l_entreprise: int
    nombre_total_annees_dans_le_poste_actuel: int

    satisfaction_salarie_environnement: conint(ge=1, le=4)
    satisfaction_salarie_nature_travail: conint(ge=1, le=4)
    satisfaction_salarie_equipe: conint(ge=1, le=4)
    satisfaction_salarie_equilibre_pro_perso: conint(ge=1, le=4)

    note_evaluation_precedente: conint(ge=1, le=4)
    niveau_hierarchique_poste: conint(ge=1, le=5)
    note_evaluation_actuelle: conint(ge=1, le=4)

    heures_supplementaires: Literal["oui", "non"]

    precedent_pourcentage_d_augmentation: conint(ge=11, le=25)

    #a_quitte_l_entreprise: Literal["oui", "non"]

    nombre_participation_pee: conint(ge=1, le=3)

    nombre_de_formations_suivies: conint(ge=0, le=6)

    distance_domicile_travail: conint(ge=1, le=30)

    niveau_education: conint(ge=1, le=5)

    domaine_etude: Literal[
        "infra_et_cloud",
        "autre",
        "transformation_digitale",
        "marketing",
        "entrepreunariat",
        "ressources_humaines"
    ]

    frequence_deplacement: Literal["occasionnel", "frequent", "aucun"]

    nombre_d_annees_depuis_la_derniere_promotion: conint(ge=0, le=15)

    nombre_d_annees_sous_le_responsable_actuel: conint(ge=0, le=20)


class PredictionRequest(BaseModel):
    employees: List[Employee]
