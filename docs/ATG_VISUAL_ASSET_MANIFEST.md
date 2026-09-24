# ATG Manual-Derived Visual Asset Manifest

Branch: `atg-explanation-visual-rebuild`

Visual standard: source-derived aircraft technical/manual figures only. Preserve source geometry and terminology; PilotVault branding is limited to the presentation frame/header. No generic machinery or unrelated infographic substitutions.

## Piston Engines

- ~~`reciprocating-engine-basic-parts-v1.webp`~~ — removed 2026-09-24: the file was never a valid image
- ~~`four-stroke-cycle-v1.webp`~~ — removed 2026-09-24: the file was never a valid image
- `float-type-carburettor-v2.svg` — handbook-grounded, QA reviewed
- `carburettor-icing-v1.svg` — handbook-grounded, QA reviewed
- `normal-combustion-vs-detonation-v1.svg` — handbook-grounded, QA reviewed

## Pressure / Gyroscopic Instruments / Magnetic Compass

- ~~`pitot-static-system-v1.svg`~~ — removed 2026-09-24: crude drawing
- `sensitive-altimeter-v1.svg` — handbook-grounded, QA reviewed
- `vertical-speed-indicator-v1.svg` — handbook-grounded, QA reviewed
- `airspeed-indicator-markings-v1.svg` — handbook-grounded, QA reviewed
- `vacuum-gyro-system-v1.svg` — handbook-grounded, QA reviewed
- ~~`turn-coordinator-v1.svg`~~ — removed 2026-09-24: crude drawing
- `turn-slip-skid-v1.svg` — handbook-grounded, QA reviewed
- `heading-indicator-v1.svg` — handbook-grounded, QA reviewed
- ~~`attitude-indicator-v1.svg`~~ — removed 2026-09-24: crude drawing
- `attitude-indicator-interpretation-v1.svg` — handbook-grounded, QA reviewed
- ~~`magnetic-compass-v1.svg`~~ — removed 2026-09-24: crude drawing
- ~~`earth-magnetic-field-v1.svg`~~ — removed 2026-09-24: crude drawing

## Integration rule

Map these visuals to Supabase only after the full 17-asset library is committed, the static asset URLs return successfully, and the ATG practice page is verified in preview before production release.

The 24 Sept 2026 review of every ATG image in use is recorded in `data/atg-explanations/image-review-2026-09-24.md`. Its row backup (`removed-images-2026-09-24.json`) restores the removed mappings if needed.
