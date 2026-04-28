from fastapi import APIRouter, Depends
from app.ml.predict_pipeline import predict_employees
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse
from app.core.deps import get_current_user

router = APIRouter()

from app.db.database import get_connection
#from app.db.connection import get_connection
from app.db.repository import (
    insert_employee,
    insert_features,
    insert_prediction
)
from app.db.repository import log_api
from app.ml.predict_pipeline import predict_employees
import uuid
import json
# ------------------------
# HEALTH (public)
# ------------------------
@router.get("/health")
def health():
    return {"status": "ok"}


# ------------------------
# PREDICT (JWT protected)
# ------------------------

#@router.post("/predict", response_model=PredictionResponse)
#def predict(
#    data: PredictionRequest,
#    user=Depends(get_current_user)
#):
#    #results = predict_employees(data.dict())
#    results = predict_employees(data.dict(), include_waterfall=False)
#
#    return {
#        "status": "success",
#        "n_predictions": len(results),
#        "results": results
#    }

@router.post("/predict_test")
def predict_test(data: PredictionRequest):

    results = predict_employees(
        data.model_dump(),
        include_waterfall=False
    )

    return {
        "status": "success",
        "mode": "test_no_db",
        "n_predictions": len(results),
        "results": results
    }

@router.post("/predict")
def predict(data: PredictionRequest):

    conn = get_connection()
    results = []
    
    # Clé de traçabilité des échanges
    request_id = str(uuid.uuid4())

    try:
        
        # =====================================================
        # 1. LOG INPUT API
        # =====================================================
        log_api(
            conn,
            request_id,
            None,
            "input_received",
            "success",
            payload=data.model_dump()
        )

        for emp in data.employees:

            emp_dict = emp.model_dump()
            emp_dict.pop("id", None)

            # 1. INSERT EMPLOYEE
            employee_id = insert_employee(conn, emp_dict)
            log_api(conn, request_id, employee_id, "insert_employee", "success", payload=emp_dict)

            # IMPORTANT : garder cohérence
            emp_dict["id"] = employee_id

            # 2. PREDICTION
            result = predict_employees({"employees": [emp_dict]})[0]
            log_api(conn, request_id, employee_id, "prediction_compute", "success", payload=result)

            # 3. FEATURES
            insert_features(conn, employee_id, result["features"])
            log_api(conn, request_id, employee_id, "insert_features", "success", payload=result["features"])

            # 4. PREDICTION DB
            insert_prediction(conn, employee_id, result)
            log_api(conn, request_id, employee_id, "insert_prediction", "success")

            conn.commit()

            results.append(result)

        # =====================================================
        # FINAL RESPONSE API_LOGS
        # =====================================================
        log_api(
            conn,
            request_id,
            None,
            "request_completed",
            "success",
            payload={"n_predictions": len(results)}
        )
        
        conn.close()

        return {
        "status": "success",
        "request_id": request_id, # pour audit
        "mode": "db",
        "n_predictions": len(results),
        "results": results
        }

    except Exception as e:
#        conn.rollback()
#        log_api(conn, request_id, None, "error", "fail", str(e))
#        raise e
    
        log_api(
            conn,
            request_id,
            None,
            "error",
            "fail",
            message=str(e),
            payload=data.model_dump()
        )

        conn.close()

        return {
            "status": "error",
            "request_id": request_id,
            "message": str(e)
        }


#      return {
#        "status": "success",
#        "request_id": request_id, # pour audit
#        "mode": "db",
#        "n_predictions": len(results),
#        "results": results
#    }

    # =========================
    # 4. LOGS
    # =========================
#    insert_log(
#        user_id=user,
#        endpoint="/predict",
#        payload=data.dict(),
#        status=200
#    )
#
#    return {
#        "status": "success",
#        "n_predictions": len(results),
#        "results": results
#    }



# ------------------------
# WATERFALL endpoint dédié
# ------------------------
@router.post("/explain/waterfall")
def waterfall(
    data: PredictionRequest,
    user=Depends(get_current_user)
):
    #results = predict_employees(data.dict())
    results = predict_employees(data.model_dump(), include_waterfall=True)

    return {
        "status": "success",
        "waterfalls": [r["explainability"]["waterfall_plot"] for r in results]
    }
