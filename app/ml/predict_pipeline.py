import joblib
import json
import numpy as np
import pandas as pd
import shap
import os

from app.ml.feature_builder import FeatureBuilder, FeatureConfig

# =========================================================
# PATH ROOT PROJET (IMPORTANT PRODUCTION)
# =========================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
THRESHOLD_PATH = os.path.join(BASE_DIR, "models", "threshold.json")


# =========================================================
# LOAD ARTIFACTS
# =========================================================
model = joblib.load(MODEL_PATH)

with open(THRESHOLD_PATH, "r") as f:
    threshold = json.load(f)["threshold"]


# =========================================================
# SHAP SETUP
# =========================================================
classifier = model.named_steps["classifier"]
preprocessor = model.named_steps["preprocessor"]
explainer = shap.TreeExplainer(classifier)
# récupération de l'espérance
base_value = explainer.expected_value

# cas classification binaire
if isinstance(base_value, (list, np.ndarray)):
    base_value = base_value[1]

# =========================================================
# PREDICTION FUNCTION (PRODUCTION CORE)
# =========================================================
def predict_employees(data_json: dict):

    # ---------------------
    # LOAD DATA
    # ---------------------
    df = pd.DataFrame(data_json["employees"])

    # ---------------------
    # FEATURE ENGINEERING
    # ---------------------
    fb = FeatureBuilder()
    df_mod = fb.build(df)

    # ---------------------
    # FEATURE SELECTION
    # ---------------------
    final_features = FeatureConfig.get_final_features(df_mod)
    X = df_mod[final_features].copy()

    # bool -> int (IMPORTANT cohérence sklearn)
    bool_cols = X.select_dtypes(include="bool").columns
    X[bool_cols] = X[bool_cols].astype(int)

    # ---------------------
    # PREDICTION PROBA
    # ---------------------
    proba = model.predict_proba(X)[:, 1]
    pred = (proba >= threshold).astype(int)

    # ---------------------
    # SHAP
    # ---------------------
    X_transformed = preprocessor.transform(X)

    shap_values = explainer(X_transformed)

    # class 1 (churn = départ)
    shap_class1 = shap_values.values[:, :, 1] if shap_values.values.ndim == 3 else shap_values.values

    # ---------------------
    # OUTPUT
    # ---------------------
    results = []

    feature_names = preprocessor.get_feature_names_out()

    for i in range(len(X)):
        shap_sum = float(np.sum(shap_class1[i]))

        results.append({
            "employee_id": int(df.iloc[i]["id"]) if "id" in df.columns else None,

            # input brut (utile audit / DB)
            "input": df.iloc[i].to_dict(),

            # prédiction métier
            "prediction": int(pred[i]),
            "probability": float(proba[i]),

            # explicabilité (stockage DB / endpoint futur)
            "explainability": {
                "feature_names": feature_names.tolist(),
                "base_value": float(base_value),
                "shap_values": shap_class1[i].tolist(),
                "shap_sum": shap_sum
            }
        })

    return results
