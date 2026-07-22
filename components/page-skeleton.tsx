import { LoadingScreen } from "@/components/loading-screen"

type PageSkeletonProps = {
  variant?: "dashboard" | "profile" | "practice"
}

const loadingMessages: Record<NonNullable<PageSkeletonProps["variant"]>, string> = {
  dashboard: "Loading your dashboard...",
  profile: "Loading your profile...",
  practice: "Loading your training session...",
}

export function PageSkeleton({
  variant = "dashboard",
}: PageSkeletonProps) {
  return <LoadingScreen message={loadingMessages[variant]} />
}
