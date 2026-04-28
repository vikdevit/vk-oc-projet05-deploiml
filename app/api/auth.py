import os
import json
from fastapi import APIRouter, HTTPException
from functools import lru_cache

from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.schemas.request import LoginRequest
from app.schemas.response import LoginResponse

router = APIRouter()


#@lru_cache
#def load_user():
#    
#    with open("data/user.json", "r") as f:
#        return json.load(f)

# chemin robuste (local + docker + HF)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USER_PATH = os.path.join(BASE_DIR, "data", "user.json")


def load_user():
    
    if settings.environment == "hf":
        return {
            "username": os.getenv("ADMIN_USER", "admin"),
            "password_hash": os.getenv("ADMIN_PASSWORD_HASH")
        }

    with open(USER_PATH, "r") as f:
        return json.load(f)


@router.post("/auth/login", response_model=LoginResponse)
def login(data: LoginRequest):

    fake_user = load_user()

    # vérification username
    if data.username != fake_user["username"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # vérification password bcrypt
    if not verify_password(data.password, fake_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # génération du token JWT
    token = create_access_token({"sub": data.username})

    return LoginResponse(
        access_token=token,
        token_type="bearer"
    )
