'use client'

import { useState } from 'react'
import { cn } from '@/lib/utils'
import { ChevronDown, Pencil } from 'lucide-react'

interface SceneCategory {
  name: string
  scenes: { id: string; name: string; emoji: string }[]
}

const SCENE_CATEGORIES: SceneCategory[] = [
  {
    name: 'Studio',
    scenes: [
      { id: 'white_studio', name: 'White Studio', emoji: '⬜' },
      { id: 'black_studio', name: 'Black Studio', emoji: '⬛' },
      { id: 'gradient_studio', name: 'Gradient', emoji: '🌈' },
      { id: 'minimal', name: 'Minimal', emoji: '✨' },
    ],
  },
  {
    name: 'Home',
    scenes: [
      { id: 'kitchen', name: 'Kitchen', emoji: '🍳' },
      { id: 'bathroom', name: 'Bathroom', emoji: '🛁' },
      { id: 'living_room', name: 'Living Room', emoji: '🛋️' },
      { id: 'bedroom', name: 'Bedroom', emoji: '🛏️' },
      { id: 'dining', name: 'Dining', emoji: '🍽️' },
      { id: 'office', name: 'Office', emoji: '💼' },
    ],
  },
  {
    name: 'Outdoor',
    scenes: [
      { id: 'outdoor', name: 'Garden', emoji: '🌿' },
      { id: 'beach', name: 'Beach', emoji: '🏖️' },
      { id: 'forest', name: 'Forest', emoji: '🌲' },
      { id: 'mountain', name: 'Mountain', emoji: '🏔️' },
      { id: 'park', name: 'Park', emoji: '🌳' },
    ],
  },
  {
    name: 'Lifestyle',
    scenes: [
      { id: 'cafe', name: 'Cafe', emoji: '☕' },
      { id: 'restaurant', name: 'Restaurant', emoji: '🍷' },
      { id: 'gym', name: 'Gym', emoji: '💪' },
      { id: 'yoga', name: 'Yoga', emoji: '🧘' },
      { id: 'pool', name: 'Pool', emoji: '🏊' },
    ],
  },
  {
    name: 'Luxury',
    scenes: [
      { id: 'luxury', name: 'Luxury', emoji: '💎' },
      { id: 'jewelry', name: 'Jewelry', emoji: '💍' },
      { id: 'fashion', name: 'Fashion', emoji: '👗' },
      { id: 'art_gallery', name: 'Gallery', emoji: '🖼️' },
    ],
  },
  {
    name: 'Tech',
    scenes: [
      { id: 'tech', name: 'Tech', emoji: '💻' },
      { id: 'gaming', name: 'Gaming', emoji: '🎮' },
      { id: 'workspace', name: 'Workspace', emoji: '🖥️' },
    ],
  },
  {
    name: 'Seasonal',
    scenes: [
      { id: 'christmas', name: 'Christmas', emoji: '🎄' },
      { id: 'autumn', name: 'Autumn', emoji: '🍂' },
      { id: 'spring', name: 'Spring', emoji: '🌸' },
      { id: 'summer', name: 'Summer', emoji: '☀️' },
    ],
  },
  {
    name: 'Food',
    scenes: [
      { id: 'food_flat', name: 'Flat Lay', emoji: '📸' },
      { id: 'rustic_food', name: 'Rustic', emoji: '🥖' },
      { id: 'bar', name: 'Bar', emoji: '🍸' },
    ],
  },
  {
    name: 'Nature',
    scenes: [
      { id: 'nature', name: 'Nature', emoji: '🌱' },
      { id: 'botanical', name: 'Botanical', emoji: '🌺' },
      { id: 'stone', name: 'Stone', emoji: '🪨' },
    ],
  },
]

interface SceneSelectorProps {
  selected: string
  customPrompt: string
  onSelect: (scene: string) => void
  onCustomPromptChange: (prompt: string) => void
}

export function SceneSelector({ 
  selected, 
  customPrompt,
  onSelect, 
  onCustomPromptChange 
}: SceneSelectorProps) {
  const [expandedCategory, setExpandedCategory] = useState<string | null>('Studio')
  const [useCustom, setUseCustom] = useState(false)

  // Find which category the selected scene belongs to
  const findSelectedCategory = () => {
    for (const cat of SCENE_CATEGORIES) {
      if (cat.scenes.some(s => s.id === selected)) {
        return cat.name
      }
    }
    return null
  }

  const selectedCategory = findSelectedCategory()
  const selectedScene = SCENE_CATEGORIES
    .flatMap(c => c.scenes)
    .find(s => s.id === selected)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <label className="block text-sm font-medium text-gray-700">
          Scene Template
        </label>
        <button
          onClick={() => setUseCustom(!useCustom)}
          className={cn(
            'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all',
            useCustom
              ? 'bg-brand-500 text-white'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          )}
        >
          <Pencil className="w-3.5 h-3.5" />
          Custom
        </button>
      </div>

      {useCustom ? (
        <div className="space-y-2">
          <textarea
            value={customPrompt}
            onChange={(e) => onCustomPromptChange(e.target.value)}
            placeholder="Describe your scene... e.g., 'rustic wooden table with morning coffee, soft window light, cozy autumn atmosphere'"
            className="w-full h-24 px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-brand-500 focus:border-transparent resize-none text-sm"
          />
          <p className="text-xs text-gray-500">
            Be descriptive! Include surface, lighting, mood, and atmosphere.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {/* Category tabs */}
          <div className="flex flex-wrap gap-1.5">
            {SCENE_CATEGORIES.map((category) => (
              <button
                key={category.name}
                onClick={() => setExpandedCategory(
                  expandedCategory === category.name ? null : category.name
                )}
                className={cn(
                  'px-3 py-1.5 rounded-lg text-xs font-medium transition-all',
                  expandedCategory === category.name
                    ? 'bg-brand-500 text-white'
                    : selectedCategory === category.name
                      ? 'bg-brand-100 text-brand-700'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                )}
              >
                {category.name}
              </button>
            ))}
          </div>

          {/* Scenes in selected category */}
          {expandedCategory && (
            <div className="grid grid-cols-4 gap-2 p-3 bg-gray-50 rounded-xl">
              {SCENE_CATEGORIES.find(c => c.name === expandedCategory)?.scenes.map((scene) => (
                <button
                  key={scene.id}
                  onClick={() => onSelect(scene.id)}
                  className={cn(
                    'flex flex-col items-center p-2.5 rounded-lg border-2 transition-all',
                    selected === scene.id
                      ? 'border-brand-500 bg-white text-brand-700 shadow-sm'
                      : 'border-transparent bg-white/50 text-gray-600 hover:bg-white hover:border-gray-200'
                  )}
                >
                  <span className="text-xl mb-1">{scene.emoji}</span>
                  <span className="text-xs font-medium text-center leading-tight">{scene.name}</span>
                </button>
              ))}
            </div>
          )}

          {/* Currently selected indicator */}
          {selectedScene && !expandedCategory && (
            <div className="flex items-center gap-2 p-3 bg-brand-50 rounded-xl">
              <span className="text-2xl">{selectedScene.emoji}</span>
              <div>
                <p className="text-sm font-medium text-brand-700">{selectedScene.name}</p>
                <p className="text-xs text-brand-600">Click a category above to change</p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
