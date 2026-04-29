from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "192.168.1.108"
    DB_PORT: int = 3306
    DB_USER: str = "chenwei"
    DB_PASSWORD: str = "761211"
    DB_NAME: str = "dunhuang_grottoes"
    UPLOAD_DIR: str = "/app/uploads"
    API_BASE_URL: str = "http://localhost:5204"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()