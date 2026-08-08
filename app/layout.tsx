import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter'
})

export const metadata: Metadata = {
  title: 'PilotVault SA | Pass Your SACAA Exams with Confidence',
  description: 'The most trusted exam preparation platform for student pilots in South Africa. 5000+ questions, 8 subjects, and a 98% pass rate.',
  keywords: ['SACAA', 'pilot exam', 'aviation', 'South Africa', 'PPL', 'CPL', 'flight training'],
  icons: {
    icon: [
      {
        url: '/icon.png?v=3',
        type: 'image/png',
        sizes: '512x512',
      },
      {
        url: '/favicon.ico?v=3',
        type: 'image/x-icon',
        sizes: '16x16 32x32 48x48 64x64',
      },
    ],
    shortcut: '/favicon.ico?v=3',
    apple: [
      {
        url: '/apple-icon.png?v=3',
        type: 'image/png',
        sizes: '180x180',
      },
    ],
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-background">
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
