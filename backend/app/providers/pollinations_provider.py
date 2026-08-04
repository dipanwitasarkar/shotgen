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
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://image.pollinations.ai/prompt"
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        self.client = httpx.AsyncClient(
            headers=headers,
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
                # Pollinations max seed is 2147483647 (32-bit signed int max)
                if request.seed:
                    seed = min(request.seed + i, 2147483647)
                else:
                    seed = (int(time.time()) + i) % 2147483647
                
                # Build URL with minimal parameters for free tier
                # Note: Free tier has rate limits (1 req/15s for anonymous)
                # Use simple parameters that don't require pollen
                params = {
                    "width": request.output_width,
                    "height": request.output_height,
                    "seed": seed,
                    "nologo": "true",  # Remove watermark
                }
                
                # URL encode the prompt
                import urllib.parse
                encoded_prompt = urllib.parse.quote(prompt)
                url = f"{self.base_url}/{encoded_prompt}"
                
                print(f"[Pollinations] Requesting: {url} with params: {params}")
                response = await self.client.get(url, params=params)
                print(f"[Pollinations] Response status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"[Pollinations] Error response: {response.text[:500]}")
                
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
            # Extract user-friendly error message
            error_msg = "Service temporarily unavailable"
            
            # Handle specific error codes
            if e.response.status_code == 402:
                error_msg = "Free tier limit reached. Pollinations requires an API key for enhanced features. Try again in 15 seconds or use a different provider."
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Free tier: 1 request per 15 seconds. Please wait and try again."
            else:
                try:
                    error_data = e.response.json()
                    if "message" in error_data:
                        error_msg = error_data["message"]
                    elif "error" in error_data and isinstance(error_data["error"], dict):
                        error_msg = error_data["error"].get("message", error_msg)
                except:
                    pass
            
            raise Exception(f"Pollinations.ai: {error_msg}")
        except Exception as e:
            # Clean up error message
            error_str = str(e)
            if "Pollinations.ai" not in error_str:
                raise Exception(f"Pollinations.ai: {error_str}")
            raise
    
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
