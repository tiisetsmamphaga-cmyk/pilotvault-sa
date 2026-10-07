# PilotVault SA

- UI work follows the PilotVault UI standard in
  `docs/PILOTVAULT_UI_STANDARD.md` (reference: the mock exam set-up pop-up).
  Keep screens minimal: no decorative icons, short labels, one primary action.
  Don't restyle the exam simulator or results screen unless asked.
- Explanation pictures follow `docs/EXPLANATION_ILLUSTRATION_STANDARD.md`
  (reference: the anabatic/katabatic wind picture). Design for a phone first
  (900 px canvas, stacked panels, labels ≥ 32 px), build from the shared parts
  in `scripts/trial_visuals/scene.py`, measure real objects from a reference
  instead of drawing freehand, and pass `scripts/trial_visuals/check.py`
  before showing anyone.
- Duplicate questions: hide only direct duplicates (the same question
  reworded, with the same answer). Keep questions that ask the same fact a
  different way, e.g. giving the description and asking for the name.
- Deployment rules are in `docs/DEPLOYMENT_POLICY.md`.
- Use pnpm.
