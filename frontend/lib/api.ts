/**
 * API client for ShotGen backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_PREFIX = '/api/v1'

export interface GenerationParams {
  scene?: string
  style?: string
  lighting?: string
  angle?: string
  width?: number
  height?: number
  variations?: number
  removeBackground?: boolean
  seed?: number
}

export interface GenerationResult {
  id: string
  images: string[] // Base64 encoded
  product_cutout: string
  seeds: number[]
  provider: string
  model: string
  generation_time_ms: number
  cost_usd: number | null
}

export interface SceneTemplates {
  templates: Record<string, string>
}

export interface HealthStatus {
  status: string
  ai_provider: {
    name: string
    healthy: boolean
  }
  background_removal: {
    healthy: boolean
  }
}

class APIClient {
  private baseUrl: string

  constructor() {
    this.baseUrl = `${API_URL}${API_PREFIX}`
  }

  async generateProductShot(
    image: File,
    params: GenerationParams = {}
  ): Promise<GenerationResult> {
    const formData = new FormData()
    formData.append('image', image)
    
    // Add optional parameters
    if (params.scene) formData.append('scene', params.scene)
    if (params.style) formData.append('style', params.style)
    if (params.lighting) formData.append('lighting', params.lighting)
    if (params.angle) formData.append('angle', params.angle)
    if (params.width) formData.append('width', params.width.toString())
    if (params.height) formData.append('height', params.height.toString())
    if (params.variations) formData.append('variations', params.variations.toString())
    if (params.removeBackground !== undefined) {
      formData.append('remove_background', params.removeBackground.toString())
    }
    if (params.seed) formData.append('seed', params.seed.toString())

    const response = await fetch(`${this.baseUrl}/generate`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Generation failed')
    }

    return response.json()
  }

  async removeBackground(image: File): Promise<Blob> {
    const formData = new FormData()
    formData.append('image', image)

    const response = await fetch(`${this.baseUrl}/remove-background`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Background removal failed')
    }

    return response.blob()
  }

  async getSceneTemplates(): Promise<SceneTemplates> {
    const response = await fetch(`${this.baseUrl}/scenes`)
    
    if (!response.ok) {
      throw new Error('Failed to fetch scene templates')
    }

    return response.json()
  }

  async healthCheck(): Promise<HealthStatus> {
    const response = await fetch(`${this.baseUrl}/health`)
    
    if (!response.ok) {
      throw new Error('Health check failed')
    }

    return response.json()
  }
}

export const api = new APIClient()

// Helper to convert base64 to blob URL
export function base64ToUrl(base64: string): string {
  return `data:image/png;base64,${base64}`
}

// Helper to download image
export function downloadImage(base64: string, filename: string): void {
  const link = document.createElement('a')
  link.href = base64ToUrl(base64)
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
