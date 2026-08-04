"""
Factory for creating AI providers.
"""
from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.replicate_provider import ReplicateProvider
from app.providers.stability_provider import StabilityProvider
from app.providers.nvidia_provider import NVIDIAProvider
from app.providers.together_provider import TogetherProvider
from app.providers.huggingface_provider import HuggingFaceProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""
    
    _providers: dict[str, type[AIProvider]] = {
        "nvidia": NVIDIAProvider,
        "together": TogetherProvider,
        "huggingface": HuggingFaceProvider,
        "replicate": ReplicateProvider,
        "stability": StabilityProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: str | None = None, api_key: str | None = None) -> AIProvider:
        """
        Get an AI provider instance.
        
        Args:
            provider_name: Name of provider, or None to use default from settings
            api_key: API key for the provider, or None to use from settings
            
        Returns:
            AIProvider instance
            
        Raises:
            ValueError: If provider is not supported or API key missing
        """
        # Import here to avoid circular dependency
        from app.api.routes import get_runtime_settings
        
        runtime = get_runtime_settings()
        
        # Determine provider name
        name = provider_name or runtime.get("provider") or settings.ai_provider
        
        if name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown provider: {name}. Available: {available}")
        
        # Get API key from runtime settings or parameter
        key = api_key or runtime.get("api_key")
        
        # Fallback to environment variables
        if not key:
            if name == "replicate":
                key = settings.replicate_api_token
            elif name == "stability":
                key = settings.stability_api_key
        
        if not key:
            raise ValueError(f"API key required for {name}. Configure in Settings panel.")
        
        return cls._providers[name](key)
    
    @classmethod
    def list_providers(cls) -> list[str]:
        """List all available providers."""
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type[AIProvider]) -> None:
        """Register a new provider."""
        cls._providers[name] = provider_class


def get_ai_provider() -> AIProvider:
    """Dependency injection helper for FastAPI."""
    return ProviderFactory.get_provider()
