# Quick Guide: Adding New Models

This is the simplest way to add more models to existing providers.

## Step 1: Find the Model ID

For **Replicate**, browse https://replicate.com/explore and copy the model path.

Example:
- `stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b`
- `black-forest-labs/flux-schnell`
- `lucataco/juggernaut-xl-v9`

## Step 2: Add to Frontend

Edit `frontend/components/SettingsPanel.tsx` (around line 17):

```typescript
const PROVIDERS = [
  {
    id: 'replicate',
    name: 'Replicate',
    description: 'Easy to use, pay-per-use pricing',
    keyUrl: 'https://replicate.com/account/api-tokens',
    models: [
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'Best quality, slower' },
      { id: 'sdxl-lightning', name: 'SDXL Lightning', description: 'Fast, good quality' },
      { id: 'flux-schnell', name: 'Flux Schnell', description: 'Very fast, free tier' },
      { id: 'flux-dev', name: 'Flux Dev', description: 'High quality, slower' },
      
      // Add your new models here:
      { id: 'playground-v2.5', name: 'Playground v2.5', description: 'Photorealistic, vibrant' },
      { id: 'juggernaut-xl', name: 'Juggernaut XL', description: 'Ultra realistic' },
      { id: 'realvisxl', name: 'RealVisXL v4', description: 'Hyperrealistic' },
      { id: 'proteus', name: 'Proteus', description: 'Versatile, high quality' },
    ],
  },
  // ... other providers
]
```

## Step 3: Add to Backend Models Endpoint

Edit `backend/app/api/routes.py` (around line 285):

```python
@router.get("/models", response_model=ModelsResponse)
async def get_available_models():
    """Get available models for each provider."""
    return ModelsResponse(
        models={
            "replicate": [
                {"id": "sdxl", "name": "Stable Diffusion XL", "description": "Best quality, slower"},
                {"id": "sdxl-lightning", "name": "SDXL Lightning", "description": "Fast, good quality"},
                {"id": "flux-schnell", "name": "Flux Schnell", "description": "Very fast, free tier"},
                {"id": "flux-dev", "name": "Flux Dev", "description": "High quality, slower"},
                
                # Add your new models here:
                {"id": "playground-v2.5", "name": "Playground v2.5", "description": "Photorealistic, vibrant"},
                {"id": "juggernaut-xl", "name": "Juggernaut XL", "description": "Ultra realistic"},
                {"id": "realvisxl", "name": "RealVisXL v4", "description": "Hyperrealistic"},
                {"id": "proteus", "name": "Proteus", "description": "Versatile, high quality"},
            ],
            # ... other providers
        }
    )
```

## Step 4: Map Model IDs to Replicate Paths

Edit `backend/app/providers/replicate_provider.py` (around line 20):

```python
class ReplicateProvider(AIProvider):
    """Replicate AI provider using their API."""
    
    # Map model IDs to Replicate model versions
    MODELS = {
        "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "sdxl-lightning": "bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637",
        "flux-schnell": "black-forest-labs/flux-schnell",
        "flux-dev": "black-forest-labs/flux-dev",
        
        # Add your new model mappings:
        "playground-v2.5": "playgroundai/playground-v2.5-1024px-aesthetic:a45f82a1382bed5c7aeb861dac7c7d191b0fdf74d8d57c4a0e6ed7d4d0bf7d24",
        "juggernaut-xl": "lucataco/juggernaut-xl-v9:bea09cf018e513cef0841719559ea86d2299e05583423b5e4e6c6b5e5e6e6e6e",
        "realvisxl": "lucataco/realvisxl-v4.0:7d7e2e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e8e",
        "proteus": "datacte/proteus-v0.2:06775cd262843edbde5abab958abdbb65a0a6b58ca301c9fd78fa55c775fc019",
    }
```

**Note**: Replace the version hashes with actual ones from Replicate. Find them by:
1. Go to the model page on Replicate
2. Click "API" tab
3. Copy the full model path with version hash

## Step 5: Restart Backend

```bash
# Kill the running backend
pkill -f "uvicorn app.main"

# Restart
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Frontend will auto-reload.

## Step 6: Test

1. Open http://localhost:3000
2. Click Settings
3. Select Replicate
4. You should see your new models in the dropdown
5. Select one, add API key, Save
6. Upload an image and generate!

---

## Popular Models to Add

### Photorealistic
- **Juggernaut XL v9**: `lucataco/juggernaut-xl-v9`
- **RealVisXL v4**: `lucataco/realvisxl-v4.0`
- **Proteus v0.2**: `datacte/proteus-v0.2`

### Artistic
- **Playground v2.5**: `playgroundai/playground-v2.5-1024px-aesthetic`
- **DreamShaper XL**: `lucataco/dreamshaper-xl-turbo`

### Fast
- **SDXL Turbo**: `stability-ai/sdxl-turbo`
- **LCM-LoRA**: `fofr/sdxl-lcm-lora`

### Specialized
- **Product Photography**: `fofr/product-photo`
- **Food Photography**: `fofr/food-photography`

---

## Troubleshooting

**Model not appearing in UI?**
- Check you added it to BOTH frontend and backend
- Restart both servers
- Clear browser cache

**Generation fails?**
- Check the model ID is correct on Replicate
- Verify the version hash is current
- Check Replicate API logs

**Wrong output?**
- Some models need specific prompt formats
- Check the model's documentation on Replicate
- Adjust the prompt building in `_build_prompt()`

---

That's it! You can now add any Replicate model in ~5 minutes.
