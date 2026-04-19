from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PredictionResult(BaseModel):
    employee_id: Optional[int]
    prediction: int
    probability: float
    explainability: Dict[str, Any]


class PredictionResponse(BaseModel):
    status: str
    n_predictions: int
    results: List[PredictionResult]
