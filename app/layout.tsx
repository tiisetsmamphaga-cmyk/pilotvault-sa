import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import { AppMobileNavigation } from '@/components/app-mobile-navigation'
import { SessionGuard } from '@/components/session-guard'
import {
  CONTACT_EMAIL,
  SITE_DESCRIPTION,
  SITE_NAME,
  SITE_TITLE,
  SITE_URL,
  openGraphDefaults,
} from '@/lib/seo'
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

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: SITE_TITLE,
    template: `%s | ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  keywords: ['SACAA', 'pilot exam', 'aviation', 'South Africa', 'PPL', 'CPL', 'flight training'],
  openGraph: {
    ...openGraphDefaults,
    title: SITE_TITLE,
    description: SITE_DESCRIPTION,
    url: SITE_URL,
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

// Tells search engines who runs the site and what it is, for richer search listings.
const structuredData = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'EducationalOrganization',
      '@id': `${SITE_URL}/#organization`,
      name: SITE_NAME,
      url: SITE_URL,
      logo: `${SITE_URL}/images/logo.png`,
      email: CONTACT_EMAIL,
      areaServed: { '@type': 'Country', name: 'South Africa' },
      description: SITE_DESCRIPTION,
    },
    {
      '@type': 'WebSite',
      '@id': `${SITE_URL}/#website`,
      name: SITE_NAME,
      url: SITE_URL,
      inLanguage: 'en-ZA',
      publisher: { '@id': `${SITE_URL}/#organization` },
    },
  ],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className="bg-background">
      <body className={`${inter.variable} font-sans antialiased`}>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(structuredData).replace(/</g, '\\u003c'),
          }}
        />
        {children}
        <SessionGuard />
        <AppMobileNavigation />
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
