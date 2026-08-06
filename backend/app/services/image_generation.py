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
    strength: float = 0.85
    guidance_scale: float = 7.5
    inference_steps: int = 30


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
    
    # Pre-defined scene templates - organized by category
    SCENE_TEMPLATES = {
        # Studio & Professional
        "white_studio": "clean white studio background, soft shadows, professional product photography, commercial quality",
        "black_studio": "elegant black studio background, dramatic rim lighting, high-end product photography",
        "gradient_studio": "smooth gradient background, professional studio lighting, clean commercial look",
        "minimal": "minimalist background, solid neutral color, clean and simple, modern aesthetic",
        
        # Home & Living
        "kitchen": "modern kitchen counter, marble surface, natural daylight from window, lifestyle photography",
        "bathroom": "luxury bathroom vanity, marble countertop, soft natural light, spa-like atmosphere",
        "living_room": "cozy living room setting, soft sofa, warm ambient lighting, lifestyle feel",
        "bedroom": "elegant bedroom setting, soft bedding, morning light through curtains, peaceful mood",
        "dining": "dining table setting, elegant tableware, warm candlelight ambiance, dinner party mood",
        "office": "modern home office desk, clean workspace, natural window light, productive atmosphere",
        
        # Outdoor & Nature
        "outdoor": "outdoor garden setting, natural greenery, soft sunlight, fresh organic feel",
        "beach": "sandy beach setting, ocean waves in background, golden hour sunlight, vacation vibes",
        "forest": "forest floor setting, moss and ferns, dappled sunlight through trees, natural organic",
        "mountain": "mountain landscape background, crisp clean air feel, adventure outdoor setting",
        "park": "city park setting, green grass, trees, natural daylight, urban nature",
        
        # Lifestyle & Social
        "cafe": "cozy cafe table, coffee shop ambiance, warm lighting, rustic wood textures",
        "restaurant": "upscale restaurant table, elegant dining setting, ambient mood lighting",
        "gym": "modern fitness studio, gym equipment background, energetic lighting, active lifestyle",
        "yoga": "peaceful yoga studio, natural materials, soft diffused light, zen atmosphere",
        "pool": "poolside setting, blue water reflections, summer vibes, resort luxury",
        
        # Luxury & Premium
        "luxury": "luxury setting, dark marble, gold accents, dramatic lighting, premium feel",
        "jewelry": "velvet display surface, soft spotlight, luxury jewelry presentation, elegant",
        "fashion": "fashion runway backdrop, dramatic lighting, high-end editorial style",
        "art_gallery": "white gallery wall, museum lighting, artistic presentation, sophisticated",
        
        # Tech & Modern
        "tech": "modern tech environment, sleek surfaces, blue accent lighting, futuristic feel",
        "gaming": "RGB gaming setup, neon accents, dark background, tech enthusiast aesthetic",
        "workspace": "modern workspace, clean desk setup, tech accessories, productivity aesthetic",
        
        # Seasonal & Holiday
        "christmas": "festive holiday setting, christmas decorations, warm cozy lighting, winter mood",
        "autumn": "autumn leaves, warm orange tones, rustic wood, harvest season feel",
        "spring": "fresh spring flowers, pastel colors, bright natural light, renewal theme",
        "summer": "bright summer setting, vibrant colors, outdoor sunshine, energetic mood",
        
        # Food & Beverage
        "food_flat": "flat lay food photography, marble surface, ingredients scattered artfully",
        "rustic_food": "rustic wooden table, natural ingredients, farmhouse kitchen style",
        "bar": "cocktail bar setting, dark moody lighting, sophisticated drinks presentation",
        
        # Nature & Organic
        "nature": "natural setting with plants and wood textures, organic feel, earthy tones",
        "botanical": "botanical garden setting, lush greenery, natural light, plant lover aesthetic",
        "stone": "natural stone surface, raw textures, earthy organic feel, grounded aesthetic",
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
            strength=request.strength,
            guidance_scale=request.guidance_scale,
            inference_steps=request.inference_steps,
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
