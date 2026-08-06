"""
Free.ai provider - FREE image-to-image with no signup required!
6000 tokens/day anonymous, 30000 tokens/day with free account.
"""
import io
import time
import base64
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult, build_img2img_prompt


class FreeAIProvider(AIProvider):
    """Free.ai - FREE img2img provider."""
    
    MODELS = {
        "sdxl": "sdxl",
        "flux-schnell": "flux-schnell",
        "sd-turbo": "sd-turbo",
    }
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key.strip() if api_key else ""  # Remove whitespace
        self.base_url = "https://api.free.ai/v1"
        headers = {}
        if self.api_key and self.api_key != "no-key-needed":
            headers["Authorization"] = f"Bearer {self.api_key}"
        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "freeai"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Free.ai IMAGE-TO-IMAGE API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Convert product image to base64
        img_byte_arr = io.BytesIO()
        request.product_image.save(img_byte_arr, format='PNG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
        
        images = []
        seeds = []
        
        try:
            for i in range(request.num_variations):
                seed = request.seed + i if request.seed else None
                
                # Use JSON payload with base64 image for img2img
                payload = {
                    "prompt": prompt,
                    "model": "sdxl",
                    "image": f"data:image/png;base64,{img_b64}",  # Reference image
                    "strength": request.strength,  # From UI slider
                    "guidance_scale": request.guidance_scale,  # From UI slider
                    "num_inference_steps": request.inference_steps,  # From UI slider
                }
                
                if seed:
                    payload["seed"] = seed
                
                print(f"[Free.ai] IMG2IMG request:")
                print(f"  Model: {payload['model']}")
                print(f"  Prompt: {prompt}")
                print(f"  Strength: {payload['strength']}")
                
                response = await self.client.post(
                    f"{self.base_url}/image/generate/",  # Correct Free.ai endpoint
                    json=payload
                )
                
                print(f"[Free.ai] Response status: {response.status_code}")
                
                if response.status_code != 200:
                    error_text = response.text[:500]
                    print(f"[Free.ai] Error: {error_text}")
                    raise Exception(f"Free.ai API error: {error_text}")
                
                result = response.json()
                print(f"[Free.ai] Response keys: {result.keys()}")
                
                # Try OpenAI-compatible format first: {"data": [{"url": "..." or "b64_json": "..."}]}
                if "data" in result and len(result["data"]) > 0:
                    img_data = result["data"][0]
                    if "b64_json" in img_data:
                        img_bytes = base64.b64decode(img_data["b64_json"])
                        img = Image.open(io.BytesIO(img_bytes))
                        images.append(img)
                        seeds.append(seed or 0)
                        print(f"[Free.ai] Image from b64_json")
                    elif "url" in img_data:
                        print(f"[Free.ai] Downloading from: {img_data['url']}")
                        img_response = await self.client.get(img_data["url"])
                        img = Image.open(io.BytesIO(img_response.content))
                        images.append(img)
                        seeds.append(seed or 0)
                # Fallback to direct URL fields
                else:
                    image_url = result.get("url") or result.get("image_url") or result.get("output_url")
                    if image_url:
                        print(f"[Free.ai] Downloading from: {image_url}")
                        img_response = await self.client.get(image_url)
                        img = Image.open(io.BytesIO(img_response.content))
                        images.append(img)
                        seeds.append(seed or 0)
                    else:
                        print(f"[Free.ai] No image in response: {result}")
                        raise Exception("Free.ai: No image in response")
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=seeds,
                provider=self.name,
                model="sdxl",
                generation_time_ms=generation_time_ms,
                cost_usd=0.0,  # FREE!
            )
        
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg = error_data["error"]
            except:
                pass
            raise Exception(f"Free.ai: {error_msg}")
        except Exception as e:
            if "Free.ai" not in str(e):
                raise Exception(f"Free.ai: {str(e)}")
            raise
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for Free.ai img2img."""
        return build_img2img_prompt(request)
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Completely FREE! 6000 tokens/day anonymous, 30000/day with free account."""
        return 0.0
    
    async def health_check(self) -> bool:
        """Check if Free.ai is available."""
        try:
            response = await self.client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except Exception:
            return False
