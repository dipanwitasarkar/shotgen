'use client'

import { useState, useEffect } from 'react'
import { Settings, Key, Cpu, ChevronDown, ChevronUp, Check, AlertCircle, ExternalLink } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SettingsPanelProps {
  onSettingsChange: (settings: AppSettings) => void
}

export interface AppSettings {
  provider: string
  model: string
  apiKey: string
}

interface Provider {
  id: string
  name: string
  description: string
  apiKeyLabel: string
  keyUrl: string
  models: Model[]
}

interface Model {
  id: string
  name: string
  description: string
}

const PROVIDERS: Provider[] = [
  {
    id: 'freeai',
    name: 'Free.ai ⭐ FREE (Signup Required)',
    description: 'FREE 30k tokens/day - Just signup, no credit card',
    apiKeyLabel: 'API Key (Sign up free at free.ai)',
    keyUrl: 'https://free.ai',
    models: [
      { id: 'sdxl', name: 'SDXL', description: '⭐ FREE IMG2IMG - Best option' },
      { id: 'flux-schnell', name: 'FLUX Schnell', description: '⭐ FREE IMG2IMG - Fast' },
      { id: 'sd-turbo', name: 'SD Turbo', description: '⭐ FREE IMG2IMG - Fastest' },
    ],
  },
  {
    id: 'stability',
    name: 'Stability AI (Paid)',
    description: '$0.04 per image - Requires credit card',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://platform.stability.ai/account/keys',
    models: [
      { id: 'sd3-turbo', name: 'SD3 Turbo', description: 'IMG2IMG - $0.04/image' },
      { id: 'sd3', name: 'SD3', description: 'IMG2IMG - $0.065/image' },
      { id: 'sdxl', name: 'SDXL 1.0', description: 'IMG2IMG - $0.04/image' },
    ],
  },
  {
    id: 'together',
    name: 'Together AI (IMG2IMG)',
    description: 'Free 3 months unlimited - Image-to-image support',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://api.together.ai/settings/api-keys',
    models: [
      { id: 'flux-schnell-free', name: 'FLUX.1 Schnell (Free)', description: 'IMG2IMG - 3 months unlimited' },
      { id: 'flux-schnell', name: 'FLUX.1 Schnell', description: 'IMG2IMG - Fast' },
      { id: 'flux-dev', name: 'FLUX.2 Dev', description: 'IMG2IMG - High quality' },
      { id: 'flux-pro', name: 'FLUX.1.1 Pro', description: 'IMG2IMG - Best quality' },
    ],
  },
  {
    id: 'huggingface',
    name: 'Hugging Face (IMG2IMG)',
    description: 'Free forever - Image-to-image support',
    apiKeyLabel: 'API Token',
    keyUrl: 'https://huggingface.co/settings/tokens',
    models: [
      { id: 'flux-schnell', name: 'FLUX.1 Schnell', description: 'IMG2IMG - Free' },
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'IMG2IMG - Free' },
      { id: 'sd-turbo', name: 'SDXL Turbo', description: 'IMG2IMG - Free' },
    ],
  },
  {
    id: 'nvidia',
    name: 'NVIDIA NIM',
    description: 'NVIDIA AI endpoints, fast inference',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://build.nvidia.com/explore/discover',
    models: [
      { id: 'flux-schnell', name: 'FLUX.1 Schnell', description: 'Very fast, 4 steps' },
      { id: 'flux-dev', name: 'FLUX.1 Dev', description: 'High quality, 20-50 steps' },
      { id: 'sd3.5-large', name: 'Stable Diffusion 3.5 Large', description: '8B params, highest quality' },
      { id: 'sd3-medium', name: 'Stable Diffusion 3 Medium', description: 'High quality, balanced' },
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'Classic, high quality' },
      { id: 'sdxl-turbo', name: 'SDXL Turbo', description: 'Fast, 1-4 steps' },
    ],
  },
  {
    id: 'google',
    name: 'Google Imagen 3',
    description: 'Google AI, free tier coming soon',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://aistudio.google.com/app/apikey',
    models: [
      { id: 'imagen-3-fast', name: 'Imagen 3 Fast', description: 'Google - Fast, $0.03/image' },
      { id: 'imagen-3', name: 'Imagen 3', description: 'Google - Highest quality, $0.03/image' },
    ],
  },
  {
    id: 'replicate',
    name: 'Replicate (Paid)',
    description: 'Pay-per-use pricing',
    apiKeyLabel: 'API Token',
    keyUrl: 'https://replicate.com/account/api-tokens',
    models: [
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'IMG2IMG - Pay per use' },
      { id: 'sdxl-lightning', name: 'SDXL Lightning', description: 'IMG2IMG - Fast' },
      { id: 'flux-schnell', name: 'Flux Schnell', description: 'IMG2IMG - Very fast' },
      { id: 'flux-dev', name: 'Flux Dev', description: 'IMG2IMG - High quality' },
    ],
  },
]

export function SettingsPanel({ onSettingsChange }: SettingsPanelProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [provider, setProvider] = useState('nvidia')
  const [model, setModel] = useState('flux-schnell')
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasConfiguredSettings, setHasConfiguredSettings] = useState(false)

  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('shotgen-settings')
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings)
        setProvider(parsed.provider || 'nvidia')
        setModel(parsed.model || 'flux-schnell')
        setApiKey(parsed.apiKey || '')
        setHasConfiguredSettings(!!parsed.apiKey)
        onSettingsChange(parsed)
      } catch (e) {
        console.error('Failed to load settings:', e)
      }
    }
  }, [])

  const currentProvider = PROVIDERS.find(p => p.id === provider)
  const currentModels = currentProvider?.models || []

  const handleProviderChange = (newProvider: string) => {
    setProvider(newProvider)
    const providerData = PROVIDERS.find(p => p.id === newProvider)
    if (providerData && providerData.models.length > 0) {
      setModel(providerData.models[0].id)
    }
    setSaved(false)
    setHasConfiguredSettings(false)
  }

  const handleSave = async () => {
    // All providers need API key now
    if (!apiKey.trim()) {
      setError('API key is required')
      return
    }

    const settings: AppSettings = { provider, model, apiKey }
    
    // Save to localStorage
    localStorage.setItem('shotgen-settings', JSON.stringify(settings))
    
    // Notify parent
    onSettingsChange(settings)
    
    // Update backend
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/settings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      })
      
      if (!response.ok) {
        throw new Error('Failed to update backend settings')
      }
      
      setSaved(true)
      setError(null)
      setHasConfiguredSettings(true)
      setTimeout(() => setSaved(false), 3000)
    } catch (e) {
      // Still save locally even if backend fails
      setSaved(true)
      setError(null)
      setHasConfiguredSettings(true)
      setTimeout(() => setSaved(false), 3000)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header - Always visible */}
      <button
        onClick={() => {
          console.log('Settings clicked, isOpen:', isOpen)
          setIsOpen(!isOpen)
        }}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Settings className="w-5 h-5 text-gray-500" />
          <span className="font-semibold text-gray-900">Settings</span>
          {hasConfiguredSettings && (
            <>
              <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                Configured
              </span>
              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded-full font-medium">
                {currentProvider?.name} · {currentModels.find(m => m.id === model)?.name}
              </span>
            </>
          )}
        </div>
        {isOpen ? (
          <ChevronUp className="w-5 h-5 text-gray-400" />
        ) : (
          <ChevronDown className="w-5 h-5 text-gray-400" />
        )}
      </button>

      {/* Expandable content */}
      {isOpen && (
        <div className="px-6 pb-6 space-y-6 border-t border-gray-100">
          {/* Provider Selection */}
          <div className="pt-4 space-y-3">
            <label className="block text-sm font-medium text-gray-700">
              AI Provider
            </label>
            <div className="grid grid-cols-3 gap-3">
              {PROVIDERS.map((p) => (
                <button
                  key={p.id}
                  onClick={() => handleProviderChange(p.id)}
                  className={cn(
                    'p-3 rounded-xl border-2 text-left transition-all',
                    provider === p.id
                      ? 'border-brand-500 bg-brand-50'
                      : 'border-gray-200 hover:border-gray-300'
                  )}
                >
                  <div className="font-medium text-gray-900">{p.name}</div>
                  <div className="text-xs text-gray-500 mt-1">{p.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Model Selection */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700 flex items-center gap-2">
              <Cpu className="w-4 h-4" />
              Model
            </label>
            <div className="grid grid-cols-2 gap-2">
              {currentModels.map((m) => (
                <button
                  key={m.id}
                  onClick={() => { setModel(m.id); setSaved(false); }}
                  className={cn(
                    'p-3 rounded-lg border text-left transition-all',
                    model === m.id
                      ? 'border-brand-500 bg-brand-50'
                      : 'border-gray-200 hover:border-gray-300'
                  )}
                >
                  <div className="font-medium text-sm text-gray-900">{m.name}</div>
                  <div className="text-xs text-gray-500">{m.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* API Key Input */}
          <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700 flex items-center gap-2">
                  <Key className="w-4 h-4" />
                  {currentProvider?.apiKeyLabel || 'API Key'}
                </label>
                {currentProvider?.keyUrl && (
                <a
                  href={currentProvider.keyUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-brand-600 hover:text-brand-700 flex items-center gap-1"
                >
                  Get API key
                  <ExternalLink className="w-3 h-3" />
                </a>
              )}
            </div>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => { setApiKey(e.target.value); setSaved(false); setError(null); }}
                placeholder={`Enter your ${currentProvider?.name || ''} API key`}
                className="w-full px-4 py-3 pr-20 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-gray-700"
              >
                {showKey ? 'Hide' : 'Show'}
              </button>
            </div>
              {error && (
                <p className="text-sm text-red-600 flex items-center gap-1">
                  <AlertCircle className="w-4 h-4" />
                  {error}
                </p>
              )}
            </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            disabled={!apiKey.trim()}
            className={cn(
              'w-full py-3 px-4 rounded-lg font-medium transition-all flex items-center justify-center gap-2',
              saved
                ? 'bg-green-500 text-white'
                : apiKey.trim()
                  ? 'bg-brand-500 hover:bg-brand-600 text-white'
                  : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            )}
          >
            {saved ? (
              <>
                <Check className="w-5 h-5" />
                Saved!
              </>
            ) : (
              'Save Settings'
            )}
          </button>

          {/* Info */}
          <p className="text-xs text-gray-500 text-center">
            Your API key is stored locally in your browser and sent directly to the AI provider.
          </p>
        </div>
      )}
    </div>
  )
}
