# PilotVault explanation illustration standard

The reference is the anabatic/katabatic wind picture
(`public/explanation-images/meteorology/refined-batch-2/anabatic-katabatic-v3.webp`,
drawn by `scripts/trial_visuals/met_phone.py` from the parts in
`scripts/trial_visuals/scene.py`). New explanation pictures should look like it.

**Scope:** every new diagram follows this standard, and bad existing drawings
are fixed: when a subject is worked on, each drawn picture in it that fails
`check.py`, is wrong, or is hard to read on a phone is redrawn to this standard
(the earlier Air Law, Flight Planning and Radio Telephony drawings currently
all fail `check.py`). Textbook figures and branded images are not redrawn.

## 1. Phone first

Most students study on a phone, where a picture is about **330 px wide**. Design
for that size first; desktop is the easy case.

- **Canvas 900 px wide.** One scene is about 900 × 500–620. A comparison is two
  panels **stacked top and bottom** (never side by side), each 900 × about 470,
  with its caption underneath: about 900 × 1080 in all.
- **Text sizes** (on the 900 canvas → on a phone):
  main label 42 px (15 px), secondary label 34 px (12 px), caption 38 px
  (14 px). **Nothing below 32 px** (about 12 px on a phone). `scene.label()`
  refuses anything smaller.
- **At most two labels per panel**: one main label, one short secondary label.
  Break long labels over two lines rather than shrinking them.
- **Thick lines:** main airflow streamlines 9 px, arrowheads to match
  (`scene.flow_band`).
- Students can tap any picture to open it full screen, but the picture must
  already read without zooming.

## 2. What the picture looks like

- **A scene, not a chart.** Draw the real situation (a slope, a sky, an
  airfield) with shaded sky, ground and objects, not boxes and arrows on white.
- **Comparisons as two stacked panels** (day/night, high/low, cool/hot), rounded
  corners, thin grey border (`scene.stack`).
- **The physics is drawn as flow.** Three smooth parallel streamlines with
  arrowheads, strongest nearest the surface, fading outwards.
- **Labels sit on the picture** with a soft halo. No leader lines, call-out
  boxes, pills or tables.
- **A caption under each panel** in the panel's colour, naming the answer
  (e.g. "DAY — ANABATIC (upslope)").
- **Colour carries meaning.** Red for warm/rising/high, blue for
  cold/sinking/low.
- **Scene details stay quiet:** sun or moon, a few trees, stars. Nothing that
  competes with the flow arrows or labels.

The KEY FACT card under the picture carries the title, the full answer and the
numbers, so the picture only needs to show the idea.

## 3. Shared parts — always build from these

`scripts/trial_visuals/scene.py` holds every reusable part so all subjects
match: canvas and text sizes, panel stacks with captions, sky and ground
gradients, terrain, sun, moon, stars, trees, streamlines, labels, molecule
grids, **clouds** (cumulus, cumulonimbus, rain, lightning, fog) and the
**aircraft** (`aircraft.py`). Add a new part there rather than drawing a
one-off inside a picture.

## 4. Real objects: measure, don't freehand

Aircraft, instruments, clouds and other real objects are never drawn from
memory. Freehand shapes come out wrong (the first barometer, plane and cloud
drafts).

1. **Extract it from an existing PilotVault picture first**, the way the
   aircraft was taken from the QFE/QNE diagrams and the clouds from the cloud
   types chart: search `public/explanation-images/` and the question images
   for the object in the right view. Only when no existing picture has it,
   use a manual figure or a photo.
2. **Measure it on a grid.**
   `python3 scripts/trial_visuals/measure.py <image> x0 y0 x1 y1 out.png [zoom] [step]`
   gives a zoomed crop with labelled grid lines; read the outline, proportions
   and key positions off it.
3. **Redraw it once as a clean part** in `scene.py` (or its own module):
   smooth curves, gradients, a consistent outline, **no registrations, logos or
   school names**, with options for position, size, angle and facing. Write
   the measured proportions in its docstring.
4. **Reuse the part** everywhere, and add variants (iced, gear up, top view)
   to it instead of drawing one-offs.

Parts measured so far:
- `aircraft.py` — low-wing trainer, side view (from the QFE/QNE diagrams).
- `scene.cumulus`, `scene.cumulonimbus` — from `cloud-types-chart-v1.png`:
  cumulus height ≈ 0.42 × width with the tallest dome just left of centre;
  cumulonimbus height ≈ 2.4 × base width, bulging to ≈ 1.3 × the base width
  mid-tower and narrowing to ≈ 0.76 × at the top, anvil ≈ 1.4 × the base width
  and ≈ 8% of the height, flat dark base.

## 5. Checks before anyone sees a picture

Run the automatic check, then look at the phone preview yourself:

```
python3 scripts/trial_visuals/check.py <module> [--only id,id] [--out dir]
```

It fails the picture if any text is under 11 px on a phone, labels overlap,
an airflow arrow crosses a label, or a label runs outside its panel, and it
writes a phone-size preview of each picture. Then check by eye: objects
floating above the ground, arrows that don't follow the surface, and that the
facts in the picture match the KEY FACT card.
