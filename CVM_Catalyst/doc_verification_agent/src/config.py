"""Configuration management for the document verification agent."""

import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Configuration
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-opus-20240229")

    # Document Fetching
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    max_retries: int = int(os.getenv("MAX_RETRIES", "3"))
    user_agent: str = os.getenv("USER_AGENT", "DocumentVerificationAgent/1.0")

    # Confluence Settings
    confluence_base_url: Optional[str] = os.getenv("CONFLUENCE_BASE_URL")
    confluence_username: Optional[str] = os.getenv("CONFLUENCE_USERNAME")
    confluence_api_token: Optional[str] = os.getenv("CONFLUENCE_API_TOKEN")

    # Scoring Configuration
    min_score: int = int(os.getenv("MIN_SCORE", "1"))
    max_score: int = int(os.getenv("MAX_SCORE", "10"))
    scoring_model: str = os.getenv("SCORING_MODEL", "gpt-4")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "json")

    # Application
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
