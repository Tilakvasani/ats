from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret_key: str
    access_token_expire_minutes: int = 1440
    database_url: str
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"

settings = Settings()