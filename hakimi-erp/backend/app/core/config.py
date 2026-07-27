from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "HAKIMI ERP"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database configuration
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "hakimi_erp"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
