"""
NVIDIA NIM API provider for image generation.
"""
import asyncio
import base64
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class NVIDIAProvider(AIProvider):
    """NVIDIA NIM API provider using Flux models."""
    
    MODELS = {
        "flux-schnell": "black-forest-labs/flux-schnell",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.nvcf.nvidia.com/v2/nvcf"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "nvidia"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using NVIDIA NIM API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Convert product image to base64
        buffer = io.BytesIO()
        request.product_image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Prepare request payload
        payload = {
            "prompt": prompt,
            "image": image_b64,
            "width": request.output_width,
            "height": request.output_height,
            "num_outputs": request.num_variations,
            "guidance_scale": 7.5,
            "num_inference_steps": 4,  # Schnell is optimized for 4 steps
        }
        
        if request.seed is not None:
            payload["seed"] = request.seed
        
        # Call NVIDIA API
        try:
            response = await self.client.post(
                "/pexec/functions/black-forest-labs/flux-schnell",
                json=payload,
            )
            response.raise_for_status()
            result = response.json()
            
            # Parse response and download images
            images = []
            seeds = []
            
            if "images" in result:
                for img_data in result["images"]:
                    # If base64 encoded
                    if isinstance(img_data, str):
                        img_bytes = base64.b64decode(img_data)
                        img = Image.open(io.BytesIO(img_bytes))
                        images.append(img)
                    # If URL
                    elif isinstance(img_data, dict) and "url" in img_data:
                        img_response = await self.client.get(img_data["url"])
                        img = Image.open(io.BytesIO(img_response.content))
                        images.append(img)
                
                seeds = result.get("seeds", [request.seed or 0] * len(images))
            
            # Calculate generation time
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=seeds,
                provider=self.name,
                model="flux-schnell",
                generation_time_ms=generation_time_ms,
                cost_usd=self.estimate_cost(request),
            )
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"NVIDIA API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"NVIDIA generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt for NVIDIA API."""
        parts = [
            request.scene_prompt,
            f"{request.style} style",
            f"{request.lighting} lighting",
            f"{request.angle} angle view",
            "professional product photography",
            "high quality",
            "detailed",
        ]
        return ", ".join(parts)
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost for NVIDIA API."""
        # NVIDIA NIM pricing varies, estimate ~$0.003 per image for Flux Schnell
        return 0.003 * request.num_variations
    
    async def health_check(self) -> bool:
        """Check if NVIDIA API is available."""
        try:
            response = await self.client.get("/functions")
            return response.status_code == 200
        except Exception:
            return False
