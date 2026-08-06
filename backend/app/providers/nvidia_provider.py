"""
NVIDIA NIM API provider for image generation.
"""
import asyncio
import base64
import io
import time
from PIL import Image
import httpx

from app.providers.base import AIProvider, GenerationRequest, GenerationResult, build_img2img_prompt, build_background_prompt, composite_product_on_background


class NVIDIAProvider(AIProvider):
    """NVIDIA NIM API provider using Flux and Qwen-Image models."""
    
    MODELS = {
        "flux-schnell": "black-forest-labs/flux.1-schnell",
        "flux-dev": "black-forest-labs/flux.1-dev",
        "sd3.5-large": "stabilityai/stable-diffusion-3.5-large",
        "sd3-medium": "stabilityai/stable-diffusion-3-medium",
        "sdxl": "stabilityai/stable-diffusion-xl",
        "sdxl-turbo": "stabilityai/sdxl-turbo",
    }
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://ai.api.nvidia.com"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "Content-Type": "application/json",
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
        
        # Get model - use runtime settings model if available
        from app.api.routes import get_runtime_settings
        runtime = get_runtime_settings()
        model_key = runtime.get("model", "flux-schnell")
        model_path = self.MODELS.get(model_key, self.MODELS["flux-schnell"])
        
        # NVIDIA uses /v1/genai/{vendor}/{slug} format
        # e.g., /v1/genai/black-forest-labs/flux.1-schnell
        endpoint = f"/v1/genai/{model_path}"
        
        # NVIDIA native payload format
        payload = {
            "prompt": prompt,
            "width": request.output_width,
            "height": request.output_height,
            "guidance_scale": request.guidance_scale,  # From UI slider
            "num_inference_steps": request.inference_steps,  # From UI slider
        }
        
        if request.seed is not None:
            payload["seed"] = request.seed
        
        # For edit models, add the uploaded image
        is_edit_model = "edit" in model_key
        if is_edit_model and hasattr(request, 'input_image') and request.input_image:
            # Convert PIL image to base64
            buffered = io.BytesIO()
            request.input_image.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()
            payload["image"] = img_b64
        
        # Call NVIDIA API (generate multiple images sequentially if needed)
        images = []
        seeds = []
        
        try:
            for _ in range(request.num_variations):
                print(f"[NVIDIA] Endpoint: {endpoint}")
                print(f"[NVIDIA] Payload: {payload}")
                
                response = await self.client.post(
                    endpoint,
                    json=payload,
                )
                
                print(f"[NVIDIA] Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"[NVIDIA] Error: {response.text}")
                
                response.raise_for_status()
                result = response.json()
                
                # NVIDIA FLUX response format
                # {"artifacts": [{"base64": "...", "finishReason": "SUCCESS"}]}
                if "artifacts" in result and len(result["artifacts"]) > 0:
                    img_b64 = result["artifacts"][0]["base64"]
                    img_bytes = base64.b64decode(img_b64)
                    img = Image.open(io.BytesIO(img_bytes))
                    images.append(img)
                    seeds.append(result.get("seed", request.seed or 0))
                else:
                    raise Exception(f"Unexpected response format: {result}")
            
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
            error_detail = e.response.text
            print(f"[NVIDIA] HTTP Error: {e.response.status_code} - {error_detail}")
            raise Exception(f"NVIDIA API error: {e.response.status_code} - {error_detail}")
        except Exception as e:
            print(f"[NVIDIA] Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"NVIDIA generation failed: {str(e)}")
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build prompt using shared img2img prompt builder."""
        return build_img2img_prompt(request)

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
