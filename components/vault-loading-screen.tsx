import Image from "next/image"

type VaultLoadingScreenProps = {
  message?: string
}

const tickMarks = Array.from({ length: 24 })
const lockingBars = Array.from({ length: 8 })

export function VaultLoadingScreen({
  message = "Opening your PilotVault...",
}: VaultLoadingScreenProps) {
  return (
    <div
      className="fixed inset-0 z-[240] flex min-h-screen items-center justify-center overflow-hidden bg-[#0b121b] px-6 text-white"
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
            "radial-gradient(circle at 50% 42%, rgba(31,78,121,0.26), transparent 24%), radial-gradient(circle at 50% 52%, rgba(137,183,220,0.10), transparent 40%), linear-gradient(180deg,#0b121b 0%,#0e1722 100%)",
        }}
      />

      <div
        className="pointer-events-none absolute inset-0 opacity-[0.055]"
        aria-hidden="true"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,.7) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.7) 1px, transparent 1px)",
          backgroundSize: "42px 42px",
          maskImage: "radial-gradient(circle at 50% 46%, black 0%, transparent 70%)",
        }}
      />

      <div className="relative flex flex-col items-center text-center">
        <div className="pv-vault-stage relative h-[292px] w-[292px] sm:h-[338px] sm:w-[338px]" aria-hidden="true">
          <div className="pv-vault-ambient absolute inset-[2%] rounded-full bg-[#2b6d9f]/10 blur-3xl" />

          <div className="absolute inset-[7%] rounded-[34px] border border-white/[0.08] bg-[linear-gradient(145deg,#243443_0%,#121e29_45%,#0d1720_100%)] shadow-[0_36px_90px_rgba(0,0,0,0.58),inset_0_1px_0_rgba(255,255,255,0.07),inset_0_0_0_1px_rgba(0,0,0,0.5)]">
            <div className="absolute inset-[4.2%] rounded-[28px] border border-white/[0.05] bg-[#0a121a] shadow-[inset_0_0_40px_rgba(0,0,0,0.75)]" />

            <div className="absolute inset-[12%] overflow-hidden rounded-full border-[8px] border-[#283b4c] bg-[#06101a] shadow-[inset_0_0_42px_rgba(0,0,0,.9),0_0_0_1px_rgba(255,255,255,.04)]">
              <div className="pv-vault-glow absolute inset-0 bg-[radial-gradient(circle_at_50%_47%,rgba(119,181,226,0.5),rgba(31,78,121,0.18)_34%,rgba(5,14,22,0.95)_72%)]" />
              <div className="pv-vault-light-ring absolute inset-[8%] rounded-full border border-blue-200/20 shadow-[0_0_40px_rgba(92,158,211,0.28),inset_0_0_34px_rgba(88,160,216,0.18)]" />
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="pv-vault-logo relative rounded-3xl border border-white/10 bg-[#0b1722]/78 px-4 py-3 shadow-[0_0_55px_rgba(77,151,207,0.28)] backdrop-blur-sm">
                  <Image
                    src="/images/logo.png"
                    alt=""
                    width={132}
                    height={96}
                    className="h-[72px] w-auto object-contain sm:h-[84px]"
                    priority
                  />
                </div>
              </div>
              <div className="pv-vault-light-spill absolute bottom-[-24%] left-1/2 h-[75%] w-[55%] -translate-x-1/2 bg-[linear-gradient(to_top,rgba(90,164,219,.26),transparent)] blur-2xl" />
            </div>

            <div className="absolute left-[5%] top-[21%] flex h-[58%] w-[7%] flex-col justify-between py-2">
              {[0, 1, 2].map((hinge) => (
                <div
                  key={hinge}
                  className="h-[29%] rounded-lg border border-white/[0.08] bg-[linear-gradient(90deg,#344b5e,#182938)] shadow-[inset_0_1px_0_rgba(255,255,255,.08),0_4px_12px_rgba(0,0,0,.35)]"
                />
              ))}
            </div>

            <div className="pv-vault-door-shell absolute inset-[11.7%]">
              <div className="relative h-full w-full rounded-full border-[7px] border-[#42596b] bg-[radial-gradient(circle_at_35%_28%,#42647e_0%,#29465d_18%,#173044_48%,#0e2232_72%,#0a1926_100%)] shadow-[0_24px_50px_rgba(0,0,0,0.62),inset_0_2px_0_rgba(255,255,255,0.12),inset_0_-12px_22px_rgba(0,0,0,.34)]">
                <svg className="absolute inset-0 h-full w-full" viewBox="0 0 320 320" fill="none">
                  <defs>
                    <radialGradient id="pvVaultCenter" cx="35%" cy="30%" r="72%">
                      <stop offset="0%" stopColor="#55758f" />
                      <stop offset="38%" stopColor="#294c67" />
                      <stop offset="100%" stopColor="#132a3b" />
                    </radialGradient>
                    <linearGradient id="pvVaultMetal" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stopColor="#d7e1e8" />
                      <stop offset="35%" stopColor="#7f9aae" />
                      <stop offset="68%" stopColor="#b9cad6" />
                      <stop offset="100%" stopColor="#5e778b" />
                    </linearGradient>
                  </defs>

                  <circle cx="160" cy="160" r="139" stroke="rgba(255,255,255,.10)" strokeWidth="2" />
                  <circle cx="160" cy="160" r="126" stroke="rgba(137,183,220,.26)" strokeWidth="2" />
                  <circle cx="160" cy="160" r="106" stroke="rgba(255,255,255,.06)" strokeWidth="1" />

                  <g className="pv-vault-ticks">
                    {tickMarks.map((_, index) => (
                      <line
                        key={index}
                        x1="160"
                        y1="39"
                        x2="160"
                        y2={index % 3 === 0 ? "49" : "45"}
                        stroke={index % 3 === 0 ? "#d5e1e9" : "#708ba0"}
                        strokeOpacity={index % 3 === 0 ? ".72" : ".48"}
                        strokeWidth={index % 3 === 0 ? "2.2" : "1.4"}
                        strokeLinecap="round"
                        transform={`rotate(${index * 15} 160 160)`}
                      />
                    ))}
                  </g>

                  <g className="pv-vault-lock-bars">
                    {lockingBars.map((_, index) => (
                      <g key={index} transform={`rotate(${index * 45} 160 160)`}>
                        <rect x="154" y="53" width="12" height="57" rx="6" fill="url(#pvVaultMetal)" />
                        <rect x="156" y="55" width="3" height="51" rx="1.5" fill="rgba(255,255,255,.24)" />
                      </g>
                    ))}
                  </g>

                  <circle cx="160" cy="160" r="75" fill="url(#pvVaultCenter)" stroke="#617e94" strokeWidth="6" />
                  <circle cx="160" cy="160" r="60" stroke="rgba(255,255,255,.10)" strokeWidth="2" />

                  <g className="pv-vault-wheel">
                    {[0, 60, 120].map((angle) => (
                      <g key={angle} transform={`rotate(${angle} 160 160)`}>
                        <rect x="156" y="93" width="8" height="67" rx="4" fill="url(#pvVaultMetal)" />
                        <circle cx="160" cy="91" r="10" fill="#8fa7b9" stroke="#d8e2e9" strokeWidth="2" />
                      </g>
                    ))}
                    <circle cx="160" cy="160" r="28" fill="#173d5b" stroke="#86a6bd" strokeWidth="5" />
                    <circle cx="160" cy="160" r="12" fill="#1f4e79" stroke="rgba(214,230,247,.55)" strokeWidth="2" />
                    <circle cx="160" cy="160" r="4" fill="#d6e6f7" />
                  </g>

                  <path d="M82 82C106 59 134 49 160 48" stroke="rgba(255,255,255,.10)" strokeWidth="7" strokeLinecap="round" />
                </svg>

                <div className="absolute left-[21%] top-[18%] h-[20%] w-[8%] rounded-full bg-white/[0.045] blur-md" />
              </div>
            </div>

            <div className="pv-vault-latch absolute right-[6.3%] top-1/2 h-12 w-5 -translate-y-1/2 rounded-r-lg border border-l-0 border-white/[0.08] bg-[#263e51] shadow-[0_5px_18px_rgba(0,0,0,.4)]" />
          </div>
        </div>

        <div className="mt-1 flex items-center gap-2 rounded-full border border-blue-200/10 bg-white/[0.035] px-3 py-1.5">
          <span className="pv-vault-status-dot h-1.5 w-1.5 rounded-full bg-[#78b9e8]" />
          <span className="text-[10px] font-bold uppercase tracking-[0.23em] text-blue-100/80">Secure access verified</span>
        </div>
        <p className="mt-3 text-sm font-semibold tracking-wide text-slate-100 sm:text-base">{message}</p>
        <p className="mt-1.5 text-xs text-slate-500">PilotVault SA</p>

        <div className="mt-5 h-[3px] w-36 overflow-hidden rounded-full bg-white/[0.08]" aria-hidden="true">
          <div className="pv-vault-progress h-full rounded-full bg-[linear-gradient(90deg,#417daf,#8fc9ef)]" />
        </div>
      </div>

      <style>{`
        .pv-vault-stage {
          perspective: 1250px;
          animation: pv-vault-stage-in 260ms ease-out both;
        }
        .pv-vault-ambient {
          animation: pv-vault-ambient 1.5s ease-in-out both;
        }
        .pv-vault-door-shell {
          transform-origin: 9% 50%;
          transform-style: preserve-3d;
          backface-visibility: hidden;
          animation: pv-vault-door-open 1.62s cubic-bezier(.72,.04,.18,1) both;
          will-change: transform, filter;
        }
        .pv-vault-wheel {
          transform-origin: 160px 160px;
          animation: pv-vault-wheel-turn 700ms cubic-bezier(.48,.03,.2,1) 80ms both;
        }
        .pv-vault-lock-bars {
          transform-origin: 160px 160px;
          animation: pv-vault-bars-retract 310ms cubic-bezier(.4,0,.2,1) 620ms both;
        }
        .pv-vault-latch {
          animation: pv-vault-latch-release 260ms ease 690ms both;
        }
        .pv-vault-glow {
          opacity: 0;
          animation: pv-vault-glow-on 700ms ease-out 920ms both;
        }
        .pv-vault-light-ring {
          opacity: 0;
          animation: pv-vault-ring-on 620ms ease-out 960ms both;
        }
        .pv-vault-logo {
          opacity: 0;
          animation: pv-vault-logo-in 560ms cubic-bezier(.2,.8,.2,1) 1s both;
        }
        .pv-vault-light-spill {
          opacity: 0;
          animation: pv-vault-spill 600ms ease-out 940ms both;
        }
        .pv-vault-progress {
          width: 0;
          animation: pv-vault-progress 1.62s cubic-bezier(.22,.7,.22,1) both;
        }
        .pv-vault-status-dot {
          animation: pv-vault-status-pulse 1.1s ease-in-out infinite;
        }

        @keyframes pv-vault-stage-in {
          from { opacity: 0; transform: translateY(7px) scale(.975); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes pv-vault-ambient {
          0% { opacity: .25; transform: scale(.82); }
          100% { opacity: 1; transform: scale(1.06); }
        }
        @keyframes pv-vault-wheel-turn {
          0% { transform: rotate(0deg); }
          35% { transform: rotate(128deg); }
          61% { transform: rotate(72deg); }
          100% { transform: rotate(252deg); }
        }
        @keyframes pv-vault-bars-retract {
          0% { transform: scale(1); filter: brightness(1); }
          100% { transform: scale(.69); filter: brightness(.78); }
        }
        @keyframes pv-vault-latch-release {
          0% { transform: translateY(-50%) translateX(0); }
          100% { transform: translateY(-50%) translateX(-11px); opacity: .42; }
        }
        @keyframes pv-vault-door-open {
          0%, 52% { transform: rotateY(0deg) translateZ(0) scale(1); filter: brightness(1); }
          58% { transform: rotateY(-3deg) translateZ(4px) scale(1.002); }
          100% { transform: rotateY(-104deg) translateZ(18px) translateX(-4px) scale(.985); filter: brightness(.8); }
        }
        @keyframes pv-vault-glow-on {
          0% { opacity: 0; transform: scale(.75); }
          100% { opacity: 1; transform: scale(1.08); }
        }
        @keyframes pv-vault-ring-on {
          0% { opacity: 0; transform: scale(.86); }
          100% { opacity: 1; transform: scale(1); }
        }
        @keyframes pv-vault-logo-in {
          0% { opacity: 0; transform: scale(.82); filter: blur(6px); }
          100% { opacity: 1; transform: scale(1); filter: blur(0); }
        }
        @keyframes pv-vault-spill {
          0% { opacity: 0; transform: translateX(-50%) scaleY(.4); }
          100% { opacity: 1; transform: translateX(-50%) scaleY(1); }
        }
        @keyframes pv-vault-progress {
          0% { width: 0%; opacity: .45; }
          42% { width: 39%; }
          71% { width: 71%; }
          100% { width: 100%; opacity: 1; }
        }
        @keyframes pv-vault-status-pulse {
          0%, 100% { opacity: .55; box-shadow: 0 0 0 0 rgba(120,185,232,0); }
          50% { opacity: 1; box-shadow: 0 0 0 5px rgba(120,185,232,.09); }
        }

        @media (prefers-reduced-motion: reduce) {
          .pv-vault-stage,
          .pv-vault-ambient,
          .pv-vault-wheel,
          .pv-vault-lock-bars,
          .pv-vault-latch,
          .pv-vault-glow,
          .pv-vault-light-ring,
          .pv-vault-logo,
          .pv-vault-light-spill,
          .pv-vault-progress,
          .pv-vault-status-dot {
            animation: none;
          }
          .pv-vault-door-shell { animation: none; transform: rotateY(-96deg); }
          .pv-vault-lock-bars { transform: scale(.69); }
          .pv-vault-glow,
          .pv-vault-light-ring,
          .pv-vault-logo,
          .pv-vault-light-spill { opacity: 1; }
          .pv-vault-progress { width: 100%; }
        }
      `}</style>
    </div>
  )
}
