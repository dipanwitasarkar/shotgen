"""
Application configuration using Pydantic Settings.
"""
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # App
    app_name: str = "ShotGen"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # AI Provider
    ai_provider: Literal["replicate", "stability", "comfyui", "fal"] = "replicate"
    
    # Replicate
    replicate_api_token: str | None = None
    
    # Stability AI
    stability_api_key: str | None = None
    
    # ComfyUI
    comfyui_url: str = "http://localhost:8188"
    
    # FAL
    fal_key: str | None = None
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/shotgen"
    
    # Storage (Cloudflare R2)
    r2_account_id: str | None = None
    r2_access_key: str | None = None
    r2_secret_key: str | None = None
    r2_bucket: str = "shotgen"
    r2_public_url: str | None = None
    
    # Supabase Auth
    supabase_url: str | None = None
    supabase_anon_key: str | None = None
    supabase_service_key: str | None = None
    
    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Stripe
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    
    # Rate Limiting
    rate_limit_per_minute: int = 10
    
    # Image Settings
    max_image_size_mb: int = 10
    output_formats: list[str] = ["png", "jpg", "webp"]
    max_output_resolution: int = 4096


settings = Settings()
