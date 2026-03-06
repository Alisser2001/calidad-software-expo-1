from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "User Service"
    port: int = 8000
    # MongoDB
    mongodb_url: str
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")
        
settings = Settings()