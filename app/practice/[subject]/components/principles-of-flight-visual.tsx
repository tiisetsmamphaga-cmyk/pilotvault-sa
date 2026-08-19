"use client"

import type { Question } from "../types"
import { PrinciplesOfFlightVisualV2 } from "./principles-of-flight-visual-v2"

export function PrinciplesOfFlightVisual({ question }: { question: Question }) {
  return <PrinciplesOfFlightVisualV2 question={question} />
}
