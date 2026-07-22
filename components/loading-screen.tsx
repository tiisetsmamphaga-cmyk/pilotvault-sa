type LoadingScreenProps = {
  message?: string
  className?: string
}

export function LoadingScreen({
  message = "Loading...",
  className = "",
}: LoadingScreenProps) {
  return (
    <div
      className={`fixed inset-0 z-[200] flex min-h-screen items-center justify-center bg-[#06111f] px-6 text-white ${className}`}
      role="status"
      aria-busy="true"
      aria-live="polite"
      aria-label={message}
    >
      <div className="flex flex-col items-center text-center">
        <div className="relative h-12 w-12" aria-hidden="true">
          <div className="absolute inset-0 rounded-full border-2 border-[#1e3a5f]" />
          <div className="absolute inset-0 animate-spin rounded-full border-2 border-transparent border-t-[#f4b400] motion-reduce:animate-none" />
          <div className="absolute inset-[17px] rounded-full bg-[#f4b400]" />
        </div>

        <p className="mt-5 text-xs font-semibold uppercase tracking-[0.3em] text-[#f4b400]">
          PilotVault SA
        </p>
        <p className="mt-2 text-sm font-medium text-[#b8c7d9]">{message}</p>
      </div>
    </div>
  )
}
