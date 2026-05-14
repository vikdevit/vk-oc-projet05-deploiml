from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret: str = "dev_secret" 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # AJOUT pour HF
    environment: str = "local" # local | test | hf

    # AJOUT DB
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_db: str | None = None
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

