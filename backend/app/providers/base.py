"""
Base class for AI providers.
All providers must implement this interface.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from PIL import Image


@dataclass
class GenerationRequest:
    """Request for image generation."""
    product_image: Image.Image  # Product with background removed
    scene_prompt: str  # Description of the scene
    style: str = "realistic"  # realistic, artistic, minimal, etc.
    lighting: str = "studio"  # studio, natural, dramatic, soft
    angle: str = "front"  # front, 45-degree, top-down, etc.
    output_width: int = 1024
    output_height: int = 1024
    num_variations: int = 1
    seed: int | None = None
    strength: float = 0.85  # IMG2IMG transformation strength (0-1)
    guidance_scale: float = 7.5  # How closely to follow prompt (1-20)
    inference_steps: int = 30  # Quality steps (10-50)


@dataclass
class GenerationResult:
    """Result from image generation."""
    images: list[Image.Image]
    seeds: list[int]
    provider: str
    model: str
    generation_time_ms: int
    cost_usd: float | None = None


class AIProvider(ABC):
    """Abstract base class for AI image generation providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass
    
    @property
    @abstractmethod
    def supported_models(self) -> list[str]:
        """List of supported models."""
        pass
    
    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Generate product photos based on the request.
        
        Args:
            request: Generation parameters
            
        Returns:
            GenerationResult with generated images
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available."""
        pass
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost for generation (override in subclass)."""
        return 0.0
