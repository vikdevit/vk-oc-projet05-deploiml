import json
import pandas as pd

from app.ml.feature_builder import FeatureBuilder, FeatureConfig


# =========================================================
# LOAD JSON (INPUT PRODUCTION)
# =========================================================
with open("data/raw/test.json") as f:
    data = json.load(f)

df_joint = pd.DataFrame(data["employees"])


# =========================================================
# FEATURE ENGINEERING
# =========================================================
fb = FeatureBuilder()
df_mod = fb.build(df_joint)


# =========================================================
# FEATURES FINALES (UNE SEULE SOURCE DE VÉRITÉ)
# =========================================================
final_features = FeatureConfig.get_final_features(df_mod)


# =========================================================
# MATRICE X (INFERENCE)
# =========================================================
X = df_mod[final_features].copy()


# =========================================================
# CHECKS
# =========================================================
print("Shape de X :", X.shape)

print("\nFeatures utilisées :")
print(X.columns.tolist())

print("\nX info :")
print(X.info())


