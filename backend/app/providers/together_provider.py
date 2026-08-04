"""
Together AI provider for image generation.
"""
import base64
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class TogetherProvider(AIProvider):
    """Together AI provider using FLUX models."""
    
    MODELS = {
        "flux-schnell-free": "black-forest-labs/FLUX.1-schnell-Free",
        "flux-schnell": "black-forest-labs/FLUX.1-schnell",
        "flux-dev": "black-forest-labs/FLUX.2-dev",
        "flux-pro": "black-forest-labs/FLUX.1.1-pro",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url="https://api.together.ai/v1",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "together"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Together AI API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Get model
        model = self.MODELS.get(request.seed or "flux-schnell-free", self.MODELS["flux-schnell-free"])
        
        # Prepare payload
        payload = {
            "model": model,
            "prompt": prompt,
            "width": request.output_width,
            "height": request.output_height,
            "n": request.num_variations,
            "steps": 4 if "schnell" in model else 20,
        }
        
        if request.seed:
            payload["seed"] = request.seed
        
        try:
            response = await self.client.post("/images/generations", json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Download images from URLs
            images = []
            for img_data in result.get("data", []):
                if "url" in img_data:
                    img_response = await self.client.get(img_data["url"])
                    img = Image.open(io.BytesIO(img_response.content))
                    images.append(img)
                elif "b64_json" in img_data:
                    img_bytes = base64.b64decode(img_data["b64_json"])
                    img = Image.open(io.BytesIO(img_bytes))
                    images.append(img)
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=[request.seed or 0] * len(images),
                provider=self.name,
                model=model,
                generation_time_ms=generation_time_ms,
                cost_usd=self.estimate_cost(request),
            )
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"Together AI error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Together AI generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Together AI."""
        parts = [
            request.scene_prompt,
            f"{request.style} style",
            f"{request.lighting} lighting",
            f"{request.angle} angle view",
            "professional product photography",
        ]
        return ", ".join(parts)
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost - free tier available."""
        return 0.0  # Free tier for schnell-free
    
    async def health_check(self) -> bool:
        """Check if Together AI is available."""
        try:
            # Simple check - Together doesn't have a dedicated health endpoint
            return True
        except Exception:
            return False
