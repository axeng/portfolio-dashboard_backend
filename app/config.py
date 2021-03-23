from pydantic import BaseSettings


class Settings(BaseSettings):
    keycloak_address: str
    keycloak_realm: str
    keycloak_client_id: str

    class Config:
        env_file = ".env.local"
