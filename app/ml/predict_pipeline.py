import joblib
import json
import numpy as np
import pandas as pd
import shap
import os
import matplotlib.pyplot as plt
import shap
import io
import base64

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
    base_value = float(np.array(base_value).flatten()[1])
else:
    base_value = float(base_value)

# =========================================================
# UTILS - SHAP VISUALIZATION
# =========================================================
def shap_waterfall_base64(shap_exp, index=0):
    import matplotlib.pyplot as plt
    import io
    import base64
    import numpy as np
    import shap

    plt.figure()

    # 1. récupérer explication brute
    exp = shap_exp[index]

    # 2. CAS MULTI-CLASSE (très important)
    # shap.values = (n_features, n_classes)
    if hasattr(exp, "values") and len(exp.values.shape) == 2:

        exp = shap.Explanation(
            values=exp.values[:, 1],  # classe 1 = churn
            base_values=(
                exp.base_values[1]
                if isinstance(exp.base_values, (list, np.ndarray))
                else exp.base_values
            ),
            data=exp.data,
            feature_names=exp.feature_names
        )

    # 3. FORCER base_value scalaire (CRUCIAL)
    exp = shap.Explanation(
        values=exp.values,
        base_values=float(np.array(exp.base_values).reshape(-1)[0]),
        data=exp.data,
        feature_names=exp.feature_names
    )

    # 4. waterfall
    shap.plots.waterfall(exp, show=False)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()

    return base64.b64encode(buf.getvalue()).decode("utf-8")

# =========================================================
# PREDICTION FUNCTION (PRODUCTION CORE)
# =========================================================
#def predict_employees(data_json: dict):
def predict_employees(data_json: dict, include_waterfall: bool = False):

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
    
    feature_names = preprocessor.get_feature_names_out()

    X_transformed_df = pd.DataFrame(
        X_transformed,
        columns=feature_names
    )

    shap_exp = explainer(X_transformed_df)

    #shap_exp = explainer(X_transformed)

    # shap values classe 1
    if len(shap_exp.values.shape) == 3:
        shap_class1 = shap_exp.values[:, :, 1]
    else:
        shap_class1 = shap_exp.values


    # ---------------------
    # OUTPUT
    # ---------------------
    results = []

    #feature_names = preprocessor.get_feature_names_out()

    for i in range(len(X)):
        shap_sum = float(np.sum(shap_class1[i]))

        #waterfall = shap_waterfall_base64(shap_exp, i)
        waterfall = None
        if include_waterfall:
            waterfall = shap_waterfall_base64(shap_exp, i)

        results.append({
            "employee_id": int(df.iloc[i]["id"]) if "id" in df.columns else None,

            # input brut (utile audit / DB)
            "input": df.iloc[i].to_dict(),

            # 👇 AJOUT IMPORTANT POUR LA DB FEATURES
            "features": X.iloc[i].to_dict(),

            # prédiction métier
            "prediction": int(pred[i]),
            "probability": float(proba[i]),

            # explicabilité (stockage DB / endpoint futur)
            "explainability": {
                "feature_names": feature_names.tolist(),
                "base_value": float(base_value),
                "shap_values": shap_class1[i].tolist(),
                "shap_sum": shap_sum,
                "waterfall_plot": waterfall
            }
        })

    return results
