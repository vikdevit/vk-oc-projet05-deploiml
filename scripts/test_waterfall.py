import requests
import base64
import matplotlib.pyplot as plt
from PIL import Image
import io

# ==============================
# CONFIG
# ==============================
BASE_URL = "http://127.0.0.1:8000"

LOGIN_PAYLOAD = {
    "username": "admin",
    "password": "Test123!"
}

PREDICT_PAYLOAD = {
    "employees": [
        {
            "id": 1471,
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
}

OUTPUT_FILE = "waterfall_test.png"

# ==============================
# 1. LOGIN
# ==============================
print("🔐 Login...")
login_res = requests.post(f"{BASE_URL}/auth/login", json=LOGIN_PAYLOAD)

if login_res.status_code != 200:
    raise Exception(f"Login failed: {login_res.text}")

token = login_res.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# ==============================
# 2. CALL WATERFALL ENDPOINT
# ==============================
print("📊 Request waterfall...")
res = requests.post(
    f"{BASE_URL}/explain/waterfall",
    json=PREDICT_PAYLOAD,
    headers=headers
)

if res.status_code != 200:
    raise Exception(f"API error: {res.text}")

data = res.json()

# ==============================
# 3. DECODE BASE64
# ==============================
b64_img = data["waterfalls"][0]
img_bytes = base64.b64decode(b64_img)

# ==============================
# 4. SAVE IMAGE
# ==============================
with open(OUTPUT_FILE, "wb") as f:
    f.write(img_bytes)

print(f"✅ Image sauvegardée : {OUTPUT_FILE}")
