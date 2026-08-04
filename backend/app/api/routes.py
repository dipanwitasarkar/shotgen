"""
API routes for ShotGen.
"""
import io
import base64
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
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
async def health_check(
    service: ImageGenerationService = Depends(get_image_generation_service),
):
    """Check health of all services."""
    health = await service.health_check()
    return HealthResponse(**health)
