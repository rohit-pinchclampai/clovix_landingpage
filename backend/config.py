"""
Configuration management for the Clovix backend API
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "Clovix Landing Page API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_path: str = "prospects.db"
    database_url: str = ""  # For PostgreSQL in production
    
    # CORS
    frontend_url: str = "http://localhost:5173,http://localhost:3000"
    
    # Security
    api_key: str = ""  # For admin endpoints
    rate_limit_per_minute: int = 10
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins list"""
        origins = self.frontend_url.split(",")
        origins.extend([
            "http://localhost:5173",
            "http://localhost:3000",
        ])
        
        # In development, allow all origins
        if self.environment != "production":
            origins.append("*")
        
        return origins
    
    @property
    def use_postgresql(self) -> bool:
        """Check if PostgreSQL should be used"""
        return bool(self.database_url and self.database_url.startswith("postgres"))


# Global settings instance
settings = Settings()

