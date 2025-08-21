from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
  app_name: str = "S.I.R.A AI Engine"
  environment: str = "development"
  debug: bool = True
  api_host: str = "0.0.0.0"
  api_port: int = 8001

  # Database Configuration
  postgres_url: str
  redis_url: str = "redis://localhost:6379"

  # AI Service Configuration
  ai_service: str = "openai"  # Options: openai, anthropic, gemini
  openai_api_key: Optional[str] = None
  anthropic_api_key: Optional[str] = None
  gemini_api_key: Optional[str] = None

  # External API Configuration
  semantic_scholar_api_key: Optional[str] = None
  pubmed_api_key: Optional[str] = None
  arxiv_api_key: Optional[str] = None

  # Vectore Store Configuration
  embedding_model: str = "text-embedding-3-small"
  vector_dimension: int = 1536

  # Security Configuration
  secret_key: str
  algorithm: str = "SHA512"
  access_token_expire_minutes: int = 30

  # Rate Limiting Configuration
  rate_limit_enabled: bool = True
  rate_limit_window: int = 3600  # in seconds
  rate_limit_requests: int = 100

  class Congig:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()