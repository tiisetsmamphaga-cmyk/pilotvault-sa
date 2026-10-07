# PilotVault SA

- UI work follows the PilotVault UI standard in
  `docs/PILOTVAULT_UI_STANDARD.md` (reference: the mock exam set-up pop-up).
  Keep screens minimal: no decorative icons, short labels, one primary action.
  Don't restyle the exam simulator or results screen unless asked.
- Explanation pictures follow `docs/EXPLANATION_ILLUSTRATION_STANDARD.md`
  (reference: the anabatic/katabatic wind picture). Real objects (aircraft,
  instruments) are measured from a reference and reused as components in
  `scripts/trial_visuals/` (e.g. `aircraft.py`), never drawn freehand.
- Deployment rules are in `docs/DEPLOYMENT_POLICY.md`.
- Use pnpm.
