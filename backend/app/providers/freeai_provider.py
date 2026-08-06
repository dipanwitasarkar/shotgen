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
                
                # APPROACH: Generate background, then composite product on top
                # Step 1: Generate JUST the background scene (no product in prompt)
                # Step 2: Composite the product image on top
                
                # Generate background scene WITHOUT the product
                background_prompt = f"{request.scene_prompt}, {request.style} style, {request.lighting} lighting, {request.angle} angle, empty scene, no objects, background only, professional photography, 8k uhd"
                
                payload = {
                    "prompt": background_prompt,
                    "model": "sdxl",
                    # NO image parameter - generate clean background
                    "guidance_scale": request.guidance_scale,
                    "num_inference_steps": request.inference_steps,
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
                
                # Get generated background
                background_img = None
                if "data" in result and len(result["data"]) > 0:
                    img_data = result["data"][0]
                    if "b64_json" in img_data:
                        img_bytes = base64.b64decode(img_data["b64_json"])
                        background_img = Image.open(io.BytesIO(img_bytes))
                    elif "url" in img_data:
                        img_response = await self.client.get(img_data["url"])
                        background_img = Image.open(io.BytesIO(img_response.content))
                else:
                    image_url = result.get("url") or result.get("image_url") or result.get("output_url")
                    if image_url:
                        img_response = await self.client.get(image_url)
                        background_img = Image.open(io.BytesIO(img_response.content))
                
                if not background_img:
                    raise Exception("Free.ai: No background generated")
                
                print(f"[Free.ai] Background generated, compositing product...")
                
                # Composite product onto background
                # Resize product to fit nicely in scene (60-70% of image)
                bg_width, bg_height = background_img.size
                product_img = request.product_image.copy()
                
                # Calculate product size (60% of background)
                scale = 0.6
                product_width = int(bg_width * scale)
                product_height = int(product_img.height * (product_width / product_img.width))
                product_img = product_img.resize((product_width, product_height), Image.Resampling.LANCZOS)
                
                # Center the product
                x = (bg_width - product_width) // 2
                y = (bg_height - product_height) // 2
                
                # Composite (product has transparency from background removal)
                final_img = background_img.copy()
                final_img.paste(product_img, (x, y), product_img if product_img.mode == 'RGBA' else None)
                
                images.append(final_img)
                seeds.append(seed or 0)
                print(f"[Free.ai] Product composited successfully")
            
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
