# ShotGen

**AI product photography in seconds. No studio, no photographer, no problem.**

![ShotGen Banner](docs/assets/banner.png)

Transform your product photos into professional lifestyle shots using AI. Upload a product image, choose a scene, and get studio-quality photos in seconds.

## Features

- **Background Removal** - Automatically removes product backgrounds
- **Scene Generation** - Place products in lifestyle settings (kitchen, outdoor, studio, etc.)
- **Multiple AI Backends** - Pluggable architecture supporting Replicate, Stability AI, ComfyUI, FAL
- **High-Resolution Output** - Export print-ready images up to 4K
- **Batch Processing** - Generate multiple variations at once
- **Self-Hostable** - Full control over your data and costs

## Use Cases

- E-commerce product listings (Amazon, Shopify, Etsy)
- Social media marketing
- Brand catalogs
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
git clone https://github.com/yourusername/shotgen.git
cd shotgen

# Start with Docker (recommended)
docker-compose up -d

# Or run locally
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Configuration

Create a `.env` file in the root directory:

```env
# AI Provider (choose one)
AI_PROVIDER=replicate  # replicate | stability | comfyui | fal

# Replicate
REPLICATE_API_TOKEN=your_token_here

# Stability AI
STABILITY_API_KEY=your_key_here

# ComfyUI (self-hosted)
COMFYUI_URL=http://localhost:8188

# FAL
FAL_KEY=your_key_here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/shotgen

# Storage
R2_ACCOUNT_ID=your_account_id
R2_ACCESS_KEY=your_access_key
R2_SECRET_KEY=your_secret_key
R2_BUCKET=shotgen

# Auth (Supabase)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
```

## Architecture

```
shotgen/
├── frontend/          # Next.js 14 app
│   ├── app/           # App router pages
│   ├── components/    # React components
│   └── lib/           # Utilities
├── backend/           # FastAPI server
│   ├── app/
│   │   ├── api/       # API routes
│   │   ├── core/      # Config, security
│   │   ├── models/    # Database models
│   │   ├── providers/ # AI provider adapters
│   │   └── services/  # Business logic
│   └── tests/
├── docs/              # Documentation
└── docker-compose.yml
```

## AI Providers

ShotGen supports multiple AI backends through a pluggable adapter system:

| Provider | Pros | Cons | Cost |
|----------|------|------|------|
| **Replicate** | Easy setup, many models | Pay per generation | ~$0.01-0.05/image |
| **Stability AI** | Official SD API, reliable | Limited customization | ~$0.02/image |
| **ComfyUI** | Full control, free | Need GPU server | Your GPU costs |
| **FAL** | Fast, good quality | Newer service | ~$0.01/image |

## Roadmap

- [x] Core image generation pipeline
- [x] Background removal
- [x] Multiple AI provider support
- [ ] Scene templates library
- [ ] Batch processing
- [ ] API for integrations
- [ ] Shopify plugin
- [ ] Mobile app

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI, Python 3.10+, SQLAlchemy
- **Database**: PostgreSQL (via Supabase)
- **Storage**: Cloudflare R2
- **AI**: Stable Diffusion, ControlNet, Segment Anything
- **Auth**: Supabase Auth
- **Payments**: Stripe

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- [Documentation](docs/)
- [Discord Community](https://discord.gg/shotgen)
- [Twitter](https://twitter.com/shotgen_ai)

---

Built with AI by the community. Star this repo if you find it useful!
