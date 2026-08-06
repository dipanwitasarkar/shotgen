# ShotGen

**AI product photography in seconds. No studio, no photographer, no problem.**

Transform your product photos into professional lifestyle shots using AI. Upload a product image, choose a scene, and get studio-quality photos in seconds.

## Features

### 🎨 **Core Features**
- **IMAGE-TO-IMAGE Generation** - Your uploaded product appears in generated scenes
- **40+ Scene Templates** - Studio, Home, Outdoor, Lifestyle, Luxury, Tech, Seasonal, Food, Nature
- **Custom Scene Prompts** - Write your own scene descriptions for full creative control
- **Background Removal** - Automatic product cutout with rembg
- **Multiple Aspect Ratios** - 1:1, 4:3, 3:4, 16:9, 9:16, 3:2 for any platform
- **Style Options** - Realistic, Artistic, Minimal, Lifestyle, Editorial, Cinematic
- **Lighting Options** - Studio, Natural, Dramatic, Soft, Golden Hour, Neon
- **Camera Angles** - Front, 45°, Top-down, Side, Low, Hero

### 🚀 **Advanced Features** (NEW!)
- **🎯 Inpainting Mode** - Preserves product exactly, changes only background (RECOMMENDED)
- **🎨 ControlNet Mode** - Preserves product structure while changing style/scene
- **📐 Resolution Options** - 1K (1024), 2K (2048), 4K (4096) for HD/Ultra HD export
- **🖼️ Custom Backgrounds** - Upload your own background images
- **🎛️ Advanced IMG2IMG Controls** - Strength, guidance scale, inference steps
- **👁️ Prompt Preview & Editing** - See and edit the exact prompt sent to AI

### 🤖 **AI Providers**
- **7 AI Providers** - Free.ai, Together AI, Hugging Face, Stability AI, Replicate, NVIDIA NIM, Google Imagen
- **Free Options** - Free.ai (signup required), Together AI (free trial), Hugging Face (free forever)
- **In-App API Key Configuration** - No need to edit .env files
- **All Providers Support IMG2IMG** - Product image + all parameters sent to every provider

### 🔌 **Developer API** (NEW!)
- **Public REST API** - `/api/v1/public/v1/generate` endpoint
- **API Key Authentication** - Secure access with X-API-Key header
- **Complete Documentation** - Python, cURL, JavaScript examples
- **Rate Limiting** - Free (10/hr), Pro (100/hr), Enterprise (unlimited)
- **Self-Hostable** - Full control over your data and costs

## Use Cases

- E-commerce product listings (Amazon, Shopify, Etsy)
- Social media marketing (Instagram, TikTok, Facebook)
- Brand catalogs and lookbooks
- Dropshipping businesses
- Small business product photography

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker (optional, for self-hosting)

### Installation

```bash
# Clone the repo
git clone https://github.com/dipanwitasarkar/shotgen.git
cd shotgen

# Start with Docker (recommended)
docker-compose up -d

# Or run locally
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Configuration

**In-App Settings (Recommended)**

1. Open http://localhost:3000
2. Click the Settings panel (⚙️)
3. Choose your AI provider:
   - **Stability AI** ⭐ **RECOMMENDED** - Best for product photography (Inpainting + ControlNet)
   - **Replicate** - Good alternative (Inpainting + ControlNet support)
   - **Together AI** - Free trial available (IMG2IMG support)
   - **Hugging Face** - Free forever (IMG2IMG support)
   - **NVIDIA NIM** - Enterprise (IMG2IMG support)
   - **Google Imagen** - Pay per image (IMG2IMG support)
   - **Free.ai** ⚠️ **NOT RECOMMENDED** - Text-to-image only, does NOT preserve product
4. Select a model (SDXL, FLUX, SD3, etc.)
5. Paste your API key
6. Click Save

> **⚠️ Important:** Free.ai does NOT support image-to-image generation. It will ignore your product image and generate from text only. For proper product photography, use **Stability AI** (recommended) or any other provider.

### Get API Keys

- **Stability AI** ⭐ **RECOMMENDED** (Paid): https://platform.stability.ai/account/keys
  - Best for product photography
  - Inpainting mode (preserves product)
  - ControlNet support (structure preservation)
  - ~$0.05 per image
- **Replicate** (Paid): https://replicate.com/account/api-tokens
  - Good alternative with Inpainting + ControlNet
- **Together AI** (Free trial): https://api.together.ai/settings/api-keys
  - Free trial available, IMG2IMG support
- **Hugging Face** (Free forever): https://huggingface.co/settings/tokens
  - Free forever, IMG2IMG support
- **NVIDIA NIM** (Paid): https://build.nvidia.com/explore/discover
  - Enterprise, IMG2IMG support
- **Google Imagen** (Paid): https://aistudio.google.com/app/apikey
  - IMG2IMG support
- **Free.ai** ⚠️ **NOT RECOMMENDED** (FREE with signup): https://free.ai
  - Text-to-image only, does NOT preserve product

## Usage

### Basic Workflow
1. Upload your product image
2. Select a scene template or write a custom prompt
3. Choose aspect ratio, style, lighting, and angle
4. Click "Generate Product Shots"
5. Download your results

### Advanced Workflow (NEW!)
1. Upload your product image
2. **Enable Inpainting Mode** (recommended) - preserves product exactly
3. Select resolution (1K/2K/4K)
4. Optional: Upload custom background
5. Optional: Enable ControlNet for structure preservation
6. Adjust advanced controls (strength, guidance, steps)
7. Generate and download

### Using the Public API
```bash
# Generate with inpainting (preserves product)
curl -X POST http://localhost:8000/api/v1/public/v1/generate \
  -H "X-API-Key: your-api-key" \
  -F "image=@product.png" \
  -F "scene=beach" \
  -F "useInpainting=true" \
  -F "width=2048" \
  -F "height=2048"
```

See `/api/v1/public/v1/docs` for complete API documentation.

## Scene Templates

| Category | Scenes |
|----------|--------|
| Studio | White, Black, Gradient, Minimal |
| Home | Kitchen, Bathroom, Living Room, Bedroom, Dining, Office |
| Outdoor | Garden, Beach, Forest, Mountain, Park |
| Lifestyle | Cafe, Restaurant, Gym, Yoga, Pool |
| Luxury | Luxury, Jewelry, Fashion, Gallery |
| Tech | Tech, Gaming, Workspace |
| Seasonal | Christmas, Autumn, Spring, Summer |
| Food | Flat Lay, Rustic, Bar |
| Nature | Nature, Botanical, Stone |

## Aspect Ratios

| Ratio | Dimensions | Best For |
|-------|-----------|----------|
| 1:1 | 1024×1024 | Instagram posts |
| 4:3 | 1024×768 | Product pages |
| 3:4 | 768×1024 | Mobile |
| 16:9 | 1024×576 | Banners/YouTube |
| 9:16 | 576×1024 | Instagram/TikTok stories |
| 3:2 | 1024×683 | Traditional photography |

## Architecture

```
shotgen/
├── frontend/          # Next.js 14 app
│   ├── app/           # App router pages
│   ├── components/    # React components
│   │   ├── SettingsPanel.tsx
│   │   ├── SceneSelector.tsx
│   │   ├── GenerationSettings.tsx
│   │   └── ...
│   └── lib/           # Utilities
├── backend/           # FastAPI server
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Config, security
│   │   ├── providers/ # AI provider adapters
│   │   │   ├── replicate_provider.py
│   │   │   ├── stability_provider.py
│   │   │   └── ...
│   │   └── services/  # Business logic
│   │       ├── image_generation.py
│   │       └── background_removal.py
│   └── tests/
└── docker-compose.yml
```

## AI Providers & Models

### NVIDIA NIM
- **Flux Schnell** - NVIDIA NIM - Very fast, 4 steps

### Together AI ⭐ (Free Tier Available)
- **FLUX.1 Schnell (Free)** - Free tier - Fast, 4 steps
- **FLUX.1 Schnell** - Fast, good quality
- **FLUX.2 Dev** - High quality, customizable
- **FLUX.1.1 Pro** - Best quality

### Hugging Face ⭐ (All Free)
- **FLUX.1 Schnell** - Free tier - Fast
- **Stable Diffusion XL** - Free tier - High quality
- **SDXL Turbo** - Free tier - Ultra fast

### Replicate
- **SDXL** - Best quality, slower
- **SDXL Lightning** - Fast, good quality
- **Flux Schnell** - Very fast, free tier
- **Flux Dev** - High quality, slower

### Stability AI
- **Stable Diffusion 3** - Latest model
- **SDXL 1.0** - Production ready
- **SD Turbo** - Ultra fast

## API Endpoints

### Internal API (Web App)
```
POST   /api/v1/generate         - Generate product shots
POST   /api/v1/remove-background - Remove background
GET    /api/v1/scenes           - Get scene templates
GET    /api/v1/models           - Get available models
POST   /api/v1/settings         - Update runtime settings
GET    /api/v1/settings         - Get current settings
GET    /api/v1/health           - Health check
POST   /api/v1/preview-prompt   - Preview generated prompt
```

### Public API (Developers) - NEW!
```
POST   /api/v1/public/v1/generate  - Generate product shots (requires API key)
GET    /api/v1/public/v1/docs      - API documentation with examples
```

**Authentication:** Include `X-API-Key` header with your API key

**Example:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/v1/public/v1/generate',
    headers={'X-API-Key': 'your-api-key'},
    files={'image': open('product.png', 'rb')},
    data={
        'scene': 'beach',
        'useInpainting': 'true',
        'width': 2048,
        'height': 2048
    }
)

result = response.json()
print(f"Generated {len(result['images'])} images")
```

## Roadmap

### ✅ Completed
- [x] Core image generation pipeline
- [x] Background removal
- [x] Multiple AI provider support (7 providers)
- [x] Scene templates library (40+ scenes)
- [x] Custom scene prompts
- [x] Aspect ratio options
- [x] Quality control
- [x] In-app API key configuration
- [x] **Inpainting mode** (preserves product)
- [x] **ControlNet support** (structure preservation)
- [x] **Resolution options** (1K/2K/4K)
- [x] **Custom background upload**
- [x] **Public API** (developer access)
- [x] **API documentation** (Python, cURL, JS examples)

### 🚧 In Progress
- [ ] Batch processing queue
- [ ] Image history/gallery
- [ ] A/B comparison view

### 📋 Planned
- [ ] Shopify plugin
- [ ] WooCommerce integration
- [ ] Mobile app (iOS/Android)
- [ ] Video generation
- [ ] 3D product placement

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Python 3.10+, Pydantic
- **Image Processing**: Pillow, rembg, OpenCV
- **AI**: Stable Diffusion, Flux, SD3 (via providers)
- **HTTP**: httpx, uvicorn

## Extending

### Add Custom Providers (Easy - No Code!)

Click Settings → "Add Custom" in the app to add any AI provider:
- OpenAI, Hugging Face, Together AI
- Self-hosted ComfyUI, A1111, InvokeAI
- RunPod, Replicate custom models
- Any REST API endpoint

See [docs/CUSTOM_PROVIDERS_UI.md](docs/CUSTOM_PROVIDERS_UI.md) for examples.

### Add Providers to Codebase (Advanced)

For custom API logic or contributing to the project:
- [docs/ADDING_MODELS.md](docs/ADDING_MODELS.md) - Add models to existing providers
- [docs/ADDING_PROVIDERS.md](docs/ADDING_PROVIDERS.md) - Add new provider classes

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- GitHub Issues: https://github.com/dipanwitasarkar/shotgen/issues
- Documentation: This README

---

Built with AI. Star this repo if you find it useful!
