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
    """NVIDIA NIM API provider using Flux and Qwen-Image models."""
    
    MODELS = {
        "flux-schnell": "black-forest-labs/flux-schnell",
        "qwen-image": "qwen/qwen-image",
        "qwen-image-2512": "qwen/qwen-image-2512",
        "qwen-image-edit": "qwen/qwen-image-edit",
        "qwen-image-edit-2509": "qwen/qwen-image-edit-2509",
        "qwen-image-edit-2511": "qwen/qwen-image-edit-2511",
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
        model_name = self.MODELS.get(model_key, self.MODELS["flux-schnell"])
        
        # NVIDIA uses OpenAI-compatible endpoints
        # Generation: /v1/images/generations
        # Editing: /v1/images/edits
        
        is_edit_model = "edit" in model_key
        endpoint = "/v1/images/edits" if is_edit_model else "/v1/images/generations"
        
        # OpenAI-compatible payload
        payload = {
            "model": model_name,
            "prompt": prompt,
            "n": 1,  # NVIDIA only supports 1 sample at a time
            "size": f"{request.output_width}x{request.output_height}",
        }
        
        if request.seed is not None:
            payload["seed"] = request.seed
        
        # For edit models, add the uploaded image
        if is_edit_model and hasattr(request, 'input_image') and request.input_image:
            # Convert PIL image to base64
            buffered = io.BytesIO()
            request.input_image.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()
            payload["image"] = f"data:image/png;base64,{img_b64}"
        
        # Call NVIDIA API (generate multiple images sequentially if needed)
        images = []
        seeds = []
        
        try:
            for _ in range(request.num_variations):
                response = await self.client.post(
                    endpoint,
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                
                # OpenAI-compatible response format
                # {"data": [{"b64_json": "...", "revised_prompt": "..."}]}
                if "data" in result and len(result["data"]) > 0:
                    img_data = result["data"][0]
                    if "b64_json" in img_data:
                        img_b64 = img_data["b64_json"]
                        img_bytes = base64.b64decode(img_b64)
                        img = Image.open(io.BytesIO(img_bytes))
                        images.append(img)
                        seeds.append(request.seed or 0)
                    elif "url" in img_data:
                        # Some models return URL instead
                        raise Exception("URL response not supported yet")
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
