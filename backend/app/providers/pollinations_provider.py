"""
Pollinations.ai provider for FREE image generation.
No API key required, no signup, completely free.
"""
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class PollinationsProvider(AIProvider):
    """Pollinations.ai FREE image generation provider."""
    
    MODELS = {
        "flux": "flux",
        "flux-realism": "flux-realism",
        "flux-anime": "flux-anime",
        "turbo": "turbo",
    }
    
    def __init__(self, api_key: str = ""):
        # No API key needed, but accept it for compatibility
        self.base_url = "https://image.pollinations.ai/prompt"
        self.client = httpx.AsyncClient(
            timeout=120.0,
            follow_redirects=True,
        )
    
    @property
    def name(self) -> str:
        return "pollinations"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Pollinations.ai FREE API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Pollinations uses URL parameters
        # Format: https://image.pollinations.ai/prompt/{prompt}?width={w}&height={h}&model={model}&seed={seed}
        
        images = []
        seeds = []
        
        try:
            for i in range(request.num_variations):
                # Use different seeds for variations
                seed = request.seed if request.seed else int(time.time() * 1000) + i
                
                # Build URL with parameters
                params = {
                    "width": request.output_width,
                    "height": request.output_height,
                    "seed": seed,
                    "model": self.MODELS.get("flux", "flux"),
                    "nologo": "true",  # Remove watermark
                    "enhance": "true",  # Better quality
                }
                
                # URL encode the prompt
                import urllib.parse
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"{self.base_url}/{encoded_prompt}"
                
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                
                # Pollinations returns image bytes directly
                img = Image.open(io.BytesIO(response.content))
                images.append(img)
                seeds.append(seed)
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=seeds,
                provider=self.name,
                model="flux",
                generation_time_ms=generation_time_ms,
                cost_usd=0.0,  # Completely FREE!
            )
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"Pollinations.ai error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Pollinations.ai generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Pollinations.ai."""
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
        """Completely FREE!"""
        return 0.0
    
    async def health_check(self) -> bool:
        """Check if Pollinations.ai is available."""
        try:
            response = await self.client.get(f"{self.base_url}/test")
            return response.status_code in [200, 404]  # 404 is ok, means service is up
        except Exception:
            return False
