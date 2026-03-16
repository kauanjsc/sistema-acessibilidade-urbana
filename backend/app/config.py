"""
config.py
Carrega e valida as variáveis de ambiente com pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # Banco de dados
    database_url: str = "postgresql://postgres:senha@localhost:5432/teresina_acessivel"

    # JWT
    secret_key: str = "dev_secret_troque_em_producao"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    # Ambiente
    environment: str = "development"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações."""
    return Settings()