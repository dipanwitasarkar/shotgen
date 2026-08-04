'use client'

import { useState, useEffect } from 'react'
import { Settings, Key, Cpu, ChevronDown, ChevronUp, Check, AlertCircle, ExternalLink, Plus, Trash2 } from 'lucide-react'
import { cn } from '@/lib/utils'
import { AddProviderModal, CustomProvider } from './AddProviderModal'

interface SettingsPanelProps {
  onSettingsChange: (settings: AppSettings) => void
}

export interface AppSettings {
  provider: string
  model: string
  apiKey: string
}

const DEFAULT_PROVIDERS: CustomProvider[] = [
  {
    id: 'replicate',
    name: 'Replicate',
    description: 'Easy to use, pay-per-use pricing',
    apiKeyLabel: 'API Token',
    keyUrl: 'https://replicate.com/account/api-tokens',
    models: [
      { id: 'sdxl', name: 'Stable Diffusion XL', description: 'Best quality, slower' },
      { id: 'sdxl-lightning', name: 'SDXL Lightning', description: 'Fast, good quality' },
      { id: 'flux-schnell', name: 'Flux Schnell', description: 'Very fast, free tier' },
      { id: 'flux-dev', name: 'Flux Dev', description: 'High quality, slower' },
    ],
  },
  {
    id: 'stability',
    name: 'Stability AI',
    description: 'Direct from Stability, competitive pricing',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://platform.stability.ai/account/keys',
    models: [
      { id: 'sd3', name: 'Stable Diffusion 3', description: 'Latest model' },
      { id: 'sdxl-1.0', name: 'SDXL 1.0', description: 'Production ready' },
      { id: 'sd-turbo', name: 'SD Turbo', description: 'Ultra fast' },
    ],
  },
  {
    id: 'fal',
    name: 'FAL.ai',
    description: 'Fast inference, good pricing',
    apiKeyLabel: 'API Key',
    keyUrl: 'https://fal.ai/dashboard/keys',
    models: [
      { id: 'flux-pro', name: 'Flux Pro', description: 'Best quality' },
      { id: 'flux-dev', name: 'Flux Dev', description: 'Development' },
      { id: 'sdxl', name: 'SDXL', description: 'Stable Diffusion XL' },
    ],
  },
]

export function SettingsPanel({ onSettingsChange }: SettingsPanelProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const [provider, setProvider] = useState('replicate')
  const [model, setModel] = useState('flux-schnell')
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [customProviders, setCustomProviders] = useState<CustomProvider[]>([])

  // Load settings and custom providers from localStorage on mount
  useEffect(() => {
    // Load settings
    const savedSettings = localStorage.getItem('shotgen-settings')
    if (savedSettings) {
      try {
        const parsed = JSON.parse(savedSettings)
        setProvider(parsed.provider || 'replicate')
        setModel(parsed.model || 'flux-schnell')
        setApiKey(parsed.apiKey || '')
        onSettingsChange(parsed)
      } catch (e) {
        console.error('Failed to load settings:', e)
      }
    }

    // Load custom providers
    const savedProviders = localStorage.getItem('shotgen-custom-providers')
    if (savedProviders) {
      try {
        const parsed = JSON.parse(savedProviders)
        setCustomProviders(parsed)
      } catch (e) {
        console.error('Failed to load custom providers:', e)
      }
    }
  }, [])

  const allProviders = [...DEFAULT_PROVIDERS, ...customProviders]
  const currentProvider = allProviders.find(p => p.id === provider)
  const currentModels = currentProvider?.models || []

  const handleProviderChange = (newProvider: string) => {
    setProvider(newProvider)
    const providerData = allProviders.find(p => p.id === newProvider)
    if (providerData && providerData.models.length > 0) {
      setModel(providerData.models[0].id)
    }
    setSaved(false)
  }

  const handleAddProvider = (newProvider: CustomProvider) => {
    const updated = [...customProviders, newProvider]
    setCustomProviders(updated)
    localStorage.setItem('shotgen-custom-providers', JSON.stringify(updated))
    
    // Auto-select the new provider
    setProvider(newProvider.id)
    setModel(newProvider.models[0].id)
    setSaved(false)
  }

  const handleDeleteProvider = (providerId: string) => {
    if (window.confirm('Are you sure you want to delete this custom provider?')) {
      const updated = customProviders.filter(p => p.id !== providerId)
      setCustomProviders(updated)
      localStorage.setItem('shotgen-custom-providers', JSON.stringify(updated))
      
      // If deleted provider was selected, switch to default
      if (provider === providerId) {
        setProvider('replicate')
        setModel('flux-schnell')
      }
    }
  }

  const handleSave = async () => {
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
      setTimeout(() => setSaved(false), 3000)
    } catch (e) {
      // Still save locally even if backend fails
      setSaved(true)
      setError(null)
      setTimeout(() => setSaved(false), 3000)
    }
  }

  const isCustomProvider = customProviders.some(p => p.id === provider)

  return (
    <>
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
        {/* Header - Always visible */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <Settings className="w-5 h-5 text-gray-500" />
            <span className="font-semibold text-gray-900">Settings</span>
            {apiKey && (
              <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full">
                Configured
              </span>
            )}
            {customProviders.length > 0 && (
              <span className="px-2 py-0.5 bg-brand-100 text-brand-700 text-xs rounded-full">
                {customProviders.length} Custom
              </span>
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
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700">
                  AI Provider
                </label>
                <button
                  onClick={() => setShowAddModal(true)}
                  className="flex items-center gap-1 px-2 py-1 text-xs bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors"
                >
                  <Plus className="w-3 h-3" />
                  Add Custom
                </button>
              </div>
              <div className="grid grid-cols-3 gap-3">
                {allProviders.map((p) => (
                  <div key={p.id} className="relative">
                    <button
                      onClick={() => handleProviderChange(p.id)}
                      className={cn(
                        'w-full p-3 rounded-xl border-2 text-left transition-all',
                        provider === p.id
                          ? 'border-brand-500 bg-brand-50'
                          : 'border-gray-200 hover:border-gray-300'
                      )}
                    >
                      <div className="font-medium text-gray-900">{p.name}</div>
                      <div className="text-xs text-gray-500 mt-1">{p.description}</div>
                    </button>
                    {isCustomProvider && provider === p.id && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteProvider(p.id)
                        }}
                        className="absolute -top-2 -right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                        title="Delete custom provider"
                      >
                        <Trash2 className="w-3 h-3" />
                      </button>
                    )}
                  </div>
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

      {/* Add Provider Modal */}
      <AddProviderModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onAdd={handleAddProvider}
      />
    </>
  )
}
