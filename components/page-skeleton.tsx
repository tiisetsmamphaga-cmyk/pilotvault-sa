type PageSkeletonProps = {
  variant?: "dashboard" | "profile" | "practice"
}

function SkeletonBlock({ className = "" }: { className?: string }) {
  return (
    <div
      className={`animate-pulse rounded-xl bg-[#15304b] motion-reduce:animate-none ${className}`}
    />
  )
}

function DashboardSkeleton() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <header className="border-b border-[#1e3a5f]">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="space-y-2">
            <SkeletonBlock className="h-2.5 w-24" />
            <SkeletonBlock className="h-4 w-28" />
          </div>
          <div className="flex gap-2">
            <SkeletonBlock className="h-11 w-11 sm:w-28" />
            <SkeletonBlock className="h-11 w-11" />
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="rounded-3xl border border-[#1e3a5f] bg-[#081726] p-5 sm:p-8">
          <SkeletonBlock className="h-3 w-28" />
          <SkeletonBlock className="mt-4 h-8 w-64 max-w-full" />
          <SkeletonBlock className="mt-4 h-4 w-96 max-w-full" />
        </div>

        <div className="mt-6 grid grid-cols-2 gap-3 sm:gap-5 lg:grid-cols-4">
          {Array.from({ length: 8 }, (_, index) => (
            <div
              key={index}
              className="min-h-[142px] rounded-2xl border border-[#1e3a5f] bg-[#081726] p-4 sm:min-h-[178px] sm:p-6"
            >
              <SkeletonBlock className="h-10 w-10 sm:h-12 sm:w-12" />
              <SkeletonBlock className="mt-5 h-4 w-3/4" />
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

function ProfileSkeleton() {
  return (
    <main className="min-h-screen bg-[#06111f] text-white">
      <section className="mx-auto max-w-xl px-4 pb-12 pt-6 sm:px-6 sm:pt-10">
        <div className="flex items-center justify-between">
          <SkeletonBlock className="h-10 w-10 rounded-full" />
          <SkeletonBlock className="h-3 w-24" />
        </div>

        <SkeletonBlock className="mt-8 h-9 w-32" />

        <div className="mt-6 flex items-center gap-4">
          <SkeletonBlock className="h-16 w-16 rounded-full" />
          <div className="flex-1 space-y-3">
            <SkeletonBlock className="h-5 w-40" />
            <SkeletonBlock className="h-4 w-56 max-w-full" />
          </div>
        </div>

        <div className="mt-8 space-y-4">
          {Array.from({ length: 3 }, (_, index) => (
            <div
              key={index}
              className="rounded-2xl border border-[#1e3a5f] bg-[#081726] p-5"
            >
              <SkeletonBlock className="h-4 w-28" />
              <SkeletonBlock className="mt-4 h-6 w-48 max-w-full" />
              <SkeletonBlock className="mt-3 h-4 w-full" />
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

function PracticeSkeleton() {
  return (
    <main className="min-h-screen bg-[#071522] text-white">
      <header className="border-b border-[#29476d] bg-[#081726]">
        <div className="mx-auto flex min-h-16 max-w-7xl items-center justify-between px-4 sm:min-h-20 sm:px-6 lg:px-8">
          <div className="space-y-2">
            <SkeletonBlock className="h-2.5 w-24" />
            <SkeletonBlock className="h-4 w-32" />
          </div>
          <SkeletonBlock className="h-10 w-10 rounded-full" />
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8">
        <div className="rounded-3xl border border-[#29476d] bg-[#0b1d31] p-5 sm:p-8">
          <SkeletonBlock className="h-8 w-72 max-w-full" />
          <SkeletonBlock className="mt-3 h-4 w-56 max-w-full" />
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-2">
          {Array.from({ length: 2 }, (_, index) => (
            <div
              key={index}
              className="min-h-[210px] rounded-2xl border border-[#29476d] bg-[#0b1d31] p-5 sm:p-6"
            >
              <SkeletonBlock className="h-11 w-11" />
              <SkeletonBlock className="mt-5 h-6 w-40" />
              <SkeletonBlock className="mt-3 h-4 w-3/4" />
              <SkeletonBlock className="mt-10 h-9 w-28" />
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

export function PageSkeleton({
  variant = "dashboard",
}: PageSkeletonProps) {
  return (
    <div role="status" aria-live="polite" aria-label="Loading page">
      {variant === "profile" ? (
        <ProfileSkeleton />
      ) : variant === "practice" ? (
        <PracticeSkeleton />
      ) : (
        <DashboardSkeleton />
      )}
    </div>
  )
}
