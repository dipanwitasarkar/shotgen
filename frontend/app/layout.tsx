import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ShotGen - AI Product Photography',
  description: 'AI product photography in seconds. No studio, no photographer, no problem.',
  keywords: ['AI', 'product photography', 'e-commerce', 'image generation'],
  authors: [{ name: 'ShotGen' }],
  openGraph: {
    title: 'ShotGen - AI Product Photography',
    description: 'Generate professional product photos with AI',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
