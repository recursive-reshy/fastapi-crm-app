import uvicorn
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__

# Application instance
app = FastAPI(
  title = "CRM App",
  description = "CRM App for managing customers and their interactions",
  version = "0.1.0",
  docs_url = "/docs",
  redoc_url = "/redoc" # Redoc is an alternative to Swagger UI
)

# CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins = [ "*" ], # TODO: Change to only allow specific origins
  allow_credentials = True,
  allow_methods = [ "*" ],
  allow_headers = [ "*" ]
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
    "service": "crm-app",
    "version": __version__
  }

# Root
@app.get( "/" )
async def root():
  """
  Root endpoint with basic application information
  """
  return {
    "message": "CRM App",
    "docs": "/docs",
    "health": "/health"
  }

if __name__ == "__main__":
  uvicorn.run(
    "app.main:app", # TODO: Check what this is
    host = "0.0.0.0", # TODO: Take from environment variable
    port = 8000, # TODO: Take from environment variable
    reload = True, # TODO: Take from environment variable
    log_level = "info" # TODO: Take from environment variable
  )