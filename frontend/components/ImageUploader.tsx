'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon } from 'lucide-react'
import { cn, formatBytes } from '@/lib/utils'

interface ImageUploaderProps {
  onImageSelect: (file: File) => void
  selectedImage: File | null
  onClear: () => void
}

export function ImageUploader({ onImageSelect, selectedImage, onClear }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      onImageSelect(file)
      const reader = new FileReader()
      reader.onload = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }, [onImageSelect])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  })

  const handleClear = () => {
    setPreview(null)
    onClear()
  }

  if (selectedImage && preview) {
    return (
      <div className="relative rounded-xl overflow-hidden border-2 border-gray-200 bg-gray-50">
        <img
          src={preview}
          alt="Selected product"
          className="w-full h-64 object-contain bg-white"
        />
        <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
          <div className="flex items-center justify-between text-white">
            <div className="flex items-center gap-2">
              <ImageIcon className="w-4 h-4" />
              <span className="text-sm font-medium truncate max-w-[200px]">
                {selectedImage.name}
              </span>
              <span className="text-xs opacity-75">
                ({formatBytes(selectedImage.size)})
              </span>
            </div>
            <button
              onClick={handleClear}
              className="p-1.5 rounded-full bg-white/20 hover:bg-white/30 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div
      {...getRootProps()}
      className={cn(
        'dropzone flex flex-col items-center justify-center h-64',
        isDragActive && 'active'
      )}
    >
      <input {...getInputProps()} />
      <Upload className={cn(
        'w-12 h-12 mb-4 transition-colors',
        isDragActive ? 'text-brand-500' : 'text-gray-400'
      )} />
      <p className="text-lg font-medium text-gray-700">
        {isDragActive ? 'Drop your product image here' : 'Drag & drop your product image'}
      </p>
      <p className="text-sm text-gray-500 mt-2">
        or click to browse (PNG, JPG, WebP up to 10MB)
      </p>
    </div>
  )
}
