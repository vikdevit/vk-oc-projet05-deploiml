from pydantic_settings import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret: str 
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # AJOUT pour HF
    environment: str = "local" # local | hf

    # AJOUT DB
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    model_config = SettingsConfigDict(env_file=".env")

    #class Config:
    #    env_file = ".env"

settings = Settings()

#class Settings(BaseSettings):

    # =====================
    # JWT CONFIG
    # =====================
#    JWT_SECRET: str
#    JWT_ALGORITHM: str = "HS256"
#    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =====================
    # POSTGRES CONFIG
    # =====================
#    POSTGRES_USER: str
#    POSTGRES_PASSWORD: str
#    POSTGRES_DB: str
#    POSTGRES_HOST: str = "localhost"
#    POSTGRES_PORT: int = 5432

#    class Config:
#        env_file = ".env"
#        extra = "ignore"


#settings = Settings()



# ne pas oublier après de mettre cela en ENV variables / GitHub Secrets
