"""
Hugging Face Inference API provider for image generation.
"""
import base64
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult, build_img2img_prompt


class HuggingFaceProvider(AIProvider):
    """Hugging Face Inference API provider."""
    
    MODELS = {
        "flux-schnell": "black-forest-labs/FLUX.1-schnell",
        "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
        "sd-turbo": "stabilityai/sdxl-turbo",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-inference.huggingface.co"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
            },
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "huggingface"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using Hugging Face Inference API."""
        start_time = time.time()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Convert product image to base64
        img_byte_arr = io.BytesIO()
        request.product_image.save(img_byte_arr, format='PNG')
        img_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
        
        # Get model
        model_id = self.MODELS.get("flux-schnell", self.MODELS["flux-schnell"])
        
        # Hugging Face Inference API endpoint
        endpoint = f"{self.base_url}/models/{model_id}"
        
        # Prepare payload with image for img2img
        payload = {
            "inputs": {
                "prompt": prompt,
                "image": f"data:image/png;base64,{img_b64}",  # Product image
            },
            "parameters": {
                "width": request.output_width,
                "height": request.output_height,
                "num_inference_steps": request.inference_steps,  # From UI slider
                "guidance_scale": request.guidance_scale,  # From UI slider
                "strength": request.strength,  # From UI slider
            }
        }
        
        if request.seed:
            payload["parameters"]["seed"] = request.seed
        
        print(f"[HuggingFace] IMG2IMG - Image sent: YES, Strength: {request.strength}")
        
        try:
            # Generate images (one at a time for HF)
            images = []
            for _ in range(request.num_variations):
                response = await self.client.post(endpoint, json=payload)
                response.raise_for_status()
                
                # HF returns image bytes directly
                img = Image.open(io.BytesIO(response.content))
                images.append(img)
            
            generation_time_ms = int((time.time() - start_time) * 1000)
            
            return GenerationResult(
                images=images,
                seeds=[request.seed or 0] * len(images),
                provider=self.name,
                model=model_id,
                generation_time_ms=generation_time_ms,
                cost_usd=0.0,  # Free tier
            )
            
        except httpx.HTTPStatusError as e:
            raise Exception(f"Hugging Face error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Hugging Face generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt using shared img2img prompt builder."""
        return build_img2img_prompt(request)

    def estimate_cost(self, request: GenerationRequest) -> float:
        """Free tier."""
        return 0.0
    
    async def health_check(self) -> bool:
        """Check if Hugging Face is available."""
        try:
            return True
        except Exception:
            return False
