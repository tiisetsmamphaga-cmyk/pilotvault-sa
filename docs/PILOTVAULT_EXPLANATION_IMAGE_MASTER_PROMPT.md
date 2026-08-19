# PilotVault Explanation Image Master Prompt

Use this as the standing standard whenever explanation images are created or edited for PilotVault SA.

## Objective
Create high-quality aviation training diagrams that look intentionally designed, technically correct, and suitable for a paid SACAA exam-prep platform. Quality is more important than speed.

## 1. No generic diagram generator
Do not create one generic React/SVG renderer that auto-positions labels, arrows and shapes for dozens of concepts. Do not mass-produce procedural layouts. Create finished, individually designed static diagrams for each important visual concept.

## 2. Question-specific images
Read the actual question, correct answer and explanation first. Decide what visual specifically helps that question. Closely related questions may share an image only when the exact same visual genuinely explains both. Do not assign one generic image to an entire topic. If a question does not benefit from an image, do not force one.

## 3. Visual style
Every explanation image must look like a professional aviation textbook / ground-school manual diagram upgraded with PilotVault branding.

Avoid AI-looking aircraft, decorative infographic icons, unnecessary gradients, cartoon graphics, fake 3D objects, generic SaaS infographic layouts, oversized rounded cards and visual clutter.

Prefer clean technical line drawings, conventional aviation diagram conventions, straight arrows, clearly labelled forces/angles/components, simple aircraft or aerofoil silhouettes where required, white diagram backgrounds, navy/gold/grey accents and clear hierarchy.

## 4. PilotVault banner
At the top of every explanation image use a dark navy banner with small centred gold uppercase text `PILOTVAULT [SUBJECT]`, followed by a large bold centred white uppercase diagram title. Keep this consistent with the approved Meteorology banner style.

## 5. No collisions
No line may pass through text. No arrow may overlap a label. No label may touch an image boundary. No text may be clipped or overflow. Angle labels must not cover the angle. No unexplained empty arrows. Use generous whitespace and callout lines where necessary.

## 6. Real aviation diagram logic
Use conventional textbook layouts as structural inspiration and create original PilotVault versions. A student should understand the principle within seconds.

## 7. Technical accuracy first
Verify force directions, airflow directions, control movements, angles, terminology and aerodynamic relationships. Do not guess.

## 8. Audit before implementation
Audit all questions in the subject and group them by actual visual concept, not just database topic. Example: angle-of-attack definition, relative airflow and critical AoA must not automatically share one image.

## 9. Visual QA is mandatory
A successful build, valid SVG, 200 response or Vercel deployment is not visual QA. Before calling an image finished: render it, inspect it at practice-page size, check desktop/mobile scaling, clipping, collisions, arrows, geometry, technical correctness and whether it looks AI-generated. Fix anything questionable before deployment.

## 10. Quality over quantity
Prefer 20 excellent diagrams to 60 mediocre ones.

## 11. Stable assets
Use stable local PilotVault assets wherever practical with clear versioned filenames. When replacing cached assets, use a new version (`-v2`, `-v3`, etc.).

## 12. Implementation
After diagrams pass visual QA, map them to the correct questions, preserve existing question-reference figures, support Practice and Results/Review, push to `main`, deploy to production and verify production.

## 13. Definition of done
Do not say `done`, `perfect`, `fixed` or `complete` until the visual has actually been rendered and inspected, has no clipping/overlap, is technically accurate and question-relevant, uses the approved banner, does not look AI-generated, and displays correctly in production.

## Current Principles of Flight instruction
Do not patch the old broken POF visual generator. Audit the POF question bank and replace weak explanation graphics with individually designed static aviation-training diagrams. Use conventional ground-school/textbook clarity (including the supplied Angle of Attack reference) as the standard. Visually QA every diagram before deployment.