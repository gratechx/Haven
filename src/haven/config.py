"""Configuration management for Haven"""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # AI Provider Configuration
    ai_provider: str = Field(default="openai", description="AI provider to use")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key")
    
    # GitHub Configuration
    github_token: Optional[str] = Field(default=None, description="GitHub personal access token")
    
    # Azure Configuration
    azure_subscription_id: Optional[str] = Field(default=None, description="Azure subscription ID")
    azure_tenant_id: Optional[str] = Field(default=None, description="Azure tenant ID")
    azure_client_id: Optional[str] = Field(default=None, description="Azure client ID")
    azure_client_secret: Optional[str] = Field(default=None, description="Azure client secret")
    
    # Application Settings
    database_url: str = Field(default="sqlite:///./haven.db", description="Database connection URL")
    log_level: str = Field(default="INFO", description="Logging level")
    language: str = Field(default="ar", description="Default language (ar/en/auto)")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
