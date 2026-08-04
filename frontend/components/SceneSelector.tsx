'use client'

import { cn } from '@/lib/utils'

const SCENES = [
  { id: 'white_studio', name: 'White Studio', emoji: '⬜' },
  { id: 'kitchen', name: 'Kitchen', emoji: '🍳' },
  { id: 'outdoor', name: 'Outdoor', emoji: '🌿' },
  { id: 'lifestyle', name: 'Lifestyle', emoji: '🏠' },
  { id: 'minimal', name: 'Minimal', emoji: '✨' },
  { id: 'luxury', name: 'Luxury', emoji: '💎' },
  { id: 'nature', name: 'Nature', emoji: '🌲' },
  { id: 'tech', name: 'Tech', emoji: '💻' },
]

interface SceneSelectorProps {
  selected: string
  onSelect: (scene: string) => void
}

export function SceneSelector({ selected, onSelect }: SceneSelectorProps) {
  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">
        Scene Template
      </label>
      <div className="grid grid-cols-4 gap-2">
        {SCENES.map((scene) => (
          <button
            key={scene.id}
            onClick={() => onSelect(scene.id)}
            className={cn(
              'flex flex-col items-center p-3 rounded-lg border-2 transition-all',
              selected === scene.id
                ? 'border-brand-500 bg-brand-50 text-brand-700'
                : 'border-gray-200 hover:border-gray-300 text-gray-600'
            )}
          >
            <span className="text-2xl mb-1">{scene.emoji}</span>
            <span className="text-xs font-medium">{scene.name}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
