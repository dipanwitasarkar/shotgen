'use client'

import { Download, Loader2 } from 'lucide-react'
import { base64ToUrl, downloadImage } from '@/lib/api'
import { formatDuration } from '@/lib/utils'

interface ResultGalleryProps {
  images: string[]
  cutout: string | null
  isLoading: boolean
  generationTime?: number
  cost?: number | null
}

export function ResultGallery({
  images,
  cutout,
  isLoading,
  generationTime,
  cost,
}: ResultGalleryProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
        <Loader2 className="w-12 h-12 text-brand-500 animate-spin mb-4" />
        <p className="text-gray-600 font-medium">Generating your product shots<span className="loading-dots"></span></p>
        <p className="text-sm text-gray-500 mt-2">This may take 10-30 seconds</p>
      </div>
    )
  }

  if (images.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-64 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
        <p className="text-gray-500">Generated images will appear here</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Stats */}
      {generationTime && (
        <div className="flex items-center gap-4 text-sm text-gray-500">
          <span>Generated in {formatDuration(generationTime)}</span>
          {cost !== null && cost !== undefined && (
            <span>Cost: ${cost.toFixed(3)}</span>
          )}
        </div>
      )}

      {/* Main results */}
      <div className="grid grid-cols-2 gap-4">
        {images.map((image, index) => (
          <div
            key={index}
            className="relative group rounded-xl overflow-hidden border border-gray-200 bg-white"
          >
            <img
              src={base64ToUrl(image)}
              alt={`Generated product shot ${index + 1}`}
              className="w-full aspect-square object-contain"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
              <button
                onClick={() => downloadImage(image, `shotgen-${index + 1}.png`)}
                className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg text-gray-800 font-medium hover:bg-gray-100 transition-colors"
              >
                <Download className="w-4 h-4" />
                Download
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Cutout preview */}
      {cutout && (
        <div className="mt-6">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Product Cutout</h3>
          <div className="relative group w-32 h-32 rounded-lg overflow-hidden border border-gray-200 bg-[url('/checkerboard.svg')] bg-repeat">
            <img
              src={base64ToUrl(cutout)}
              alt="Product cutout"
              className="w-full h-full object-contain"
            />
            <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
              <button
                onClick={() => downloadImage(cutout, 'cutout.png')}
                className="p-2 bg-white rounded-lg hover:bg-gray-100 transition-colors"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
