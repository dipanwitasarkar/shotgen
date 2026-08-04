'use client'

import { useState } from 'react'
import { Sparkles, Zap, Camera, AlertTriangle } from 'lucide-react'
import { ImageUploader } from '@/components/ImageUploader'
import { SceneSelector } from '@/components/SceneSelector'
import { GenerationSettings } from '@/components/GenerationSettings'
import { ResultGallery } from '@/components/ResultGallery'
import { SettingsPanel, AppSettings } from '@/components/SettingsPanel'
import { api, GenerationResult } from '@/lib/api'

export default function Home() {
  // State
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [scene, setScene] = useState('white_studio')
  const [style, setStyle] = useState('realistic')
  const [lighting, setLighting] = useState('studio')
  const [angle, setAngle] = useState('front')
  const [variations, setVariations] = useState(2)
  
  const [isGenerating, setIsGenerating] = useState(false)
  const [result, setResult] = useState<GenerationResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  
  // Settings state
  const [appSettings, setAppSettings] = useState<AppSettings | null>(null)

  const handleSettingsChange = (settings: AppSettings) => {
    setAppSettings(settings)
  }

  const handleGenerate = async () => {
    if (!selectedImage) return
    
    if (!appSettings?.apiKey) {
      setError('Please configure your API key in Settings first')
      return
    }

    setIsGenerating(true)
    setError(null)
    setResult(null)

    try {
      const generationResult = await api.generateProductShot(selectedImage, {
        scene,
        style,
        lighting,
        angle,
        variations,
        removeBackground: true,
      })
      setResult(generationResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Generation failed')
    } finally {
      setIsGenerating(false)
    }
  }

  const handleClear = () => {
    setSelectedImage(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Camera className="w-8 h-8 text-brand-500" />
              <span className="text-xl font-bold text-gray-900">ShotGen</span>
            </div>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com/yourusername/shotgen"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-center">
        <h1 className="text-4xl sm:text-5xl font-bold text-gray-900 mb-4">
          AI Product Photography
          <span className="text-brand-500"> in Seconds</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          No studio, no photographer, no problem. Upload your product and get professional lifestyle shots instantly.
        </p>
      </section>

      {/* Main App */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column - Input */}
          <div className="space-y-6">
            {/* Settings Panel - API Keys & Model Selection */}
            <SettingsPanel onSettingsChange={handleSettingsChange} />
            
            {/* Warning if not configured */}
            {!appSettings?.apiKey && (
              <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-amber-800 flex items-start gap-3">
                <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium">API Key Required</p>
                  <p className="text-sm mt-1">Open Settings above to add your API key and select a model.</p>
                </div>
              </div>
            )}
            
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-brand-500" />
                Upload Product
              </h2>
              <ImageUploader
                selectedImage={selectedImage}
                onImageSelect={setSelectedImage}
                onClear={handleClear}
              />
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <SceneSelector selected={scene} onSelect={setScene} />
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Generation Options
              </h2>
              <GenerationSettings
                style={style}
                lighting={lighting}
                angle={angle}
                variations={variations}
                onStyleChange={setStyle}
                onLightingChange={setLighting}
                onAngleChange={setAngle}
                onVariationsChange={setVariations}
              />
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={!selectedImage || isGenerating || !appSettings?.apiKey}
              className="w-full py-4 px-6 bg-brand-500 hover:bg-brand-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors flex items-center justify-center gap-2"
            >
              <Sparkles className="w-5 h-5" />
              {isGenerating ? 'Generating...' : 'Generate Product Shots'}
            </button>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
                {error}
              </div>
            )}
          </div>

          {/* Right Column - Output */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Camera className="w-5 h-5 text-brand-500" />
              Generated Shots
            </h2>
            <ResultGallery
              images={result?.images || []}
              cutout={result?.product_cutout || null}
              isLoading={isGenerating}
              generationTime={result?.generation_time_ms}
              cost={result?.cost_usd}
            />
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-gray-50 border-t border-gray-200 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-12">
            Why ShotGen?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-12 h-12 bg-brand-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Zap className="w-6 h-6 text-brand-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Lightning Fast</h3>
              <p className="text-gray-600">Generate professional shots in seconds, not hours</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-brand-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Camera className="w-6 h-6 text-brand-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Studio Quality</h3>
              <p className="text-gray-600">AI-powered photography that rivals professional studios</p>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-brand-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-6 h-6 text-brand-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Multiple Scenes</h3>
              <p className="text-gray-600">Kitchen, outdoor, lifestyle - endless possibilities</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-500 text-sm">
          <p>Built with AI. Open source on GitHub.</p>
        </div>
      </footer>
    </div>
  )
}
