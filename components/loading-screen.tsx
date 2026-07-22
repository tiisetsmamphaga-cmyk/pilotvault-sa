import { Cloud, Plane } from "lucide-react"

type LoadingScreenProps = {
  message?: string
  className?: string
}

export function LoadingScreen({
  message = "Preparing for takeoff...",
  className = "",
}: LoadingScreenProps) {
  return (
    <div
      className={`fixed inset-0 z-[200] flex min-h-screen items-center justify-center overflow-hidden bg-[#06111f] px-6 text-white ${className}`}
      role="status"
      aria-busy="true"
      aria-live="polite"
      aria-label={message}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-90"
        aria-hidden="true"
        style={{
          background:
            "radial-gradient(circle at 54% 42%, rgba(30, 58, 95, 0.5), transparent 28%), radial-gradient(circle at 50% 55%, rgba(244, 180, 0, 0.045), transparent 46%)",
        }}
      />

      <div className="relative flex flex-col items-center text-center">
        <div
          className="pointer-events-none absolute left-1/2 top-8 h-44 w-44 -translate-x-1/2 rounded-full bg-[#f4b400]/8 blur-3xl"
          aria-hidden="true"
        />

        <div className="relative h-40 w-72 max-w-[82vw] overflow-hidden" aria-hidden="true">
          <Cloud className="absolute left-3 top-10 h-7 w-7 text-[#29476d]/65" strokeWidth={1.25} />
          <Cloud className="absolute right-5 top-5 h-9 w-9 text-[#29476d]/45" strokeWidth={1.1} />

          <svg
            className="absolute inset-0 h-full w-full"
            viewBox="0 0 288 160"
            fill="none"
            preserveAspectRatio="none"
          >
            <path
              className="pv-flight-path"
              d="M18 136C78 136 104 119 132 92C168 57 202 37 272 22"
              stroke="rgba(244,180,0,0.38)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeDasharray="4 7"
            />
          </svg>

          <div className="absolute bottom-4 left-2 h-px w-24 bg-[#29476d]">
            <span className="absolute -top-px left-3 h-px w-6 bg-[#f4b400]/60" />
            <span className="absolute -top-px left-12 h-px w-3 bg-[#f4b400]/35" />
          </div>

          <div className="pv-plane-takeoff absolute bottom-2 left-4 text-[#f4b400]">
            <span className="absolute left-0 top-1/2 h-2 w-9 -translate-x-5 -translate-y-1/2 rounded-full bg-[#f4b400]/20 blur-md" />
            <Plane
              className="relative h-11 w-11 drop-shadow-[0_0_10px_rgba(244,180,0,0.5)]"
              fill="currentColor"
              strokeWidth={1.15}
            />
          </div>
        </div>

        <p className="mt-2 text-[11px] font-bold uppercase tracking-[0.36em] text-[#f4b400]">
          PilotVault SA
        </p>
        <p className="mt-2.5 text-sm font-medium text-[#c7d4e3]">{message}</p>

        <div className="mt-5 flex items-center gap-1.5" aria-hidden="true">
          <span className="pv-status-dot h-1 w-4 rounded-full bg-[#f4b400]" />
          <span className="pv-status-dot h-1 w-4 rounded-full bg-[#f4b400] [animation-delay:180ms]" />
          <span className="pv-status-dot h-1 w-4 rounded-full bg-[#f4b400] [animation-delay:360ms]" />
        </div>
      </div>
    </div>
  )
}
