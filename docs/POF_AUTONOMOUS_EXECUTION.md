# PilotVault POF Autonomous Execution Protocol

## Purpose

This protocol is the standing operating authority for completing Principles of Flight visual work without routine interruptions.

The goal is continuous execution across batches while preserving the PilotVault POF quality gates, fail-closed behavior, deployment policy, exact resume checkpoints, and truthful execution status in the chat.

## Standing authorization

The active instruction is:

> Continue working on POF autonomously until the entire suitable visual system is complete. Never stop at a batch boundary. Never ask for routine approval. Persist progress after every meaningful stage. If interrupted, verify state and resume from the last confirmed checkpoint.

This standing authorization remains active until explicitly revoked or replaced.

## Active-turn execution rule

Autonomous execution only exists while the current ChatGPT turn is actively running.

- Progress updates are intermediate status messages inside the active turn and do not pause work.
- After posting a progress update, continue directly with the next tool/action unless a genuine stop condition is reached.
- Do not send a final response merely to say that work is continuing.
- A final response means the active execution run has ended, paused at a verified checkpoint, completed a requested scope, or hit a genuine blocker.
- Never claim to be working in the background after a final response has been sent.
- If the chat UI is idle after a final response, execution has stopped until a new user turn starts another active run.
- If an execution limit forces the turn to end before the work is complete, persist the exact checkpoint and state clearly that the run has stopped; never imply invisible continuation.

The preferred long-run pattern is:

`tool/action -> short progress update -> tool/action -> short progress update -> ... -> verified checkpoint/blocker/completion -> final response`

## Batch rules

- Maximum five visual concepts per batch.
- A completed batch immediately rolls into the next batch; a batch boundary is not a stop point while the active turn is still running.
- The five locked Batch 1 visuals remain the minimum quality benchmark.
- No generic, approximate, placeholder, bulk-converted, or loosely related visual may be used to keep progress moving.
- If a correct teaching visual is not ready, fail closed and show no image.

## User progress visibility

Short progress updates are enabled during active execution.

Post a concise update at meaningful checkpoints such as:

- source/question set selected
- a visual is refined or rejected
- technical/teaching/visual QA passes or fails
- preview is ready
- mappings are applied
- production is deployed
- live verification is complete

These updates are informational only. They must not pause execution or wait for user acknowledgement.

A more complete summary may still be given after every three completed batches, but that summary is not a stop point and does not replace the live checkpoint updates.

Do not ask whether to continue unless a genuine stop condition requires a user decision.

## Allowed autonomous actions

Within the established POF workflow, autonomous execution may:

- audit questions and explanations
- inspect the approved handbook source
- select the next questions that materially benefit from visuals
- prepare design briefs
- create/refine raster assets
- run technical, teaching, visual, repository, and mapping QA
- create and update working branches
- make batched Git commits
- create a deliberate `preview/*` branch only when the batch is QA-approved
- verify previews
- open and merge approved PRs
- update Supabase mappings and statuses with fail-closed preflight checks
- verify production state
- lock LIVE_VERIFIED assets

All actions remain subject to the POF visual workflow and deployment policy.

## Stop conditions

Stop and ask for user input only for:

1. `source_ambiguity` - the approved source cannot establish the technical relationship with sufficient confidence.
2. `irreversible_product_risk` - a decision materially changes the product, pricing, business model, data ownership, destructive production behavior, or another irreversible area outside the already-approved workflow.
3. `unrecoverable_external_blocker` - a required external system remains unavailable and no useful independent work can continue.

Routine implementation choices are not stop conditions.

## External-service failure behavior

One unavailable service must not stop unrelated work.

Examples:

- Vercel unavailable -> continue source work, design briefs, asset creation, local/repository QA, and GitHub work that does not require deployment.
- Supabase unavailable -> continue image/source/QA work and preserve intended mappings in state.
- GitHub temporarily unavailable -> continue non-GitHub analysis and preserve the exact pending action in state.

Never create duplicate writes or speculative retries.

## Verify-before-retry rule

After any timeout, connection error, or uncertain tool result:

1. Verify whether the previous action actually completed.
2. Compare remote state against the last verified checkpoint.
3. Resume from the last confirmed successful stage.
4. Retry only the missing operation.
5. Never mark a stage complete from an unverified tool response.

## Persistent checkpoint rule

`data/pof-autonomous-state.json` is the execution checkpoint.

Update it after every meaningful stage, including:

- batch selected
- questions selected
- source confirmed
- design brief complete
- assets created
- QA result
- preview state
- mapping state
- production state
- LIVE_VERIFIED lock

The state must always include a precise `next_action`.

If a future session resumes POF work, read this state before doing new work and continue from `last_verified_checkpoint` / `next_action` rather than restarting the audit.

## Deployment discipline

Follow `docs/DEPLOYMENT_POLICY.md`.

POF development commits happen on non-preview working branches and must not consume Vercel builds.

Only create a `preview/*` branch when the exact batch state is QA-approved and ready for one deliberate preview build.

Then merge/squash the approved state into `main` for one production build.

Do not create metadata-only deployment churn.

## Completion rule

POF is complete only when every question that materially benefits from a visual has either:

- a question-specific, source-grounded, Batch-1-quality visual that reached LIVE_VERIFIED and lock, or
- an explicit audited decision that no visual is required.

Coverage percentage alone is never a completion criterion.
