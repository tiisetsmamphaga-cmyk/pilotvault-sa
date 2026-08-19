from PIL import Image, ImageDraw, ImageFont
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "explanation-images" / "principles-of-flight" / "static-v4"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 1000
NAVY = "#06111f"
GOLD = "#f4b400"
BLUE = "#1f4e79"
GREY = "#64748b"
LIGHT = "#d7e0ea"
PALE = "#f8fafc"
RED = "#b91c1c"
GREEN = "#166534"
WHITE = "#ffffff"
BLACK = "#111827"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(size, bold=False):
    try:
        return ImageFont.truetype(FONT_BOLD if bold else FONT, size)
    except OSError:
        return ImageFont.truetype("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def text_center(d, xy, txt, size, fill=BLACK, bold=False):
    f = F(size, bold)
    spacing = max(4, int(size * 0.2))
    b = d.multiline_textbbox((0, 0), txt, font=f, spacing=spacing, align="center")
    tw, th = b[2] - b[0], b[3] - b[1]
    d.multiline_text((xy[0] - tw / 2, xy[1] - th / 2), txt, font=f, fill=fill, spacing=spacing, align="center")


def arrow(d, p1, p2, fill=GOLD, width=8, head=22):
    d.line([p1, p2], fill=fill, width=width)
    a = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    pts = [
        p2,
        (p2[0] - head * math.cos(a - 0.55), p2[1] - head * math.sin(a - 0.55)),
        (p2[0] - head * math.cos(a + 0.55), p2[1] - head * math.sin(a + 0.55)),
    ]
    d.polygon(pts, fill=fill)


def label_box(d, xy, txt, size=26, width=None, textfill=BLACK, fill=WHITE, outline=LIGHT, bold=True, pad=14):
    f = F(size, bold)
    b = d.multiline_textbbox((0, 0), txt, font=f, spacing=6, align="center")
    tw, th = b[2] - b[0], b[3] - b[1]
    bw = max(width or 0, tw + 2 * pad)
    bh = th + 2 * pad
    box = (xy[0] - bw / 2, xy[1] - bh / 2, xy[0] + bw / 2, xy[1] + bh / 2)
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=2)
    d.multiline_text((xy[0] - tw / 2, xy[1] - th / 2), txt, font=f, fill=textfill, spacing=6, align="center")
    return box


def callout(d, target, box_center, txt, size=23, width=240):
    d.line([target, box_center], fill=GREY, width=3)
    label_box(d, box_center, txt, size, width)


def base(title):
    im = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 190), fill=NAVY)
    text_center(d, (800, 55), "PILOTVAULT PRINCIPLES OF FLIGHT", 28, GOLD, True)
    text_center(d, (800, 125), title.upper(), 48, WHITE, True)
    d.rounded_rectangle((55, 225, 1545, 935), radius=20, fill=WHITE, outline=LIGHT, width=3)
    return im, d


def footer(d, txt):
    text_center(d, (800, 900), txt, 26, GREY, False)


def save(im, name):
    path = OUT / f"{name}.png"
    im.save(path, optimize=True)


def airfoil_poly(x0, y0, x1, y1, camber=0.06, thickness=0.11, n=80):
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    ang = math.atan2(dy, dx)
    up, lo = [], []
    for i in range(n + 1):
        t = i / n
        x = t * L
        yt = 5 * thickness * L * (0.2969 * math.sqrt(max(t, 1e-6)) - 0.1260 * t - 0.3516 * t * t + 0.2843 * t**3 - 0.1015 * t**4)
        yc = camber * L * 4 * t * (1 - t)
        for arr, yy in ((up, yc + yt), (lo, yc - yt)):
            X = x0 + x * math.cos(ang) - yy * math.sin(ang)
            Y = y0 + x * math.sin(ang) + yy * math.cos(ang)
            arr.append((X, Y))
    return up + lo[::-1]


def angle_of_attack():
    im, d = base("Angle of Attack")
    arrow(d, (120, 500), (400, 500), GREY, 10, 28)
    label_box(d, (260, 445), "AIRCRAFT FLIGHT PATH", 21, 300, textfill=GREY)
    arrow(d, (400, 590), (120, 590), BLUE, 11, 30)
    label_box(d, (260, 650), "RELATIVE AIRFLOW", 22, 280, textfill=BLUE)
    pts = airfoil_poly(520, 540, 1320, 410, 0.07, 0.10)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line((520, 540, 1320, 410), fill=GOLD, width=7)
    d.line((430, 690, 1340, 690), fill=BLUE, width=6)
    arrow(d, (560, 690), (430, 690), BLUE, 6, 20)
    d.arc((430, 500, 650, 720), start=305, end=360, fill=GOLD, width=10)
    label_box(d, (610, 620), "α  ANGLE OF ATTACK", 27, 320, textfill=NAVY)
    callout(d, (535, 530), (340, 330), "LEADING EDGE", 22, 240)
    callout(d, (1300, 414), (1320, 330), "TRAILING EDGE", 22, 250)
    callout(d, (920, 475), (970, 330), "CHORD LINE", 22, 220)
    callout(d, (910, 430), (770, 310), "UPPER CAMBER", 22, 260)
    callout(d, (920, 525), (1000, 610), "LOWER CAMBER", 22, 260)
    footer(d, "Angle of attack is measured between the chord line and the relative airflow.")
    save(im, "angle-of-attack-v5")


def relative_airflow():
    im, d = base("Relative Airflow")
    arrow(d, (250, 500), (1330, 500), GREY, 10, 30)
    arrow(d, (1330, 675), (250, 675), BLUE, 12, 32)
    label_box(d, (800, 425), "AIRCRAFT MOTION / FLIGHT PATH", 28, 540, textfill=GREY)
    label_box(d, (800, 750), "RELATIVE AIRFLOW", 30, 390, textfill=BLUE)
    footer(d, "Relative airflow is parallel and opposite to the aircraft's motion through the air mass.")
    save(im, "relative-airflow-v4")


def aerofoil_geometry():
    im, d = base("Aerofoil Geometry")
    pts = airfoil_poly(260, 570, 1340, 550, 0.08, 0.12)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line((260, 570, 1340, 550), fill=BLUE, width=5)
    callout(d, (280, 560), (240, 350), "LEADING EDGE", 23, 230)
    callout(d, (1320, 550), (1340, 350), "TRAILING EDGE", 23, 245)
    callout(d, (810, 560), (810, 350), "CHORD LINE", 23, 220)
    callout(d, (800, 450), (990, 365), "UPPER CAMBER", 23, 260)
    callout(d, (800, 625), (990, 720), "LOWER CAMBER", 23, 260)
    d.line((680, 455, 680, 625), fill=GOLD, width=5)
    label_box(d, (560, 540), "MAX\nTHICKNESS", 23, 200)
    footer(d, "The chord line is the straight reference joining the leading and trailing edges.")
    save(im, "aerofoil-geometry-v4")


def lift_drag_directions():
    im, d = base("Lift and Drag Directions")
    arrow(d, (1300, 700), (300, 700), BLUE, 10, 30)
    label_box(d, (800, 755), "RELATIVE AIRFLOW / FLIGHT PATH", 24, 520, textfill=BLUE)
    o = (800, 580)
    d.ellipse((782, 562, 818, 598), fill=NAVY)
    arrow(d, o, (800, 330), GOLD, 11, 28)
    arrow(d, o, (1100, 580), GREY, 10, 28)
    label_box(d, (800, 290), "LIFT\n90° TO RELATIVE AIRFLOW", 27, 380)
    label_box(d, (1230, 580), "DRAG\nPARALLEL & OPPOSITE", 24, 330, textfill=GREY)
    footer(d, "Lift acts perpendicular to the relative airflow; drag acts parallel and opposite to it.")
    save(im, "lift-drag-directions-v4")


def lift_pressure():
    im, d = base("Pressure Distribution Produces Lift")
    pts = airfoil_poly(300, 590, 1320, 575, 0.08, 0.11)
    d.polygon(pts, fill=PALE, outline=NAVY)
    for x in range(480, 1200, 160):
        arrow(d, (x, 360), (x, 470), BLUE, 6, 18)
        arrow(d, (x, 780), (x, 650), GOLD, 6, 18)
    label_box(d, (800, 315), "LOWER STATIC PRESSURE ABOVE", 25, 470, textfill=BLUE)
    label_box(d, (800, 825), "HIGHER STATIC PRESSURE BELOW", 25, 500)
    arrow(d, (1390, 590), (1390, 340), GOLD, 12, 30)
    label_box(d, (1390, 290), "NET LIFT", 26, 220)
    footer(d, "The pressure difference around the aerofoil produces an upward aerodynamic resultant.")
    save(im, "lift-pressure-distribution-v4")


def centre_pressure():
    im, d = base("Centre of Pressure")
    pts = airfoil_poly(290, 600, 1310, 575, 0.07, 0.10)
    d.polygon(pts, fill=PALE, outline=NAVY)
    cp = (850, 585)
    d.ellipse((836, 571, 864, 599), fill=GOLD)
    arrow(d, cp, (850, 340), GOLD, 11, 28)
    label_box(d, (850, 300), "RESULTANT LIFT", 26, 300)
    label_box(d, (850, 700), "CENTRE OF PRESSURE", 27, 360)
    footer(d, "The centre of pressure is the point through which the resultant aerodynamic force acts.")
    save(im, "centre-of-pressure-v4")


def centre_pressure_shift():
    im, d = base("Centre of Pressure Shift")
    for y, cp_x, title in [(450, 980, "LOWER AoA"), (700, 790, "HIGHER AoA")]:
        pts = airfoil_poly(280, y, 1320, y - 15, 0.06, 0.08)
        d.polygon(pts, fill=PALE, outline=NAVY)
        d.ellipse((cp_x - 12, y - 12, cp_x + 12, y + 12), fill=GOLD)
        label_box(d, (210, y), title, 21, 210, textfill=GREY)
        label_box(d, (cp_x, y - 85), "CP", 21, 90)
    arrow(d, (960, 580), (820, 580), GOLD, 9, 25)
    label_box(d, (890, 580), "CP MOVES\nFORWARD", 24, 240)
    footer(d, "For the conventional aerofoil assumed here, increasing angle of attack moves CP forward in normal flight.")
    save(im, "centre-pressure-shift-v4")


def lift_speed_squared():
    im, d = base("Lift and Airspeed Squared")
    ox, oy, xe, yt = 300, 800, 1320, 320
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pts = []
    for i in range(101):
        t = i / 100
        pts.append((ox + t * (xe - ox), oy - t * t * (oy - yt) * 0.92))
    d.line(pts, fill=GOLD, width=8)
    label_box(d, (920, 370), "L ∝ V²", 36, 250)
    label_box(d, (800, 860), "TRUE AIRSPEED", 24, 300, textfill=GREY)
    label_box(d, (170, 550), "LIFT", 24, 150, textfill=GREY)
    text_center(d, (580, 680), "2× SPEED", 24, BLUE, True)
    text_center(d, (1000, 485), "4× LIFT", 24, BLUE, True)
    footer(d, "With density, wing area and CL unchanged, doubling true airspeed produces four times the lift.")
    save(im, "lift-speed-squared-v4")


def boundary_layer():
    im, d = base("Boundary Layer and Transition")
    pts = airfoil_poly(260, 670, 1340, 640, 0.06, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    for off, c, w in [(70, BLUE, 4), (120, BLUE, 3), (170, GREY, 3)]:
        path = [(280 + i * 20, 600 - off * (1 - i / 60 * 0.15) - 16 * math.sin(i / 60 * math.pi)) for i in range(50)]
        d.line(path, fill=c, width=w)
    d.line((780, 450, 780, 690), fill=GOLD, width=6)
    label_box(d, (470, 370), "LAMINAR REGION", 24, 300, textfill=BLUE)
    label_box(d, (780, 345), "TRANSITION POINT", 24, 320)
    label_box(d, (1080, 370), "TURBULENT REGION", 24, 330, textfill=GREY)
    footer(d, "The boundary layer may begin laminar and transition to turbulent flow before separation.")
    save(im, "boundary-layer-transition-v4")


def wing_polar():
    im, d = base("Reading a Wing Polar")
    ox, oy, xe, yt = 320, 810, 1320, 300
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pts = []
    for i in range(101):
        t = i / 100
        x = 420 + 700 * (0.12 + 0.75 * t + 0.1 * t * t)
        y = 770 - 420 * (4 * t * (1 - t) * 0.72 + t * 0.12)
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=8)
    pleft = min(pts, key=lambda p: p[0])
    ptop = min(pts, key=lambda p: p[1])
    d.ellipse((pleft[0] - 12, pleft[1] - 12, pleft[0] + 12, pleft[1] + 12), fill=GOLD)
    d.ellipse((ptop[0] - 12, ptop[1] - 12, ptop[0] + 12, ptop[1] + 12), fill=RED)
    callout(d, pleft, (520, 650), "MINIMUM DRAG", 21, 260)
    callout(d, ptop, (1050, 340), "CLmax / CRITICAL AoA", 21, 330)
    d.line((ox, oy, 820, 490), fill=GOLD, width=4)
    label_box(d, (760, 545), "BEST L/D\nTANGENT", 21, 230)
    label_box(d, (820, 865), "DRAG COEFFICIENT CD", 22, 350, textfill=GREY)
    label_box(d, (180, 540), "LIFT\nCOEFFICIENT CL", 22, 250, textfill=GREY)
    footer(d, "Best L/D is found by the tangent from the origin; CLmax marks the critical angle.")
    save(im, "wing-polar-v4")


def newtons_laws():
    im, d = base("Newton's Laws in Flight")
    for x, a, b in [(350, "1ST LAW", "INERTIA / EQUILIBRIUM"), (800, "2ND LAW", "F = m a"), (1250, "3RD LAW", "ACTION ↔ REACTION")]:
        d.rounded_rectangle((x - 180, 380, x + 180, 650), radius=16, fill=PALE, outline=LIGHT, width=3)
        text_center(d, (x, 455), a, 30, NAVY, True)
        text_center(d, (x, 555), b, 27, BLUE, True)
    footer(d, "First: inertia. Second: force causes acceleration. Third: every action has an equal and opposite reaction.")
    save(im, "newtons-laws-v4")


def venturi():
    im, d = base("Venturi: Continuity and Bernoulli")
    d.line([(170, 400), (560, 400), (720, 500), (880, 400), (1430, 400)], fill=NAVY, width=6)
    d.line([(170, 700), (560, 700), (720, 600), (880, 700), (1430, 700)], fill=NAVY, width=6)
    arrow(d, (230, 550), (1360, 550), BLUE, 10, 30)
    label_box(d, (350, 320), "WIDE SECTION\nLOWER V\nHIGHER STATIC P", 21, 330)
    label_box(d, (800, 300), "THROAT\nHIGHER V\nLOWER STATIC P", 21, 330)
    label_box(d, (1240, 320), "PRESSURE\nRECOVERS", 21, 250)
    footer(d, "For steady subsonic flow, mass flow stays constant; velocity rises as area narrows and static pressure falls.")
    save(im, "venturi-bernoulli-v4")


def dynamic_pressure():
    im, d = base("Static, Dynamic and Total Pressure")
    label_box(d, (420, 520), "STATIC PRESSURE\nAMBIENT", 29, 370)
    label_box(d, (1180, 520), "TOTAL PRESSURE\nSTAGNATION", 29, 390)
    arrow(d, (650, 520), (950, 520), GOLD, 10, 28)
    label_box(d, (800, 430), "+ DYNAMIC q", 25, 270)
    label_box(d, (800, 720), "q = ½ ρ V²", 36, 300, textfill=BLUE)
    footer(d, "Dynamic pressure = total pressure − static pressure.")
    save(im, "dynamic-pressure-v4")


def propeller_torque():
    im, d = base("Propeller Torque Reaction")
    d.ellipse((620, 330, 980, 690), outline=LIGHT, width=4)
    d.line((800, 370, 800, 650), fill=GOLD, width=24)
    d.arc((600, 310, 1000, 710), start=290, end=60, fill=BLUE, width=10)
    arrow(d, (960, 420), (1030, 455), BLUE, 8, 22)
    d.arc((480, 250, 1120, 790), start=115, end=230, fill=RED, width=10)
    arrow(d, (550, 650), (500, 600), RED, 8, 22)
    label_box(d, (1180, 420), "PROP ROTATION\nCLOCKWISE FROM COCKPIT", 23, 370, textfill=BLUE)
    label_box(d, (410, 690), "TORQUE REACTION\nROLLS AIRCRAFT LEFT", 23, 340, textfill=RED)
    footer(d, "Newton's third law creates a reaction torque opposite the propeller's rotation.")
    save(im, "propeller-torque-reaction-v4")


def p_factor():
    im, d = base("Asymmetric Blade Effect (P-Factor)")
    d.ellipse((570, 340, 1030, 800), outline=LIGHT, width=4)
    d.line((800, 370, 800, 770), fill=NAVY, width=18)
    d.line((800, 560, 800, 770), fill=GOLD, width=30)
    arrow(d, (930, 610), (1200, 610), GOLD, 10, 28)
    label_box(d, (1220, 535), "DESCENDING BLADE\nMORE THRUST", 23, 330)
    arrow(d, (680, 840), (480, 840), RED, 10, 28)
    label_box(d, (800, 840), "NET YAW LEFT → RIGHT RUDDER REQUIRED", 23, 690)
    footer(d, "At high power and high angle of attack, the descending blade can produce more thrust than the ascending blade.")
    save(im, "p-factor-v4")


def aircraft_axes():
    im, d = base("Aircraft Axes and Primary Controls")
    d.polygon([(800, 350), (900, 580), (840, 620), (800, 780), (760, 620), (700, 580)], fill=PALE, outline=NAVY)
    d.line((310, 560, 1290, 560), fill=NAVY, width=18)
    d.ellipse((785, 545, 815, 575), fill=GOLD)
    arrow(d, (800, 850), (800, 290), BLUE, 8, 22)
    arrow(d, (300, 560), (1300, 560), GOLD, 8, 22)
    arrow(d, (540, 790), (1060, 330), GREY, 8, 22)
    label_box(d, (1080, 285), "LONGITUDINAL AXIS\nROLL — AILERONS", 22, 360)
    label_box(d, (1280, 650), "LATERAL AXIS\nPITCH — ELEVATOR", 22, 330)
    label_box(d, (450, 300), "VERTICAL / NORMAL AXIS\nYAW — RUDDER", 22, 390)
    footer(d, "All three axes intersect at the centre of gravity.")
    save(im, "aircraft-axes-controls-v4")


def control_effects():
    im, d = base("Primary and Further Control Effects")
    for x, name, a, b, c in [(350, "AILERON", "ROLL", "YAW", "SPIRAL"), (800, "RUDDER", "YAW", "ROLL", "SPIRAL"), (1250, "ELEVATOR", "PITCH", "", "")]:
        label_box(d, (x, 350), name, 26, 270)
        arrow(d, (x, 405), (x, 480), GOLD, 7, 20)
        label_box(d, (x, 525), a, 24, 210, textfill=BLUE)
        if b:
            arrow(d, (x, 570), (x, 640), GREY, 6, 18)
            label_box(d, (x, 680), b, 22, 190, textfill=GREY)
            arrow(d, (x, 720), (x, 785), GREY, 5, 16)
            label_box(d, (x, 825), c, 21, 190, textfill=GREY)
    save(im, "control-effects-v4")


def adverse_yaw():
    im, d = base("Adverse Aileron Yaw")
    d.line((250, 540, 1350, 540), fill=NAVY, width=22)
    d.line((250, 540, 420, 470), fill=GOLD, width=18)
    d.line((1180, 540, 1350, 600), fill=GOLD, width=18)
    label_box(d, (360, 380), "UP-GOING AILERON\nLESS LIFT / LESS INDUCED DRAG", 21, 410)
    label_box(d, (1240, 690), "DOWN-GOING AILERON\nMORE LIFT / MORE INDUCED DRAG", 21, 430)
    arrow(d, (970, 820), (630, 820), RED, 10, 28)
    label_box(d, (800, 850), "ADVERSE YAW — OPPOSITE THE INTENDED ROLL", 23, 650, textfill=RED)
    save(im, "adverse-yaw-v4")


def differential_ailerons():
    im, d = base("Differential Ailerons")
    d.line((250, 500, 1350, 500), fill=NAVY, width=18)
    d.line((250, 500, 470, 420), fill=GOLD, width=18)
    d.line((1130, 500, 1350, 545), fill=GOLD, width=18)
    label_box(d, (360, 350), "UP AILERON\nLARGER DEFLECTION", 22, 330, textfill=BLUE)
    label_box(d, (1240, 620), "DOWN AILERON\nSMALLER DEFLECTION", 22, 350)
    footer(d, "Differential ailerons reduce adverse yaw by making the up-going aileron move farther than the down-going aileron.")
    save(im, "differential-ailerons-v4")


def frise_aileron():
    im, d = base("Frise Aileron")
    d.line((320, 520, 1100, 520), fill=NAVY, width=20)
    d.line((900, 520, 1250, 420), fill=GOLD, width=20)
    d.ellipse((875, 500, 915, 540), fill=BLUE)
    d.polygon([(875, 520), (930, 535), (900, 585)], fill=GOLD)
    label_box(d, (690, 380), "HINGE", 22, 150)
    callout(d, (910, 565), (980, 700), "NOSE PROJECTS INTO AIRFLOW\nWHEN AILERON MOVES UP", 21, 400)
    footer(d, "The projecting nose adds drag on the up-going aileron side, helping reduce adverse yaw.")
    save(im, "frise-aileron-v4")


def four_forces():
    im, d = base("Four Forces in Level Flight")
    d.polygon([(520, 550), (1040, 550), (1160, 585), (1040, 620), (520, 620), (430, 585)], fill=PALE, outline=NAVY)
    arrow(d, (800, 550), (800, 300), GOLD, 11, 30)
    label_box(d, (800, 260), "LIFT", 27, 180)
    arrow(d, (800, 620), (800, 850), GREY, 11, 30)
    label_box(d, (800, 870), "WEIGHT", 27, 220, textfill=GREY)
    arrow(d, (1040, 585), (1390, 585), GOLD, 11, 30)
    label_box(d, (1290, 525), "THRUST", 27, 220)
    arrow(d, (520, 585), (180, 585), BLUE, 11, 30)
    label_box(d, (300, 525), "DRAG", 27, 180, textfill=BLUE)
    footer(d, "Steady straight-and-level flight: lift = weight and thrust = drag.")
    save(im, "four-forces-level-flight-v4")


def cg_cp_pitch():
    im, d = base("CG, Centre of Pressure and Pitch")
    pts = airfoil_poly(270, 570, 1320, 550, 0.05, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    cg, cp = (670, 565), (910, 560)
    d.ellipse((657, 552, 683, 578), fill=GOLD)
    d.ellipse((897, 547, 923, 573), fill=BLUE)
    label_box(d, (cg[0], 430), "CG", 22, 100)
    label_box(d, (cp[0], 430), "CP", 22, 100, textfill=BLUE)
    arrow(d, cp, (cp[0], 330), GOLD, 8, 22)
    arrow(d, cg, (cg[0], 790), GREY, 8, 22)
    label_box(d, (800, 825), "CONVENTIONAL ARRANGEMENT: CG AHEAD OF CP", 23, 590)
    footer(d, "This force couple contributes to the aircraft's normal pitching balance.")
    save(im, "cg-centre-pressure-pitch-v4")


def climb_forces():
    im, d = base("Forces in a Steady Climb")
    d.line((320, 760, 1250, 510), fill=LIGHT, width=5)
    d.line((650, 665, 930, 590), fill=NAVY, width=18)
    o = (790, 628)
    arrow(d, o, (1110, 540), GOLD, 10, 28)
    label_box(d, (1165, 500), "THRUST", 23, 190)
    arrow(d, o, (470, 715), BLUE, 10, 28)
    label_box(d, (410, 760), "DRAG", 23, 170, textfill=BLUE)
    arrow(d, o, (790, 365), GOLD, 10, 28)
    label_box(d, (860, 330), "LIFT", 23, 170)
    arrow(d, o, (790, 875), GREY, 10, 28)
    label_box(d, (875, 850), "WEIGHT", 23, 200, textfill=GREY)
    footer(d, "In a steady climb at constant speed, thrust > drag and lift < weight.")
    save(im, "steady-climb-forces-v4")


def vx_vy():
    im, d = base("Best Angle and Best Rate of Climb")
    d.line((220, 820, 1380, 820), fill=NAVY, width=5)
    d.rectangle((1230, 470, 1290, 820), fill=GREY)
    d.line((260, 800, 1210, 500), fill=GOLD, width=8)
    d.line((260, 800, 920, 420), fill=BLUE, width=8)
    label_box(d, (1040, 455), "VX — BEST ANGLE\nMAX HEIGHT / DISTANCE", 22, 420)
    label_box(d, (730, 390), "VY — BEST RATE\nMAX HEIGHT / TIME", 22, 400, textfill=BLUE)
    label_box(d, (1260, 430), "OBSTACLE", 21, 180, textfill=GREY)
    footer(d, "VX is used for obstacle clearance; VY gives the greatest climb rate.")
    save(im, "vx-vy-v4")


def descent_power():
    im, d = base("Power and Rate of Descent")
    d.line((250, 380, 1350, 790), fill=LIGHT, width=5)
    label_box(d, (470, 470), "POWER ↑\nRATE OF DESCENT ↓", 27, 360, textfill=BLUE)
    label_box(d, (1120, 710), "POWER ↓\nRATE OF DESCENT ↑", 27, 360)
    arrow(d, (600, 520), (850, 610), GOLD, 10, 28)
    footer(d, "At constant airspeed, increasing power reduces rate of descent; reducing power increases it.")
    save(im, "power-rate-of-descent-v4")


def drag_curves():
    im, d = base("Induced, Parasite and Total Drag")
    ox, oy, xe, yt = 300, 800, 1330, 310
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pi, pp, pt = [], [], []
    for i in range(1, 101):
        t = i / 100
        x = ox + 70 + t * (xe - ox - 110)
        induced = 330 / (t + 0.25)
        parasite = 90 + 330 * t * t
        pi.append((x, oy - min(420, induced) * 0.85))
        pp.append((x, oy - min(420, parasite) * 0.85))
        pt.append((x, oy - min(460, induced + parasite - 160) * 0.75))
    d.line(pi, fill=BLUE, width=7)
    d.line(pp, fill=GOLD, width=7)
    d.line(pt, fill=NAVY, width=8)
    label_box(d, (470, 385), "INDUCED DRAG", 21, 240, textfill=BLUE)
    label_box(d, (1160, 390), "PARASITE DRAG", 21, 260)
    label_box(d, (900, 520), "TOTAL DRAG", 21, 220)
    pmin = max(pt, key=lambda p: p[1])
    d.ellipse((pmin[0] - 12, pmin[1] - 12, pmin[0] + 12, pmin[1] + 12), fill=RED)
    label_box(d, (pmin[0], pmin[1] + 75), "VMD / BEST L/D", 20, 240, textfill=RED)
    footer(d, "Induced drag falls with speed; parasite drag rises. Their sum has a minimum.")
    save(im, "drag-curves-v4")


def induced_drag():
    im, d = base("Wingtip Vortices and Induced Drag")
    d.line((300, 520, 1300, 520), fill=NAVY, width=28)
    label_box(d, (800, 410), "LOW PRESSURE ABOVE", 23, 340, textfill=BLUE)
    label_box(d, (800, 650), "HIGH PRESSURE BELOW", 23, 360)
    d.arc((150, 500, 450, 800), start=20, end=330, fill=BLUE, width=8)
    d.arc((1150, 500, 1450, 800), start=210, end=520, fill=BLUE, width=8)
    arrow(d, (520, 720), (520, 580), GOLD, 7, 20)
    arrow(d, (1080, 720), (1080, 580), GOLD, 7, 20)
    footer(d, "Pressure flows around the wingtips, producing vortices, downwash and induced drag.")
    save(im, "wingtip-vortices-induced-drag-v4")


def skin_friction():
    im, d = base("Skin-Friction Drag")
    d.line((200, 650, 1400, 650), fill=NAVY, width=12)
    for y, c in [(620, BLUE), (560, BLUE), (500, GREY), (440, GREY)]:
        arrow(d, (240, y), (1360, y), c, 4, 16)
    label_box(d, (450, 745), "AIR AT SURFACE\nVELOCITY ≈ 0", 23, 300)
    label_box(d, (1100, 380), "FREE-STREAM AIR\nFASTEST", 23, 300, textfill=GREY)
    label_box(d, (800, 560), "BOUNDARY LAYER", 24, 280, textfill=BLUE)
    footer(d, "Viscous shear slows the air next to the surface and contributes to parasite drag.")
    save(im, "skin-friction-v4")


def aspect_ratio():
    im, d = base("Aspect Ratio and Induced Drag")
    d.rectangle((180, 430, 730, 570), fill=PALE, outline=NAVY, width=4)
    d.rectangle((960, 365, 1160, 635), fill=PALE, outline=NAVY, width=4)
    label_box(d, (455, 330), "HIGH ASPECT RATIO", 25, 340)
    label_box(d, (1060, 290), "LOW ASPECT RATIO", 25, 320)
    label_box(d, (455, 690), "LESS INDUCED DRAG", 24, 330, textfill=BLUE)
    label_box(d, (1060, 690), "MORE INDUCED DRAG", 24, 350, textfill=RED)
    footer(d, "Aspect ratio compares wingspan with mean aerodynamic chord.")
    save(im, "aspect-ratio-v4")


def washout():
    im, d = base("Washout")
    d.polygon([(260, 500), (800, 420), (1340, 500), (800, 610)], fill=PALE, outline=NAVY)
    d.line((760, 450, 840, 580), fill=GOLD, width=8)
    d.line((1250, 480, 1350, 505), fill=BLUE, width=8)
    label_box(d, (800, 335), "ROOT — GREATER INCIDENCE", 23, 360)
    label_box(d, (1270, 625), "TIP — LOWER INCIDENCE", 23, 330, textfill=BLUE)
    arrow(d, (1030, 720), (1270, 720), GOLD, 8, 22)
    label_box(d, (1150, 790), "INCIDENCE DECREASES TOWARD THE TIP", 21, 520)
    footer(d, "Washout delays wingtip stall and helps preserve aileron effectiveness.")
    save(im, "washout-v4")


def flap_effects():
    im, d = base("Trailing-Edge Flap Effects")
    pts = airfoil_poly(160, 500, 690, 490, 0.05, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    pts2 = airfoil_poly(900, 500, 1380, 490, 0.08, 0.09)
    d.polygon(pts2, fill=PALE, outline=NAVY)
    d.line((1280, 495, 1420, 590), fill=GOLD, width=18)
    label_box(d, (420, 340), "CLEAN WING", 25, 260)
    label_box(d, (1160, 340), "FLAP EXTENDED", 25, 300)
    label_box(d, (420, 700), "LOWER CLmax\nLOWER DRAG", 23, 280, textfill=BLUE)
    label_box(d, (1160, 700), "CLmax ↑\nDRAG ↑\nAoA FOR SAME LIFT ↓", 23, 320)
    footer(d, "Trailing-edge flaps increase camber and CLmax, but also increase drag.")
    save(im, "trailing-edge-flap-effects-v4")


def fowler_flap():
    im, d = base("Fowler Flap")
    pts = airfoil_poly(260, 520, 1120, 500, 0.05, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line((1080, 505, 1340, 650), fill=GOLD, width=22)
    arrow(d, (1050, 700), (1310, 700), BLUE, 8, 22)
    arrow(d, (1330, 650), (1330, 760), BLUE, 8, 22)
    label_box(d, (1200, 800), "MOVES AFT + DOWN", 23, 350, textfill=BLUE)
    label_box(d, (650, 350), "WING AREA INCREASES", 25, 360)
    footer(d, "A Fowler flap slides aft before moving down, increasing both wing area and camber.")
    save(im, "fowler-flap-v4")


def flaps_glide():
    im, d = base("Flaps and Glide Performance")
    d.line((260, 330, 1370, 720), fill=BLUE, width=8)
    d.line((260, 330, 1100, 820), fill=GOLD, width=9)
    label_box(d, (1190, 670), "CLEAN\nSHALLOWER GLIDE", 23, 290, textfill=BLUE)
    label_box(d, (880, 800), "FLAPS\nSTEEPER GLIDE", 23, 280)
    footer(d, "Flap extension normally reduces best L/D and shortens maximum gliding distance.")
    save(im, "flaps-glide-v4")


def wind_glide():
    im, d = base("Wind Effect on Glide Over the Ground")
    d.line((150, 820, 1450, 820), fill=NAVY, width=5)
    d.line((250, 350, 850, 820), fill=GOLD, width=8)
    d.line((250, 350, 1300, 820), fill=BLUE, width=8)
    arrow(d, (700, 290), (430, 290), GREY, 8, 22)
    label_box(d, (570, 235), "HEADWIND", 22, 220, textfill=GREY)
    label_box(d, (720, 720), "STEEPER\nOVER GROUND", 22, 250)
    label_box(d, (1210, 720), "TAILWIND\nSHALLOWER OVER GROUND", 22, 350, textfill=BLUE)
    footer(d, "Wind changes the ground glide path through groundspeed; it does not directly change the air-mass rate of descent.")
    save(im, "wind-glide-groundpath-v4")


def flap_cp():
    im, d = base("Flaps, Centre of Pressure and Pitch")
    for x0, title, cp_x, flap in [(180, "CLEAN", 520, False), (880, "FLAP DOWN", 1100, True)]:
        pts = airfoil_poly(x0, 560, x0 + 500, 550, 0.05 if not flap else 0.08, 0.08)
        d.polygon(pts, fill=PALE, outline=NAVY)
        if flap:
            d.line((x0 + 420, 553, x0 + 560, 650), fill=GOLD, width=18)
        d.ellipse((cp_x - 12, 545, cp_x + 12, 569), fill=BLUE)
        label_box(d, (x0 + 250, 370), title, 23, 230)
        label_box(d, (cp_x, 700), "CP", 21, 90, textfill=BLUE)
    arrow(d, (700, 780), (1000, 780), GOLD, 8, 22)
    label_box(d, (850, 840), "INITIAL CP SHIFT AFT", 22, 320)
    footer(d, "On the conventional wing assumed here, lowering trailing-edge flaps initially moves the centre of pressure aft.")
    save(im, "flap-centre-pressure-pitch-v4")


def leading_edge_slot():
    im, d = base("Leading-Edge Slot")
    pts = airfoil_poly(440, 610, 1300, 580, 0.07, 0.10)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line((320, 590, 430, 540), fill=GOLD, width=20)
    arrow(d, (250, 660), (470, 560), BLUE, 8, 22)
    arrow(d, (470, 560), (780, 430), BLUE, 8, 22)
    label_box(d, (365, 475), "SLOT", 23, 150)
    label_box(d, (850, 360), "ENERGISED AIRFLOW\nOVER UPPER SURFACE", 23, 360, textfill=BLUE)
    footer(d, "The slot re-energises the upper-surface boundary layer and delays separation to a higher angle of attack.")
    save(im, "leading-edge-slot-v4")


def flap_vs_no_flap():
    im, d = base("Flap vs No-Flap Approach")
    d.rectangle((120, 800, 1480, 835), fill=GREY)
    d.line((260, 330, 1120, 790), fill=GOLD, width=8)
    d.line((260, 330, 1380, 790), fill=BLUE, width=8)
    label_box(d, (690, 560), "FULL FLAP\nLOWER NOSE / STEEPER PATH", 21, 360)
    label_box(d, (1180, 560), "NO FLAP\nHIGHER NOSE / HIGHER SPEED", 21, 360, textfill=BLUE)
    footer(d, "A no-flap approach normally requires a higher approach/landing speed and a higher nose attitude.")
    save(im, "flap-vs-no-flap-approach-v4")


def stability():
    im, d = base("Static and Dynamic Stability")
    d.line((200, 580, 1400, 580), fill=LIGHT, width=4)
    pts = []
    for i in range(240):
        x = 250 + i * 4.5
        t = i / 239 * 7
        y = 580 - 180 * math.exp(-0.35 * t) * math.sin(2.5 * t)
        pts.append((x, y))
    d.line(pts, fill=BLUE, width=7)
    label_box(d, (530, 340), "POSITIVE STATIC\nINITIAL RESTORING TENDENCY", 22, 390)
    label_box(d, (1130, 470), "POSITIVE DYNAMIC\nOSCILLATIONS DECAY", 22, 360, textfill=BLUE)
    footer(d, "Static stability describes the initial tendency; dynamic stability describes how the motion changes with time.")
    save(im, "static-dynamic-stability-v4")


def cg_stability():
    im, d = base("Centre of Gravity and Longitudinal Stability")
    d.line((260, 560, 1340, 560), fill=NAVY, width=8)
    d.ellipse((470, 540, 510, 580), fill=GOLD)
    d.ellipse((1000, 540, 1040, 580), fill=BLUE)
    label_box(d, (490, 430), "FORWARD CG", 25, 260)
    label_box(d, (1020, 430), "AFT CG", 25, 230, textfill=BLUE)
    label_box(d, (490, 700), "MORE STABILITY\nMORE CONTROL FORCE", 23, 320)
    label_box(d, (1020, 700), "LESS STABILITY\nMORE SENSITIVE PITCH", 23, 330, textfill=RED)
    footer(d, "Moving the CG forward increases longitudinal stability; moving it aft reduces the stability margin.")
    save(im, "cg-longitudinal-stability-v4")


def longitudinal_dihedral():
    im, d = base("Longitudinal Dihedral")
    d.line((220, 700, 1380, 700), fill=LIGHT, width=5)
    d.line((300, 570, 820, 500), fill=NAVY, width=14)
    d.line((1030, 610, 1340, 640), fill=BLUE, width=14)
    label_box(d, (570, 390), "MAINPLANE\nHIGHER INCIDENCE", 23, 300)
    label_box(d, (1190, 770), "TAILPLANE\nLOWER INCIDENCE", 23, 300, textfill=BLUE)
    footer(d, "The incidence relationship between mainplane and tailplane contributes to longitudinal stability.")
    save(im, "longitudinal-dihedral-v4")


def dihedral():
    im, d = base("Dihedral and Lateral Stability")
    d.line((800, 600, 380, 430), fill=NAVY, width=18)
    d.line((800, 600, 1220, 430), fill=NAVY, width=18)
    arrow(d, (180, 780), (520, 610), BLUE, 9, 24)
    label_box(d, (260, 830), "SIDESLIP", 22, 220, textfill=BLUE)
    arrow(d, (500, 550), (500, 330), GOLD, 10, 26)
    arrow(d, (1100, 520), (1100, 390), GREY, 8, 22)
    label_box(d, (500, 290), "LOWER WING\nMORE EFFECTIVE AoA / LIFT", 21, 360)
    label_box(d, (1100, 330), "UPPER WING\nLESS LIFT", 21, 300, textfill=GREY)
    footer(d, "In a sideslip, dihedral creates a restoring rolling moment toward wings level.")
    save(im, "dihedral-lateral-stability-v4")


def vertical_fin():
    im, d = base("Directional Stability and the Vertical Fin")
    d.polygon([(300, 560), (1080, 560), (1240, 600), (1080, 640), (300, 640), (190, 600)], fill=PALE, outline=NAVY)
    d.polygon([(1000, 560), (1120, 320), (1190, 330), (1160, 575)], fill=PALE, outline=NAVY)
    d.ellipse((670, 585, 700, 615), fill=GOLD)
    label_box(d, (685, 500), "CG", 21, 100)
    arrow(d, (1450, 380), (1180, 500), BLUE, 9, 24)
    label_box(d, (1330, 320), "SIDE GUST / YAW", 22, 260, textfill=BLUE)
    d.arc((600, 670, 1080, 950), start=200, end=330, fill=GOLD, width=9)
    label_box(d, (1010, 800), "WEATHERCOCK\nRESTORING MOMENT", 22, 300)
    footer(d, "Keel/fin area behind the CG strengthens directional stability about the normal axis.")
    save(im, "vertical-fin-directional-stability-v4")


def dutch_roll():
    im, d = base("Dutch Roll")
    d.line((250, 600, 1350, 600), fill=LIGHT, width=4)
    pts = [(260 + i * 7.5, 600 + 110 * math.sin(i / 10)) for i in range(140)]
    d.line(pts, fill=BLUE, width=7)
    for x in [450, 750, 1050]:
        d.line((x, 500, x + 80, 700), fill=GOLD, width=7)
    label_box(d, (800, 350), "COUPLED YAW + ROLL OSCILLATION", 27, 560)
    footer(d, "Dutch roll is a coupled lateral-directional oscillation involving both yaw and roll.")
    save(im, "dutch-roll-v4")


def trim_tab():
    im, d = base("Trim Tab Principle")
    d.line((280, 560, 1150, 560), fill=NAVY, width=24)
    d.line((1030, 560, 1330, 650), fill=GOLD, width=18)
    label_box(d, (660, 410), "MAIN CONTROL SURFACE", 25, 380)
    label_box(d, (1260, 730), "TRIM TAB", 25, 220)
    arrow(d, (1260, 790), (1260, 860), BLUE, 8, 22)
    footer(d, "The trim tab's aerodynamic force holds the main surface at the trimmed position, removing sustained pilot force.")
    save(im, "trim-tab-v4")


def balance_tab():
    im, d = base("Balance Tab Movement")
    d.line((260, 520, 1120, 620), fill=NAVY, width=24)
    d.line((1000, 605, 1330, 480), fill=GOLD, width=18)
    arrow(d, (600, 380), (600, 505), BLUE, 8, 22)
    label_box(d, (600, 320), "MAIN SURFACE DOWN", 23, 300)
    arrow(d, (1230, 710), (1230, 520), GOLD, 8, 22)
    label_box(d, (1230, 760), "TAB MOVES OPPOSITE", 23, 330)
    footer(d, "A balance tab moves opposite to the main control surface so its aerodynamic force assists the pilot.")
    save(im, "balance-tab-v4")


def anti_servo():
    im, d = base("Anti-Servo / Anti-Balance Tab")
    d.line((260, 520, 1120, 620), fill=NAVY, width=24)
    d.line((1000, 605, 1330, 690), fill=GOLD, width=18)
    arrow(d, (600, 380), (600, 505), BLUE, 8, 22)
    label_box(d, (600, 320), "STABILATOR DOWN", 23, 300)
    arrow(d, (1230, 520), (1230, 675), GOLD, 8, 22)
    label_box(d, (1230, 770), "TAB MOVES SAME DIRECTION", 23, 390)
    footer(d, "The anti-servo tab moves with the stabilator, increasing control force and control feel.")
    save(im, "anti-servo-tab-v4")


def mass_balance_flutter():
    im, d = base("Mass Balance and Flutter")
    d.line((760, 330, 760, 800), fill=BLUE, width=6)
    d.line((760, 560, 1370, 560), fill=NAVY, width=24)
    d.ellipse((560, 500, 680, 620), fill=GOLD)
    label_box(d, (760, 285), "HINGE LINE", 23, 220)
    label_box(d, (620, 690), "MASS AHEAD OF HINGE", 23, 330)
    pts = [(900 + i * 7, 780 - 70 * math.sin(i / 4) * (i / 60)) for i in range(60)]
    d.line(pts, fill=RED, width=6)
    label_box(d, (1190, 860), "FLUTTER = SELF-EXCITED OSCILLATION", 21, 470, textfill=RED)
    footer(d, "Mass balancing helps reduce the tendency of a control surface to flutter.")
    save(im, "mass-balance-flutter-v4")


def horn_balance():
    im, d = base("Aerodynamic / Horn Balance")
    d.line((650, 340, 650, 800), fill=BLUE, width=6)
    d.polygon([(650, 430), (1350, 520), (1350, 650), (650, 580)], fill=PALE, outline=NAVY)
    d.polygon([(520, 390), (730, 430), (690, 540), (530, 510)], fill=WHITE, outline=GOLD)
    label_box(d, (650, 300), "HINGE LINE", 23, 230)
    label_box(d, (500, 620), "AREA AHEAD OF HINGE", 23, 350)
    footer(d, "Aerodynamic area ahead of the hinge creates a moment that reduces pilot control force.")
    save(im, "horn-balance-v4")


def bank_load():
    im, d = base("Bank Angle and Load Factor")
    ox, oy, xe, yt = 300, 810, 1320, 310
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pts = []
    for deg in range(76):
        n = 1 / max(math.cos(math.radians(deg)), 0.15)
        x = ox + deg / 75 * (xe - ox - 60)
        y = oy - min((n - 1) * 160, 440)
        pts.append((x, y))
    d.line(pts, fill=GOLD, width=8)
    x60 = ox + 60 / 75 * (xe - ox - 60)
    y60 = oy - 160
    d.line((x60, y60, x60, oy), fill=BLUE, width=4)
    d.ellipse((x60 - 12, y60 - 12, x60 + 12, y60 + 12), fill=RED)
    label_box(d, (x60, y60 - 70), "60° = 2 G", 23, 220, textfill=RED)
    label_box(d, (820, 860), "BANK ANGLE", 23, 240, textfill=GREY)
    label_box(d, (180, 520), "LOAD FACTOR", 23, 240, textfill=GREY)
    footer(d, "In a coordinated level turn, load factor n = 1 / cos(bank angle).")
    save(im, "bank-angle-load-factor-v4")


def turn_lift():
    im, d = base("Lift Components in a Level Turn")
    o = (760, 630)
    arrow(d, o, (1000, 360), GOLD, 11, 28)
    label_box(d, (1070, 330), "TOTAL LIFT", 24, 240)
    arrow(d, o, (760, 360), BLUE, 10, 26)
    label_box(d, (650, 330), "VERTICAL COMPONENT", 22, 320, textfill=BLUE)
    arrow(d, o, (1000, 630), GOLD, 10, 26)
    label_box(d, (1120, 630), "HORIZONTAL COMPONENT\nCENTRIPETAL FORCE", 22, 380)
    arrow(d, o, (760, 860), GREY, 10, 26)
    label_box(d, (880, 850), "WEIGHT", 22, 220, textfill=GREY)
    footer(d, "The vertical component supports weight; the horizontal component turns the aircraft.")
    save(im, "turn-lift-components-v4")


def slip_skid():
    im, d = base("Balanced, Slipping and Skidding Turns")
    for title, x, off in [("BALANCED", 380, 0), ("SLIP", 800, -100), ("SKID", 1220, 100)]:
        d.arc((x - 180, 420, x + 180, 760), start=200, end=340, fill=NAVY, width=10)
        bx = x + off
        d.ellipse((bx - 28, 572, bx + 28, 628), fill=GOLD)
        label_box(d, (x, 350), title, 24, 220, textfill=BLUE if title == "BALANCED" else NAVY)
    footer(d, "Ball centred = coordinated. In a left turn, ball left = slip and ball right = skid.")
    save(im, "slip-skid-indicator-v4")


def stall_speed_load():
    im, d = base("Stall Speed and Load Factor")
    ox, oy, xe, yt = 300, 810, 1320, 310
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pts = []
    for i in range(101):
        n = 1 + i * 0.03
        t = (n - 1) / 3
        x = ox + t * (xe - ox - 60)
        y = oy - (math.sqrt(n) - 1) * 340
        pts.append((x, y))
    d.line(pts, fill=GOLD, width=8)
    label_box(d, (930, 390), "VS,new = VS,1g × √n", 29, 450)
    footer(d, "For constant weight and configuration, stall speed increases with the square root of load factor.")
    save(im, "stall-speed-load-factor-v4")


def critical_stall():
    im, d = base("Critical Angle of Attack and Stall")
    pts = airfoil_poly(180, 590, 720, 540, 0.05, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    for y in [420, 460, 500]:
        arrow(d, (180, y), (690, y - 30), BLUE, 4, 14)
    label_box(d, (450, 340), "BELOW CRITICAL AoA\nFLOW MOSTLY ATTACHED", 21, 360, textfill=BLUE)
    pts2 = airfoil_poly(900, 640, 1400, 510, 0.05, 0.08)
    d.polygon(pts2, fill=PALE, outline=NAVY)
    for k, y in enumerate([410, 455, 500]):
        path = [(900 + j * 7, y - 35 * math.sin(j / 7) - k * 8) for j in range(70)]
        d.line(path, fill=RED, width=4)
    label_box(d, (1160, 340), "CRITICAL AoA EXCEEDED\nSEPARATION GROWS", 21, 370, textfill=RED)
    footer(d, "A stall occurs because the critical angle of attack is exceeded — not because of one particular airspeed.")
    save(im, "critical-angle-stall-v4")


def stall_warning():
    im, d = base("Approaching the Stall")
    pts = airfoil_poly(250, 610, 1320, 550, 0.05, 0.08)
    d.polygon(pts, fill=PALE, outline=NAVY)
    for y in [415, 455]:
        path = [(700 + j * 10, y - 30 * math.sin(j / 5)) for j in range(55)]
        d.line(path, fill=RED, width=5)
    label_box(d, (1020, 345), "BUFFET / SEPARATION", 23, 330, textfill=RED)
    label_box(d, (420, 350), "STALL WARNING\nACTIVATES BEFORE FULL STALL", 22, 390)
    label_box(d, (800, 780), "CONTROL EFFECTIVENESS DECREASES AS AIRFLOW OVER THE CONTROLS WEAKENS", 21, 880, textfill=GREY)
    save(im, "stall-warning-v4")


def root_stall():
    im, d = base("Root-First Stall Progression")
    d.polygon([(180, 500), (800, 420), (1420, 500), (1200, 650), (400, 650)], fill=PALE, outline=NAVY)
    d.rectangle((640, 450, 960, 650), fill="#fee2e2", outline=RED, width=3)
    label_box(d, (800, 350), "ROOT STALLS FIRST", 25, 320, textfill=RED)
    label_box(d, (300, 730), "TIP STILL FLYING", 22, 290, textfill=BLUE)
    label_box(d, (1290, 730), "AILERON EFFECT RETAINED", 22, 340, textfill=BLUE)
    footer(d, "Washout reduces incidence toward the tip so the root reaches the critical angle first.")
    save(im, "root-first-stall-washout-v4")


def spin_autorotation():
    im, d = base("Spin Autorotation")
    d.line((420, 490, 1180, 650), fill=NAVY, width=24)
    d.arc((500, 300, 1100, 860), start=300, end=110, fill=GOLD, width=10)
    arrow(d, (1070, 430), (1130, 500), GOLD, 8, 24)
    label_box(d, (430, 390), "INNER WING\nMORE DEEPLY STALLED", 22, 350, textfill=RED)
    label_box(d, (1160, 760), "OUTER WING\nLESS STALLED / FASTER", 22, 330, textfill=BLUE)
    footer(d, "A spin requires a stall plus yaw. The inner wing is more deeply stalled, sustaining autorotation.")
    save(im, "spin-autorotation-v4")


def spin_recovery():
    im, d = base("Spin Recovery — Aerodynamic Principle")
    xs = [250, 620, 990, 1360]
    steps = [("1  POWER", "AS APPROVED"), ("2  OPPOSITE RUDDER", "STOP YAW"), ("3  REDUCE AoA", "UNSTALL WINGS"), ("4  RECOVER", "SMOOTHLY")]
    for i, (a, b) in enumerate(steps):
        label_box(d, (xs[i], 520), a + "\n" + b, 22, 300)
        if i < 3:
            arrow(d, (xs[i] + 165, 520), (xs[i + 1] - 165, 520), GOLD, 7, 20)
    footer(d, "Always use the aircraft's approved recovery procedure; aerodynamically, stop yaw and reduce angle of attack.")
    save(im, "spin-recovery-v4")


def airspeed_chain():
    im, d = base("IAS → CAS/RAS → TAS")
    xs = [320, 800, 1280]
    labels = [("IAS", "INSTRUMENT READING"), ("CAS / RAS", "IAS CORRECTED FOR\nINSTRUMENT + POSITION ERROR"), ("TAS", "CAS/RAS CORRECTED FOR\nDENSITY / TEMP-ALTITUDE")]
    for x, (a, b) in zip(xs, labels):
        label_box(d, (x, 520), a + "\n" + b, 23, 380, textfill=BLUE if a == "TAS" else NAVY)
    arrow(d, (520, 520), (600, 520), GOLD, 8, 22)
    arrow(d, (1000, 520), (1080, 520), GOLD, 8, 22)
    footer(d, "True airspeed is the aircraft's speed relative to the surrounding air mass.")
    save(im, "airspeed-chain-v4")


def v_speeds():
    im, d = base("Common V-Speeds")
    d.line((230, 560, 1370, 560), fill=NAVY, width=14)
    marks = [(340, "VFE", "MAX FLAP EXTENDED", BLUE), (560, "VA", "MANOEUVRING", GOLD), (800, "VNO", "MAX STRUCTURAL CRUISE", GREEN), (1040, "VNE", "NEVER EXCEED", RED), (1280, "VLO", "GEAR OPERATING", GREY)]
    for x, code, desc, c in marks:
        d.line((x, 520, x, 600), fill=c, width=10)
        label_box(d, (x, 420), code, 24, 130, textfill=c)
        text_center(d, (x, 680), desc, 17, GREY, True)
    footer(d, "Exact V-speed values are aircraft-specific and must come from approved aircraft data.")
    save(im, "v-speeds-v4")


def va_envelope():
    im, d = base("Design Manoeuvring Speed VA")
    ox, oy, xe, yt = 310, 810, 1320, 300
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    d.line((350, 760, 820, 430), fill=BLUE, width=8)
    d.line((820, 430, 1280, 430), fill=RED, width=8)
    d.ellipse((805, 415, 835, 445), fill=GOLD)
    label_box(d, (820, 360), "VA INTERSECTION", 23, 280)
    label_box(d, (1120, 365), "POSITIVE LIMIT LOAD", 21, 300, textfill=RED)
    label_box(d, (540, 650), "STALL BOUNDARY", 21, 260, textfill=BLUE)
    footer(d, "At or below VA, a full abrupt single-axis input is intended to stall the wing before exceeding the positive limit load.")
    save(im, "va-envelope-v4")


def isa():
    im, d = base("International Standard Atmosphere")
    d.line((760, 800, 760, 320), fill=NAVY, width=8)
    arrow(d, (760, 760), (760, 370), GOLD, 8, 22)
    label_box(d, (500, 720), "MSL TEMP\n+15°C", 24, 260)
    label_box(d, (1050, 720), "MSL PRESSURE\n1013.25 hPa", 24, 300)
    label_box(d, (500, 430), "MSL DENSITY\n1.225 kg/m³", 24, 280)
    label_box(d, (1050, 430), "LAPSE RATE\n≈1.98°C / 1000 ft", 24, 320)
    footer(d, "ISA provides standard reference values used for aircraft performance and aerodynamic calculations.")
    save(im, "isa-v4")


def humidity_density():
    im, d = base("Humidity and Air Density")
    d.rounded_rectangle((180, 360, 700, 720), radius=20, fill=PALE, outline=NAVY, width=4)
    d.rounded_rectangle((900, 360, 1420, 720), radius=20, fill=PALE, outline=NAVY, width=4)
    text_center(d, (440, 315), "DRY AIR", 27, NAVY, True)
    text_center(d, (1160, 315), "HUMID AIR", 27, NAVY, True)
    for x in range(280, 650, 100):
        for y in range(450, 670, 100):
            d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=BLUE)
    for x in range(1000, 1370, 100):
        for y in range(450, 670, 100):
            d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=GOLD)
    label_box(d, (440, 800), "MORE DENSE", 24, 260, textfill=BLUE)
    label_box(d, (1160, 800), "LESS DENSE", 24, 260, textfill=RED)
    footer(d, "Water-vapour molecules are lighter than the nitrogen/oxygen molecules they displace, so humid air is less dense.")
    save(im, "humidity-density-v4")


def pressure_temperature_density():
    im, d = base("Pressure, Temperature and Density")
    label_box(d, (430, 500), "PRESSURE ↑\nDENSITY ↑\n(if temperature constant)", 26, 420)
    label_box(d, (1170, 500), "TEMPERATURE ↑\nDENSITY ↓\n(if pressure constant)", 26, 430)
    label_box(d, (800, 740), "ρ ∝ P / T", 38, 320, textfill=BLUE)
    footer(d, "In the gas relationship, temperature must be absolute temperature.")
    save(im, "pressure-temperature-density-v4")


def dry_air():
    im, d = base("Composition of Dry Air")
    x0, y0, total, h = 220, 500, 1160, 140
    segs = [("NITROGEN 78%", 0.78, BLUE), ("OXYGEN 21%", 0.21, GOLD), ("OTHER ≈1%", 0.01, GREY)]
    x = x0
    for name, p, c in segs:
        w = total * p
        d.rectangle((x, y0, x + w, y0 + h), fill=c)
        if p > 0.05:
            text_center(d, (x + w / 2, y0 + h / 2), name, 27, WHITE, True)
        x += w
    label_box(d, (1200, 760), "ARGON ≈0.95%\nCO₂ ≈0.05%", 22, 300, textfill=GREY)
    footer(d, "Dry air is approximately 78% nitrogen, 21% oxygen and about 1% other gases.")
    save(im, "dry-air-composition-v4")


def static_pressure():
    im, d = base("Static Pressure")
    d.ellipse((560, 360, 1040, 840), outline=NAVY, width=6)
    for ang in range(0, 360, 45):
        r = math.radians(ang)
        p1 = (800 + 170 * math.cos(r), 600 + 170 * math.sin(r))
        p2 = (800 + 270 * math.cos(r), 600 + 270 * math.sin(r))
        arrow(d, p1, p2, BLUE, 6, 18)
    label_box(d, (800, 600), "OBJECT IN\nSTILL AIR", 27, 260)
    footer(d, "Static pressure is the ambient atmospheric pressure acting in all directions.")
    save(im, "static-pressure-v4")


def centre_gravity():
    im, d = base("Centre of Gravity")
    d.polygon([(350, 560), (1050, 560), (1200, 600), (1050, 640), (350, 640), (220, 600)], fill=PALE, outline=NAVY)
    cg = (760, 600)
    d.ellipse((746, 586, 774, 614), fill=GOLD)
    arrow(d, cg, (760, 850), GREY, 11, 28)
    label_box(d, (760, 500), "CENTRE OF GRAVITY", 26, 360)
    label_box(d, (850, 840), "TOTAL WEIGHT ACTS HERE", 23, 350, textfill=GREY)
    footer(d, "The centre of gravity is the point through which the aircraft's total weight is considered to act.")
    save(im, "centre-of-gravity-v4")


def anhedral():
    im, d = base("Anhedral")
    d.line((800, 560, 350, 720), fill=NAVY, width=20)
    d.line((800, 560, 1250, 720), fill=NAVY, width=20)
    label_box(d, (800, 370), "WINGS SLOPE DOWNWARD\nFROM ROOT TO TIP", 27, 520)
    footer(d, "Anhedral reduces the natural dihedral effect and therefore reduces lateral stability.")
    save(im, "anhedral-v4")


def main():
    generators = [
        angle_of_attack, relative_airflow, aerofoil_geometry, lift_drag_directions, lift_pressure,
        centre_pressure, centre_pressure_shift, lift_speed_squared, boundary_layer, wing_polar,
        newtons_laws, venturi, dynamic_pressure, propeller_torque, p_factor, aircraft_axes,
        control_effects, adverse_yaw, differential_ailerons, frise_aileron, four_forces, cg_cp_pitch,
        climb_forces, vx_vy, descent_power, drag_curves, induced_drag, skin_friction, aspect_ratio,
        washout, flap_effects, fowler_flap, flaps_glide, wind_glide, flap_cp, leading_edge_slot,
        flap_vs_no_flap, stability, cg_stability, longitudinal_dihedral, dihedral, vertical_fin,
        dutch_roll, trim_tab, balance_tab, anti_servo, mass_balance_flutter, horn_balance, bank_load,
        turn_lift, slip_skid, stall_speed_load, critical_stall, stall_warning, root_stall,
        spin_autorotation, spin_recovery, airspeed_chain, v_speeds, va_envelope, isa,
        humidity_density, pressure_temperature_density, dry_air, static_pressure, centre_gravity, anhedral,
    ]
    for generator in generators:
        generator()
    print(f"Generated {len(generators)} POF static assets in {OUT}")


if __name__ == "__main__":
    main()
