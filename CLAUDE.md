# PilotVault SA

- UI work follows the PilotVault UI standard in
  `docs/PILOTVAULT_UI_STANDARD.md` (reference: the mock exam set-up pop-up).
  Keep screens minimal: no decorative icons, short labels, one primary action.
  Don't restyle the exam simulator or results screen unless asked.
- Explanation pictures follow `docs/EXPLANATION_ILLUSTRATION_STANDARD.md`
  (reference: the anabatic/katabatic wind picture). Design for a phone first
  (900 px canvas, stacked panels, labels ≥ 32 px), build from the shared parts
  in `scripts/trial_visuals/scene.py`, measure real objects instead of drawing
  freehand (extract them from existing PilotVault pictures first, as the
  aircraft was from the QFE diagram), and pass `scripts/trial_visuals/check.py`
  before showing anyone. Bad existing drawings (failing `check.py`, wrong, or
  unreadable on a phone) are redrawn to the standard when their subject is
  worked on; textbook figures and branded images stay.
- Duplicate questions: hide only word-for-word duplicates. Questions that ask
  the same fact in different words stay in the bank.
- Deployment rules are in `docs/DEPLOYMENT_POLICY.md`.
- Use pnpm.
