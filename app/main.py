from functools import lru_cache

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from starlette.middleware.cors import CORSMiddleware

from app import config

app = FastAPI()


@lru_cache()
def get_settings():
    return config.Settings()


origins = [
    "http://localhost:8081"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

keycloak_openid = KeycloakOpenID(
    server_url=get_settings().keycloak_address + "/",
    client_id=get_settings().keycloak_client_id,
    realm_name=get_settings().keycloak_realm
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{get_settings().keycloak_address}/realms/{get_settings().keycloak_realm}/protocol/openid-connect/auth",
    tokenUrl=f"{get_settings().keycloak_address}/realms/{get_settings().keycloak_realm}/protocol/openid-connect/token"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = (
                "-----BEGIN PUBLIC KEY-----\n"
                + keycloak_openid.public_key()
                + "\n-----END PUBLIC KEY-----"
        )
        return keycloak_openid.decode_token(
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


@app.get("/secure")
async def secure(current_user: dict = Depends(get_current_user)):
    print(current_user)
    return {"Bravo": "Congrats"}


@app.get("/")
def root():
    return {"Hello": "World"}
