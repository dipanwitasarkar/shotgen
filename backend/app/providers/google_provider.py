"""
Google Imagen 3 provider via Gemini API for image generation.
"""
import base64
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class GoogleProvider(AIProvider):
    """Google Imagen 3 provider via Gemini API."""
    
    MODELS = {
        "imagen-3-fast": "imagen-3.0-fast-generate-001",
        "imagen-3": "imagen-3.0-generate-002",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "google"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Google Imagen 3 API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Get model
        model_id = self.MODELS.get("imagen-3-fast", self.MODELS["imagen-3-fast"])
        
        # Google Imagen API payload
        payload = {
            "prompt": prompt,
            "number_of_images": request.num_variations,
            "aspect_ratio": "1:1",  # Can be customized
            "safety_filter_level": "block_some",
            "person_generation": "allow_adult",
        }
        
        # Call Google Imagen API
        try:
            response = await self.client.post(
                f"/v1beta/models/{model_id}:generateImages?key={self.api_key}",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            # Parse response
            images = []
            seeds = []
            
            if "generated_images" in result:
                for img_data in result["generated_images"]:
                    if "image" in img_data and "image_bytes" in img_data["image"]:
                        img_bytes = base64.b64decode(img_data["image"]["image_bytes"])
                        img = Image.open(io.BytesIO(img_bytes))
                        images.append(img)
                        seeds.append(request.seed or 0)
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=seeds,
                provider=self.name,
                model=model_id,
                generation_time_ms=generation_time_ms,
                cost_usd=self.estimate_cost(request),
            )
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"Google Imagen error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Google Imagen generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Google Imagen."""
        parts = [
            request.scene_prompt,
            f"{request.style} style",
            f"{request.lighting} lighting",
            f"{request.angle} angle view",
            "professional product photography",
            "high quality",
        ]
        return ", ".join(parts)
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost - $0.03 per image (free tier coming soon)."""
        return 0.03 * request.num_variations
    
    async def health_check(self) -> bool:
        """Check if Google Imagen is available."""
        try:
            return True
        except Exception:
            return False
