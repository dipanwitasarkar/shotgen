# Adding New AI Providers and Models

> **Note**: You can now add custom providers and models directly from the UI! Click Settings → "Add Custom" in the app. This guide is for developers who want to add providers that require custom API logic or contribute to the codebase.

This guide shows you how to extend ShotGen with new AI providers and models in the code.

## Quick: Add Models to Existing Providers

### 1. Update Frontend Model List

Edit `frontend/components/SettingsPanel.tsx`:

```typescript
const PROVIDERS = [
  {
    id: 'replicate',
    name: 'Replicate',
    models: [
      // Existing models...
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'Best quality, slower' },
      
      // Add new models here:
      { id: 'playground-v2.5', name: 'Playground v2.5', description: 'High quality, fast' },
      { id: 'juggernaut-xl', name: 'Juggernaut XL', description: 'Photorealistic' },
      { id: 'realvisxl', name: 'RealVisXL', description: 'Ultra realistic' },
    ],
  },
]
```

### 2. Update Backend Model List

Edit `backend/app/api/routes.py` in the `/models` endpoint:

```python
@router.get("/models", response_model=ModelsResponse)
async def get_available_models():
    return ModelsResponse(
        models={
            "replicate": [
                {"id": "sdxl", "name": "Stable Diffusion XL", "description": "Best quality, slower"},
                # Add new models:
                {"id": "playground-v2.5", "name": "Playground v2.5", "description": "High quality, fast"},
                {"id": "juggernaut-xl", "name": "Juggernaut XL", "description": "Photorealistic"},
            ],
        }
    )
```

### 3. Update Provider Implementation

Edit the provider file (e.g., `backend/app/providers/replicate_provider.py`):

```python
class ReplicateProvider(AIProvider):
    MODELS = {
        "sdxl": "stability-ai/sdxl:...",
        "flux-schnell": "black-forest-labs/flux-schnell",
        
        # Add new model mappings:
        "playground-v2.5": "playgroundai/playground-v2.5-1024px-aesthetic",
        "juggernaut-xl": "lucataco/juggernaut-xl-v9",
        "realvisxl": "lucataco/realvisxl-v4.0",
    }
```

That's it! The model will now appear in the Settings panel.

---

## Advanced: Add a Completely New Provider

### Step 1: Create Provider Class

Create `backend/app/providers/your_provider.py`:

```python
"""
Your Custom AI Provider
"""
import httpx
from typing import Optional
from app.providers.base import AIProvider, GenerationRequest, GenerationResult
from PIL import Image
import io
import base64

class YourProvider(AIProvider):
    """Your custom AI provider implementation."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url="https://api.yourprovider.com",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=120.0,
        )
    
    @property
    def name(self) -> str:
        return "yourprovider"
    
    @property
    def supported_models(self) -> list[str]:
        return ["model-1", "model-2", "model-3"]
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        """Generate images using your provider's API."""
        
        # Convert PIL Image to base64 for API
        buffer = io.BytesIO()
        request.product_image.save(buffer, format="PNG")
        image_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Build prompt
        prompt = self._build_prompt(request)
        
        # Call your provider's API
        response = await self.client.post("/generate", json={
            "prompt": prompt,
            "image": image_b64,
            "width": request.output_width,
            "height": request.output_height,
            "num_outputs": request.num_variations,
            "seed": request.seed,
        })
        
        response.raise_for_status()
        data = response.json()
        
        # Parse response and convert to PIL Images
        images = []
        for img_data in data["images"]:
            img_bytes = base64.b64decode(img_data)
            images.append(Image.open(io.BytesIO(img_bytes)))
        
        return GenerationResult(
            images=images,
            seeds=data.get("seeds", [request.seed or 0] * len(images)),
            provider=self.name,
            model=data.get("model", "model-1"),
            generation_time_ms=data.get("generation_time_ms", 0),
            cost_usd=data.get("cost_usd"),
        )
    
    def _build_prompt(self, request: GenerationRequest) -> str:
        """Build the generation prompt."""
        parts = [
            request.scene_prompt,
            f"{request.style} style",
            f"{request.lighting} lighting",
            f"{request.angle} angle view",
            "professional product photography",
        ]
        return ", ".join(parts)
    
    async def health_check(self) -> bool:
        """Check if the provider is available."""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception:
            return False
```

### Step 2: Register Provider in Factory

Edit `backend/app/providers/factory.py`:

```python
from app.providers.your_provider import YourProvider

class ProviderFactory:
    _providers: dict[str, type[AIProvider]] = {
        "replicate": ReplicateProvider,
        "stability": StabilityProvider,
        "yourprovider": YourProvider,  # Add here
    }
    
    @classmethod
    def list_providers(cls) -> list[str]:
        return list(cls._providers.keys())
```

### Step 3: Add Configuration

Edit `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    # Existing...
    replicate_api_token: str | None = None
    stability_api_key: str | None = None
    
    # Add your provider:
    yourprovider_api_key: str | None = None
```

### Step 4: Update Frontend Settings Panel

Edit `frontend/components/SettingsPanel.tsx`:

```typescript
const PROVIDERS = [
  // Existing providers...
  {
    id: 'yourprovider',
    name: 'Your Provider',
    description: 'Your custom AI provider',
    keyUrl: 'https://yourprovider.com/api-keys',
    models: [
      { id: 'model-1', name: 'Model 1', description: 'Fast and efficient' },
      { id: 'model-2', name: 'Model 2', description: 'High quality' },
      { id: 'model-3', name: 'Model 3', description: 'Best results' },
    ],
  },
]
```

### Step 5: Update Backend Models Endpoint

Edit `backend/app/api/routes.py`:

```python
@router.get("/models", response_model=ModelsResponse)
async def get_available_models():
    return ModelsResponse(
        models={
            "replicate": [...],
            "stability": [...],
            "yourprovider": [
                {"id": "model-1", "name": "Model 1", "description": "Fast and efficient"},
                {"id": "model-2", "name": "Model 2", "description": "High quality"},
                {"id": "model-3", "name": "Model 3", "description": "Best results"},
            ],
        }
    )
```

### Step 6: Update Provider Factory to Use Runtime Settings

Edit `backend/app/providers/factory.py`:

```python
@classmethod
def get_provider(cls, provider_name: str | None = None, api_key: str | None = None) -> AIProvider:
    """Get AI provider instance with runtime settings support."""
    from app.core.config import settings
    from app.api.routes import get_runtime_settings
    
    runtime = get_runtime_settings()
    
    # Use runtime settings if available
    name = provider_name or runtime.get("provider") or settings.ai_provider
    key = api_key or runtime.get("api_key")
    
    if name not in cls._providers:
        raise ValueError(f"Unknown provider: {name}")
    
    # Get API key from runtime or env
    if not key:
        if name == "replicate":
            key = settings.replicate_api_token
        elif name == "stability":
            key = settings.stability_api_key
        elif name == "yourprovider":
            key = settings.yourprovider_api_key
    
    if not key:
        raise ValueError(f"{name.upper()}_API_KEY is required")
    
    return cls._providers[name](key)
```

---

## Testing Your New Provider

1. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Test the health endpoint:**
   ```bash
   curl http://localhost:8000/api/v1/models
   ```

3. **Open the frontend:**
   ```
   http://localhost:3000
   ```

4. **Configure in Settings:**
   - Select your new provider
   - Choose a model
   - Add your API key
   - Click Save

5. **Test generation:**
   - Upload a product image
   - Click Generate

---

## Example: Adding OpenAI DALL-E

Here's a real example for OpenAI:

**Provider file** (`backend/app/providers/openai_provider.py`):

```python
import httpx
from openai import AsyncOpenAI
from app.providers.base import AIProvider, GenerationRequest, GenerationResult
from PIL import Image
import io

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
    
    @property
    def name(self) -> str:
        return "openai"
    
    @property
    def supported_models(self) -> list[str]:
        return ["dall-e-3", "dall-e-2"]
    
    async def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = self._build_prompt(request)
        
        response = await self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=f"{request.output_width}x{request.output_height}",
            n=request.num_variations,
        )
        
        # Download and convert images
        images = []
        async with httpx.AsyncClient() as client:
            for img_data in response.data:
                img_response = await client.get(img_data.url)
                images.append(Image.open(io.BytesIO(img_response.content)))
        
        return GenerationResult(
            images=images,
            seeds=[0] * len(images),
            provider="openai",
            model="dall-e-3",
            generation_time_ms=0,
            cost_usd=0.04 * len(images),  # DALL-E 3 pricing
        )
    
    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False
```

Then follow steps 2-6 above to integrate it.

---

## Tips

- **API Key Security**: Never commit API keys. Use environment variables or runtime settings.
- **Error Handling**: Add proper error handling in your provider's `generate()` method.
- **Cost Tracking**: Return accurate `cost_usd` if your provider charges per generation.
- **Model Selection**: Use the `runtime.get("model")` to respect user's model choice.
- **Testing**: Test with small images first to avoid burning credits.

---

## Need Help?

- Check existing providers in `backend/app/providers/` for examples
- Read the base interface in `backend/app/providers/base.py`
- Open an issue on GitHub if you get stuck
