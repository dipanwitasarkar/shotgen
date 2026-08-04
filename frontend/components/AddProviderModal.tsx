'use client'

import { useState } from 'react'
import { X, Plus, AlertCircle } from 'lucide-react'
import { cn } from '@/lib/utils'

interface AddProviderModalProps {
  isOpen: boolean
  onClose: () => void
  onAdd: (provider: CustomProvider) => void
}

export interface CustomProvider {
  id: string
  name: string
  description: string
  apiKeyLabel: string
  baseUrl?: string
  models: CustomModel[]
}

export interface CustomModel {
  id: string
  name: string
  description: string
}

export function AddProviderModal({ isOpen, onClose, onAdd }: AddProviderModalProps) {
  const [name, setName] = useState('')
  const [id, setId] = useState('')
  const [description, setDescription] = useState('')
  const [apiKeyLabel, setApiKeyLabel] = useState('API Key')
  const [baseUrl, setBaseUrl] = useState('')
  const [models, setModels] = useState<CustomModel[]>([
    { id: '', name: '', description: '' }
  ])
  const [error, setError] = useState<string | null>(null)

  if (!isOpen) return null

  const handleAddModel = () => {
    setModels([...models, { id: '', name: '', description: '' }])
  }

  const handleRemoveModel = (index: number) => {
    setModels(models.filter((_, i) => i !== index))
  }

  const handleModelChange = (index: number, field: keyof CustomModel, value: string) => {
    const updated = [...models]
    updated[index] = { ...updated[index], [field]: value }
    setModels(updated)
  }

  const handleSubmit = () => {
    // Validation
    if (!name.trim()) {
      setError('Provider name is required')
      return
    }
    if (!id.trim()) {
      setError('Provider ID is required')
      return
    }
    if (models.length === 0 || !models[0].id) {
      setError('At least one model is required')
      return
    }

    // Filter out empty models
    const validModels = models.filter(m => m.id.trim() && m.name.trim())
    
    if (validModels.length === 0) {
      setError('At least one valid model is required')
      return
    }

    const provider: CustomProvider = {
      id: id.toLowerCase().replace(/\s+/g, '-'),
      name,
      description,
      apiKeyLabel,
      baseUrl: baseUrl.trim() || undefined,
      models: validModels,
    }

    onAdd(provider)
    handleClose()
  }

  const handleClose = () => {
    setName('')
    setId('')
    setDescription('')
    setApiKeyLabel('API Key')
    setBaseUrl('')
    setModels([{ id: '', name: '', description: '' }])
    setError(null)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Add Custom Provider</h2>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Provider Info */}
          <div className="space-y-4">
            <h3 className="font-semibold text-gray-900">Provider Information</h3>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provider Name *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g., OpenAI, Hugging Face, RunPod"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Provider ID *
              </label>
              <input
                type="text"
                value={id}
                onChange={(e) => setId(e.target.value)}
                placeholder="e.g., openai, huggingface, runpod"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500 mt-1">Lowercase, no spaces (will be auto-formatted)</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <input
                type="text"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="e.g., Fast inference, good pricing"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Key Label
              </label>
              <input
                type="text"
                value={apiKeyLabel}
                onChange={(e) => setApiKeyLabel(e.target.value)}
                placeholder="e.g., API Key, Access Token"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Base URL (optional)
              </label>
              <input
                type="text"
                value={baseUrl}
                onChange={(e) => setBaseUrl(e.target.value)}
                placeholder="e.g., https://api.provider.com/v1"
                className="w-full px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Models */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900">Models *</h3>
              <button
                onClick={handleAddModel}
                className="flex items-center gap-1 px-3 py-1.5 bg-brand-500 text-white rounded-lg text-sm hover:bg-brand-600 transition-colors"
              >
                <Plus className="w-4 h-4" />
                Add Model
              </button>
            </div>

            {models.map((model, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">Model {index + 1}</span>
                  {models.length > 1 && (
                    <button
                      onClick={() => handleRemoveModel(index)}
                      className="text-red-600 hover:text-red-700 text-sm"
                    >
                      Remove
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Model ID *
                    </label>
                    <input
                      type="text"
                      value={model.id}
                      onChange={(e) => handleModelChange(index, 'id', e.target.value)}
                      placeholder="e.g., gpt-4, sdxl"
                      className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">
                      Model Name *
                    </label>
                    <input
                      type="text"
                      value={model.name}
                      onChange={(e) => handleModelChange(index, 'name', e.target.value)}
                      placeholder="e.g., GPT-4, SDXL"
                      className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">
                    Description
                  </label>
                  <input
                    type="text"
                    value={model.description}
                    onChange={(e) => handleModelChange(index, 'description', e.target.value)}
                    placeholder="e.g., Best quality, slower"
                    className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                  />
                </div>
              </div>
            ))}
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg flex items-start gap-2 text-red-700">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <p className="text-sm">{error}</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="sticky bottom-0 bg-gray-50 border-t border-gray-200 px-6 py-4 flex items-center justify-end gap-3">
          <button
            onClick={handleClose}
            className="px-4 py-2 text-gray-700 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors"
          >
            Add Provider
          </button>
        </div>
      </div>
    </div>
  )
}
