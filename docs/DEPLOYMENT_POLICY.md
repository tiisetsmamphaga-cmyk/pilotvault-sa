# PilotVault Deployment Policy

## Goal

Protect PilotVault from unnecessary Vercel builds and deployment-rate limits while keeping GitHub development checkpoints flexible.

## Vercel branch policy

`vercel.json` is the source of truth for automatic Git deployments.

- Working branches do **not** auto-deploy to Vercel.
- `main` may auto-deploy to production.
- `preview/*` branches may auto-deploy for deliberate QA previews.
- Unspecified or experimental branches must remain deployment-disabled by the wildcard rule.

## Required workflow

1. Do development work on a normal working branch such as `pof-*`, `fix/*`, `chore/*`, or another non-preview branch.
2. Commit freely while developing; those commits must not consume Vercel builds.
3. Automation must batch related file additions, replacements, or deletions into a single logical commit whenever practical. Never create one commit per generated/deleted asset.
4. Do not create a Vercel preview for intermediate states.
5. When a batch has passed source, technical, teaching, visual, and repository QA, point or create a `preview/*` branch at the exact QA-approved commit.
6. Allow exactly one intentional Vercel preview build for that finished state.
7. Verify the actual preview UI.
8. Merge or squash the approved work into `main`.
9. Allow the resulting `main` commit to create the production deployment.
10. Do not make metadata-only follow-up commits merely to trigger additional Vercel builds. State changes should be batched with the production-ready commit where the workflow allows it.

## POF visual batches

For Principles of Flight visual work, the deployment sequence is:

`WORKING BRANCH (no Vercel) -> QA -> preview/pof-* (one Vercel preview) -> live preview verification -> main (one production deployment) -> live verification -> lock`

A POF batch remains limited to five visual concepts. Vercel deployment frequency must never be used as a substitute for local/GitHub QA.

## Failure rule

If Vercel reports a deployment-rate limit, do not create extra commits or duplicate deployments trying to bypass it. Verify the last successful deployment, preserve the exact Git checkpoint, and resume from that checkpoint when deployment capacity is available.
