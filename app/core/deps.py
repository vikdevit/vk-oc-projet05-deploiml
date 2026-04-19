from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token

# schéma simple Bearer JWT
security = HTTPBearer(auto_error=True)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    try:
        token = credentials.credentials  # <-- le JWT brut
        payload = decode_token(token)
        return payload.get("sub")

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
