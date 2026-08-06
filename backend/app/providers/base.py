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


def composite_product_on_background(product_image: Image.Image, background_image: Image.Image, scale: float = 0.6) -> Image.Image:
    """
    Composite product onto background - the RIGHT way to do product photography.
    
    Args:
        product_image: Product with transparent background (from background removal)
        background_image: Generated scene background
        scale: Product size as fraction of background (0.6 = 60%)
    
    Returns:
        Final composited image with product on background
    """
    bg_width, bg_height = background_image.size
    product_img = product_image.copy()
    
    # Calculate product size
    product_width = int(bg_width * scale)
    product_height = int(product_img.height * (product_width / product_img.width))
    product_img = product_img.resize((product_width, product_height), Image.Resampling.LANCZOS)
    
    # Center the product
    x = (bg_width - product_width) // 2
    y = (bg_height - product_height) // 2
    
    # Composite (product has transparency from background removal)
    final_img = background_image.copy()
    final_img.paste(product_img, (x, y), product_img if product_img.mode == 'RGBA' else None)
    
    return final_img


def build_background_prompt(request: GenerationRequest) -> str:
    """
    Build prompt for generating JUST the background scene (no product).
    This is used for the composite approach.
    """
    prompt_parts = [
        f"{request.scene_prompt}, empty scene, no objects, background only",
    ]
    
    # Add style details
    style_descriptors = {
        "realistic": "photorealistic, highly detailed, professional photography",
        "artistic": "artistic composition, creative styling, aesthetic",
        "minimal": "minimalist, clean composition, simple background",
        "lifestyle": "lifestyle photography, natural setting, authentic feel",
        "editorial": "editorial style, magazine quality, sophisticated",
        "cinematic": "cinematic lighting, dramatic composition, film-like quality",
    }
    if request.style in style_descriptors:
        prompt_parts.append(style_descriptors[request.style])
    
    # Add lighting details
    lighting_descriptors = {
        "studio": "professional studio lighting, soft shadows, even illumination",
        "natural": "natural daylight, window light, soft ambient lighting",
        "dramatic": "dramatic lighting, high contrast, deep shadows",
        "soft": "soft diffused lighting, gentle shadows, flattering light",
        "golden_hour": "golden hour lighting, warm sunset glow, soft warm tones",
        "neon": "neon lighting, vibrant colors, glowing accents",
    }
    if request.lighting in lighting_descriptors:
        prompt_parts.append(lighting_descriptors[request.lighting])
    
    # Add quality boosters
    prompt_parts.append("sharp focus, high resolution, professional quality, 8k uhd")
    
    return ", ".join(prompt_parts)


def build_img2img_prompt(request: GenerationRequest) -> str:
    """
    Build a detailed, effective prompt for image-to-image generation.
    Works for all AI models (SDXL, FLUX, SD3, etc.)
    """
    # Start with the main scene - IMPORTANT: tell AI to keep the product
    prompt_parts = [
        f"product photography, keep the product intact and visible, place product in {request.scene_prompt}",
    ]
    
    # Add style details
    style_descriptors = {
        "realistic": "photorealistic, highly detailed, professional photography",
        "artistic": "artistic composition, creative styling, aesthetic",
        "minimal": "minimalist, clean composition, simple background",
        "lifestyle": "lifestyle photography, natural setting, authentic feel",
        "editorial": "editorial style, magazine quality, sophisticated",
        "cinematic": "cinematic lighting, dramatic composition, film-like quality",
    }
    if request.style in style_descriptors:
        prompt_parts.append(style_descriptors[request.style])
    else:
        prompt_parts.append(f"{request.style} style")
    
    # Add lighting details
    lighting_descriptors = {
        "studio": "professional studio lighting, soft shadows, even illumination",
        "natural": "natural daylight, window light, soft ambient lighting",
        "dramatic": "dramatic lighting, high contrast, deep shadows",
        "soft": "soft diffused lighting, gentle shadows, flattering light",
        "golden_hour": "golden hour lighting, warm sunset glow, soft warm tones",
        "neon": "neon lighting, vibrant colors, glowing accents",
    }
    if request.lighting in lighting_descriptors:
        prompt_parts.append(lighting_descriptors[request.lighting])
    else:
        prompt_parts.append(f"{request.lighting} lighting")
    
    # Add camera angle details
    angle_descriptors = {
        "front": "straight-on view, centered composition",
        "45-degree": "45-degree angle, dynamic perspective",
        "top-down": "overhead view, flat lay composition",
        "side": "side view, profile angle",
        "low": "low angle shot, upward perspective",
        "hero": "hero shot, dramatic angle, eye-catching composition",
    }
    if request.angle in angle_descriptors:
        prompt_parts.append(angle_descriptors[request.angle])
    else:
        prompt_parts.append(f"{request.angle} angle")
    
    # Add quality boosters and product preservation instructions
    prompt_parts.append("sharp focus, high resolution, professional quality")
    prompt_parts.append("8k uhd, detailed textures")
    prompt_parts.append("preserve product appearance, do not alter the product itself")
    
    # Join all parts
    full_prompt = ", ".join(prompt_parts)
    
    return full_prompt


def build_negative_prompt() -> str:
    """
    Build negative prompt to prevent AI from altering the product.
    Use this with providers that support negative prompts.
    """
    return "deformed product, distorted product, altered product, different product, product transformation, product mutation, blurry product, low quality product"


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
