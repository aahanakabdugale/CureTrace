from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "CureTrace"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./curetrace.db"

    class Config:
        env_file = ".env"


settings = Settings()
