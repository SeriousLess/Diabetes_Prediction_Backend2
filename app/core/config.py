from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origins: str | None = None
    recaptcha_secret: str  

    # 👇 credenciales de Brevo
    brevo_api_key: str  
    mail_from: str   # remitente validado en Brevo (ej: tu correo verificado)

    class Config:
        env_file = ".env"

    @property
    def cors_list(self) -> list[str]:
        if self.cors_origins:
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return []

settings = Settings()