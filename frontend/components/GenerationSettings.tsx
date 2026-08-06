'use client'

import { cn } from '@/lib/utils'

interface GenerationSettingsProps {
  style: string
  lighting: string
  angle: string
  aspectRatio: string
  quality: number
  variations: number
  strength?: number
  guidanceScale?: number
  inferenceSteps?: number
  onStyleChange: (style: string) => void
  onLightingChange: (lighting: string) => void
  onAngleChange: (angle: string) => void
  onAspectRatioChange: (ratio: string) => void
  onQualityChange: (quality: number) => void
  onVariationsChange: (variations: number) => void
  onStrengthChange?: (strength: number) => void
  onGuidanceScaleChange?: (scale: number) => void
  onInferenceStepsChange?: (steps: number) => void
}

const STYLES = [
  { id: 'realistic', name: 'Realistic', description: 'Photo-realistic' },
  { id: 'artistic', name: 'Artistic', description: 'Creative style' },
  { id: 'minimal', name: 'Minimal', description: 'Clean & simple' },
  { id: 'lifestyle', name: 'Lifestyle', description: 'Natural feel' },
  { id: 'editorial', name: 'Editorial', description: 'Magazine style' },
  { id: 'cinematic', name: 'Cinematic', description: 'Movie-like' },
]

const LIGHTING = [
  { id: 'studio', name: 'Studio', description: 'Professional' },
  { id: 'natural', name: 'Natural', description: 'Window light' },
  { id: 'dramatic', name: 'Dramatic', description: 'High contrast' },
  { id: 'soft', name: 'Soft', description: 'Diffused' },
  { id: 'golden_hour', name: 'Golden Hour', description: 'Warm sunset' },
  { id: 'neon', name: 'Neon', description: 'Colorful glow' },
]

const ANGLES = [
  { id: 'front', name: 'Front', icon: '⬆️' },
  { id: '45-degree', name: '45°', icon: '↗️' },
  { id: 'top-down', name: 'Top', icon: '⬇️' },
  { id: 'side', name: 'Side', icon: '➡️' },
  { id: 'low', name: 'Low', icon: '📐' },
  { id: 'hero', name: 'Hero', icon: '🦸' },
]

const ASPECT_RATIOS = [
  { id: '1:1', name: 'Square', width: 1024, height: 1024, icon: '⬜' },
  { id: '4:3', name: 'Standard', width: 1024, height: 768, icon: '🖼️' },
  { id: '3:4', name: 'Portrait', width: 768, height: 1024, icon: '📱' },
  { id: '16:9', name: 'Wide', width: 1024, height: 576, icon: '🖥️' },
  { id: '9:16', name: 'Story', width: 576, height: 1024, icon: '📲' },
  { id: '3:2', name: 'Photo', width: 1024, height: 683, icon: '📷' },
]

export function GenerationSettings({
  style,
  lighting,
  angle,
  aspectRatio,
  quality,
  variations,
  strength,
  guidanceScale,
  inferenceSteps,
  onStyleChange,
  onLightingChange,
  onAngleChange,
  onAspectRatioChange,
  onQualityChange,
  onVariationsChange,
  onStrengthChange,
  onGuidanceScaleChange,
  onInferenceStepsChange,
}: GenerationSettingsProps) {
  return (
    <div className="space-y-6">
      {/* Aspect Ratio */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Aspect Ratio</label>
        <div className="grid grid-cols-6 gap-2">
          {ASPECT_RATIOS.map((ratio) => (
            <button
              key={ratio.id}
              onClick={() => onAspectRatioChange(ratio.id)}
              className={cn(
                'flex flex-col items-center p-2 rounded-lg border-2 transition-all',
                aspectRatio === ratio.id
                  ? 'border-brand-500 bg-brand-50 text-brand-700'
                  : 'border-gray-200 hover:border-gray-300 text-gray-600'
              )}
            >
              <span className="text-lg">{ratio.icon}</span>
              <span className="text-xs font-medium mt-1">{ratio.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Style */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Style</label>
        <div className="grid grid-cols-3 gap-2">
          {STYLES.map((s) => (
            <button
              key={s.id}
              onClick={() => onStyleChange(s.id)}
              className={cn(
                'px-3 py-2 rounded-lg text-sm font-medium transition-all text-left',
                style === s.id
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              <div>{s.name}</div>
              <div className={cn(
                'text-xs mt-0.5',
                style === s.id ? 'text-brand-100' : 'text-gray-400'
              )}>{s.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Lighting */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Lighting</label>
        <div className="grid grid-cols-3 gap-2">
          {LIGHTING.map((l) => (
            <button
              key={l.id}
              onClick={() => onLightingChange(l.id)}
              className={cn(
                'px-3 py-2 rounded-lg text-sm font-medium transition-all text-left',
                lighting === l.id
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              )}
            >
              <div>{l.name}</div>
              <div className={cn(
                'text-xs mt-0.5',
                lighting === l.id ? 'text-brand-100' : 'text-gray-400'
              )}>{l.description}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Angle */}
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Camera Angle</label>
        <div className="grid grid-cols-6 gap-2">
          {ANGLES.map((a) => (
            <button
              key={a.id}
              onClick={() => onAngleChange(a.id)}
              className={cn(
                'flex flex-col items-center p-2 rounded-lg border-2 transition-all',
                angle === a.id
                  ? 'border-brand-500 bg-brand-50 text-brand-700'
                  : 'border-gray-200 hover:border-gray-300 text-gray-600'
              )}
            >
              <span className="text-lg">{a.icon}</span>
              <span className="text-xs font-medium mt-1">{a.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Quality Slider */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="block text-sm font-medium text-gray-700">
            Quality
          </label>
          <span className="text-sm text-gray-500">
            {quality <= 30 ? 'Fast' : quality <= 60 ? 'Balanced' : 'High Quality'}
          </span>
        </div>
        <input
          type="range"
          min={10}
          max={100}
          step={10}
          value={quality}
          onChange={(e) => onQualityChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
        />
        <div className="flex justify-between text-xs text-gray-400">
          <span>Faster</span>
          <span>Better</span>
        </div>
      </div>

      {/* Variations */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="block text-sm font-medium text-gray-700">
            Variations
          </label>
          <span className="text-sm font-medium text-brand-600">{variations}</span>
        </div>
        <input
          type="range"
          min={1}
          max={4}
          value={variations}
          onChange={(e) => onVariationsChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
        />
        <div className="flex justify-between text-xs text-gray-400">
          <span>1</span>
          <span>2</span>
          <span>3</span>
          <span>4</span>
        </div>
      </div>

      {/* Advanced IMG2IMG Settings */}
      {(strength !== undefined || guidanceScale !== undefined || inferenceSteps !== undefined) && (
        <div className="space-y-4 pt-4 border-t border-gray-200">
          <h3 className="text-sm font-semibold text-gray-700">🎛️ Advanced IMG2IMG</h3>
          
          {/* Transformation Strength */}
          {strength !== undefined && onStrengthChange && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="block text-sm font-medium text-gray-700">
                  Transformation Strength
                </label>
                <span className="text-sm font-medium text-brand-600">{strength.toFixed(2)}</span>
              </div>
              <input
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={strength}
                onChange={(e) => onStrengthChange(parseFloat(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
              />
              <p className="text-xs text-gray-500">Higher = more scene transformation</p>
            </div>
          )}

          {/* Guidance Scale */}
          {guidanceScale !== undefined && onGuidanceScaleChange && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="block text-sm font-medium text-gray-700">
                  Prompt Guidance
                </label>
                <span className="text-sm font-medium text-brand-600">{guidanceScale.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min={1}
                max={20}
                step={0.5}
                value={guidanceScale}
                onChange={(e) => onGuidanceScaleChange(parseFloat(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
              />
              <p className="text-xs text-gray-500">Higher = follow prompt more strictly</p>
            </div>
          )}

          {/* Inference Steps */}
          {inferenceSteps !== undefined && onInferenceStepsChange && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="block text-sm font-medium text-gray-700">
                  Quality Steps
                </label>
                <span className="text-sm font-medium text-brand-600">{inferenceSteps}</span>
              </div>
              <input
                type="range"
                min={10}
                max={50}
                step={5}
                value={inferenceSteps}
                onChange={(e) => onInferenceStepsChange(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-brand-500"
              />
              <p className="text-xs text-gray-500">More steps = better quality (slower)</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Export aspect ratio dimensions for use in API calls
export const ASPECT_RATIO_DIMENSIONS: Record<string, { width: number; height: number }> = {
  '1:1': { width: 1024, height: 1024 },
  '4:3': { width: 1024, height: 768 },
  '3:4': { width: 768, height: 1024 },
  '16:9': { width: 1024, height: 576 },
  '9:16': { width: 576, height: 1024 },
  '3:2': { width: 1024, height: 683 },
}
