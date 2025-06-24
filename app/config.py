import os
from dotenv import load_dotenv
from typing import List, Optional # Type hints
from pydantic_settings import BaseSettings # Base class for settings

from app import __app_name__, __version__

load_dotenv()

class Settings( BaseSettings ):
  """
  Application settings
  Uses pydantic_settings to load environment variables from .env file with proper type validation
  """

  # Application settings
  app_name: str = os.getenv( "APP_NAME", __app_name__ )
  app_version: str = os.getenv( "APP_VERSION", __version__ )
  app_port: int = os.getenv( "APP_PORT", 8080 )
  app_host: str = os.getenv( "APP_HOST", "0.0.0.0" )
  debug: bool = os.getenv( "DEBUG", False )
  env: str = os.getenv( "ENVIRONMENT", "development" )

  # DB settings
  db_url: str = os.getenv( "DATABASE_URL", "postgresql://username:password@localhost:5432/crm_db" )
  db_url_test: Optional[ str ] = os.getenv( "DATABASE_URL_TEST", None )

  # Security settings
  secret_key: str = os.getenv( "SECRET_KEY", "your-secret-key" )
  algorithm: str = os.getenv( "ALGORITHM", "HS256" )
  access_token_expire_minutes: int = os.getenv( "ACCESS_TOKEN_EXPIRE_MINUTES", 30 )
  refresh_token_expire_days: int = os.getenv( "REFRESH_TOKEN_EXPIRE_DAYS", 7 )

  # Password settings
  pwd_min_length: int = os.getenv( "PWD_MIN_LENGTH", 8 )
  pwd_max_length: int = os.getenv( "PWD_MAX_LENGTH", 128 )

  # CORS settings
  allow_origins: List[ str ] = [ 
    os.getenv( "ALLOW_ORIGINS", "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000,http://127.0.0.1:8080" )
  ]

  # API settings
  api_version_prefix: str = os.getenv( "API_VERSION_PREFIX", "/api/v1" )
  docs_url: str = os.getenv( "DOCS_URL", "/docs" )
  redoc_url: str = os.getenv( "REDOC_URL", "/redoc" )

  # Pagination settings
  default_page_size: int = os.getenv( "DEFAULT_PAGE_SIZE", 50 )
  max_page_size: int = os.getenv( "MAX_PAGE_SIZE", 100 )

  # Rate limiting settings (Future implementation)
  rate_limit_per_minute: int = os.getenv( "RATE_LIMIT_PER_MINUTE", 60 )

  # Logging settings
  log_level: str = os.getenv( "LOG_LEVEL", "info" ).lower()
  log_format: str = os.getenv( "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s" )

class Config:
  # Load environment variables from .env file
  env_file = ".env"
  env_file_encoding = "utf-8"
  case_sensitive = False

  # Allow environment variables to override .env file
  env_prefix = ""

  @property
  def is_development( self ) -> bool:
    """Check if the application is running in development mode"""
    return self.environment.lower() in [ "development", "dev" ]
  
  @property
  def is_production( self ) -> bool:
    """Check if the application is running in production mode"""
    return self.environment.lower() in [ "production", "prod" ]
  
  @property
  def is_testing( self ) -> bool:
    """Check if the application is running in testing mode"""
    return self.environment.lower() in [ "testing", "test" ]
  
  def get_db_url( self ) -> str:
    """Get the database URL based on the environment"""
    if self.is_testing and self.db_url_test:
      return self.db_url_test
    return self.db_url
  
settings = Settings()

def get_settings() -> Settings:
  """
  Dependency function to get settings instance
  Useful for dependency injection in FastAPI routes
  """
  return settings