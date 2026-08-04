# ShotGen

**AI product photography in seconds. No studio, no photographer, no problem.**

Transform your product photos into professional lifestyle shots using AI. Upload a product image, choose a scene, and get studio-quality photos in seconds.

## Features

- **40+ Scene Templates** - Organized by category: Studio, Home, Outdoor, Lifestyle, Luxury, Tech, Seasonal, Food, Nature
- **Custom Scene Prompts** - Write your own scene descriptions for full creative control
- **Multiple Aspect Ratios** - 1:1, 4:3, 3:4, 16:9, 9:16, 3:2 for any platform
- **Quality Control** - Adjustable quality slider (Fast/Balanced/High Quality)
- **Background Removal** - Automatic product cutout with rembg
- **Style Options** - Realistic, Artistic, Minimal, Lifestyle, Editorial, Cinematic
- **Lighting Options** - Studio, Natural, Dramatic, Soft, Golden Hour, Neon
- **Camera Angles** - Front, 45°, Top-down, Side, Low, Hero
- **Multiple AI Backends** - Replicate, Stability AI, FAL.ai with runtime switching
- **In-App API Key Configuration** - No need to edit .env files
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

**Option 1: In-App Settings (Recommended)**

1. Open http://localhost:3000
2. Click the Settings panel
3. Choose your AI provider (Replicate, Stability AI, or FAL)
4. Select a model (SDXL, Flux, SD3, etc.)
5. Paste your API key
6. Click Save

**Option 2: Environment Variables**

Create a `.env` file in the root directory:

```env
# AI Provider (choose one)
AI_PROVIDER=replicate  # replicate | stability | fal

# Replicate
REPLICATE_API_TOKEN=your_token_here

# Stability AI
STABILITY_API_KEY=your_key_here

# FAL
FAL_KEY=your_key_here

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost:5432/shotgen
```

### Get API Keys

- **Replicate**: https://replicate.com/account/api-tokens
- **Stability AI**: https://platform.stability.ai/account/keys
- **FAL.ai**: https://fal.ai/dashboard/keys

## Usage

1. Upload your product image
2. Select a scene template or write a custom prompt
3. Choose aspect ratio, style, lighting, and angle
4. Adjust quality based on your needs
5. Click "Generate Product Shots"
6. Download your results

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

### Replicate
- **SDXL** - Best quality, slower
- **SDXL Lightning** - Fast, good quality
- **Flux Schnell** - Very fast, free tier
- **Flux Dev** - High quality, slower

### Stability AI
- **Stable Diffusion 3** - Latest model
- **SDXL 1.0** - Production ready
- **SD Turbo** - Ultra fast

### FAL.ai
- **Flux Pro** - Best quality
- **Flux Dev** - Development
- **SDXL** - Stable Diffusion XL

## API Endpoints

```
POST   /api/v1/generate         - Generate product shots
POST   /api/v1/remove-background - Remove background
GET    /api/v1/scenes           - Get scene templates
GET    /api/v1/models           - Get available models
POST   /api/v1/settings         - Update runtime settings
GET    /api/v1/settings         - Get current settings
GET    /api/v1/health           - Health check
```

## Roadmap

- [x] Core image generation pipeline
- [x] Background removal
- [x] Multiple AI provider support
- [x] Scene templates library (40+ scenes)
- [x] Custom scene prompts
- [x] Aspect ratio options
- [x] Quality control
- [x] In-app API key configuration
- [ ] Batch processing queue
- [ ] API for integrations
- [ ] Shopify plugin
- [ ] Mobile app

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: FastAPI, Python 3.10+, Pydantic
- **Image Processing**: Pillow, rembg, OpenCV
- **AI**: Stable Diffusion, Flux, SD3 (via providers)
- **HTTP**: httpx, uvicorn

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- GitHub Issues: https://github.com/dipanwitasarkar/shotgen/issues
- Documentation: This README

---

Built with AI. Star this repo if you find it useful!
