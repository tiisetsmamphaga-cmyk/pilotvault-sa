import { Plane } from "lucide-react"

type LoadingScreenProps = {
  message?: string
  className?: string
}

export function LoadingScreen({
  message = "Preparing your flight deck...",
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
        className="pointer-events-none absolute inset-0 opacity-80"
        aria-hidden="true"
        style={{
          background:
            "radial-gradient(circle at 50% 46%, rgba(30, 58, 95, 0.48), transparent 30%), radial-gradient(circle at 50% 50%, rgba(244, 180, 0, 0.05), transparent 48%)",
        }}
      />

      <div className="relative flex flex-col items-center text-center">
        <div
          className="pointer-events-none absolute left-1/2 top-12 h-40 w-40 -translate-x-1/2 rounded-full bg-[#f4b400]/10 blur-3xl"
          aria-hidden="true"
        />

        <div className="relative h-28 w-28" aria-hidden="true">
          <div className="absolute inset-0 rounded-full border border-[#29476d]" />
          <div className="absolute inset-[9px] rounded-full border border-dashed border-[#29476d]/80" />
          <div className="pv-radar-sweep absolute inset-[15px] rounded-full" />

          <span className="absolute left-1/2 top-0 h-1.5 w-px -translate-x-1/2 bg-[#f4b400]/70" />
          <span className="absolute bottom-0 left-1/2 h-1.5 w-px -translate-x-1/2 bg-[#29476d]" />
          <span className="absolute left-0 top-1/2 h-px w-1.5 -translate-y-1/2 bg-[#29476d]" />
          <span className="absolute right-0 top-1/2 h-px w-1.5 -translate-y-1/2 bg-[#29476d]" />

          <div className="pv-plane-orbit absolute inset-0">
            <div className="absolute left-1/2 top-[-5px] flex h-7 w-7 -translate-x-1/2 items-center justify-center rounded-full border border-[#f4b400]/40 bg-[#102740] text-[#f4b400] shadow-[0_0_18px_rgba(244,180,0,0.35)]">
              <Plane className="h-4 w-4 rotate-90" strokeWidth={2} />
            </div>
          </div>

          <div className="absolute inset-[39px] flex items-center justify-center rounded-full border border-[#f4b400]/50 bg-[#0b1f35] shadow-[0_0_22px_rgba(244,180,0,0.18)]">
            <span className="pv-loader-beacon h-2.5 w-2.5 rounded-full bg-[#f4b400]" />
          </div>
        </div>

        <p className="mt-6 text-[11px] font-bold uppercase tracking-[0.36em] text-[#f4b400]">
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
