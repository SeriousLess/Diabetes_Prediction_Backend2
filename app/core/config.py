from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origins: str | None = None  # se lee como string: "http://...,https://..."
    recaptcha_secret: str  

    # 👇 credenciales de correo
    mail_username: str
    mail_password: str
    mail_from: str | None = None  # opcional, si quieres diferenciar remitente
    mail_port: int = 587
    mail_server: str = "smtp.gmail.com"
    mail_starttls: bool = True   # 👈 nombre correcto para fastapi-mail
    mail_ssl_tls: bool = False   # 👈 nombre correcto para fastapi-mail

    class Config:
        env_file = ".env"

    # 👇 propiedad que devuelve lista en vez de string
    @property
    def cors_list(self) -> list[str]:
        if self.cors_origins:
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return []

settings = Settings()
