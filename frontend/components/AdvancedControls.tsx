'use client'

import { Upload, Wand2, Grid3x3 } from 'lucide-react'

interface AdvancedControlsProps {
  resolution: '1024' | '2048' | '4096'
  useInpainting: boolean
  useControlNet: boolean
  customBackground: File | null
  onResolutionChange: (resolution: '1024' | '2048' | '4096') => void
  onUseInpaintingChange: (use: boolean) => void
  onUseControlNetChange: (use: boolean) => void
  onCustomBackgroundChange: (file: File | null) => void
}

const RESOLUTIONS = [
  { value: '1024', label: '1K', description: 'Fast (1024×1024)' },
  { value: '2048', label: '2K', description: 'HD (2048×2048)' },
  { value: '4096', label: '4K', description: 'Ultra HD (4096×4096)' },
]

export function AdvancedControls({
  resolution,
  useInpainting,
  useControlNet,
  customBackground,
  onResolutionChange,
  onUseInpaintingChange,
  onUseControlNetChange,
  onCustomBackgroundChange,
}: AdvancedControlsProps) {
  const handleBackgroundUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      onCustomBackgroundChange(file)
    }
  }

  return (
    <div className="space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-700">🎨 Advanced Features</h3>
        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">Pro</span>
      </div>

      {/* Resolution Selector */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          <Grid3x3 className="w-4 h-4 inline mr-1" />
          Resolution
        </label>
        <div className="grid grid-cols-3 gap-2">
          {RESOLUTIONS.map((res) => (
            <button
              key={res.value}
              onClick={() => onResolutionChange(res.value as any)}
              className={`p-2 rounded-lg border-2 transition-all ${
                resolution === res.value
                  ? 'border-brand-500 bg-brand-50 text-brand-700'
                  : 'border-gray-200 hover:border-gray-300 text-gray-700'
              }`}
            >
              <div className="font-semibold text-sm">{res.label}</div>
              <div className="text-xs text-gray-500">{res.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Product Preservation Mode */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          <Wand2 className="w-4 h-4 inline mr-1" />
          Product Preservation
        </label>
        
        <div className="space-y-2">
          <label className="flex items-start gap-2 p-3 rounded-lg border-2 cursor-pointer transition-all hover:bg-gray-50 ${
            useInpainting ? 'border-brand-500 bg-brand-50' : 'border-gray-200'
          }">
            <input
              type="checkbox"
              checked={useInpainting}
              onChange={(e) => onUseInpaintingChange(e.target.checked)}
              className="mt-1"
            />
            <div className="flex-1">
              <div className="font-medium text-sm text-gray-900">Inpainting Mode</div>
              <div className="text-xs text-gray-600">
                ✅ Preserves product exactly, changes only background
              </div>
            </div>
          </label>

          <label className="flex items-start gap-2 p-3 rounded-lg border-2 cursor-pointer transition-all hover:bg-gray-50 ${
            useControlNet ? 'border-brand-500 bg-brand-50' : 'border-gray-200'
          }">
            <input
              type="checkbox"
              checked={useControlNet}
              onChange={(e) => onUseControlNetChange(e.target.checked)}
              className="mt-1"
            />
            <div className="flex-1">
              <div className="font-medium text-sm text-gray-900">ControlNet Mode</div>
              <div className="text-xs text-gray-600">
                🎯 Preserves product structure, changes style/scene
              </div>
            </div>
          </label>
        </div>

        {useInpainting && useControlNet && (
          <div className="text-xs text-amber-600 bg-amber-50 p-2 rounded">
            ⚠️ Both modes enabled - Inpainting takes priority
          </div>
        )}
      </div>

      {/* Custom Background Upload */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          <Upload className="w-4 h-4 inline mr-1" />
          Custom Background
        </label>
        
        <div className="relative">
          <input
            type="file"
            accept="image/*"
            onChange={handleBackgroundUpload}
            className="hidden"
            id="custom-background-upload"
          />
          <label
            htmlFor="custom-background-upload"
            className="flex items-center justify-center gap-2 p-3 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-brand-500 hover:bg-brand-50 transition-all"
          >
            <Upload className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">
              {customBackground ? customBackground.name : 'Upload your own background'}
            </span>
          </label>
        </div>

        {customBackground && (
          <button
            onClick={() => onCustomBackgroundChange(null)}
            className="text-xs text-red-600 hover:text-red-700"
          >
            Remove custom background
          </button>
        )}

        <div className="text-xs text-gray-500">
          💡 Upload a background image to composite your product onto
        </div>
      </div>
    </div>
  )
}
