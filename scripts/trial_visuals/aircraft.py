"""A generic low-wing trainer for explanation illustrations: side view and top (plan) view.

Side view: outline measured from the aircraft in the existing QFE/QNE diagrams, redrawn as clean curves without
registration or school markings. Local drawing space: nose on the left, about 660 x 250 units.
Top view: measured from the plan view in principles-of-flight/refined-batch-19/pof-rudder-effect-v2.webp
(span 1300 px, length 1070 px, wing root chord 250 / tip chord 175, tailplane span 485, cabin 160 wide).
Local space centred on the wing, nose towards -x.
Call aircraft_defs() once per SVG, then aircraft(...) or aircraft_top(...) for each aircraft.
"""

BODY = ("M 98,125 L 205,122 L 266,85 C 280,81 300,80 320,82 L 440,97 L 580,113 L 671,9 C 674,4 679,4 682,8 "
        "L 712,18 L 690,128 L 692,140 C 693,150 690,156 684,158 L 600,174 C 520,186 440,193 380,195 L 250,197 "
        "C 180,196 140,194 122,190 C 108,185 98,175 95,163 L 95,130 C 95,127 96,125 98,125 Z")
FIN = "M 580,113 L 671,9 C 674,4 679,4 682,8 L 712,18 L 690,128 Z"
WINDOWS = [
    "M 208,123 L 264,87 C 266,86 268,87 267,89 L 242,131 Z",
    "M 270,100 L 320,99 C 325,99 327,102 327,106 L 327,127 C 327,131 324,133 320,133 L 268,133 "
    "C 263,133 261,129 263,125 L 266,107 C 267,103 268,100 270,100 Z",
    "M 344,102 L 384,104 C 388,104 390,107 390,111 L 390,128 C 390,132 387,134 383,134 L 345,133 "
    "C 341,133 339,130 339,126 L 339,107 C 339,104 341,102 344,102 Z",
    "M 407,111 L 426,112 C 430,112 432,115 432,118 L 432,127 C 432,130 430,132 427,132 L 407,131 "
    "C 404,131 402,129 402,126 L 402,116 C 402,113 404,111 407,111 Z",
]
WING = ("M 262,152 C 266,140 285,136 305,136 L 400,152 L 400,184 C 360,190 300,192 268,188 "
        "C 258,180 257,162 262,152 Z")


def aircraft_defs():
    return ('<linearGradient id="ac_body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/>'
            '<stop offset="1" stop-color="#d9e0e8"/></linearGradient>'
            '<linearGradient id="ac_blue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f86e0"/>'
            '<stop offset="1" stop-color="#1257a8"/></linearGradient>'
            '<linearGradient id="ac_glass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2edf7"/>'
            '<stop offset="0.55" stop-color="#9fb8cf"/><stop offset="1" stop-color="#6f8aa6"/></linearGradient>'
            '<linearGradient id="ac_wing" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fc4f5"/>'
            '<stop offset="1" stop-color="#3a8ad8"/></linearGradient>'
            '<linearGradient id="ac_spinner" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1f5f9"/>'
            '<stop offset="1" stop-color="#94a3b8"/></linearGradient>'
            '<linearGradient id="act_wing" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8fc4f5"/>'
            '<stop offset="1" stop-color="#2f78c4"/></linearGradient>'
            '<linearGradient id="act_body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cbd5e1"/>'
            '<stop offset="0.5" stop-color="#ffffff"/><stop offset="1" stop-color="#cbd5e1"/></linearGradient>'
            f'<clipPath id="ac_clip" clipPathUnits="userSpaceOnUse"><path d="{BODY}"/></clipPath>'
            f'<clipPath id="ac_fin" clipPathUnits="userSpaceOnUse"><path d="{FIN}"/></clipPath>')


def _rime():
    """White rime teeth on the leading edges (spinner, wing, fin), pointing forward (left in local space)."""
    s = ""
    for k in range(6):
        y = 136 + k * 5
        s += f'<path d="M {60 + abs(k - 2.5) * 6:.1f},{y} l -9,2.5 l 9,2.5 z" fill="#ffffff" stroke="#60a5fa" stroke-width="1.2"/>'
    for k in range(6):
        y = 152 + k * 6
        s += f'<path d="M {260 - (2 if 0 < k < 5 else 0)},{y} l -10,3 l 10,3 z" fill="#ffffff" stroke="#60a5fa" stroke-width="1.2"/>'
    for k in range(8):
        f = k / 8
        x, y = 580 + 91 * f, 113 - 104 * f
        s += f'<path d="M {x:.1f},{y:.1f} l -9,-4 l 4,9 z" fill="#ffffff" stroke="#60a5fa" stroke-width="1.2"/>'
    return s


def aircraft(x, y, width=160, pitch=0, nose_right=True, rime=False, prop=True):
    """Aircraft centred on (x, y), `width` canvas units long, nose-up `pitch` degrees."""
    k = width / 660
    sx = -k if nose_right else k
    rot = -pitch if nose_right else pitch
    stroke = 'stroke="#334155" stroke-width="2.4" stroke-linejoin="round"'
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sx:.4f},{k:.4f}) translate(-385,-130)">'
    # landing gear behind the body
    s += f'<path d="M 128,190 L 131,226" stroke="#64748b" stroke-width="6" fill="none"/>'
    s += '<circle cx="133" cy="230" r="14" fill="#111827"/><circle cx="133" cy="230" r="5.5" fill="#e5e7eb"/>'
    s += f'<path d="M 318,188 L 336,188 L 331,218 L 326,218 Z" fill="url(#ac_blue)" {stroke}/>'
    s += '<circle cx="332" cy="228" r="18" fill="#111827"/><circle cx="332" cy="228" r="7" fill="#e5e7eb"/>'
    # fuselage: white top, stripes, blue lower half, blue fin tip
    s += f'<path d="{BODY}" fill="url(#ac_body)"/>'
    s += ('<g clip-path="url(#ac_clip)"><rect x="0" y="155" width="760" height="100" fill="url(#ac_blue)"/>'
          '<rect x="0" y="145" width="760" height="4" fill="#e3b505"/><rect x="0" y="150" width="760" height="3" fill="#0f2f5c"/></g>')
    s += '<g clip-path="url(#ac_fin)"><rect x="560" y="0" width="200" height="44" fill="url(#ac_blue)"/></g>'
    s += f'<path d="{BODY}" fill="none" {stroke}/>'
    s += f'<path d="M 676,58 L 662,124" fill="none" stroke="#64748b" stroke-width="2"/>'  # rudder hinge
    s += f'<path d="M 200,123 L 198,150 M 332,99 L 332,190" fill="none" stroke="#94a3b8" stroke-width="1.6"/>'  # cowl, door
    s += f'<rect x="636" y="133" width="80" height="8" rx="4" fill="url(#ac_body)" {stroke}/>'  # tailplane
    for w in WINDOWS:
        s += f'<path d="{w}" fill="url(#ac_glass)" stroke="#111827" stroke-width="3" stroke-linejoin="round"/>'
    s += f'<path d="{WING}" fill="url(#ac_wing)" {stroke}/>'
    s += '<path d="M 262,152 C 300,163 360,162 400,152" fill="none" stroke="#1e4f8f" stroke-width="2"/>'
    s += f'<path d="M 93,131 C 76,133 63,140 58,148 C 63,156 76,162 93,164 Z" fill="url(#ac_spinner)" {stroke}/>'
    if prop:
        s += '<ellipse cx="93" cy="147" rx="5" ry="58" fill="#64748b" fill-opacity="0.28"/>'
    if rime:
        s += _rime()
    return s + "</g>\n"


# Top view, measured in source pixels and shifted so the wing centre (600, 680) is the origin; nose towards -x.
TOP_HALF_WIDTH = [(-440, 0), (-432, 30), (-410, 57), (-265, 64), (-150, 76), (0, 80), (120, 76), (250, 60),
                  (390, 40), (550, 22), (605, 10)]
TOP_WING = [(-190, 78), (-130, 115), (-75, 648), (100, 640), (122, 90)]
TOP_TAILPLANE = [(385, 25), (495, 240), (595, 240), (600, 20)]


def _smooth(pts):
    """Catmull-Rom spline through pts as SVG cubic segments (no move-to)."""
    d = ""
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


def _mirror(pts):
    return [(x, -y) for x, y in pts]


def aircraft_top(x, y, span=160, heading=0, prop=True):
    """Aircraft seen from above, centred on (x, y), wingspan `span` canvas units, nose pointing to `heading`
    (degrees, 0 = up/north, clockwise)."""
    k = span / 1300
    stroke = f'stroke="#334155" stroke-width="{max(2.2 / k / 6, 6):.1f}" stroke-linejoin="round"'
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({90 + heading}) scale({k:.4f})">'
    w = _mirror(TOP_WING) + list(reversed(TOP_WING))
    s += '<path d="M ' + " L ".join(f"{a},{b}" for a, b in w) + f' Z" fill="url(#act_wing)" {stroke}/>'
    s += f'<path d="M 57,-630 L 70,-330 L 114,-330 M 57,630 L 70,330 L 114,330" fill="none" stroke="#1e4f8f" stroke-width="5"/>'
    t = _mirror(TOP_TAILPLANE) + list(reversed(TOP_TAILPLANE))
    s += '<path d="M ' + " L ".join(f"{a},{b}" for a, b in t) + f' Z" fill="url(#act_wing)" {stroke}/>'
    s += '<path d="M 553,-236 L 556,-24 M 553,236 L 556,24" fill="none" stroke="#1e4f8f" stroke-width="5"/>'
    upper = [(a, -b) for a, b in TOP_HALF_WIDTH]
    lower = list(reversed(TOP_HALF_WIDTH))
    body = f"M {upper[0][0]},{upper[0][1]}" + _smooth(upper) + f" L {lower[0][0]},{lower[0][1]}" + _smooth(lower) + " Z"
    s += f'<path d="{body}" fill="url(#act_body)" {stroke}/>'
    s += '<path d="M 230,0 Q 420,-14 610,0 Q 420,14 230,0 Z" fill="#e2e8f0" stroke="#334155" stroke-width="5"/>'  # fin
    s += ('<path d="M -255,-30 C -250,-60 -210,-58 -160,-58 L -60,-56 C -50,-56 -45,-50 -45,-40 L -45,40 C -45,50 -50,56 -60,56 '
          'L -160,58 C -210,58 -250,60 -255,30 Z" fill="url(#ac_glass)" stroke="#111827" stroke-width="7"/>')  # canopy
    s += '<path d="M -150,-57 L -150,57" stroke="#111827" stroke-width="6"/>'
    s += '<path d="M -438,-26 C -455,-24 -470,-10 -472,0 C -470,10 -455,24 -438,26 Z" fill="url(#ac_spinner)" stroke="#334155" stroke-width="5"/>'
    if prop:
        s += '<ellipse cx="-440" cy="0" rx="9" ry="145" fill="#64748b" fill-opacity="0.3"/>'
    return s + "</g>\n"


# Airliner side view (wake-turbulence "heavy"): measured from the Boeing 767-300 side view in Julien Scavini's
# schematic on Wikimedia Commons (Boeing_767_family_v1.0.png, crop x 240-1200, y 1060-1360). Points are in
# crop pixels: nose tip (20, 207), tail cone (903, 192), ground under the wheels y = 284, so the aircraft is
# 883 px long and the fin top (y 28) is 256 px high (15.9 m on a 54.9 m airframe, as published).
# Front view, derived from the side and top views above (side units x 1.6 = top units; span 1300): cabin section
# 160 wide x 187 deep with its centre as the origin, low wing 40 thick at the root and 26 at the tip with 6 deg
# dihedral, tailplane span 480 level with the cabin centre, fin rising 213 above it, main wheels (radius 29)
# 143 below on a track of 0.3 x span, nose wheel radius 22, propeller radius 110 at the spinner (0, 22).


def aircraft_front(x, y, span=700, prop=True):
    """Trainer seen from straight ahead, centred on the cabin at (x, y), wingspan `span` canvas units."""
    k = span / 1300
    st = 'stroke="#334155" stroke-width="5" stroke-linejoin="round"'
    s = f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.4f})">'
    s += f'<path d="M -8,-30 L -5,-215 L 5,-215 L 8,-30 Z" fill="url(#ac_blue)" {st}/>'            # fin
    s += f'<path d="M -240,-6 L 240,-6 L 240,6 L -240,6 Z" fill="url(#ac_body)" {st}/>'           # tailplane
    for side in (-1, 1):                                                                       # wings
        tip_y = 72 - (648 - 78) * 0.105
        s += (f'<path d="M {side * 78},{52} L {side * 648},{tip_y - 13:.1f} L {side * 648},{tip_y + 13:.1f} '
              f'L {side * 78},{92} Z" fill="url(#ac_wing)" {st}/>')
        s += f'<path d="M {side * 190},{88} L {side * 195},{120}" stroke="#64748b" stroke-width="12"/>'
        s += f'<rect x="{side * 195 - 8}" y="114" width="16" height="58" rx="7" fill="#111827"/>'          # main wheels
    s += '<path d="M 0,90 L 0,128" stroke="#64748b" stroke-width="10"/>'
    s += '<rect x="-7" y="125" width="14" height="44" rx="6" fill="#111827"/>'                  # nose wheel
    s += (f'<path d="M -70,-94 C -30,-102 30,-102 70,-94 C 82,-60 82,40 74,72 C 50,94 -50,94 -74,72 '
          f'C -82,40 -82,-60 -70,-94 Z" fill="url(#ac_body)" {st}/>')                            # fuselage
    s += f'<path d="M -74,30 C -80,52 -76,66 -74,72 C -50,94 50,94 74,72 C 76,66 80,52 74,30 Z" fill="url(#ac_blue)"/>'
    s += f'<path d="M -58,-82 L 58,-82 L 52,-34 L -52,-34 Z" fill="url(#ac_glass)" stroke="#111827" stroke-width="5"/>'
    s += f'<ellipse cx="0" cy="22" rx="62" ry="50" fill="#e5e9ef" {st}/>'                          # cowling
    s += '<ellipse cx="-30" cy="46" rx="16" ry="9" fill="#1f2937"/><ellipse cx="30" cy="46" rx="16" ry="9" fill="#1f2937"/>'
    if prop:
        s += '<circle cx="0" cy="22" r="110" fill="#64748b" fill-opacity="0.16"/>'
        for a in (25, 205):
            s += f'<ellipse cx="0" cy="-33" rx="11" ry="55" fill="#1f2937" transform="rotate({a} 0 22)"/>'
    s += f'<circle cx="0" cy="22" r="18" fill="url(#ac_spinner)" {st}/>'
    return s + "</g>\n"


AL_BODY = [(20, 207), (24, 199), (31, 192), (40, 185), (52, 178), (66, 172), (84, 167), (110, 163), (150, 160),
           (720, 160), (780, 167), (840, 177), (880, 184), (898, 187), (903, 192), (900, 198), (888, 204),
           (860, 212), (820, 222), (760, 233), (700, 244), (640, 250), (560, 253), (300, 253), (140, 252),
           (100, 249), (70, 244), (48, 236), (32, 226), (23, 216), (20, 207)]
AL_FIN = "M 715,161 C 740,157 752,148 760,141 L 872,28 L 907,28 L 848,181 Z"
AL_STAB = [(775, 199), (800, 193), (860, 186), (900, 185), (880, 193), (840, 201), (800, 203), (775, 199)]
AL_WING = [(310, 226), (360, 216), (450, 210), (540, 203), (612, 196), (560, 214), (470, 229), (380, 234), (320, 232)]
AL_ENGINE = [(333, 228), (345, 224), (395, 225), (430, 232), (462, 243), (468, 247), (462, 251), (430, 254),
             (395, 261), (345, 265), (333, 262)]
AL_MAIN, AL_GROUND = 476, 284   # main-gear contact point: the pivot for rotation


def airliner_side(x, y, length=420, pitch=0, facing_right=True):
    """Twin-engine wide-body airliner from the side, `length` canvas units nose to tail, standing with its main
    wheels on (x, y) and rotating about them by `pitch` degrees nose-up."""
    k = length / 883
    sx = -k if facing_right else k
    rot = -pitch if facing_right else pitch
    sw = 1.6 / k
    stroke = f'stroke="#334155" stroke-width="{sw:.1f}" stroke-linejoin="round"'
    pts = lambda p: f"M {p[0][0]},{p[0][1]}" + _smooth(p) + " Z"  # noqa: E731
    s = f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({sx:.4f},{k:.4f}) translate(-{AL_MAIN},-{AL_GROUND})">'
    s += f'<path d="M 92,250 L 92,276 M 476,250 L 476,274" stroke="#64748b" stroke-width="4" fill="none"/>'
    for cx, r in ((92, 7), (465, 9), (488, 9)):
        cy = AL_GROUND - r
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#111827"/><circle cx="{cx}" cy="{cy}" r="{r * 0.4:.1f}" fill="#e5e7eb"/>'
    s += f'<path d="{pts(AL_BODY)}" fill="url(#ac_body)" {stroke}/>'
    s += f'<path d="M 30,236 C 200,256 560,258 700,244 L 640,250 L 300,253 L 140,252 Z" fill="#cbd5e1"/>'  # belly shade
    s += f'<path d="{AL_FIN}" fill="url(#ac_blue)" {stroke}/>'
    s += f'<path d="M 893,28 L 812,175" stroke="#1e4f8f" stroke-width="{sw:.1f}"/>'
    s += f'<path d="M 140,197 L 700,197" stroke="#1e293b" stroke-width="7" stroke-dasharray="4 7"/>'  # cabin windows
    s += f'<path d="M 38,193 L 48,186 L 66,186 L 69,195 L 58,198 Z" fill="#1e293b"/>'  # flight deck
    s += f'<path d="M 100,184 L 118,184 L 118,212 L 100,212 Z" fill="none" stroke="#94a3b8" stroke-width="{sw * 0.8:.1f}"/>'
    s += f'<path d="{pts(AL_STAB)}" fill="url(#ac_body)" {stroke}/>'
    s += f'<path d="{pts(AL_WING)}" fill="url(#ac_wing)" {stroke}/>'
    s += f'<path d="{pts(AL_ENGINE)}" fill="url(#metal)" {stroke}/>'
    s += f'<ellipse cx="336" cy="244.5" rx="4" ry="19" fill="#475569" {stroke}/>'
    return s + "</g>\n"
