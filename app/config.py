from pydantic import BaseSettings


class KeycloakSettings(BaseSettings):
    address: str
    realm: str
    client_id: str

    class Config:
        env_prefix = "PD_KEYCLOAK_"


class CelerySettings(BaseSettings):
    broker_address: str
    backend_address: str

    class Config:
        env_prefix = "PD_CELERY_"


class Settings(BaseSettings):
    keycloak: KeycloakSettings = KeycloakSettings()
    celery: CelerySettings = CelerySettings()
