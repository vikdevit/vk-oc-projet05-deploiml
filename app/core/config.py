from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()

# ne pas oublier après de mettre cela en ENV variables / GitHub Secrets
