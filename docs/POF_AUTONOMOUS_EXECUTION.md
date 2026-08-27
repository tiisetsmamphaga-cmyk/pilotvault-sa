# PilotVault POF Autonomous Execution Protocol

## Purpose

This protocol is the standing operating authority for completing Principles of Flight visual work without routine interruptions.

The goal is continuous execution across batches while preserving the PilotVault POF quality gates, fail-closed behavior, deployment policy, and exact resume checkpoints.

## Standing authorization

The active instruction is:

> Continue working on POF autonomously until the entire suitable visual system is complete. Never stop at a batch boundary. Never ask for routine approval. Persist progress after every meaningful stage. If interrupted, verify state and resume from the last confirmed checkpoint.

This standing authorization remains active until explicitly revoked or replaced.

## Batch rules

- Maximum five visual concepts per batch.
- A completed batch immediately rolls into the next batch; a batch boundary is not a stop point.
- The five locked Batch 1 visuals remain the minimum quality benchmark.
- No generic, approximate, placeholder, bulk-converted, or loosely related visual may be used to keep progress moving.
- If a correct teaching visual is not ready, fail closed and show no image.

## User reporting cadence

Normal progress messages are suppressed.

Send the user a progress report only after every three completed batches.

The reporting windows are therefore:

- Batches 2-4 -> report
- Batches 5-7 -> report
- Batches 8-10 -> report
- continue in groups of three thereafter

A report is also allowed before the three-batch boundary only when a stop condition below is reached and user input is genuinely required.

Do not send routine messages such as:

- asking whether to continue
- announcing the start of the next batch
- reporting ordinary GitHub commits
- reporting ordinary QA passes
- reporting routine Supabase mappings
- reporting ordinary preview creation

Record those events in the persistent state instead.

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
