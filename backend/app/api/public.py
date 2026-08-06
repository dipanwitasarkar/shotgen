"""
Public API endpoints for developers.
Requires API key authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Header, File, Form, UploadFile
from typing import Annotated
from PIL import Image

from app.api.routes import GenerationResponse, image_to_base64, load_image_from_upload
from app.services.image_generation import ImageGenerationService, ProductShotRequest, get_image_generation_service

router = APIRouter(prefix="/public", tags=["Public API"])

# Simple API key validation (in production, use proper auth)
async def verify_api_key(x_api_key: Annotated[str | None, Header()] = None):
    """Verify API key from header."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required. Include X-API-Key header.")
    
    # In production, validate against database
    # For now, just check it's not empty
    if len(x_api_key) < 10:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return x_api_key


@router.post("/v1/generate", response_model=GenerationResponse)
async def public_generate(
    # Required
    image: Annotated[UploadFile, File(description="Product image")],
    scene: Annotated[str, Form(description="Scene description")] = "white_studio",
    
    # Optional - Basic
    style: Annotated[str, Form()] = "realistic",
    lighting: Annotated[str, Form()] = "studio",
    angle: Annotated[str, Form()] = "front",
    width: Annotated[int, Form(ge=256, le=4096)] = 1024,
    height: Annotated[int, Form(ge=256, le=4096)] = 1024,
    variations: Annotated[int, Form(ge=1, le=4)] = 1,
    
    # Optional - Advanced
    strength: Annotated[float, Form(ge=0.0, le=1.0)] = 0.5,
    guidanceScale: Annotated[float, Form(ge=1.0, le=20.0)] = 7.5,
    inferenceSteps: Annotated[int, Form(ge=10, le=50)] = 30,
    useInpainting: Annotated[bool, Form()] = True,
    useControlNet: Annotated[bool, Form()] = False,
    customBackground: Annotated[UploadFile | None, File()] = None,
    
    # Dependencies
    api_key: str = Depends(verify_api_key),
    service: ImageGenerationService = Depends(get_image_generation_service),
):
    """
    **Public API for Product Photography Generation**
    
    Generate professional product photos programmatically.
    
    **Authentication:**
    - Include `X-API-Key` header with your API key
    
    **Rate Limits:**
    - Free tier: 10 requests/hour
    - Pro tier: 100 requests/hour
    - Enterprise: Unlimited
    
    **Example:**
    ```bash
    curl -X POST https://api.shotgen.ai/api/v1/public/v1/generate \\
      -H "X-API-Key: your-api-key" \\
      -F "image=@product.png" \\
      -F "scene=beach" \\
      -F "style=realistic" \\
      -F "useInpainting=true"
    ```
    
    **Response:**
    - `id`: Generation ID
    - `images`: Array of base64-encoded images
    - `provider`: AI provider used
    - `cost_usd`: Cost in USD (if applicable)
    """
    # Load images
    product_image = load_image_from_upload(image)
    custom_bg = load_image_from_upload(customBackground) if customBackground else None
    
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
        remove_background=True,  # Always remove background for public API
        strength=strength,
        guidance_scale=guidanceScale,
        inference_steps=inferenceSteps,
        use_inpainting=useInpainting,
        use_controlnet=useControlNet,
        custom_background=custom_bg,
    )
    
    # Generate
    try:
        result = await service.generate(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")
    
    # Convert images to base64
    images_b64 = [image_to_base64(img) for img in result.images]
    product_cutout_b64 = image_to_base64(result.product_cutout)
    
    return GenerationResponse(
        id=result.id,
        images=images_b64,
        product_cutout=product_cutout_b64,
        seeds=result.seeds,
        provider=result.provider,
        model=result.model,
        generation_time_ms=result.generation_time_ms,
        cost_usd=result.cost_usd,
    )


@router.get("/v1/docs")
async def api_documentation():
    """
    Get API documentation and examples.
    """
    return {
        "name": "ShotGen Public API",
        "version": "1.0.0",
        "description": "Generate professional product photography with AI",
        "authentication": {
            "type": "API Key",
            "header": "X-API-Key",
            "get_key": "https://shotgen.ai/dashboard/api-keys"
        },
        "endpoints": {
            "/public/v1/generate": {
                "method": "POST",
                "description": "Generate product photos",
                "parameters": {
                    "image": "Product image file (required)",
                    "scene": "Scene template or custom description",
                    "style": "realistic | artistic | minimal | lifestyle",
                    "lighting": "studio | natural | dramatic | soft",
                    "useInpainting": "Preserve product (recommended: true)",
                    "useControlNet": "Preserve structure (advanced)",
                }
            }
        },
        "examples": {
            "python": """
import requests

response = requests.post(
    'https://api.shotgen.ai/api/v1/public/v1/generate',
    headers={'X-API-Key': 'your-api-key'},
    files={'image': open('product.png', 'rb')},
    data={
        'scene': 'beach',
        'style': 'realistic',
        'useInpainting': 'true',
        'variations': 2
    }
)

result = response.json()
print(f"Generated {len(result['images'])} images")
""",
            "curl": """
curl -X POST https://api.shotgen.ai/api/v1/public/v1/generate \\
  -H "X-API-Key: your-api-key" \\
  -F "image=@product.png" \\
  -F "scene=beach" \\
  -F "style=realistic" \\
  -F "useInpainting=true" \\
  -F "variations=2"
""",
            "javascript": """
const formData = new FormData();
formData.append('image', productFile);
formData.append('scene', 'beach');
formData.append('style', 'realistic');
formData.append('useInpainting', 'true');

const response = await fetch('https://api.shotgen.ai/api/v1/public/v1/generate', {
  method: 'POST',
  headers: {
    'X-API-Key': 'your-api-key'
  },
  body: formData
});

const result = await response.json();
console.log(`Generated ${result.images.length} images`);
"""
        },
        "rate_limits": {
            "free": "10 requests/hour",
            "pro": "100 requests/hour",
            "enterprise": "Unlimited"
        },
        "pricing": {
            "free": "$0 - 10 generations/hour",
            "pro": "$29/month - 100 generations/hour",
            "enterprise": "Custom pricing - Unlimited"
        }
    }
