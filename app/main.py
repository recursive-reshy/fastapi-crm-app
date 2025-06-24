import uvicorn
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__, __description__

from .config import settings

# Application instance
app = FastAPI(
  title = settings.app_name,
  description = __description__,
  version = settings.app_version,
  docs_url = settings.docs_url,
  redoc_url = settings.redoc_url # Redoc is an alternative to Swagger UI
)

# CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins = settings.allow_origins,
  allow_credentials = True,
  allow_methods = [ "*" ], # TODO: Change to only allow specific methods
  allow_headers = [ "*" ] # TODO: Change to only allow specific headers
)

# Health check
@app.get( "/health" )
async def health_check():
  """
  Health check endpoint to verify the service is running
  """
  return {
    "status": "healthy",
    "timestamp": datetime.now().isoformat(),
    "service": settings.app_name,
    "version": settings.app_version,
    "environment": settings.env,
    "debug": settings.debug
  }

# Root
@app.get( "/" )
async def root():
  """
  Root endpoint with basic application information
  """
  return {
    "message": f"{settings.app_name} API",
    "version": settings.app_version,
    "environment": settings.env,
    "docs": f"{settings.api_version_prefix}{settings.docs_url}",
    "health": f"{settings.api_version_prefix}/health"
  }

if __name__ == "__main__":
  uvicorn.run(
    "app.main:app", # Refers to main.py file and app variable
    host = settings.app_host,
    port = settings.app_port,
    reload = settings.debug,
    log_level = settings.log_level
  )