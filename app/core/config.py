from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origins: str | None = None  # se lee como string: "http://...,https://..."

    class Config:
        env_file = ".env"

    # 👇 propiedad que devuelve lista en vez de string
    @property
    def cors_list(self) -> list[str]:
        if self.cors_origins:
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return []
        

settings = Settings()