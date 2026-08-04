"""
Main image generation service that orchestrates the pipeline.
"""
import io
import uuid
from dataclasses import dataclass
from PIL import Image

from app.providers.base import GenerationRequest, GenerationResult
from app.providers.factory import get_ai_provider
from app.services.background_removal import get_background_removal_service


@dataclass
class ProductShotRequest:
    """High-level request for product shot generation."""
    product_image: Image.Image
    scene: str  # "kitchen counter", "outdoor garden", "white studio", etc.
    style: str = "realistic"
    lighting: str = "studio"
    angle: str = "front"
    width: int = 1024
    height: int = 1024
    variations: int = 1
    remove_background: bool = True
    seed: int | None = None


@dataclass
class ProductShotResult:
    """Result from product shot generation."""
    id: str
    images: list[Image.Image]
    product_cutout: Image.Image  # Product with background removed
    seeds: list[int]
    provider: str
    model: str
    generation_time_ms: int
    cost_usd: float | None


class ImageGenerationService:
    """
    Main service for generating product photos.
    Handles the full pipeline: background removal -> scene generation -> compositing
    """
    
    # Pre-defined scene templates
    SCENE_TEMPLATES = {
        "white_studio": "clean white studio background, soft shadows, professional product photography",
        "kitchen": "modern kitchen counter, marble surface, natural daylight from window",
        "outdoor": "outdoor garden setting, natural greenery, soft sunlight",
        "lifestyle": "cozy home interior, lifestyle setting, warm ambient lighting",
        "minimal": "minimalist background, solid color, clean and simple",
        "luxury": "luxury setting, dark marble, gold accents, dramatic lighting",
        "nature": "natural setting with plants and wood textures, organic feel",
        "tech": "modern tech environment, sleek surfaces, blue accent lighting",
    }
    
    def __init__(self):
        self.bg_service = get_background_removal_service()
        self.ai_provider = get_ai_provider()
    
    async def generate(self, request: ProductShotRequest) -> ProductShotResult:
        """
        Generate product photos.
        
        Pipeline:
        1. Remove background from product image
        2. Generate scene with AI
        3. Return results
        """
        generation_id = str(uuid.uuid4())
        
        # Step 1: Remove background if requested
        if request.remove_background:
            product_cutout = self.bg_service.remove_background(request.product_image)
        else:
            product_cutout = request.product_image
        
        # Step 2: Build scene prompt
        scene_prompt = self._build_scene_prompt(request.scene)
        
        # Step 3: Generate with AI provider
        gen_request = GenerationRequest(
            product_image=product_cutout,
            scene_prompt=scene_prompt,
            style=request.style,
            lighting=request.lighting,
            angle=request.angle,
            output_width=request.width,
            output_height=request.height,
            num_variations=request.variations,
            seed=request.seed,
        )
        
        result = await self.ai_provider.generate(gen_request)
        
        return ProductShotResult(
            id=generation_id,
            images=result.images,
            product_cutout=product_cutout,
            seeds=result.seeds,
            provider=result.provider,
            model=result.model,
            generation_time_ms=result.generation_time_ms,
            cost_usd=result.cost_usd,
        )
    
    def _build_scene_prompt(self, scene: str) -> str:
        """Build scene prompt from template or custom input."""
        # Check if it's a template name
        if scene.lower().replace(" ", "_") in self.SCENE_TEMPLATES:
            return self.SCENE_TEMPLATES[scene.lower().replace(" ", "_")]
        
        # Otherwise use as custom prompt
        return scene
    
    def list_scene_templates(self) -> dict[str, str]:
        """Get available scene templates."""
        return self.SCENE_TEMPLATES.copy()
    
    async def health_check(self) -> dict:
        """Check health of all services."""
        ai_healthy = await self.ai_provider.health_check()
        
        return {
            "status": "healthy" if ai_healthy else "degraded",
            "ai_provider": {
                "name": self.ai_provider.name,
                "healthy": ai_healthy,
            },
            "background_removal": {
                "healthy": True,  # rembg is local, always available
            },
        }


# Singleton
_service: ImageGenerationService | None = None


def get_image_generation_service() -> ImageGenerationService:
    """Get or create the image generation service."""
    global _service
    if _service is None:
        _service = ImageGenerationService()
    return _service


def reset_service():
    """Reset the service to pick up new settings."""
    global _service
    _service = None
