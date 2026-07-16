import type { ReactNode } from "react"

export default function SubjectPracticeLayout({
  children,
}: Readonly<{
  children: ReactNode
}>) {
  return (
    <>
      <style>{`
        img[alt="Question reference"] {
          display: block;
          width: auto !important;
          max-width: min(100%, 30rem) !important;
          max-height: 22rem;
          margin-left: auto;
          margin-right: auto;
          object-fit: contain;
        }

        @media (min-width: 640px) {
          img[alt="Question reference"] {
            max-height: 26rem;
          }
        }
      `}</style>
      {children}
    </>
  )
}
