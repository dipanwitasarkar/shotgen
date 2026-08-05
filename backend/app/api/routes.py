"""
API routes for ShotGen.
"""
import io
import base64
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image

from app.services.image_generation import (
    ImageGenerationService,
    ProductShotRequest,
    get_image_generation_service,
)
from app.services.background_removal import (
    BackgroundRemovalService,
    get_background_removal_service,
)
from app.providers.factory import ProviderFactory


router = APIRouter()

# Runtime settings storage (in production, use Redis or database)
_runtime_settings: dict = {
    "provider": None,
    "model": None,
    "api_key": None,
}


def get_runtime_settings():
    """Get current runtime settings."""
    return _runtime_settings


# Response Models
class GenerationResponse(BaseModel):
    """Response from image generation."""
    id: str
    images: list[str]  # Base64 encoded images
    product_cutout: str  # Base64 encoded cutout
    seeds: list[int]
    provider: str
    model: str
    generation_time_ms: int
    cost_usd: float | None


class SceneTemplatesResponse(BaseModel):
    """Available scene templates."""
    templates: dict[str, str]


class ProvidersResponse(BaseModel):
    """Available AI providers."""
    providers: list[str]
    current: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    ai_provider: dict
    background_removal: dict


class SettingsRequest(BaseModel):
    """Settings update request."""
    provider: str
    model: str
    apiKey: str


class SettingsResponse(BaseModel):
    """Settings response."""
    provider: str
    model: str
    configured: bool


class ModelsResponse(BaseModel):
    """Available models response."""
    models: dict[str, list[dict]]


# Helper functions
def image_to_base64(image: Image.Image, format: str = "PNG") -> str:
    """Convert PIL Image to base64 string."""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode()


def load_image_from_upload(file: UploadFile) -> Image.Image:
    """Load PIL Image from uploaded file."""
    try:
        return Image.open(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")


# Routes
@router.post("/generate", response_model=GenerationResponse)
async def generate_product_shot(
    image: Annotated[UploadFile, File(description="Product image to process")],
    scene: Annotated[str, Form(description="Scene description or template name")] = "white_studio",
    style: Annotated[str, Form(description="Style: realistic, artistic, minimal, lifestyle")] = "realistic",
    lighting: Annotated[str, Form(description="Lighting: studio, natural, dramatic, soft")] = "studio",
    angle: Annotated[str, Form(description="Angle: front, 45-degree, top-down")] = "front",
    width: Annotated[int, Form(description="Output width", ge=256, le=4096)] = 1024,
    height: Annotated[int, Form(description="Output height", ge=256, le=4096)] = 1024,
    variations: Annotated[int, Form(description="Number of variations", ge=1, le=4)] = 1,
    remove_background: Annotated[bool, Form(description="Remove background first")] = True,
    seed: Annotated[int | None, Form(description="Random seed for reproducibility")] = None,
    service: ImageGenerationService = Depends(get_image_generation_service),
):
    """
    Generate professional product photos.
    
    Upload a product image and get back studio-quality lifestyle shots.
    """
    # Load image
    product_image = load_image_from_upload(image)
    
    # Create request
    request = ProductShotRequest(
        product_image=product_image,
        scene=scene,
        style=style,
        lighting=lighting,
        angle=angle,
        width=width,
        height=height,
        variations=variations,
        remove_background=remove_background,
        seed=seed,
    )
    
    # Generate
    try:
        result = await service.generate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")
    
    # Convert images to base64
    images_b64 = [image_to_base64(img) for img in result.images]
    cutout_b64 = image_to_base64(result.product_cutout)
    
    return GenerationResponse(
        id=result.id,
        images=images_b64,
        product_cutout=cutout_b64,
        seeds=result.seeds,
        provider=result.provider,
        model=result.model,
        generation_time_ms=result.generation_time_ms,
        cost_usd=result.cost_usd,
    )


@router.post("/remove-background")
async def remove_background(
    image: Annotated[UploadFile, File(description="Image to remove background from")],
    service: BackgroundRemovalService = Depends(get_background_removal_service),
):
    """
    Remove background from an image.
    
    Returns PNG with transparent background.
    """
    # Load image
    input_image = load_image_from_upload(image)
    
    # Remove background
    try:
        result = service.remove_background(input_image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background removal failed: {e}")
    
    # Return as PNG
    buffer = io.BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=cutout.png"},
    )


@router.get("/scenes", response_model=SceneTemplatesResponse)
async def get_scene_templates(
    service: ImageGenerationService = Depends(get_image_generation_service),
):
    """Get available scene templates."""
    return SceneTemplatesResponse(templates=service.list_scene_templates())


@router.get("/providers", response_model=ProvidersResponse)
async def get_providers():
    """Get available AI providers."""
    from app.core.config import settings
    
    return ProvidersResponse(
        providers=ProviderFactory.list_providers(),
        current=settings.ai_provider,
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check health of all services."""
    from app.core.config import settings
    
    runtime = get_runtime_settings()
    
    # Check if API key is configured (runtime or env)
    ai_healthy = False
    ai_name = runtime.get("provider") or settings.ai_provider
    
    # Check runtime settings first, then env
    if runtime.get("api_key"):
        ai_healthy = True
    elif settings.ai_provider == "replicate" and settings.replicate_api_token:
        ai_healthy = True
    elif settings.ai_provider == "stability" and settings.stability_api_key:
        ai_healthy = True
    
    return HealthResponse(
        status="healthy" if ai_healthy else "degraded",
        ai_provider={
            "name": ai_name,
            "healthy": ai_healthy,
            "message": "API key configured" if ai_healthy else "API key not configured - add in Settings panel"
        },
        background_removal={
            "healthy": True,
            "message": "rembg ready"
        }
    )


@router.post("/settings", response_model=SettingsResponse)
async def update_settings(request: SettingsRequest):
    """Update runtime settings (provider, model, API key)."""
    global _runtime_settings
    
    _runtime_settings["provider"] = request.provider
    _runtime_settings["model"] = request.model
    _runtime_settings["api_key"] = request.apiKey
    
    # Reset the cached service so it picks up new settings
    from app.services.image_generation import reset_service
    reset_service()
    
    return SettingsResponse(
        provider=request.provider,
        model=request.model,
        configured=bool(request.apiKey),
    )


@router.get("/settings", response_model=SettingsResponse)
async def get_settings():
    """Get current settings."""
    from app.core.config import settings
    
    runtime = get_runtime_settings()
    
    return SettingsResponse(
        provider=runtime.get("provider") or settings.ai_provider,
        model=runtime.get("model") or "flux-schnell",
        configured=bool(runtime.get("api_key") or settings.replicate_api_token or settings.stability_api_key),
    )


@router.get("/models", response_model=ModelsResponse)
async def get_available_models():
    """Get available models for each provider."""
    return ModelsResponse(
        models={
            "nvidia": [
                {"id": "flux-schnell", "name": "FLUX.1 Schnell", "description": "Very fast, 4 steps"},
                {"id": "flux-dev", "name": "FLUX.1 Dev", "description": "High quality, 20-50 steps"},
                {"id": "sd3.5-large", "name": "Stable Diffusion 3.5 Large", "description": "8B params, highest quality"},
                {"id": "sd3-medium", "name": "Stable Diffusion 3 Medium", "description": "High quality, balanced"},
                {"id": "sdxl", "name": "Stable Diffusion XL", "description": "Classic, high quality"},
                {"id": "sdxl-turbo", "name": "SDXL Turbo", "description": "Fast, 1-4 steps"},
            ],
            "together": [
                {"id": "flux-schnell-free", "name": "FLUX.1 Schnell (Free)", "description": "⭐ FREE - 3 months unlimited"},
                {"id": "flux-schnell", "name": "FLUX.1 Schnell", "description": "Fast, good quality"},
                {"id": "flux-dev", "name": "FLUX.2 Dev", "description": "High quality, customizable"},
                {"id": "flux-pro", "name": "FLUX.1.1 Pro", "description": "Best quality"},
            ],
            "huggingface": [
                {"id": "flux-schnell", "name": "FLUX.1 Schnell", "description": "Free tier - Fast"},
                {"id": "sdxl", "name": "Stable Diffusion XL", "description": "Free tier - High quality"},
                {"id": "sd-turbo", "name": "SDXL Turbo", "description": "Free tier - Ultra fast"},
            ],
            "replicate": [
                {"id": "sdxl", "name": "Stable Diffusion XL", "description": "Best quality, slower"},
                {"id": "sdxl-lightning", "name": "SDXL Lightning", "description": "Fast, good quality"},
                {"id": "flux-schnell", "name": "Flux Schnell", "description": "Very fast, free tier"},
                {"id": "flux-dev", "name": "Flux Dev", "description": "High quality, slower"},
            ],
            "stability": [
                {"id": "sd3", "name": "Stable Diffusion 3", "description": "Latest model"},
                {"id": "sdxl-1.0", "name": "SDXL 1.0", "description": "Production ready"},
                {"id": "sd-turbo", "name": "SD Turbo", "description": "Ultra fast"},
            ],
        }
    )
