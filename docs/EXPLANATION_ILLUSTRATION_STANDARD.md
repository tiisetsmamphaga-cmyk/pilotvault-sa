# PilotVault explanation illustration standard

The reference is the anabatic/katabatic wind picture
(`public/explanation-images/meteorology/refined-batch-2/anabatic-katabatic-v2.webp`,
drawn by `scripts/trial_visuals/met_illustrated.py`). New explanation pictures
should look like it.

## What makes it work

- **A scene, not a chart.** Draw the real situation (a slope, a sky, an
  airfield) with shaded sky, ground and objects, not boxes and arrows on white.
- **Side-by-side contrast when the fact is a comparison** (day/night,
  high/low, cool/hot). Two equal panels with rounded corners and a thin grey
  border.
- **The physics is drawn as flow.** Three smooth parallel streamlines with
  arrowheads, fading from the strongest (nearest the surface) outwards.
- **Few labels, on the picture.** One bold headline label per panel (about 26 px)
  with a soft halo so it reads over the scene, plus one or two short secondary
  labels. No leader lines, call-out boxes, pills or tables.
- **A caption under each panel** in the panel's colour, naming the answer
  (e.g. "DAY — ANABATIC (upslope)").
- **Colour carries meaning.** Red for warm/rising/high, blue for cold/sinking/low.
- **Details that set the scene stay quiet:** sun or moon, a few trees, stars.
  Nothing decorative that competes with the flow arrows or labels.

The KEY FACT card under the picture carries the title, the full answer and the
numbers, so the picture only needs to show the idea.

## Drawing real objects: measure, don't freehand

Aircraft, instruments, clouds and other real objects are never drawn from
memory. Freehand shapes come out wrong (the first barometer and plane drafts).

1. **Find a reference picture** of the object: an existing PilotVault diagram,
   a manual figure, or a photo with the right view.
2. **Measure it on a grid.**
   `python3 scripts/trial_visuals/measure.py <image> x0 y0 x1 y1 out.png [zoom] [step]`
   gives a zoomed crop with labelled grid lines; read the outline points and
   key positions (windows, wheels, hinge lines) off it.
3. **Redraw it once as a clean component**: smooth curves, gradients, a
   consistent outline, **no registrations, logos or school names**. Put it in
   its own module in `scripts/trial_visuals/` with a function that takes
   position, size, angle and facing (see `aircraft.py`: `aircraft()` /
   `aircraft_defs()`).
4. **Reuse the component** in every picture that needs that object, so the set
   stays consistent. Add a variant (iced, gear up, top view) to the component
   instead of drawing a one-off.

Components so far: `aircraft.py` (low-wing trainer, side view; options for
pitch, facing, rime ice, propeller).

## Checking before sending

- Render and look at every picture at full size before showing anyone.
- Check for labels overlapping arrows, objects or each other; text cut off;
  arrows that don't follow the surface; objects floating above the ground.
- Check the facts in the picture and the KEY FACT card against each other.
