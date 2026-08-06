"""
Stability AI provider implementation.
Uses Stability AI's official API.
"""
import io
import time
import base64
from PIL import Image
import httpx

from app.core.config import settings
from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class StabilityProvider(AIProvider):
    """Stability AI official API provider."""
    
    API_BASE = "https://api.stability.ai"
    
    MODELS = {
        "sd3": "sd3",
        "sd3-turbo": "sd3-turbo",
        "sdxl": "stable-diffusion-xl-1024-v1-0",
        "sd-1.6": "stable-diffusion-v1-6",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.default_model = "sd3-turbo"
    
    @property
    def name(self) -> str:
        return "stability"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate product photos using Stability AI IMAGE-TO-IMAGE."""
        start_time = time.time()
        
        prompt = self._build_prompt(request)
        
        images = []
        seeds = []
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            for i in range(request.num_variations):
                seed = request.seed + i if request.seed else 0
                
                # Convert product image to bytes for upload
                img_byte_arr = io.BytesIO()
                request.product_image.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Use IMAGE-TO-IMAGE endpoint with product as input
                response = await client.post(
                    f"{self.API_BASE}/v2beta/stable-image/generate/sd3",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Accept": "image/*",
                    },
                    files={
                        "image": ("product.png", img_byte_arr, "image/png"),
                    },
                    data={
                        "prompt": prompt,
                        "model": self.MODELS[self.default_model],
                        "mode": "image-to-image",  # IMAGE-TO-IMAGE mode
                        "output_format": "png",
                        "strength": 0.5,  # How much to transform (0.0-1.0)
                        "seed": seed,
                    },
                )
                
                print(f"[Stability] Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"[Stability] Error: {response.text}")
                
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    images.append(image)
                    seeds.append(seed)
                else:
                    raise Exception(f"Stability API error: {response.text}")
        
        generation_time = int((time.time() - start_time) * 1000)
        
        return GenerationResult(
            images=images,
            seeds=seeds,
            provider=self.name,
            model=self.default_model,
            generation_time_ms=generation_time,
            cost_usd=self.estimate_cost(request),
        )
    
    async def health_check(self) -> bool:
        """Check if Stability AI is available."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.API_BASE}/v1/user/account",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                return response.status_code == 200
        except Exception:
            return False
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost based on model."""
        costs = {
            "sd3": 0.035,
            "sd3-turbo": 0.02,
            "sdxl": 0.02,
            "sd-1.6": 0.01,
        }
        per_image = costs.get(self.default_model, 0.02)
        return per_image * request.num_variations
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Stability AI."""
        return f"""Professional product photography of a product, {request.scene_prompt},
        {request.style} style, {request.lighting} lighting, {request.angle} angle,
        commercial photography, high resolution, sharp details, studio quality"""
    
    def _get_aspect_ratio(self, request: GenerationRequest) -> str:
        """Get aspect ratio string from dimensions."""
        ratio = request.output_width / request.output_height
        if abs(ratio - 1.0) < 0.1:
            return "1:1"
        elif abs(ratio - 16/9) < 0.1:
            return "16:9"
        elif abs(ratio - 9/16) < 0.1:
            return "9:16"
        elif abs(ratio - 4/3) < 0.1:
            return "4:3"
        elif abs(ratio - 3/4) < 0.1:
            return "3:4"
        else:
            return "1:1"
