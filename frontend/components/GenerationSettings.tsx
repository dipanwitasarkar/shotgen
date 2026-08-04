'use client'

import { cn } from '@/lib/utils'

interface GenerationSettingsProps {
  style: string
  lighting: string
  angle: string
  variations: number
  onStyleChange: (style: string) => void
  onLightingChange: (lighting: string) => void
  onAngleChange: (angle: string) => void
  onVariationsChange: (variations: number) => void
}

const STYLES = [
  { id: 'realistic', name: 'Realistic' },
  { id: 'artistic', name: 'Artistic' },
  { id: 'minimal', name: 'Minimal' },
  { id: 'lifestyle', name: 'Lifestyle' },
]

const LIGHTING = [
  { id: 'studio', name: 'Studio' },
  { id: 'natural', name: 'Natural' },
  { id: 'dramatic', name: 'Dramatic' },
  { id: 'soft', name: 'Soft' },
]

const ANGLES = [
  { id: 'front', name: 'Front' },
  { id: '45-degree', name: '45 Degree' },
  { id: 'top-down', name: 'Top Down' },
  { id: 'side', name: 'Side' },
]

export function GenerationSettings({
  style,
  lighting,
  angle,
  variations,
  onStyleChange,
  onLightingChange,
  onAngleChange,
  onVariationsChange,
}: GenerationSettingsProps) {
  return (
    <div className="space-y-6">
      {/* Style */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Style</label>
        <div className="flex gap-2">
          {STYLES.map((s) => (
            <button
              key={s.id}
              onClick={() => onStyleChange(s.id)}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                style === s.id
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              {s.name}
            </button>
          ))}
        </div>
      </div>

      {/* Lighting */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Lighting</label>
        <div className="flex gap-2">
          {LIGHTING.map((l) => (
            <button
              key={l.id}
              onClick={() => onLightingChange(l.id)}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                lighting === l.id
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              {l.name}
            </button>
          ))}
        </div>
      </div>

      {/* Angle */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Angle</label>
        <div className="flex gap-2">
          {ANGLES.map((a) => (
            <button
              key={a.id}
              onClick={() => onAngleChange(a.id)}
              className={cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                angle === a.id
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              {a.name}
            </button>
          ))}
        </div>
      </div>

      {/* Variations */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">
          Variations: {variations}
        </label>
        <input
          type="range"
          min={1}
          max={4}
          value={variations}
          onChange={(e) => onVariationsChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
        />
        <div className="flex justify-between text-xs text-gray-500">
          <span>1</span>
          <span>4</span>
        </div>
      </div>
    </div>
  )
}
