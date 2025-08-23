from pydantic_settings import BaseSettings
from typing import Optional, Literal
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
  llm_provider: Literal["openai", "local", "vllm", "ollama"] = "local"

  # OpenAI Configuration (Backup LLM Provider)
  openai_api_key: Optional[str] = None
  openai_model: str = "gpt-4"

  # Local LLM Configuration
  model_name: str = "microsoft/DialoGPT-medium"
  model_path: Optional[str] = None
  device: str = "auto"
  load_in_8bit: bool = True
  load_in_4bit: bool = False
  max_memory: Optional[dict] = None

  # VLLM Configuration
  vllm_host: str = "localhost"
  vllm_port: int = 8000

  # Ollama Configuration
  ollama_host: str = "localhost"
  ollama_port: int = 11434
  ollama_model: str = "llama2:13b"

  # General LLM Parameters
  max_tokens: int = 1000
  temperature: float = 0.7
  top_p: float = 0.9
  do_sample: bool = True

  # External API Configuration
  anthropic_api_key: Optional[str] = None
  semantic_scholar_api_key: Optional[str] = None
  pubmed_api_key: Optional[str] = None
  arxiv_api_key: Optional[str] = None

  # Vectore Store Configuration
  embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
  vector_dimension: int = 384

  # Security Configuration
  secret_key: str
  algorithm: str = "HS256"
  access_token_expire_minutes: int = 30

  # Rate Limiting Configuration
  rate_limit_window: int = 3600  # in seconds
  rate_limit_requests: int = 100

  class Congig:
    env_file = ".env"
    env_file_encoding = "utf-8"

settings = Settings()