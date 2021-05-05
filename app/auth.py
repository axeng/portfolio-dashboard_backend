from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from pydantic.tools import lru_cache

from app import config
from fastapi import HTTPException, status, Depends


@lru_cache()
def get_keycloak_settings():
    return config.Settings().keycloak


keycloak_openid = KeycloakOpenID(
    server_url=get_keycloak_settings().address + "/",
    client_id=get_keycloak_settings().client_id,
    realm_name=get_keycloak_settings().realm
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{get_keycloak_settings().address}/realms/{get_keycloak_settings().realm}/protocol/openid-connect/auth",
    tokenUrl=f"{get_keycloak_settings().address}/realms/{get_keycloak_settings().realm}/protocol/openid-connect/token"
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
