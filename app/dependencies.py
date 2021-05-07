from app import auth
from app.database import SessionLocal
from fastapi import HTTPException, status, Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = (
                "-----BEGIN PUBLIC KEY-----\n"
                + auth.keycloak_openid.public_key()
                + "\n-----END PUBLIC KEY-----"
        )
        return auth.keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
