# Adding Custom Providers via UI

The easiest way to add custom AI providers and models - no code required!

## Quick Start

1. Open http://localhost:3000
2. Click **Settings** panel
3. Click **"Add Custom"** button
4. Fill in the form
5. Click **"Add Provider"**

That's it! Your custom provider is now available.

## Example: Adding OpenAI

### Step 1: Click "Add Custom"

In the Settings panel, click the blue "Add Custom" button.

### Step 2: Fill Provider Information

- **Provider Name**: `OpenAI`
- **Provider ID**: `openai` (auto-formatted)
- **Description**: `GPT-4 and DALL-E models`
- **API Key Label**: `API Key`
- **Base URL**: `https://api.openai.com/v1` (optional)

### Step 3: Add Models

Click "Add Model" for each model you want:

**Model 1:**
- Model ID: `dall-e-3`
- Model Name: `DALL-E 3`
- Description: `High quality image generation`

**Model 2:**
- Model ID: `dall-e-2`
- Model Name: `DALL-E 2`
- Description: `Faster, good quality`

### Step 4: Save

Click "Add Provider" and it will:
- Save to your browser's localStorage
- Auto-select the new provider
- Show it in the provider list

### Step 5: Configure API Key

1. Select your new provider
2. Choose a model
3. Paste your OpenAI API key
4. Click "Save Settings"

Done! You can now generate images with OpenAI.

---

## More Examples

### Hugging Face Inference API

```
Provider Name: Hugging Face
Provider ID: huggingface
Description: Open source models
API Key Label: Access Token
Base URL: https://api-inference.huggingface.co

Models:
- stable-diffusion-xl-base-1.0 | SDXL Base | High quality
- stable-diffusion-2-1 | SD 2.1 | Fast generation
```

### Together AI

```
Provider Name: Together AI
Provider ID: together
Description: Fast open source inference
API Key Label: API Key
Base URL: https://api.together.xyz

Models:
- stabilityai/stable-diffusion-xl-base-1.0 | SDXL | Best quality
- runwayml/stable-diffusion-v1-5 | SD 1.5 | Fast
```

### Self-Hosted ComfyUI

```
Provider Name: My ComfyUI
Provider ID: my-comfyui
Description: Self-hosted on my server
API Key Label: (leave as "API Key" or blank)
Base URL: http://192.168.1.100:8188

Models:
- sdxl | SDXL Workflow | My custom workflow
- sd15 | SD 1.5 Workflow | Fast workflow
```

### RunPod Serverless

```
Provider Name: RunPod
Provider ID: runpod
Description: Serverless GPU endpoints
API Key Label: API Key
Base URL: https://api.runpod.ai/v2/YOUR_ENDPOINT_ID

Models:
- sdxl | SDXL | Your deployed model
```

---

## Managing Custom Providers

### View Custom Providers

Custom providers appear in the provider grid alongside default ones (Replicate, Stability AI, FAL).

A badge shows "X Custom" in the Settings header.

### Delete Custom Provider

1. Select the custom provider
2. Click the red trash icon in the top-right corner
3. Confirm deletion

**Note**: You cannot delete default providers (Replicate, Stability AI, FAL).

### Edit Custom Provider

Currently, you need to:
1. Delete the old provider
2. Add a new one with updated settings

(Edit functionality coming soon!)

---

## Storage

Custom providers are stored in your browser's localStorage:
- Key: `shotgen-custom-providers`
- Format: JSON array
- Persists across sessions
- Per-browser (not synced across devices)

To backup your custom providers:
1. Open browser DevTools (F12)
2. Go to Application → Local Storage
3. Copy the value of `shotgen-custom-providers`
4. Save to a file

To restore:
1. Open DevTools
2. Paste the JSON into `shotgen-custom-providers`
3. Refresh the page

---

## Limitations

### What Works
- ✅ Any provider with a REST API
- ✅ Custom model names and descriptions
- ✅ Different API key labels
- ✅ Custom base URLs
- ✅ Multiple models per provider

### What Doesn't Work (Yet)
- ❌ Custom API request formats (uses standard format)
- ❌ Authentication beyond API keys (OAuth, JWT, etc.)
- ❌ Custom response parsing
- ❌ Streaming responses
- ❌ Syncing across devices

For these advanced cases, see [ADDING_PROVIDERS.md](./ADDING_PROVIDERS.md) to add a provider to the codebase.

---

## Troubleshooting

### Provider not appearing?
- Refresh the page
- Check browser console for errors (F12)
- Verify the provider ID is unique

### Generation fails?
- Check your API key is correct
- Verify the base URL is accessible
- Check the model ID matches the provider's API
- Look at browser console for error messages

### Lost custom providers?
- They're stored in localStorage (per-browser)
- Clearing browser data will delete them
- Export/backup before clearing data

---

## Need Help?

- For UI issues: Open an issue on GitHub
- For API integration: Check the provider's documentation
- For code-level providers: See [ADDING_PROVIDERS.md](./ADDING_PROVIDERS.md)
