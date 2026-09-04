from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("public/explanation-images/principles-of-flight/refined-batch-11")
OUT.mkdir(parents=True, exist_ok=True)
W, H, S = 1600, 1050, 2
NAVY = "#0B1F33"
GOLD = "#C9942E"
WHITE = "#FFFFFF"
BG = "#F6F8FA"
INK = "#162A3D"
MUTED = "#5E6C7A"
LIGHT = "#E7ECF1"
PALE_GOLD = "#F6EBD2"
PALE_NAVY = "#E7EEF5"
RED = "#A84646"
GREEN = "#2F6E5A"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def sc(v): return int(round(v*S))
def pts(seq): return [(sc(x), sc(y)) for x,y in seq]
def font(sz, bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, sc(sz))
def new_canvas(title, subtitle):
    im = Image.new("RGB", (W*S, H*S), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((sc(70),sc(48),sc(1530),sc(54)), radius=sc(3), fill=GOLD)
    d.text((sc(76),sc(82)), title, font=font(44,True), fill=NAVY)
    d.text((sc(78),sc(142)), subtitle, font=font(21), fill=MUTED)
    return im,d
def box(d,b,fill=WHITE,outline=LIGHT,width=2,radius=22):
    d.rounded_rectangle(tuple(sc(v) for v in b), radius=sc(radius), fill=fill, outline=outline, width=sc(width))
def center_text(d,xy,text,fnt,fill=INK):
    bb=d.textbbox((0,0),text,font=fnt); d.text((sc(xy[0])-(bb[2]-bb[0])//2,sc(xy[1])-(bb[3]-bb[1])//2),text,font=fnt,fill=fill)
def arrow(d,a,b,fill=NAVY,width=7,head=20):
    x1,y1=map(sc,a); x2,y2=map(sc,b); d.line((x1,y1,x2,y2),fill=fill,width=sc(width))
    ang=math.atan2(y2-y1,x2-x1); h=sc(head)
    p1=(x2+h*math.cos(ang+math.pi*0.84),y2+h*math.sin(ang+math.pi*0.84)); p2=(x2+h*math.cos(ang-math.pi*0.84),y2+h*math.sin(ang-math.pi*0.84))
    d.polygon([(x2,y2),p1,p2],fill=fill)
def line(d,a,b,fill=NAVY,width=4): d.line((*map(sc,a),*map(sc,b)),fill=fill,width=sc(width))
def polyline(d,seq,fill=NAVY,width=5): d.line(pts(seq),fill=fill,width=sc(width),joint="curve")
def save_pair(im, stem):
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    im.save(OUT/f"{stem}-v1.png", optimize=True)
    im.save(OUT/f"{stem}-v1.webp", "WEBP", quality=92, method=6)

def airfoil_points(cx,cy,chord=470,thickness=0.12,camber=0.04,n=90,truncate=1.0):
    xs=[truncate*i/(n-1) for i in range(n)]; upper=[]; lower=[]
    for x in xs:
        yt=5*thickness*(0.2969*math.sqrt(max(x,1e-6))-0.1260*x-0.3516*x*x+0.2843*x**3-0.1015*x**4)
        cm=camber*math.sin(math.pi*x)
        upper.append((cx+(x-0.5)*chord,cy-(cm+yt)*chord)); lower.append((cx+(x-0.5)*chord,cy-(cm-yt)*chord))
    return upper+lower[::-1]

def draw_airfoil_with_flap(d,cx,cy,flap_down=False):
    chord=490
    main=airfoil_points(cx-18,cy,chord,0.12,0.04,80,0.77)
    d.polygon(pts(main),fill=WHITE,outline=NAVY)
    hinge=(cx-18+(.77-.5)*chord,cy)
    if not flap_down:
        flap=[(hinge[0]-4,cy-18),(cx-18+0.5*chord,cy-7),(cx-18+0.5*chord,cy+7),(hinge[0]-4,cy+18)]
    else:
        ang=math.radians(28); length=112
        ex=hinge[0]+length*math.cos(ang); ey=hinge[1]+length*math.sin(ang)
        flap=[(hinge[0]-5,cy-15),(ex,ey-5),(ex+6,ey+9),(hinge[0]-2,cy+18)]
    d.polygon(pts(flap),fill=PALE_GOLD if flap_down else WHITE,outline=GOLD if flap_down else NAVY)
    d.ellipse((sc(hinge[0]-5),sc(hinge[1]-5),sc(hinge[0]+5),sc(hinge[1]+5)),fill=GOLD)

# 1 — Trailing-edge flap: lift and drag
im,d=new_canvas("Trailing-Edge Flaps: More Lift, More Drag","Compare the same baseline angle of attack and airspeed with the flap retracted and extended.")
for b,t in [((70,210,775,865),"FLAP UP"),((825,210,1530,865),"FLAP DOWN")]:
    box(d,b); center_text(d,((b[0]+b[2])/2,252),t,font(25,True),NAVY if t=="FLAP UP" else GOLD)
# airflow baselines
for cx in (422,1177):
    for yy in (440,500,560): arrow(d,(cx-270,yy),(cx-85,yy),fill=MUTED,width=3,head=11)
    d.text((sc(cx-265),sc(385)),"Relative wind",font=font(16,True),fill=MUTED)
draw_airfoil_with_flap(d,422,520,False); draw_airfoil_with_flap(d,1177,520,True)
# lift and drag vectors
arrow(d,(422,430),(422,310),fill=NAVY,width=8,head=22); d.text((sc(447),sc(315)),"LIFT",font=font(20,True),fill=NAVY)
# Drag is parallel to and in the same direction as the relative wind.
arrow(d,(422,520),(509,520),fill=MUTED,width=6,head=18); d.text((sc(447),sc(545)),"DRAG",font=font(18,True),fill=MUTED)
arrow(d,(1177,430),(1177,275),fill=GOLD,width=11,head=26); d.text((sc(1205),sc(285)),"MORE LIFT",font=font(21,True),fill=GOLD)
arrow(d,(1177,520),(1319,520),fill=RED,width=9,head=24); d.text((sc(1205),sc(550)),"MORE DRAG",font=font(20,True),fill=RED)
box(d,(175,700,670,815),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=15); center_text(d,(422,738),"Baseline camber",font(20,True),NAVY); center_text(d,(422,780),"Reference lift + drag",font(18),MUTED)
box(d,(930,700,1425,815),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=15); center_text(d,(1177,738),"Camber increases",font(20,True),GOLD); center_text(d,(1177,780),"Lift ↑  and  drag ↑",font(23,True),INK)
box(d,(260,910,1340,990),fill=NAVY,outline=NAVY,width=1,radius=18); center_text(d,(800,950),"Same AoA + airspeed  →  FLAP DOWN gives more lift and more drag",font(25,True),WHITE)
save_pair(im,"pof-trailing-edge-flap-lift-drag")

# 2 — Flap stall speed
im,d=new_canvas("Flaps Lower Stall Speed","For the same weight and load factor, greater maximum lift capability means a lower stall speed.")
box(d,(80,220,985,865)); box(d,(1030,220,1520,865))
# axes
ox,oy=190,760; xend,yend=900,310
arrow(d,(ox,oy),(900,oy),fill=NAVY,width=4,head=14); arrow(d,(ox,oy),(ox,300),fill=NAVY,width=4,head=14)
d.text((sc(810),sc(785)),"Angle of attack",font=font(18,True),fill=MUTED); d.text((sc(115),sc(300)),"CL",font=font(20,True),fill=MUTED)
# schematic curves
up=[]; down=[]
for i in range(101):
    x=i/100
    # rise then gentle post-peak drop
    cu=0.15+1.18*(1-math.exp(-3.0*x)) - 0.50*max(0,x-.80)**1.15*4.0
    cd=0.25+1.48*(1-math.exp(-3.1*x)) - 0.62*max(0,x-.76)**1.15*4.0
    px=ox+x*640
    up.append((px,oy-cu*270)); down.append((px,oy-cd*270))
polyline(d,up,fill=NAVY,width=6); polyline(d,down,fill=GOLD,width=7)
d.text((sc(690),sc(520)),"FLAP UP",font=font(19,True),fill=NAVY); d.text((sc(625),sc(375)),"FLAP DOWN",font=font(19,True),fill=GOLD)
# CLmax guide
peak_down=min(p[1] for p in down); line(d,(190,peak_down),(830,peak_down),fill=GOLD,width=2); d.text((sc(205),sc(peak_down-35)),"Higher CLmax",font=font(18,True),fill=GOLD)
# right logic cards
center_text(d,(1275,270),"WHY Vs DECREASES",font(23,True),NAVY)
for y,title,sub,fillc in [(350,"FLAPS DOWN","greater maximum lift",PALE_GOLD),(505,"CLmax ↑","more lift available before stall",PALE_NAVY),(660,"STALL SPEED ↓","for same weight + load factor",WHITE)]:
    box(d,(1090,y-55,1460,y+65),fill=fillc,outline=GOLD if title=="STALL SPEED ↓" else LIGHT,width=2,radius=16); center_text(d,(1275,y-12),title,font(24,True),GOLD if "FLAPS" in title or "STALL" in title else NAVY); center_text(d,(1275,y+28),sub,font(16),MUTED)
box(d,(300,910,1300,990),fill=NAVY,outline=NAVY,width=1,radius=18); center_text(d,(800,950),"Same W + load factor:  CLmax ↑  →  Vs ↓",font(28,True),WHITE)
save_pair(im,"pof-flap-stall-speed")

# 3 — Fowler flap area
im,d=new_canvas("Fowler Flap: Rearward Travel Increases Wing Area","The defining motion is aft first, then down — increasing effective chord/area as the flap extends.")
for b,t in [((80,220,750,845),"RETRACTED"),((850,220,1520,845),"EXTENDED")]: box(d,b); center_text(d,((b[0]+b[2])/2,265),t,font(25,True),NAVY if t=="RETRACTED" else GOLD)
# retracted profile
main1=airfoil_points(405,505,430,0.13,0.045,80,0.78); d.polygon(pts(main1),fill=WHITE,outline=NAVY)
h1=(405+(.78-.5)*430,505); d.polygon(pts([(h1[0]-4,487),(620,493),(620,508),(h1[0]-4,523)]),fill=WHITE,outline=NAVY); d.ellipse((sc(h1[0]-5),sc(500),sc(h1[0]+5),sc(510)),fill=GOLD)
# extended profile and translated flap
main2=airfoil_points(1160,500,430,0.13,0.045,80,0.76); d.polygon(pts(main2),fill=WHITE,outline=NAVY)
h2=(1160+(.76-.5)*430,500); ang=math.radians(25); L=175; ex=h2[0]+L*math.cos(ang); ey=h2[1]+L*math.sin(ang)
d.polygon(pts([(h2[0]+25,505),(ex,ey-8),(ex+10,ey+12),(h2[0]+22,532)]),fill=PALE_GOLD,outline=GOLD); arrow(d,(h2[0]-5,455),(h2[0]+145,455),fill=GOLD,width=6,head=20); d.text((sc(h2[0]+10),sc(410)),"SLIDES AFT",font=font(19,True),fill=GOLD)
# chord dimension comparison
line(d,(220,670),(620,670),fill=MUTED,width=3); line(d,(220,650),(220,690),fill=MUTED,width=3); line(d,(620,650),(620,690),fill=MUTED,width=3); center_text(d,(420,705),"Reference chord",font(17,True),MUTED)
line(d,(960,670),(1430,670),fill=GOLD,width=4); line(d,(960,648),(960,692),fill=GOLD,width=3); line(d,(1430,648),(1430,692),fill=GOLD,width=3); center_text(d,(1195,705),"Longer effective chord",font(18,True),GOLD)
box(d,(180,745,650,805),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=14); center_text(d,(415,775),"Wing area unchanged",font(19,True),NAVY)
box(d,(940,745,1430,805),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); center_text(d,(1185,775),"Effective wing area ↑",font(21,True),GOLD)
box(d,(315,910,1285,990),fill=NAVY,outline=NAVY,width=1,radius=18); center_text(d,(800,950),"FOWLER: slides rearward  →  effective wing area increases",font(27,True),WHITE)
save_pair(im,"pof-fowler-flap-wing-area")

# 4 — Static versus dynamic stability
im,d=new_canvas("Static vs Dynamic Stability","Static stability is the initial tendency after a disturbance; dynamic stability is what the motion does with time.")
# header distinction
box(d,(90,210,760,300),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=16); center_text(d,(425,245),"STATIC = initial tendency",font(24,True),NAVY); center_text(d,(425,278),"Does it first move back toward trim?",font(16),MUTED)
box(d,(840,210,1510,300),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=16); center_text(d,(1175,245),"DYNAMIC = response over time",font(24,True),GOLD); center_text(d,(1175,278),"Do oscillations damp or grow?",font(16),MUTED)
# two plots
for b,title,accent in [((90,345,760,845),"STATICALLY + DYNAMICALLY STABLE",GREEN),((840,345,1510,845),"STATICALLY STABLE, DYNAMICALLY UNSTABLE",RED)]:
    box(d,b); center_text(d,((b[0]+b[2])/2,385),title,font(19,True),accent)
    ox=b[0]+75; oy=610; xe=b[2]-45
    arrow(d,(ox,oy),(xe,oy),fill=MUTED,width=3,head=11); line(d,(ox,440),(ox,760),fill=MUTED,width=3)
    d.text((sc(xe-55),sc(625)),"time",font=font(15),fill=MUTED); d.text((sc(ox+8),sc(585)),"trim",font=font(14,True),fill=MUTED)
    curve=[]
    for i in range(121):
        t=i/120*8.0
        amp=(105*math.exp(-0.28*t)) if accent==GREEN else (38*math.exp(0.16*t))
        y=oy-amp*math.cos(2.4*t)
        x=ox+35+(xe-ox-55)*(i/120)
        curve.append((x,y))
    polyline(d,curve,fill=accent,width=6)
    arrow(d,(ox+40,oy-105 if accent==GREEN else oy-38),(ox+110,oy-55 if accent==GREEN else oy-20),fill=NAVY,width=4,head=13)
    d.text((sc(ox+28),sc(748)),"Initial tendency → toward trim",font=font(16,True),fill=NAVY)
    if accent==GREEN: center_text(d,((b[0]+b[2])/2,805),"Oscillations decrease → returns to trim",font(18,True),GREEN)
    else: center_text(d,((b[0]+b[2])/2,805),"Oscillations grow → dynamically unstable",font(18,True),RED)
box(d,(250,905,1350,992),fill=NAVY,outline=NAVY,width=1,radius=18); center_text(d,(800,938),"Passenger aircraft are designed for a stable, damped response",font(23,True),WHITE); center_text(d,(800,970),"Initial restoring tendency + decreasing oscillations",font(18),WHITE)
save_pair(im,"pof-static-dynamic-stability-response")

# 5 — Directional fin / weathercock stability
im,d=new_canvas("Directional Stability: The Fin Acts Like a Weather Vane","A vertical surface behind the CG creates a restoring yaw moment when the aeroplane is disturbed from the relative wind.")
box(d,(70,210,1080,900)); box(d,(1120,210,1530,900))
# main top-view aircraft yawed right relative to vertical flight path
cx,cy=565,575; ang=math.radians(15)
def rot(p,c=(cx,cy),a=ang):
    x,y=p; ox,oy=c; dx,dy=x-ox,y-oy
    return (ox+dx*math.cos(a)-dy*math.sin(a), oy+dx*math.sin(a)+dy*math.cos(a))
body=[(cx-28,cy-245),(cx+28,cy-245),(cx+34,cy+210),(cx-34,cy+210)]
wings=[(cx-300,cy-35),(cx-25,cy-75),(cx+25,cy-75),(cx+300,cy-35),(cx+300,cy+10),(cx+28,cy+55),(cx-28,cy+55),(cx-300,cy+10)]
tail=[(cx-130,cy+170),(cx-20,cy+125),(cx+20,cy+125),(cx+130,cy+170),(cx+115,cy+210),(cx-115,cy+210)]
d.polygon(pts([rot(p) for p in body]),fill=PALE_NAVY,outline=NAVY); d.polygon(pts([rot(p) for p in wings]),fill=WHITE,outline=NAVY); d.polygon(pts([rot(p) for p in tail]),fill=WHITE,outline=NAVY)
# fin top-view highlighted at aft body
fin=[(cx-12,cy+115),(cx+12,cy+115),(cx+12,cy+210),(cx-12,cy+210)]; d.polygon(pts([rot(p) for p in fin]),fill=PALE_GOLD,outline=GOLD)
# CG
cg=rot((cx,cy+20)); d.ellipse((sc(cg[0]-12),sc(cg[1]-12),sc(cg[0]+12),sc(cg[1]+12)),fill=GOLD); d.text((sc(cg[0]+18),sc(cg[1]-14)),"CG",font=font(18,True),fill=GOLD)
# relative wind vertical down
for xx in (270,345): arrow(d,(xx,290),(xx,680),fill=MUTED,width=5,head=18)
d.text((sc(185),sc(250)),"RELATIVE WIND",font=font(18,True),fill=MUTED)
# Fin sideforce is lateral: perpendicular to the yawed aircraft longitudinal axis.
# For a 15-degree clockwise yaw, the local right-lateral unit vector is (cos(ang), sin(ang)).
finpt=rot((cx,cy+165))
lat=(math.cos(ang),math.sin(ang))
finend=(finpt[0]+150*lat[0],finpt[1]+150*lat[1])
arrow(d,(finpt[0],finpt[1]),finend,fill=GOLD,width=8,head=22)
d.text((sc(finpt[0]+28),sc(finpt[1]+42)),"LATERAL FIN SIDEFORCE",font=font(16,True),fill=GOLD)
# curved restoring arc
arcbox=(sc(cg[0]-170),sc(cg[1]-170),sc(cg[0]+170),sc(cg[1]+170)); d.arc(arcbox,start=225,end=340,fill=GREEN,width=sc(8)); arrow(d,(cg[0]+155,cg[1]-64),(cg[0]+120,cg[1]-110),fill=GREEN,width=7,head=20); d.text((sc(cg[0]+105),sc(cg[1]-165)),"RESTORING YAW",font=font(19,True),fill=GREEN)
box(d,(185,805,960,865),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); center_text(d,(572,835),"Fin behind CG → restoring weathercock moment",font(21,True),NAVY)
# comparison inset
center_text(d,(1325,258),"AFT SIDE AREA",font(22,True),NAVY)
# small/larger fin cards
for y,label,wid,force in [(390,"SMALLER",75,60),(650,"LARGER",135,110)]:
    center_text(d,(1325,y-80),label,font(18,True),MUTED if label=="SMALLER" else GOLD)
    line(d,(1240,y),(1410,y),fill=NAVY,width=8)
    d.polygon(pts([(1325-wid/2,y),(1325+wid/2,y),(1325+wid/2,y-95),(1325-wid/2,y-95)]),fill=PALE_GOLD,outline=GOLD)
    arrow(d,(1325,y-50),(1325+force,y-50),fill=GOLD,width=6 if force==60 else 9,head=18)
    center_text(d,(1325,y+55),"restoring force" + (" ↑" if label=="LARGER" else ""),font(16,True),GREEN if label=="LARGER" else MUTED)
box(d,(1120,835,1530,900),fill=NAVY,outline=NAVY,width=1,radius=14); center_text(d,(1325,867),"More area aft of CG → stronger directional stability",font(16,True),WHITE)
box(d,(250,925,1050,995),fill=WHITE,outline=GOLD,width=2,radius=18); center_text(d,(650,960),"No rudder input required: this is inherent stability",font(22,True),NAVY)
save_pair(im,"pof-directional-fin-weathercock")

print("Generated Batch 11 raster pairs:")
for p in sorted(OUT.iterdir()): print(p.name)
