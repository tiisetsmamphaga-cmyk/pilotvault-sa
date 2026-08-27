# PilotVault POF Visual Production Workflow

## Purpose

Principles of Flight visuals are paid learning assets, not decoration. Every visual must make the exact question easier to understand while preserving the technical truth of the approved source handbook.

**Required pipeline:**

`QUESTION -> SOURCE -> DESIGN BRIEF -> REFINED VISUAL -> QA -> PREVIEW -> DATABASE MAPPING -> PRODUCTION -> LIVE VERIFICATION -> LOCK`

No stage may be skipped.

## Quality reference

The five locked Batch 1 visuals are the minimum accepted quality reference for POF.

A new visual must be comparable to Batch 1 in all of these ways:

- based on an exact verified source figure or source relationship
- refined specifically for the exact question being answered
- visually clean enough to look like a premium aviation learning product
- technically faithful to the handbook
- immediately understandable to a student who answered incorrectly
- not a generic diagram, placeholder, rough geometric sketch, automated infographic or bulk-converted legacy asset

A technically correct but visually weak image fails.

## Non-negotiable rules

1. Start from an exact PilotVault question and its verified correct answer/explanation.
2. Use the approved POF handbook as the technical source of truth.
3. Treat handbook figures as source material, not as the finished product. Crop, clean, enlarge, clarify and refine them into teaching visuals.
4. Preserve technical relationships from the source: arrows, force directions, axes, labels, geometry and cause/effect relationships.
5. Add only question-relevant teaching aids such as emphasis, highlights, callouts or a comparison when they materially improve understanding.
6. Keep visuals simple, readable, premium and directly relevant to the question.
7. POF learning visuals must be raster assets (`.png`, `.webp`, `.jpg`, `.jpeg`). **Do not create or introduce SVG/vector explanation visuals.**
8. If a suitable raster teaching visual is not ready, show no explanation image rather than substituting a vector, placeholder, generic infographic or loosely related figure.
9. Work in batches of at most five visual concepts.
10. A visual may map to multiple questions only when those questions test the same exact visual relationship. Sharing a topic is not sufficient.
11. Never bulk-convert legacy diagrams into production learning assets. Legacy artwork may only be used as source/reference material and must still pass the full question-specific refinement workflow.
12. Never auto-generate a large visual library and mark it approved from file integrity, dimensions, hashes or HTTP checks alone. Those are technical checks, not teaching or visual approval.
13. Never test experimental visual changes directly on `main`. Use a branch and Vercel preview first.
14. Never overwrite an approved visual because a newer version seems prettier. Approved assets are locked unless there is a technical error, visual defect or explicit user-requested change.
15. A batch is not complete until the live PilotVault experience has been visually inspected and verified.
16. PilotVault branding belongs in the website shell. New POF learning images must not have the PilotVault banner baked into the image itself.

## Required states

Every approved workflow visual in `data/pof-visual-manifest.json` must have exactly one of these states:

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

- directly helps answer the exact question
- concept becomes easier to understand
- the visual relationship shown is the relationship being tested
- no irrelevant theory
- no unnecessary complexity
- suitable for a student who answered incorrectly
- any reuse across questions is explicitly justified as the same exact visual concept

An attractive image that does not teach the answer fails. A generic topic image fails.

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
- no crude placeholder geometry
- no generic template look
- presentation quality comparable to the locked Batch 1 reference visuals

## Mandatory human visual-inspection gate

Before `QA_APPROVED`, the actual rendered image must be visually inspected as an image, not only checked through metadata or code.

The inspection must answer yes to all of the following:

1. Would this look acceptable next to a locked Batch 1 visual?
2. Does the picture itself make the answer relationship obvious?
3. Is the aircraft/component representation credible and clean?
4. Does the visual avoid the appearance of a generic generated infographic?
5. Is every annotation necessary for this exact question?

If any answer is no, the visual remains `REFINING` or becomes `QA_FAILED`.

## Export standard

Keep two outputs where practical:

- **Master:** high-quality PNG
- **Web:** high-quality WebP

Do not destroy legibility to chase a small file size.

## Branding separation

From Batch 2 onward, the learning asset contains only teaching content. The PilotVault navy/gold subject banner and diagram title are rendered by the website UI. This keeps the asset reusable, prevents duplicated branding, and lets the site control responsive presentation.

Batch 1 is grandfathered and remains unchanged because it was already approved and locked before this rule was introduced.

## Legacy artwork rule

Legacy POF SVGs, rasterized legacy diagrams and old generated concept artwork are **reference material only**.

They may not be mapped directly to production questions merely because they are technically correct or previously existed. Every new production asset must go through the exact-question source, design brief, refinement, visual inspection, preview and live verification gates above.

No bulk legacy migration is permitted.

## Preview gate

Before production:

1. Assets and code live on a preview branch.
2. Vercel preview must build successfully.
3. The actual explanation UI must be checked for size, sharpness, crop, title/caption placement and mobile readability.
4. The actual image must be visually compared against the Batch 1 quality reference.
5. Only then can status become `PREVIEW_READY`.

## Mapping gate

Each question mapping must be explicit and include a mapping reason.

Reuse is allowed only when the same visual genuinely explains the same exact relationship being tested. For example, a generic adverse-yaw image cannot be reused for separate questions about yaw direction, angle-of-attack effect, rudder coordination and induced drag unless the single visual explicitly and cleanly teaches all of those relationships without becoming cluttered.

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
- visual quality still comparable to the approved Batch 1 reference in the real UI

## Approved asset lock

A `LIVE_VERIFIED` asset is locked. Replacement requires one of:

- `technical_error`
- `visual_error`
- `user_requested_change`

Never silently regenerate or replace an approved asset.

## Failure handling

- Image problem -> remove/disable the bad mapping first, then fix only the image asset.
- Mapping problem -> rollback only the mapping.
- Code problem -> rollback the code commit.
- Preview/Vercel problem -> do not promote.
- Source ambiguity -> stop at source/design brief stage.
- Technical uncertainty -> return to the handbook.
- Visual quality below Batch 1 -> fail closed; do not map it.

Do not solve a local failure by weakening the visual standard.

## Batch completion definition

A batch is complete only when every visual in the batch is technically approved, teaching approved, visually approved by actual inspection, preview verified, correctly mapped, production deployed and live verified.

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
