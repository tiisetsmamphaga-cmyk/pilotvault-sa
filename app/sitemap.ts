import type { MetadataRoute } from "next"

const SITE_URL = "https://pilotvault.co.za"

const PUBLIC_ROUTES = ["", "/features", "/subjects", "/about", "/faq", "/terms", "/privacy"]

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date()

  return PUBLIC_ROUTES.map((route) => ({
    url: `${SITE_URL}${route}`,
    lastModified,
    changeFrequency: route === "" ? "weekly" : "monthly",
    priority: route === "" ? 1 : 0.6,
  }))
}
