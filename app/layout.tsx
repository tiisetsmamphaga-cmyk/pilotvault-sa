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
