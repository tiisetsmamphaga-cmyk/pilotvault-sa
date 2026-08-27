# PilotVault POF Hard Stage-Gate Rule

## Core rule

**Perfect current stage -> verify -> persist checkpoint -> only then advance.**

A POF visual or batch must not progress to the next workflow stage while any known defect, ambiguity, weak fit, visual problem, mapping uncertainty, source uncertainty, or technical issue remains in the current stage.

## Non-negotiable behaviour

- No known defects may be carried forward.
- No "fix it later in preview" or "clean it up before production" decisions.
- Efficiency must never override stage quality.
- If a gate fails, remain in that stage until the failure is resolved and the full gate passes again.
- A checkpoint is persisted only after the current stage has been verified.
- If source support is ambiguous, stop at source/design-brief work rather than guessing.
- If a visual is technically correct but visually weak, it remains in refinement.
- If mapping is uncertain, do not map it.
- If preview reveals a problem, return to the appropriate earlier stage rather than carrying the defect into production.
- If production/live verification fails, do not lock the asset.

## Stage advancement requirements

### SOURCE_FOUND -> REFINING
Advance only when the exact PilotVault question, correct answer/explanation, source document, page/figure, concept, and proposed teaching relationship are all verified and mutually consistent.

### REFINING -> QA_APPROVED
Advance only when the actual raster image has been inspected and is technically accurate, question-specific, clean, readable, free of visual defects/AI artifacts, and at least equal to the locked Batch 1 quality benchmark.

### QA_APPROVED -> PREVIEW_READY
Advance only when there are zero known unresolved QA issues and the approved files/manifest are internally consistent.

### PREVIEW_READY -> MAPPED
Advance only after the real PilotVault explanation UI has been verified for the exact asset, including desktop/mobile presentation and loading behaviour.

### MAPPED -> PRODUCTION_READY
Advance only after every intended question mapping is explicitly verified, duplicate ownership is absent, and the database state is complete and internally consistent.

### PRODUCTION_READY -> LIVE_VERIFIED
Advance only after the intended production deployment is READY and the exact live question/asset relationship has been verified.

### LIVE_VERIFIED -> LOCK
Lock only when no further correction is known to be necessary. Locked assets are immutable except for technical_error, visual_error, or user_requested_change.

## Efficiency rule

Work efficiently by eliminating duplicated generation, repeated unnecessary checks, branch churn, metadata-only deployments, and avoidable rework. Never gain speed by weakening a stage gate.

## Final principle

> Fix problems at the earliest stage where they exist. Never knowingly send a problem downstream.
