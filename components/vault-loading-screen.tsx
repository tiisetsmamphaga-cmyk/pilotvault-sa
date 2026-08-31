import Image from "next/image"

type VaultLoadingScreenProps = {
  message?: string
}

export function VaultLoadingScreen({
  message = "Unlocking your dashboard...",
}: VaultLoadingScreenProps) {
  return (
    <div
      className="fixed inset-0 z-[240] flex min-h-screen items-center justify-center overflow-hidden bg-[#0f1720] px-6 text-white"
      role="status"
      aria-busy="true"
      aria-live="polite"
      aria-label={message}
    >
      <div
        className="pointer-events-none absolute inset-0"
        aria-hidden="true"
        style={{
          background:
            "radial-gradient(circle at 50% 44%, rgba(31,78,121,0.34), transparent 24%), radial-gradient(circle at 50% 52%, rgba(214,230,247,0.10), transparent 42%)",
        }}
      />

      <div className="relative flex flex-col items-center text-center">
        <div className="pv-vault-stage relative h-56 w-56 sm:h-64 sm:w-64" aria-hidden="true">
          <div className="absolute inset-[8%] rounded-[28px] border border-blue-200/15 bg-[#101d2b] shadow-[0_28px_70px_rgba(0,0,0,0.45),inset_0_0_0_1px_rgba(255,255,255,0.04)]">
            <div className="absolute inset-[10%] overflow-hidden rounded-[22px] border border-[#6ea1cc]/25 bg-[#09131d]">
              <div className="pv-vault-glow absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(83,154,213,0.40),rgba(31,78,121,0.12)_42%,transparent_70%)]" />
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="pv-vault-mark rounded-2xl border border-white/10 bg-white/[0.04] p-3 shadow-[0_0_32px_rgba(83,154,213,0.20)]">
                  <Image
                    src="/images/logo.png"
                    alt=""
                    width={112}
                    height={84}
                    className="h-16 w-auto object-contain sm:h-[72px]"
                    priority
                  />
                </div>
              </div>
              <div className="pv-vault-beam absolute bottom-0 left-1/2 h-2/3 w-24 -translate-x-1/2 bg-gradient-to-t from-blue-300/15 to-transparent blur-xl" />
            </div>

            <div className="absolute left-[6%] top-[18%] h-[64%] w-2 rounded-full bg-[#253b50] shadow-inner" />
            <div className="absolute left-[3.5%] top-[25%] h-5 w-5 rounded-full border border-white/10 bg-[#142435]" />
            <div className="absolute left-[3.5%] bottom-[25%] h-5 w-5 rounded-full border border-white/10 bg-[#142435]" />

            <div className="pv-vault-door absolute inset-[9%] rounded-[24px] border border-[#8fb6d7]/25 bg-[linear-gradient(145deg,#23425f,#172c40_48%,#102232)] shadow-[0_18px_45px_rgba(0,0,0,0.55),inset_0_0_0_2px_rgba(255,255,255,0.035)]">
              <div className="absolute inset-[8%] rounded-[19px] border border-white/[0.07]" />

              <div className="pv-vault-bolt pv-vault-bolt-top absolute left-1/2 top-[8%] h-6 w-2 -translate-x-1/2 rounded-full bg-[#9bb5ca] shadow-[0_0_10px_rgba(214,230,247,0.14)]" />
              <div className="pv-vault-bolt pv-vault-bolt-bottom absolute bottom-[8%] left-1/2 h-6 w-2 -translate-x-1/2 rounded-full bg-[#9bb5ca]" />
              <div className="pv-vault-bolt pv-vault-bolt-left absolute left-[8%] top-1/2 h-2 w-6 -translate-y-1/2 rounded-full bg-[#9bb5ca]" />
              <div className="pv-vault-bolt pv-vault-bolt-right absolute right-[8%] top-1/2 h-2 w-6 -translate-y-1/2 rounded-full bg-[#9bb5ca]" />

              <div className="absolute inset-0 flex items-center justify-center">
                <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-[7px] border-[#284b68] bg-[#10283a] shadow-[0_10px_24px_rgba(0,0,0,0.45),inset_0_0_0_2px_rgba(255,255,255,0.05)] sm:h-28 sm:w-28">
                  <div className="pv-vault-dial absolute inset-2 rounded-full border border-[#8db2d1]/35">
                    <span className="absolute left-1/2 top-1 h-3 w-1 -translate-x-1/2 rounded-full bg-[#d6e6f7]" />
                    <span className="absolute bottom-1 left-1/2 h-3 w-1 -translate-x-1/2 rounded-full bg-[#6f91ad]" />
                    <span className="absolute left-1 top-1/2 h-1 w-3 -translate-y-1/2 rounded-full bg-[#6f91ad]" />
                    <span className="absolute right-1 top-1/2 h-1 w-3 -translate-y-1/2 rounded-full bg-[#6f91ad]" />
                  </div>
                  <div className="h-9 w-9 rounded-full border border-blue-100/20 bg-[#1f4e79] shadow-[0_0_18px_rgba(83,154,213,0.25)]" />
                  <div className="pv-vault-handle absolute h-1.5 w-20 rounded-full bg-[#9bb5ca] sm:w-24" />
                  <div className="pv-vault-handle absolute h-20 w-1.5 rounded-full bg-[#9bb5ca] sm:h-24" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <p className="mt-1 text-[11px] font-bold uppercase tracking-[0.32em] text-blue-200">
          PilotVault SA
        </p>
        <p className="mt-3 text-sm font-medium text-slate-200 sm:text-base">{message}</p>
        <div className="mt-5 h-1 w-32 overflow-hidden rounded-full bg-white/10" aria-hidden="true">
          <div className="pv-vault-progress h-full rounded-full bg-[#6ea1cc]" />
        </div>
      </div>

      <style>{`
        .pv-vault-stage { perspective: 900px; }
        .pv-vault-door {
          transform-origin: 7% 50%;
          transform-style: preserve-3d;
          animation: pv-vault-open 1.65s cubic-bezier(.7,.05,.2,1) forwards;
        }
        .pv-vault-dial,
        .pv-vault-handle {
          animation: pv-vault-dial 720ms cubic-bezier(.45,.05,.2,1) 80ms both;
        }
        .pv-vault-bolt-top { animation: pv-bolt-top 260ms ease 650ms forwards; }
        .pv-vault-bolt-bottom { animation: pv-bolt-bottom 260ms ease 650ms forwards; }
        .pv-vault-bolt-left { animation: pv-bolt-left 260ms ease 650ms forwards; }
        .pv-vault-bolt-right { animation: pv-bolt-right 260ms ease 650ms forwards; }
        .pv-vault-glow { animation: pv-vault-glow 1.35s ease 900ms both; }
        .pv-vault-mark { animation: pv-vault-mark 700ms ease 1s both; }
        .pv-vault-beam { animation: pv-vault-beam 900ms ease 900ms both; }
        .pv-vault-progress { animation: pv-vault-progress 1.65s ease-out both; }

        @keyframes pv-vault-dial {
          0% { transform: rotate(0deg); }
          42% { transform: rotate(150deg); }
          70% { transform: rotate(95deg); }
          100% { transform: rotate(220deg); }
        }
        @keyframes pv-bolt-top { to { transform: translate(-50%, 15px); opacity: .35; } }
        @keyframes pv-bolt-bottom { to { transform: translate(-50%, -15px); opacity: .35; } }
        @keyframes pv-bolt-left { to { transform: translate(15px, -50%); opacity: .35; } }
        @keyframes pv-bolt-right { to { transform: translate(-15px, -50%); opacity: .35; } }
        @keyframes pv-vault-open {
          0%, 50% { transform: rotateY(0deg) translateZ(0); }
          58% { transform: rotateY(-4deg) translateZ(1px); }
          100% { transform: rotateY(-108deg) translateZ(8px); }
        }
        @keyframes pv-vault-glow {
          0% { opacity: .05; transform: scale(.82); }
          100% { opacity: 1; transform: scale(1.08); }
        }
        @keyframes pv-vault-mark {
          0% { opacity: 0; transform: scale(.88); filter: blur(5px); }
          100% { opacity: 1; transform: scale(1); filter: blur(0); }
        }
        @keyframes pv-vault-beam {
          0% { opacity: 0; transform: translateX(-50%) scaleY(.35); }
          100% { opacity: 1; transform: translateX(-50%) scaleY(1); }
        }
        @keyframes pv-vault-progress {
          0% { width: 8%; opacity: .5; }
          70% { width: 72%; }
          100% { width: 100%; opacity: 1; }
        }

        @media (prefers-reduced-motion: reduce) {
          .pv-vault-door { animation: none; transform: rotateY(-94deg); }
          .pv-vault-dial,
          .pv-vault-handle,
          .pv-vault-bolt,
          .pv-vault-glow,
          .pv-vault-mark,
          .pv-vault-beam,
          .pv-vault-progress { animation: none; }
          .pv-vault-progress { width: 100%; }
        }
      `}</style>
    </div>
  )
}
