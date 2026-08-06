# CRITICAL ISSUE: Product Not Appearing in Generated Images

## Problem
When users upload a product image (e.g., camera) and select a scene (e.g., beach), the generated images show ONLY the scene WITHOUT the product.

## Root Cause
**ShotGen uses TEXT-TO-IMAGE models, not IMAGE-TO-IMAGE models.**

Current flow:
1. User uploads product image ✅
2. Background is removed ✅  
3. Prompt is built: "sandy beach, ocean waves..." ❌ **NO PRODUCT MENTIONED**
4. AI generates beach scene ❌ **WITHOUT PRODUCT**

## What's Missing
The uploaded product image is **NEVER described in the prompt** and most providers **don't support image-to-image**.

## Solutions

### Option 1: Add Product Description (Quick Fix)
Add a product description field where users describe their product:
- Input: "professional DSLR camera"
- Prompt: "professional DSLR camera on sandy beach, ocean waves..."

### Option 2: Use Image-to-Image Models (Proper Fix)
Switch to providers/models that support image-to-image:
- **Stable Diffusion img2img**
- **DALL-E image editing**
- **Qwen-Image-Edit** (requires local deployment)
- **ControlNet** (requires custom implementation)

### Option 3: Image Compositing (Original Intent)
Composite the product cutout onto generated backgrounds:
1. Generate background scene
2. Overlay product cutout
3. Blend edges with AI inpainting

## Current Status
❌ **Product photography does NOT work as expected**
✅ Scene generation works
✅ Background removal works
❌ Product + Scene combination does NOT work

## Recommended Action
1. **Immediate:** Add product description input field
2. **Short-term:** Implement image compositing
3. **Long-term:** Add image-to-image provider support

