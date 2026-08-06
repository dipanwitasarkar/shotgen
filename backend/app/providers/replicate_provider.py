"""
Replicate AI provider implementation.
Uses Replicate's API to run Stable Diffusion and other models.
"""
import io
import time
import base64
from PIL import Image
import replicate
import httpx

from app.core.config import settings
from app.providers.base import AIProvider, GenerationRequest, GenerationResult


class ReplicateProvider(AIProvider):
    """Replicate.com AI provider."""
    
    # Models optimized for product photography
    MODELS = {
        "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "sdxl-lightning": "bytedance/sdxl-lightning-4step:5f24084160c9089501c1b3545d9be3c27883ae2239b6f412990e82d4a6210f8f",
        "flux-schnell": "black-forest-labs/flux-schnell",
        "flux-dev": "black-forest-labs/flux-dev",
        "realistic-vision": "lucataco/realistic-vision-v5.1:2c8e954decbf70b7607a4414e5785ef9e4de4b8c51d50fb8b8b349160e0ef6bb",
    }
    
    def __init__(self):
        if not settings.replicate_api_token:
            raise ValueError("REPLICATE_API_TOKEN is required")
        self.client = replicate.Client(api_token=settings.replicate_api_token)
        self.default_model = "flux-schnell"
    
    @property
    def name(self) -> str:
        return "replicate"
    
    @property
    def supported_models(self) -> list[str]:
        return list(self.MODELS.keys())
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate product photos using Replicate."""
        start_time = time.time()
        
        # Convert product image to base64
        product_base64 = self._image_to_base64(request.product_image)
        
        # Build the prompt for product photography
        prompt = self._build_prompt(request)
        
        # Get model
        model_id = self.MODELS.get(self.default_model, self.MODELS["flux-schnell"])
        
        # Run generation
        images = []
        seeds = []
        
        for i in range(request.num_variations):
            seed = request.seed + i if request.seed else None
            
            # Use IMAGE-TO-IMAGE with product as input
            output = self.client.run(
                model_id,
                input={
                    "prompt": prompt,
                    "image": f"data:image/png;base64,{product_base64}",  # INPUT IMAGE
                    "width": request.output_width,
                    "height": request.output_height,
                    "num_outputs": 1,
                    "prompt_strength": 0.8,  # How much to follow prompt vs preserve image
                    "seed": seed,
                }
            )
            
            # Download and convert output
            if output:
                image_url = output[0] if isinstance(output, list) else output
                image = await self._download_image(str(image_url))
                images.append(image)
                seeds.append(seed or 0)
        
        generation_time = int((time.time() - start_time) * 1000)
        
        return GenerationResult(
            images=images,
            seeds=seeds,
            provider=self.name,
            model=self.default_model,
            generation_time_ms=generation_time,
            cost_usd=self.estimate_cost(request),
        )
    
    async def health_check(self) -> bool:
        """Check if Replicate is available."""
        try:
            # Simple API check
            self.client.models.get("stability-ai/sdxl")
            return True
        except Exception:
            return False
    
    def estimate_cost(self, request: GenerationRequest) -> float:
        """Estimate cost based on model and variations."""
        # Approximate costs per image
        costs = {
            "sdxl": 0.02,
            "sdxl-lightning": 0.01,
            "flux-schnell": 0.003,
            "flux-dev": 0.03,
            "realistic-vision": 0.02,
        }
        per_image = costs.get(self.default_model, 0.02)
        return per_image * request.num_variations
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build an optimized prompt for product photography."""
        base_prompt = f"""Professional product photography, {request.scene_prompt}, 
        {request.style} style, {request.lighting} lighting, {request.angle} angle view,
        high-end commercial photography, sharp focus, high detail, 
        clean composition, professional studio quality"""
        
        # Add style-specific enhancements
        style_additions = {
            "realistic": "photorealistic, 8k resolution, RAW photo",
            "artistic": "artistic composition, creative lighting, editorial style",
            "minimal": "minimalist, clean background, simple elegant",
            "lifestyle": "lifestyle photography, natural setting, authentic feel",
        }
        
        addition = style_additions.get(request.style, "")
        return f"{base_prompt}, {addition}"
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
    
    async def _download_image(self, url: str) -> Image.Image:
        """Download image from URL."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
