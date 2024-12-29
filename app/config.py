from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    FRONTEND_URL: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"

settings = Settings()