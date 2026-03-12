from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CureTrace"
    app_env: str = "development"
    debug: bool = True
    database_url: str = ""
    secret_key: str = "change-me"
    qr_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"


settings = Settings()
