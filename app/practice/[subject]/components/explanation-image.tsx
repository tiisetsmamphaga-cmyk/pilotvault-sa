
export function ExplanationImage({
  src,
  alt,
  priority = false,
}: ExplanationImageProps) {
  const usesBankAngleVisual =
    src.includes("/explanation-images/human-performance/load-factor-bank-")
  const isUnapprovedPofVisual =
    src.includes("/explanation-images/principles-of-flight/") &&
    !src.includes("/explanation-images/principles-of-flight/pdf-rebuild/")

  // Only the PDF-reference POF library is approved during staged QA. Older
  // POF explanation assets remain hidden; question-reference images are
  // rendered separately by QuestionReferenceImage and are unaffected.
  if (isUnapprovedPofVisual) {
    return null
  }

  if (usesBankAngleVisual) {
    return <BankAngleLoadFactorVisual />
  }

  return <StandardExplanationImage src={src} alt={alt} priority={priority} />
}
