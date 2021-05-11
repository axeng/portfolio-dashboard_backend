from fastapi import HTTPException, status, Depends
from app import auth, crud
from app.dependencies.database import get_db
from app.schemas import UserCreate, User
from sqlalchemy.orm import Session


async def get_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        KEYCLOAK_PUBLIC_KEY = (
                "-----BEGIN PUBLIC KEY-----\n"
                + auth.keycloak_openid.public_key()
                + "\n-----END PUBLIC KEY-----"
        )
        keycloak_user = auth.keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )

        keycloak_user_id = keycloak_user["sub"]

        user = crud.user.get_by_keycloak_user_id(db, keycloak_user_id)
        if not user:
            user_in = UserCreate(keycloak_user_id=keycloak_user_id)
            user = crud.user.create(db, user_in)

        return user
    except Exception as e:
        print(e)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
