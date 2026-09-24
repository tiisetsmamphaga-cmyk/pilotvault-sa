import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import { AppMobileNavigation } from '@/components/app-mobile-navigation'
import { SessionGuard } from '@/components/session-guard'
import './globals.css'
import './brand-v2-bridge.css'
import './brand-v2-profile.css'
import './brand-v2-practice.css'
import './brand-v2-edge-cases.css'
import './brand-v2-soft-canvas.css'
import './brand-v2-header-logo.css'
import './brand-v2-navigation.css'

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter'
})

const SITE_URL = 'https://pilotvault.co.za'
const SITE_TITLE = 'PilotVault SA | Pass Your SACAA Exams with Confidence'
const SITE_DESCRIPTION =
  'The most trusted exam preparation platform for student pilots in South Africa. 5000+ questions, 8 subjects, and a 98% pass rate.'

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: SITE_TITLE,
  description: SITE_DESCRIPTION,
  keywords: ['SACAA', 'pilot exam', 'aviation', 'South Africa', 'PPL', 'CPL', 'flight training'],
  openGraph: {
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    url: SITE_URL,
    siteName: 'PilotVault SA',
    images: [
      {
        url: '/images/hero-cockpit.jpg',
        width: 1600,
        height: 1200,
        alt: 'PilotVault SA',
      },
    ],
    locale: 'en_ZA',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    images: ['/images/hero-cockpit.jpg'],
  },
  icons: {
    icon: [
      {
        url: '/favicon.ico',
        type: 'image/x-icon',
        sizes: '16x16 32x32 48x48 64x64',
      },
    ],
    apple: [
      {
        url: '/apple-icon.png',
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
        <SessionGuard />
        <AppMobileNavigation />
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
