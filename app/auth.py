from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from pydantic.tools import lru_cache

from app import config


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
