"""Human Performance explanation pictures, phone-first (docs/EXPLANATION_ILLUSTRATION_STANDARD.md).

Built on the JAA Human Performance manual's own figures (prepared by hp_figures.py): the picture keeps the
textbook illustration and adds phone-size labels and a caption per panel, replacing the manual's small legend.
"""
from pathlib import Path

from common import Registry
from kit import embed, template
from scene import COMMON_DEFS, NAVY_BLUE, RED, TXT_M, W, defs, label, stack, stack_height

R = Registry("human-performance", "/explanation-images/human-performance/refined-batch-11")

FIG = Path(__file__).resolve().parent / "fig" / "hp"
SRC_W = 771          # the manual figures' original width: label positions below are in those pixels
BLUE = "#1d6fd6"


def picture(panels):
    body, _ = stack(panels)
    return defs(*COMMON_DEFS) + body


def figure_panel(name, src_h, caption, color, labels=()):
    """One manual figure filling the panel width; labels given in original figure pixels."""
    k = W / SRC_W
    h = round(src_h * k)

    def draw(w, hh):
        s, *_ = embed(FIG / name, 0, 0, w, hh)
        for x, y, text, col, anchor, halo in labels:
            s += label(x * k, y * k, text, TXT_M, col, anchor, halo=halo)
        return s
    return dict(h=h, sky="sky_day", draw=draw, caption=caption, color=color)


@R.add(2108, "runway-slope-illusion-v2", "Runway Slope Illusion",
       template("AN UPSLOPING RUNWAY MAKES YOU FEEL TOO HIGH", "SO THE APPROACH IS FLOWN LOW"),
       h=stack_height([round(383 * W / SRC_W), round(386 * W / SRC_W)]), w=W)
def _():
    up = figure_panel("upslope-8-28a.png", 383, "UPSLOPE: FEELS HIGH, FLOWN LOW", RED,
                      [(165, 92, "What you think", RED, "start", "#ffffff"),
                       (20, 262, "Where you are", BLUE, "start", "#ffffff")])
    down = figure_panel("downslope-8-29a.png", 386, "DOWNSLOPE: FEELS LOW, FLOWN HIGH", NAVY_BLUE,
                        [(165, 110, "Where you are", BLUE, "start", "#ffffff"),
                         (20, 268, "What you think", RED, "start", "#ffffff")])
    return picture([up, down])


@R.add(2795, "black-hole-approach-v2", "Black Hole Approach",
       template("ONLY THE RUNWAY LIGHTS: YOU FEEL TOO HIGH", "SO THE APPROACH IS FLOWN LOW AND SHORT"),
       h=stack_height([round(384 * W / SRC_W)]), w=W)
def _():
    return picture([figure_panel("black-hole-8-30.png", 384, "BLACK HOLE: FEELS HIGH, FLOWN LOW", RED,
                                 [(385, 40, "No lights around the runway", "#e2e8f0", "middle", "#0b1020")])])


@R.add(2214, "false-horizon-v1", "False Horizon",
       template("A SLOPING CLOUD TOP IS NOT THE HORIZON", "LEVELLING ON IT LEAVES THE WINGS BANKED"),
       h=stack_height([W]), w=W)
def _():
    p = figure_panel("false-horizon-8-25.png", SRC_W, "SLOPING CLOUD: A FALSE HORIZON", RED)
    p["h"] = W
    return picture([p])
