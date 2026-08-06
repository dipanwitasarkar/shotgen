# ShotGen v1.0.0 - Multi-Provider AI Image Generation Release

**Release Date:** August 6, 2026

## 🎉 Overview

This major release transforms ShotGen from a single-provider application into a **comprehensive multi-provider AI product photography platform** with support for 7 different AI providers and 20+ image generation models. Users can now choose between free and paid options, with significant improvements to provider management, error handling, and user experience.

---

## ✨ Major Features

### 🔌 Multi-Provider Support (7 Providers)

Added support for 7 AI image generation providers, giving users flexibility in cost, quality, and features:

#### **Free Providers** ⭐
1. **Together AI** - 3 months unlimited free tier
   - FLUX.1 Schnell (Free)
   - FLUX.1 Schnell
   - FLUX.2 Dev
   - FLUX.1.1 Pro

2. **Hugging Face** - Free forever
   - FLUX.1 Schnell
   - Stable Diffusion XL
   - SDXL Turbo

3. **Pollinations.ai** - Credit-based free tier
   - FLUX
   - FLUX Realism
   - FLUX Anime
   - Turbo

#### **Paid Providers**
4. **NVIDIA NIM** - Cloud API access
   - FLUX.1 Schnell
   - FLUX.1 Dev
   - Stable Diffusion 3.5 Large
   - Stable Diffusion 3 Medium
   - Stable Diffusion XL
   - SDXL Turbo

5. **Google Imagen 3** - $0.03-$0.06 per image
   - Imagen 3 Fast
   - Imagen 3

6. **Replicate** - Pay-per-use
   - SDXL
   - SDXL Lightning
   - Flux Schnell
   - Flux Dev

7. **Stability AI** - Pay-per-use
   - Stable Diffusion 3
   - SDXL 1.0
   - SD Turbo

### 🎨 Enhanced Settings Panel

- **Provider Selection UI** - Visual cards for each provider with descriptions
- **Model Selection** - Dynamic model list based on selected provider
- **API Key Management** - Secure storage and validation
- **Provider Status Indicator** - Shows currently configured provider/model in header
- **Quick Links** - Direct links to get API keys for each provider

### 🔧 Advanced Generation Settings

- **Custom Prompts** - Override default scene prompts
- **Aspect Ratios** - 1:1, 16:9, 9:16, 4:3, 3:4
- **Quality Presets** - Draft, Standard, High Quality
- **Multiple Variations** - Generate 1-4 images per request
- **Scene Templates** - 10+ pre-built professional scenes

---

## 🐛 Bug Fixes & Improvements

### Provider-Specific Fixes

#### NVIDIA NIM
- ✅ Fixed endpoint format: `/v1/genai/{vendor}/{slug}`
- ✅ Corrected model paths (e.g., `flux.1-schnell` not `flux-schnell`)
- ✅ Fixed response parsing for `artifacts[0].base64` format
- ✅ Added proper error handling for account access issues
- ✅ Increased timeout to 120s for slow generation
- ✅ Removed Qwen models (self-hosted only, not cloud API)

#### Hugging Face
- ✅ Fixed DNS resolution by adding `base_url` to httpx client
- ✅ Added proper error handling for network issues

#### Pollinations.ai
- ✅ Fixed seed overflow (32-bit integer limit)
- ✅ Updated to require API key (no longer anonymous)
- ✅ Added rate limit handling (1 req/15s for anonymous)
- ✅ Improved error messages

#### Google Imagen 3
- ✅ Fixed API endpoint and authentication
- ✅ Added proper model selection

#### General
- ✅ Fixed duplicate provider entries in UI
- ✅ Removed non-working Placeholdr.dev provider
- ✅ Fixed runtime settings import errors
- ✅ Improved error messages across all providers
- ✅ Added comprehensive logging for debugging

### UI/UX Improvements

- ✅ **Better Error Display** - Concise, user-friendly error messages with dismiss button
- ✅ **Provider Badge** - Shows active provider/model in settings header
- ✅ **Loading States** - Clear feedback during generation
- ✅ **Responsive Design** - Mobile-friendly settings panel
- ✅ **Icon Integration** - Added AlertCircle and other Lucide icons

---

## 📚 Documentation

### New Documentation Files

1. **ADDING_PROVIDERS.md** - Complete guide for adding new AI providers
2. **ADDING_MODELS.md** - Guide for adding models to existing providers
3. **CUSTOM_PROVIDERS_UI.md** - UI customization guide
4. **ARTICLE.md** - Medium-style article about ShotGen

### Updated Documentation

- **README.md** - Updated with all providers, features, and setup instructions
- **.env.example** - Added environment variables for all providers
- **CONTRIBUTING.md** - Updated contribution guidelines

---

## 🔒 Security & Best Practices

- ✅ API keys stored securely in environment variables
- ✅ Runtime settings separated from configuration
- ✅ No API keys exposed in frontend
- ✅ Proper error handling prevents key leakage
- ✅ CORS configured correctly for production

---

## 📦 Dependencies

### Backend
- Added `google-generativeai` for Google Imagen 3
- Updated `httpx` for better async support
- All providers use async/await for non-blocking I/O

### Frontend
- Added Lucide React icons
- Updated Next.js components for better state management

---

## 🚀 Performance

- **Async Processing** - All providers use async/await
- **Timeout Management** - 120s timeout for slow models
- **Error Recovery** - Graceful degradation on provider failures
- **Caching** - Runtime settings cached for performance

---

## 🔄 Migration Guide

### From Previous Version

1. **Update Environment Variables**
   ```bash
   cp .env.example .env
   # Add your API keys for desired providers
   ```

2. **Install Dependencies**
   ```bash
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

3. **Configure Providers**
   - Open Settings panel in UI
   - Select your preferred provider
   - Enter API key
   - Choose model
   - Save settings

---

## 🎯 Recommended Providers

### For Free Usage
1. **Together AI** - Best free option (3 months unlimited)
2. **Hugging Face** - Free forever, great for testing

### For Production
1. **NVIDIA NIM** - Best performance, enterprise-grade
2. **Stability AI** - High quality, reliable
3. **Google Imagen 3** - Excellent quality, reasonable pricing

### For Experimentation
1. **Pollinations.ai** - Credit-based, good for testing
2. **Replicate** - Pay-per-use, no commitment

---

## 📊 Statistics

- **7 Providers** supported
- **20+ Models** available
- **5,700+ lines** of code added
- **21 files** modified
- **38 commits** in this release
- **10+ scenes** pre-configured
- **4 aspect ratios** supported

---

## 🐛 Known Issues

1. **Hugging Face DNS** - May fail on some networks due to DNS resolution issues
   - **Workaround:** Use Together AI or Stability AI instead

2. **NVIDIA Account Access** - Some models require specific account permissions
   - **Workaround:** Use Stability AI provider directly with Stability AI key

3. **Pollinations Rate Limits** - 1 request per 15 seconds for anonymous users
   - **Workaround:** Get free API key from pollinations.ai

---

## 🔮 Future Roadmap

- [ ] Add more providers (Midjourney, Leonardo.ai, etc.)
- [ ] Batch processing support
- [ ] Image editing capabilities
- [ ] Custom model fine-tuning
- [ ] Provider cost comparison
- [ ] Usage analytics dashboard
- [ ] API rate limit monitoring
- [ ] Automatic provider fallback

---

## 🙏 Acknowledgments

- **Black Forest Labs** - FLUX models
- **Stability AI** - Stable Diffusion models
- **Google** - Imagen 3
- **NVIDIA** - NIM infrastructure
- **Hugging Face** - Free inference API
- **Together AI** - Free tier offering
- **Pollinations.ai** - Community-driven AI

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🔗 Links

- **Repository:** https://github.com/dipanwitasarkar/shotgen
- **Documentation:** See `/docs` folder
- **Issues:** https://github.com/dipanwitasarkar/shotgen/issues
- **Discussions:** https://github.com/dipanwitasarkar/shotgen/discussions

---

## 💬 Support

For questions, issues, or feature requests:
1. Check the documentation in `/docs`
2. Search existing issues
3. Create a new issue with detailed information
4. Join our community discussions

---

**Full Changelog:** https://github.com/dipanwitasarkar/shotgen/compare/88fb1c5...35a6229
