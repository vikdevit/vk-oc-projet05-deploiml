from datetime import datetime, timedelta
import jwt
import bcrypt
from app.core.config import settings

# ------------------
# HASH PASSWORD
# ------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ------------------
# JWT
# ------------------
def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload.update({"exp": expire})

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str):
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
