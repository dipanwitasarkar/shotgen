"""
Factory for creating AI providers.
"""
from app.core.config import settings
from app.providers.base import AIProvider
from app.providers.replicate_provider import ReplicateProvider
from app.providers.stability_provider import StabilityProvider
from app.providers.nvidia_provider import NVIDIAProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""
    
    _providers: dict[str, type[AIProvider]] = {
        "replicate": ReplicateProvider,
        "stability": StabilityProvider,
        "nvidia": NVIDIAProvider,
        # Add more providers here:
        # "comfyui": ComfyUIProvider,
        # "fal": FALProvider,
    }
    
    @classmethod
    def get_provider(cls, provider_name: str | None = None) -> AIProvider:
        """
        Get an AI provider instance.
        
        Args:
            provider_name: Name of provider, or None to use default from settings
            
        Returns:
            AIProvider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        name = provider_name or settings.ai_provider
        
        if name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ValueError(f"Unknown provider: {name}. Available: {available}")
        
        return cls._providers[name]()
    
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
