import type { Metadata } from "next"

export const SITE_URL = "https://pilotvault.co.za"
export const SITE_NAME = "PilotVault SA"
export const SITE_TITLE = "PilotVault SA | Pass Your SACAA Exams with Confidence"
export const SITE_DESCRIPTION =
  "SACAA exam preparation for student pilots in South Africa. 5000+ practice questions, timed mock exams and detailed explanations. Try it free for 3 days."
export const CONTACT_EMAIL = "contact@pilotvault.co.za"

const SHARE_IMAGE = {
  url: "/images/hero-cockpit.jpg",
  width: 1600,
  height: 1200,
  alt: SITE_NAME,
}

export const openGraphDefaults = {
  siteName: SITE_NAME,
  images: [SHARE_IMAGE],
  locale: "en_ZA",
  type: "website" as const,
}

// Page-level openGraph/twitter objects replace the layout's rather than merging
// with them, so each page repeats the shared site name, locale and share image.
export function pageMetadata({
  title,
  description,
  path,
}: {
  title: string
  description: string
  path: string
}): Metadata {
  const fullTitle = `${title} | ${SITE_NAME}`

  return {
    title,
    description,
    alternates: { canonical: path },
    openGraph: { ...openGraphDefaults, title: fullTitle, description, url: path },
    twitter: {
      card: "summary_large_image",
      title: fullTitle,
      description,
      images: [SHARE_IMAGE.url],
    },
  }
}
