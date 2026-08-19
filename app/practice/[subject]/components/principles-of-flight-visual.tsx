"use client"

import type { Question } from "../types"
import { AngleOfAttackVisual } from "./angle-of-attack-visual"
import { PrinciplesOfFlightVisualV2 } from "./principles-of-flight-visual-v2"

function shouldUseAngleOfAttackVisual(question: Question) {
  const wording = `${question.question} ${question.correctAnswer}`.toLowerCase()
  const topic = question.topic ?? ""

  const asksAoA =
    wording.includes("angle of attack") ||
    wording.includes("angle between") && wording.includes("chord line") && wording.includes("relative airflow")

  const asksRelativeAirflow =
    topic === "Basic Aerodynamics" &&
    wording.includes("relative airflow") &&
    (wording.includes("parallel and opposite") || wording.includes("direction of movement"))

  return asksAoA || asksRelativeAirflow
}

export function PrinciplesOfFlightVisual({ question }: { question: Question }) {
  if (shouldUseAngleOfAttackVisual(question)) {
    return <AngleOfAttackVisual question={question} />
  }

  return (
    <>
      <style>{`svg path[fill="PALE"] { fill: #f8fafc; }`}</style>
      <PrinciplesOfFlightVisualV2 question={question} />
    </>
  )
}
