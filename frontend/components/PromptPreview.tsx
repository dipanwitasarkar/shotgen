'use client'

import { useState, useEffect } from 'react'
import { Eye, Edit2, Copy, Check } from 'lucide-react'

interface PromptPreviewProps {
  scene: string
  style: string
  lighting: string
  angle: string
  customPrompt?: string
  onCustomPromptChange?: (prompt: string) => void
}

export function PromptPreview({
  scene,
  style,
  lighting,
  angle,
  customPrompt = '',
  onCustomPromptChange,
}: PromptPreviewProps) {
  const [promptData, setPromptData] = useState<any>(null)
  const [isEditing, setIsEditing] = useState(false)
  const [editedPrompt, setEditedPrompt] = useState('')
  const [copied, setCopied] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)

  useEffect(() => {
    fetchPromptPreview()
  }, [scene, style, lighting, angle])

  const fetchPromptPreview = async () => {
    try {
      const formData = new FormData()
      formData.append('scene', customPrompt || scene)
      formData.append('style', style)
      formData.append('lighting', lighting)
      formData.append('angle', angle)

      const response = await fetch('http://localhost:8000/api/v1/preview-prompt', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setPromptData(data)
        setEditedPrompt(data.full_prompt)
      }
    } catch (error) {
      console.error('Failed to fetch prompt preview:', error)
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(promptData?.full_prompt || '')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleSaveEdit = () => {
    if (onCustomPromptChange) {
      onCustomPromptChange(editedPrompt)
    }
    setIsEditing(false)
  }

  if (!promptData) return null

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 space-y-3">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Eye className="w-4 h-4 text-gray-500" />
          <h3 className="font-medium text-sm text-gray-700">Prompt Preview</h3>
          <span className="text-xs text-gray-500">
            ({promptData.provider} / {promptData.model})
          </span>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs text-blue-600 hover:text-blue-700"
        >
          {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </div>

      {/* Prompt Display */}
      {isExpanded && (
        <>
          <div className="space-y-2">
            <div className="text-xs text-gray-500">Scene Description:</div>
            <div className="bg-gray-50 rounded p-2 text-sm text-gray-700 font-mono">
              {promptData.scene_prompt}
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="text-xs text-gray-500">Full Prompt Sent to AI:</div>
              <div className="flex gap-2">
                {!isEditing && (
                  <>
                    <button
                      onClick={() => setIsEditing(true)}
                      className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1"
                    >
                      <Edit2 className="w-3 h-3" />
                      Edit
                    </button>
                    <button
                      onClick={handleCopy}
                      className="text-xs text-blue-600 hover:text-blue-700 flex items-center gap-1"
                    >
                      {copied ? (
                        <>
                          <Check className="w-3 h-3" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" />
                          Copy
                        </>
                      )}
                    </button>
                  </>
                )}
              </div>
            </div>

            {isEditing ? (
              <div className="space-y-2">
                <textarea
                  value={editedPrompt}
                  onChange={(e) => setEditedPrompt(e.target.value)}
                  className="w-full bg-white border border-gray-300 rounded p-2 text-sm font-mono resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={4}
                />
                <div className="flex gap-2">
                  <button
                    onClick={handleSaveEdit}
                    className="px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
                  >
                    Use This Prompt
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false)
                      setEditedPrompt(promptData.full_prompt)
                    }}
                    className="px-3 py-1 bg-gray-200 text-gray-700 text-xs rounded hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div className="bg-blue-50 border border-blue-200 rounded p-3 text-sm text-gray-800 font-mono whitespace-pre-wrap">
                {promptData.full_prompt}
              </div>
            )}
          </div>

          <div className="text-xs text-gray-500 italic">
            💡 Tip: Edit the prompt to include specific product details like "professional camera" or "red sneaker"
          </div>
        </>
      )}
    </div>
  )
}
