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


class PostgresSettings(BaseSettings):
    address: str
    user: str
    password: str
    db: str

    def get_postgres_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.address}/{self.db}"

    class Config:
        env_prefix = "PD_POSTGRES_"


class Settings(BaseSettings):
    keycloak: KeycloakSettings = KeycloakSettings()
    celery: CelerySettings = CelerySettings()
    postgres: PostgresSettings = PostgresSettings()
