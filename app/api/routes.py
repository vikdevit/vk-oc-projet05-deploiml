from fastapi import APIRouter, Depends
from app.ml.predict_pipeline import predict_employees
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse
from app.core.deps import get_current_user

router = APIRouter()

# ------------------------
# HEALTH (public)
# ------------------------
@router.get("/health")
def health():
    return {"status": "ok"}


# ------------------------
# PREDICT (JWT protected)
# ------------------------
@router.post("/predict", response_model=PredictionResponse)
def predict(
    data: PredictionRequest,
    user=Depends(get_current_user)
):
    results = predict_employees(data.dict())

    return {
        "status": "success",
        "n_predictions": len(results),
        "results": results
    }


# ------------------------
# WATERFALL endpoint dédié
# ------------------------
@router.post("/explain/waterfall")
def waterfall(
    data: PredictionRequest,
    user=Depends(get_current_user)
):
    results = predict_employees(data.dict())

    return {
        "status": "success",
        "waterfalls": [r["explainability"]["waterfall_plot"] for r in results]
    }
