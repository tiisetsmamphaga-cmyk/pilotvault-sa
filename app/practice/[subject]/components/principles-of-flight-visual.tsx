"use client"

import type { Question } from "../types"
import { PrinciplesOfFlightVisualV3 } from "./principles-of-flight-visual-v3"

export function PrinciplesOfFlightVisual({ question }: { question: Question }) {
  return <PrinciplesOfFlightVisualV3 question={question} />
}
