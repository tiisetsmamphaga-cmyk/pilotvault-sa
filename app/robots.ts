import type { MetadataRoute } from "next"

const SITE_URL = "https://pilotvault.co.za"

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/dashboard", "/profile", "/practice", "/auth", "/upgrade"],
    },
    sitemap: `${SITE_URL}/sitemap.xml`,
  }
}
