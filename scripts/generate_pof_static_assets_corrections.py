from generate_pof_static_assets import *


def angle_of_attack_v8():
    im, d = base("Angle of Attack")
    arrow(d, (170, 340), (470, 340), GREY, 10, 28)
    label_box(d, (320, 285), "AIRCRAFT FLIGHT PATH", 22, 340, textfill=GREY)
    LE, TE = (500, 625), (1320, 515)
    pts = airfoil_poly(*LE, *TE, 0.06, 0.095)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line((*LE, *TE), fill=GOLD, width=7)
    arrow(d, TE, (310, 515), BLUE, 9, 26)
    label_box(d, (620, 445), "RELATIVE AIRFLOW", 23, 310, textfill=BLUE)
    d.arc((1110, 445, 1370, 705), start=170, end=188, fill=GOLD, width=10)
    label_box(d, (1170, 650), "α  ANGLE OF ATTACK", 26, 340)
    callout(d, (515, 610), (350, 760), "LEADING EDGE", 22, 240)
    callout(d, (1310, 520), (1360, 760), "TRAILING EDGE", 22, 250)
    d.line((930, 355, 1030, 355), fill=GOLD, width=7)
    label_box(d, (1160, 355), "CHORD LINE", 22, 220)
    footer(d, "Angle of attack is the angle between the aerofoil chord line and the relative airflow.")
    save(im, "angle-of-attack-v8")


def centre_pressure_shift_v5():
    im, d = base("Centre of Pressure Shift")
    for y, cp_x, title, col in [(445, 1010, "LOWER AoA", GREY), (690, 790, "HIGHER AoA", BLUE)]:
        pts = airfoil_poly(300, y, 1320, y - 15, 0.055, 0.075)
        d.polygon(pts, fill=PALE, outline=NAVY)
        d.ellipse((cp_x - 13, y - 13, cp_x + 13, y + 13), fill=GOLD)
        label_box(d, (205, y), title, 22, 230, textfill=col)
        label_box(d, (cp_x, y - 80), "CP", 21, 90, textfill=BLUE)
    arrow(d, (1000, 570), (815, 570), GOLD, 9, 25)
    label_box(d, (910, 615), "CP MOVES FORWARD\nAS AoA INCREASES", 22, 330)
    footer(d, "For a conventional cambered aerofoil in the normal operating range, increasing AoA moves CP forward.")
    save(im, "centre-pressure-shift-v5")


def drag_curves_v6():
    im, d = base("Induced, Parasite and Total Drag")
    ox, oy, xe, yt = 300, 790, 1360, 300
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    xs, induced, parasite, total = [], [], [], []
    for i in range(151):
        v = 0.38 + i / 150 * 1.75
        x = ox + 80 + i / 150 * (xe - ox - 130)
        di = 260 / (v * v)
        dp = 72 * (v * v)
        xs.append(x)
        induced.append(di)
        parasite.append(dp)
        total.append(di + dp)

    def Y(val):
        val = min(val, 740)
        return oy - 80 - (val - 50) / (740 - 50) * (oy - yt - 120)

    pts_i = [(x, Y(v)) for x, v in zip(xs, induced)]
    pts_p = [(x, Y(v)) for x, v in zip(xs, parasite)]
    pts_t = [(x, Y(v)) for x, v in zip(xs, total)]
    d.line(pts_i, fill=BLUE, width=7)
    d.line(pts_p, fill=GOLD, width=7)
    d.line(pts_t, fill=NAVY, width=9)
    idx = min(range(len(total)), key=lambda i: total[i])
    pmin = pts_t[idx]
    d.ellipse((pmin[0] - 13, pmin[1] - 13, pmin[0] + 13, pmin[1] + 13), fill=RED)
    label_box(d, (470, 345), "INDUCED DRAG", 22, 250, textfill=BLUE)
    label_box(d, (1210, 390), "PARASITE DRAG", 22, 270, textfill=GOLD)
    label_box(d, (1030, 545), "TOTAL DRAG", 22, 230)
    d.line((pmin[0], pmin[1] + 18, pmin[0], oy), fill=RED, width=3)
    label_box(d, (pmin[0], 845), "VMD / BEST L/D SPEED", 20, 310, textfill=RED)
    label_box(d, (1250, 845), "AIRSPEED →", 21, 210, textfill=GREY)
    label_box(d, (180, 530), "DRAG", 22, 150, textfill=GREY)
    footer(d, "Induced drag decreases with speed; parasite drag increases. Their sum gives the total-drag curve.")
    save(im, "drag-curves-v6")


def lift_drag_v5():
    im, d = base("Lift and Drag Directions")
    arrow(d, (1340, 720), (260, 720), BLUE, 10, 30)
    label_box(d, (800, 795), "RELATIVE AIRFLOW", 24, 330, textfill=BLUE)
    o = (800, 590)
    d.ellipse((782, 572, 818, 608), fill=NAVY)
    arrow(d, o, (800, 330), GOLD, 11, 30)
    label_box(d, (800, 285), "LIFT\nPERPENDICULAR TO RELATIVE AIRFLOW", 24, 470)
    arrow(d, o, (500, 590), GREY, 10, 28)
    label_box(d, (375, 590), "DRAG\nPARALLEL TO RELATIVE AIRFLOW", 22, 380, textfill=GREY)
    arrow(d, (860, 440), (1200, 440), NAVY, 8, 24)
    label_box(d, (1200, 385), "AIRCRAFT MOTION", 21, 280)
    footer(d, "Lift acts perpendicular to relative airflow; drag acts parallel to relative airflow and opposite the aircraft's motion.")
    save(im, "lift-drag-directions-v5")


def lift_pressure_v5():
    im, d = base("Pressure Distribution Produces Lift")
    pts = airfoil_poly(280, 610, 1280, 590, 0.075, 0.10)
    d.polygon(pts, fill=PALE, outline=NAVY)
    for x in range(450, 1170, 145):
        arrow(d, (x, 370), (x, 450), BLUE, 5, 16)
    for x in range(450, 1170, 145):
        arrow(d, (x, 810), (x, 665), GOLD, 8, 22)
    label_box(d, (800, 315), "LOWER STATIC PRESSURE ABOVE", 24, 470, textfill=BLUE)
    label_box(d, (800, 855), "HIGHER STATIC PRESSURE BELOW", 24, 500)
    arrow(d, (1380, 620), (1380, 335), GOLD, 12, 32)
    label_box(d, (1380, 290), "NET LIFT", 25, 220)
    footer(d, "The larger lower-surface pressure contribution and lower pressure above produce an upward resultant.")
    save(im, "lift-pressure-distribution-v5")


def boundary_layer_v5():
    im, d = base("Boundary Layer and Transition")
    pts = airfoil_poly(180, 715, 1400, 680, 0.05, 0.065)
    d.polygon(pts, fill=PALE, outline=NAVY)
    d.line([(210, 675), (350, 615), (500, 585), (650, 575)], fill=BLUE, width=4)
    d.line([(210, 662), (350, 598), (500, 565), (650, 552)], fill=BLUE, width=3)
    d.line((675, 530, 675, 700), fill=GOLD, width=5)
    d.line([(690, 550), (820, 520), (950, 525), (1080, 545), (1210, 575), (1350, 620)], fill=GREY, width=5)
    d.line([(690, 525), (820, 490), (950, 492), (1080, 510), (1210, 540), (1350, 585)], fill=GREY, width=3)
    label_box(d, (420, 420), "LAMINAR BOUNDARY LAYER\nTHIN / ORDERLY", 22, 380, textfill=BLUE)
    label_box(d, (675, 395), "TRANSITION", 22, 230)
    label_box(d, (1100, 420), "TURBULENT BOUNDARY LAYER\nTHICKER / MORE MIXING", 22, 410, textfill=GREY)
    footer(d, "The boundary layer starts at the surface, grows downstream and may transition from laminar to turbulent flow.")
    save(im, "boundary-layer-transition-v5")


def static_pressure_v7():
    im, d = base("Static Pressure")
    cx, cy, r = 800, 575, 190
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=NAVY, width=6)
    for ang in range(0, 360, 45):
        rr = math.radians(ang)
        p1 = (cx + (r + 95) * math.cos(rr), cy + (r + 95) * math.sin(rr))
        p2 = (cx + r * math.cos(rr), cy + r * math.sin(rr))
        arrow(d, p1, p2, BLUE, 6, 18)
    label_box(d, (800, 575), "OBJECT IN\nSTILL AIR", 26, 260)
    label_box(d, (1190, 320), "AMBIENT STATIC PRESSURE\nACTS NORMAL TO THE SURFACE", 22, 400, textfill=BLUE)
    footer(d, "Static pressure acts normal to surfaces from all directions in the surrounding still air.")
    save(im, "static-pressure-v7")


def steady_climb_v6():
    im, d = base("Forces in a Steady Climb")
    p0, p1 = (300, 760), (1300, 440)
    d.line((p0, p1), fill=LIGHT, width=5)
    o = (800, 600)
    d.line((650, 650, 950, 555), fill=NAVY, width=18)
    dx, dy = 1000, -320
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    nx, ny = uy, -ux
    arrow(d, o, (o[0] + 330 * ux, o[1] + 330 * uy), GOLD, 10, 28)
    label_box(d, (1160, 455), "THRUST", 22, 190)
    arrow(d, o, (o[0] - 300 * ux, o[1] - 300 * uy), BLUE, 10, 28)
    label_box(d, (480, 705), "DRAG", 22, 170, textfill=BLUE)
    arrow(d, o, (o[0] + 280 * nx, o[1] + 280 * ny), GOLD, 10, 28)
    label_box(d, (650, 310), "LIFT\nPERPENDICULAR TO FLIGHT PATH", 22, 390)
    arrow(d, o, (800, 820), GREY, 10, 28)
    label_box(d, (960, 760), "WEIGHT\nVERTICAL", 22, 220, textfill=GREY)
    footer(d, "In a steady climb, thrust and drag act along the flight path; lift is perpendicular to it and weight is vertical.")
    save(im, "steady-climb-forces-v6")


def vx_vy_v7():
    im, d = base("Best Angle and Best Rate of Climb")
    d.line((220, 830, 1400, 830), fill=NAVY, width=5)
    d.rectangle((1240, 470, 1300, 830), fill=GREY)
    start, vx_end, vy_end = (270, 810), (1200, 500), (1200, 620)
    d.line((*start, *vx_end), fill=GOLD, width=9)
    d.line((*start, *vy_end), fill=BLUE, width=9)
    label_box(d, (850, 410), "VX — BEST ANGLE\nMAX HEIGHT GAIN / HORIZONTAL DISTANCE", 22, 500, textfill=GOLD)
    label_box(d, (780, 745), "VY — BEST RATE\nMAX HEIGHT GAIN / TIME", 21, 390, textfill=BLUE)
    label_box(d, (1270, 430), "OBSTACLE", 21, 180, textfill=GREY)
    footer(d, "VX gives the steepest climb angle; VY gives the greatest rate of climb.")
    save(im, "vx-vy-v7")


def wingtip_vortices_v6():
    im, d = base("Wingtip Vortices and Induced Drag")
    d.line((320, 500, 1280, 500), fill=NAVY, width=28)
    label_box(d, (800, 385), "LOW PRESSURE ABOVE", 23, 340, textfill=BLUE)
    label_box(d, (800, 560), "HIGH PRESSURE BELOW", 23, 360)
    arrow(d, (760, 640), (390, 640), GOLD, 7, 20)
    arrow(d, (840, 640), (1210, 640), GOLD, 7, 20)
    label_box(d, (800, 705), "LOWER-SURFACE FLOW MOVES OUTWARD TOWARD THE TIPS", 19, 610)
    d.arc((120, 390, 470, 750), start=240, end=570, fill=BLUE, width=8)
    arrow(d, (255, 432), (315, 400), BLUE, 6, 18)
    d.arc((1130, 390, 1480, 750), start=-30, end=300, fill=BLUE, width=8)
    arrow(d, (1345, 415), (1290, 390), BLUE, 6, 18)
    for x in (650, 800, 950):
        arrow(d, (x, 735), (x, 820), GREY, 5, 17)
    label_box(d, (1180, 805), "DOWNWASH", 20, 200, textfill=GREY)
    footer(d, "Pressure flows outward below the wing, curls around the tips, and forms trailing vortices and downwash.")
    save(im, "wingtip-vortices-induced-drag-v6")


def stall_speed_load_v6():
    im, d = base("Stall Speed and Load Factor")
    ox, oy, xe, yt = 300, 820, 1340, 320
    d.line((ox, oy, xe, oy), fill=NAVY, width=5)
    d.line((ox, oy, ox, yt), fill=NAVY, width=5)
    pts = []
    for i in range(101):
        n = 1 + 3 * i / 100
        x = ox + 80 + (n - 1) / 3 * (xe - ox - 150)
        ratio = math.sqrt(n)
        y = oy - 100 - (ratio - 1) * (oy - yt - 150)
        pts.append((x, y))
    d.line(pts, fill=GOLD, width=8)
    for n, lab in [(1, "1 G = 1.00 VS"), (4, "4 G = 2.00 VS")]:
        idx = round((n - 1) / 3 * 100)
        p = pts[idx]
        d.ellipse((p[0] - 11, p[1] - 11, p[0] + 11, p[1] + 11), fill=BLUE)
        pos = (p[0] + 30, p[1] - 70) if n == 1 else (p[0] - 20, p[1] - 80)
        label_box(d, pos, lab, 20, 220, textfill=BLUE)
    label_box(d, (600, 350), "VS,n = VS,1g × √n", 29, 420)
    label_box(d, (820, 875), "LOAD FACTOR n", 22, 260, textfill=GREY)
    label_box(d, (180, 560), "STALL SPEED", 22, 230, textfill=GREY)
    footer(d, "At constant weight and configuration, stall speed varies with the square root of load factor.")
    save(im, "stall-speed-load-factor-v6")


def spin_autorotation_v5():
    im, d = base("Spin Autorotation")
    d.line((430, 500, 1170, 660), fill=NAVY, width=30)
    d.line((760, 390, 850, 760), fill=NAVY, width=22)
    callout(d, (520, 520), (350, 380), "INNER WING\nMORE DEEPLY STALLED", 21, 330)
    callout(d, (1080, 640), (1260, 760), "OUTER WING\nLESS DEEPLY STALLED", 21, 340)
    d.arc((520, 300, 1080, 860), start=280, end=80, fill=GOLD, width=10)
    arrow(d, (1035, 430), (1080, 500), GOLD, 8, 22)
    label_box(d, (800, 815), "AUTOROTATION", 24, 260)
    footer(d, "A spin requires a stall plus yaw; the inner wing is more deeply stalled, sustaining autorotation.")
    save(im, "spin-autorotation-v5")


def trim_tab_v5():
    im, d = base("Trim Tab Principle")
    d.line((260, 560, 1120, 560), fill=NAVY, width=24)
    d.line((1000, 560, 1340, 650), fill=GOLD, width=18)
    label_box(d, (660, 410), "MAIN CONTROL SURFACE", 25, 380)
    label_box(d, (1260, 730), "TRIM TAB", 25, 220)
    callout(d, (1210, 615), (980, 770), "TAB SET RELATIVE TO\nMAIN SURFACE", 21, 340)
    footer(d, "The trim tab is set relative to the main surface so aerodynamic force removes a sustained pilot control force.")
    save(im, "trim-tab-v5")


def wind_glide_v7():
    im, d = base("Wind Effect on Glide Over the Ground")
    start, ground_y = (260, 360), 830
    head_end, tail_end = (820, ground_y), (1330, ground_y)
    d.line((*start, *head_end), fill=GOLD, width=9)
    d.line((*start, *tail_end), fill=BLUE, width=9)
    arrow(d, (650, 290), (430, 290), GOLD, 8, 22)
    label_box(d, (540, 235), "HEADWIND", 22, 220, textfill=GOLD)
    arrow(d, (900, 290), (1120, 290), BLUE, 8, 22)
    label_box(d, (1010, 235), "TAILWIND", 22, 220, textfill=BLUE)
    label_box(d, (510, 760), "HEADWIND\nSHORTER DISTANCE\nSTEEPER OVER GROUND", 20, 330, textfill=GOLD)
    label_box(d, (1200, 690), "TAILWIND\nLONGER DISTANCE\nSHALLOWER OVER GROUND", 20, 360, textfill=BLUE)
    d.line((150, ground_y, 1450, ground_y), fill=NAVY, width=5)
    footer(d, "At the same glide airspeed/configuration, wind changes groundspeed and therefore the glide path over the ground.")
    save(im, "wind-glide-groundpath-v7")


def v_speeds_v5():
    im, d = base("Common V-Speeds")
    entries = [
        ("VFE", "MAXIMUM FLAP-EXTENDED SPEED", BLUE),
        ("VA", "DESIGN MANOEUVRING SPEED", GOLD),
        ("VNO", "MAXIMUM STRUCTURAL CRUISING SPEED", GREEN),
        ("VNE", "NEVER-EXCEED SPEED", RED),
        ("VLO", "MAXIMUM LANDING-GEAR OPERATING SPEED", GREY),
    ]
    y = 340
    for code, desc, color in entries:
        d.rounded_rectangle((330, y, 1270, y + 90), radius=10, fill=PALE, outline=LIGHT, width=2)
        d.rounded_rectangle((360, y + 15, 500, y + 75), radius=8, fill=WHITE, outline=color, width=3)
        text_center(d, (430, y + 45), code, 25, color, True)
        d.text((550, y + 31), desc, font=F(23, True), fill=NAVY)
        y += 105
    footer(d, "Exact V-speed values are aircraft-specific and must be taken from approved aircraft data.")
    save(im, "v-speeds-v5")


def main():
    angle_of_attack_v8()
    centre_pressure_shift_v5()
    drag_curves_v6()
    lift_drag_v5()
    lift_pressure_v5()
    boundary_layer_v5()
    static_pressure_v7()
    steady_climb_v6()
    vx_vy_v7()
    wingtip_vortices_v6()
    stall_speed_load_v6()
    spin_autorotation_v5()
    trim_tab_v5()
    wind_glide_v7()
    v_speeds_v5()
    print("Generated QA-corrected POF static assets")


if __name__ == "__main__":
    main()
