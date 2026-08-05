"""
Placeholdr.dev provider for FREE image generation.
No API key required, no signup, completely free.
Uses Cloudflare Workers + Flux model.
"""
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class PlaceholdrProvider(AIProvider):
    """Placeholdr.dev FREE image generation provider."""
    
    MODELS = {
        "photographic": "photographic",
        "artistic": "artistic",
        "anime": "anime",
        "oil-painting": "oil-painting",
        "3d-render": "3d-render",
        "cartoon": "cartoon",
    }
    
    def __init__(self, api_key: str = ""):
        # No API key needed
        self.base_url = "https://placeholdr.dev"
        self.client = httpx.AsyncClient(
            timeout=120.0,
            follow_redirects=True,
        )
    
    @property
    def name(self) -> str:
        return "placeholdr"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Placeholdr.dev FREE API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        images = []
        seeds = []
        
        try:
            for i in range(request.num_variations):
                # Placeholdr supports seeds 1-3
                seed = ((request.seed or int(time.time())) % 3) + 1
                
                # Build URL: https://placeholdr.dev/{width}x{height}/{prompt}?style={style}&seed={seed}
                import urllib.parse
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"{self.base_url}/{request.output_width}x{request.output_height}/{encoded_prompt}"
                
                params = {
                    "style": "photographic",  # Default style
                    "seed": seed,
                }
                
                print(f"[Placeholdr] Requesting: {url} with params: {params}")
                response = await self.client.get(url, params=params)
                print(f"[Placeholdr] Response status: {response.status_code}")
                
                response.raise_for_status()
                
                # Placeholdr returns image bytes directly
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
            error_msg = f"HTTP {e.response.status_code}"
            try:
                error_msg = e.response.text[:200]
            except:
                pass
            raise Exception(f"Placeholdr.dev: {error_msg}")
        except Exception as e:
            error_str = str(e)
            if "Placeholdr" not in error_str:
                raise Exception(f"Placeholdr.dev: {error_str}")
            raise
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Placeholdr.dev."""
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
        """Check if Placeholdr.dev is available."""
        try:
            response = await self.client.get(f"{self.base_url}/128x128/test")
            return response.status_code == 200
        except Exception:
            return False
