# PilotVault POF Visual Production Workflow

## Purpose

Principles of Flight visuals are paid learning assets, not decoration. Every visual must make the exact question easier to understand while preserving the technical truth of the approved source handbook.

**Required pipeline:**

`QUESTION -> SOURCE -> DESIGN BRIEF -> REFINED VISUAL -> QA -> PREVIEW -> DATABASE MAPPING -> PRODUCTION -> LIVE VERIFICATION -> LOCK`

No stage may be skipped.

## Non-negotiable rules

1. Start from an exact PilotVault question and its verified correct answer/explanation.
2. Use the approved POF handbook as the technical source of truth.
3. Treat handbook figures as source material, not as the finished product. Crop, clean, enlarge, clarify and refine them into teaching visuals.
4. Preserve technical relationships from the source: arrows, force directions, axes, labels, geometry and cause/effect relationships.
5. Add only question-relevant teaching aids such as emphasis, highlights, callouts or a comparison when they materially improve understanding.
6. Keep visuals simple, readable, premium and directly relevant to the question.
7. POF learning visuals must be raster assets (`.png`, `.webp`, `.jpg`, `.jpeg`). **Do not create or introduce SVG/vector explanation visuals.**
8. If a suitable raster teaching visual is not ready, show no explanation image rather than substituting a vector, placeholder, generic infographic or loosely related figure.
9. Work in batches of at most five visual concepts. A visual may map to multiple questions only when each mapping is explicitly justified.
10. Never test experimental visual changes directly on `main`. Use a branch and Vercel preview first.
11. Never overwrite an approved visual because a newer version seems prettier. Approved assets are locked unless there is a technical error, visual defect or explicit user-requested change.
12. A batch is not complete until the live PilotVault experience has been verified.

## Required states

Every visual in `data/pof-visual-manifest.json` must have exactly one of these states:

- `SOURCE_FOUND`
- `REFINING`
- `QA_FAILED`
- `QA_APPROVED`
- `PREVIEW_READY`
- `MAPPED`
- `PRODUCTION_READY`
- `LIVE_VERIFIED`

Normal forward progression is:

`SOURCE_FOUND -> REFINING -> QA_APPROVED -> PREVIEW_READY -> MAPPED -> PRODUCTION_READY -> LIVE_VERIFIED`

A failed QA cycle returns to refinement:

`REFINING -> QA_FAILED -> REFINING`

## Stage 1: Question

Record:

- Question ID
- Topic
- Exact question
- Correct answer
- Explanation
- Exact concept being tested

The visual must explain the concept required to understand why the answer is correct.

## Stage 2: Source

Record:

- Source document
- Page number
- Figure number when available
- Source notes relevant to the concept

Do not invent missing aerodynamic relationships. If the source does not support a proposed visual statement, do not add it.

## Stage 3: Design brief

Before image work, define:

- `student_must_understand`: what should become obvious after viewing the visual
- `preserve`: source relationships that must remain unchanged
- `refine`: what should be cropped, enlarged, cleaned, clarified or emphasized
- `add`: only question-specific teaching aids that are justified
- `remove`: page clutter or unrelated material

## Stage 4: Refine the visual

The source figure may be:

- tightly cropped
- cleaned
- denoised
- enlarged
- sharpened
- contrast-corrected
- reorganized only when the technical relationships remain unchanged
- annotated with question-specific emphasis

The goal is not simply to make the scan HD. The goal is to create a high-quality instructional asset that makes the exact question easier to understand.

## Gate 1: Technical QA

All must pass:

- source supports the visual
- force directions are correct
- axes and rotations are correct
- aerodynamic relationships are correct
- labels are technically correct
- highlighted answer relationship matches the question

Any failure sets status to `QA_FAILED`.

## Gate 2: Teaching QA

All must pass:

- directly helps answer the question
- concept becomes easier to understand
- no irrelevant theory
- no unnecessary complexity
- suitable for a student who answered incorrectly

An attractive image that does not teach the answer fails.

## Gate 3: Visual QA

All must pass:

- raster format only
- sharp at intended display size
- readable labels
- clean crop
- sensible whitespace
- no spelling errors
- no AI artifacts
- no distorted aircraft/components
- consistent PilotVault presentation

## Export standard

Keep two outputs where practical:

- **Master:** high-quality PNG
- **Web:** high-quality WebP

Do not destroy legibility to chase a small file size.

## Preview gate

Before production:

1. Assets and code live on a preview branch.
2. Vercel preview must build successfully.
3. The actual explanation UI must be checked for size, sharpness, crop, title/caption placement and mobile readability.
4. Only then can status become `PREVIEW_READY`.

## Mapping gate

Each question mapping must be explicit and include a mapping reason. Reuse is allowed only when the same visual genuinely explains the mapped question.

Mapping is not complete merely because two questions share a topic.

## Production gate

After preview approval:

1. Promote the tested commit to `main`.
2. Activate the exact database mappings.
3. Verify production deployment is ready.
4. Verify the live question renders the correct visual.

Only then can status become `LIVE_VERIFIED`.

## Live verification checklist

- correct question
- correct visual
- correct title
- correct caption
- no broken image
- no stretching
- no blur caused by upscaling
- good desktop presentation
- good mobile presentation
- acceptable loading behavior

## Approved asset lock

A `LIVE_VERIFIED` asset is locked. Replacement requires one of:

- `technical_error`
- `visual_error`
- `user_requested_change`

Never silently regenerate or replace an approved asset.

## Failure handling

- Image problem -> fix only the image asset.
- Mapping problem -> rollback only the mapping.
- Code problem -> rollback the code commit.
- Preview/Vercel problem -> do not promote.
- Source ambiguity -> stop at source/design brief stage.
- Technical uncertainty -> return to the handbook.

Do not solve a local failure by redesigning the visual system.

## Batch completion definition

A batch is complete only when every visual in the batch is technically approved, visually approved, preview verified, correctly mapped, production deployed and live verified.

Reporting format:

```
POF BATCH XX

VISUALS
5 created
5 QA approved
5 preview verified

QUESTIONS
<count> mapped

SOURCE
Pages <...>

DEPLOYMENT
GitHub: PASS/FAIL
Vercel Preview: PASS/FAIL
Supabase: PASS/FAIL
Production: PASS/FAIL
Live UI: PASS/FAIL

STATUS
COMPLETE / NOT COMPLETE
```

## Final product rule

> We are not creating images for PilotVault. We are creating instructional assets that students are paying to learn from.
