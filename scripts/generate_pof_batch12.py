from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("public/explanation-images/principles-of-flight/refined-batch-12")
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
    d.text((sc(78),sc(142)), subtitle, font=font(20), fill=MUTED)
    return im,d

def box(d,b,fill=WHITE,outline=LIGHT,width=2,radius=22):
    d.rounded_rectangle(tuple(sc(v) for v in b), radius=sc(radius), fill=fill, outline=outline, width=sc(width))

def center_text(d,xy,text,fnt,fill=INK):
    bb=d.textbbox((0,0),text,font=fnt)
    d.text((sc(xy[0])-(bb[2]-bb[0])//2, sc(xy[1])-(bb[3]-bb[1])//2), text, font=fnt, fill=fill)

def arrow(d,a,b,fill=NAVY,width=7,head=20):
    x1,y1=map(sc,a); x2,y2=map(sc,b)
    d.line((x1,y1,x2,y2),fill=fill,width=sc(width))
    ang=math.atan2(y2-y1,x2-x1); h=sc(head)
    p1=(x2+h*math.cos(ang+math.pi*0.84),y2+h*math.sin(ang+math.pi*0.84))
    p2=(x2+h*math.cos(ang-math.pi*0.84),y2+h*math.sin(ang-math.pi*0.84))
    d.polygon([(x2,y2),p1,p2],fill=fill)

def line(d,a,b,fill=NAVY,width=4): d.line((*map(sc,a),*map(sc,b)),fill=fill,width=sc(width))
def polyline(d,seq,fill=NAVY,width=5): d.line(pts(seq),fill=fill,width=sc(width),joint="curve")

def save_pair(im, stem):
    im=im.resize((W,H),Image.Resampling.LANCZOS)
    im.save(OUT/f"{stem}-v1.png", optimize=True)
    im.save(OUT/f"{stem}-v1.webp", "WEBP", quality=92, method=6)

# ---------- reusable aircraft icons ----------
def top_aircraft(d,cx,cy,scale=1.0,angle_deg=0,bank=False,accent=NAVY, rudder=False, aileron=False):
    # clean top-view light-aircraft silhouette; rotated as one group
    layer=Image.new("RGBA",(sc(420*scale),sc(420*scale)),(0,0,0,0))
    ld=ImageDraw.Draw(layer)
    ox=210*scale; oy=210*scale
    def P(x,y): return (sc((ox+x*scale)),sc((oy+y*scale)))
    fus=[P(-10,-118),P(12,-118),P(20,-48),P(18,82),P(9,122),P(-8,122),P(-18,82),P(-20,-48)]
    ld.polygon(fus,fill=WHITE,outline=accent)
    ld.polygon([P(-18,-25),P(-125,20),P(-116,42),P(-18,28)],fill=PALE_NAVY,outline=accent)
    ld.polygon([P(18,-25),P(125,20),P(116,42),P(18,28)],fill=PALE_NAVY,outline=accent)
    ld.polygon([P(-12,75),P(-65,98),P(-61,113),P(-8,100)],fill=WHITE,outline=accent)
    ld.polygon([P(12,75),P(65,98),P(61,113),P(8,100)],fill=WHITE,outline=accent)
    ld.polygon([P(-4,74),P(2,74),P(10,122),P(1,122)],fill=PALE_GOLD if rudder else WHITE,outline=GOLD if rudder else accent)
    if aileron:
        ld.polygon([P(-119,29),P(-83,16),P(-78,28),P(-113,41)],fill=GOLD,outline=GOLD)
        ld.polygon([P(83,16),P(119,29),P(113,41),P(78,28)],fill=RED,outline=RED)
    if bank:
        ld.line((sc((ox-145*scale)),sc(oy),sc((ox+145*scale)),sc(oy)),fill=GOLD,width=sc(8*scale))
    if angle_deg:
        layer=layer.rotate(-angle_deg,resample=Image.Resampling.BICUBIC,expand=False)
    d._image.paste(layer,(sc(cx-210*scale),sc(cy-210*scale)),layer)

def curved_arrow(d, center, radius, start_deg, end_deg, fill=GOLD, width=7, head=20):
    cx,cy=center
    steps=36
    seq=[]
    for i in range(steps+1):
        a=math.radians(start_deg+(end_deg-start_deg)*i/steps)
        seq.append((cx+radius*math.cos(a),cy+radius*math.sin(a)))
    polyline(d,seq,fill=fill,width=width)
    arrow(d,seq[-2],seq[-1],fill=fill,width=width,head=head)

def front_aircraft(d,cx,cy,bank_deg=0,highlight_ailerons=False):
    # Front-view geometry makes roll/bank unmistakable. Positive bank_deg raises viewer-left wing.
    ang=math.radians(bank_deg)
    def rot(x,y):
        return (cx+x*math.cos(ang)-y*math.sin(ang), cy+x*math.sin(ang)+y*math.cos(ang))
    # horizon / roll reference
    line(d,(cx-155,cy+115),(cx+155,cy+115),fill=LIGHT,width=3)
    # fuselage/nose
    c=rot(0,0)
    d.ellipse((sc(c[0]-34),sc(c[1]-45),sc(c[0]+34),sc(c[1]+45)),fill=WHITE,outline=NAVY,width=sc(4))
    # wings
    l0=rot(-28,0); lt=rot(-145,18); r0=rot(28,0); rt=rot(145,18)
    line(d,l0,lt,fill=NAVY,width=10); line(d,r0,rt,fill=NAVY,width=10)
    # aileron cues at outer trailing portions
    if highlight_ailerons:
        la1=rot(-95,20); la2=rot(-142,35); ra1=rot(95,20); ra2=rot(142,5)
        line(d,la1,la2,fill=GOLD,width=8); line(d,ra1,ra2,fill=RED,width=8)
    # vertical tail hint
    t1=rot(0,-35); t2=rot(0,-105); line(d,t1,t2,fill=NAVY,width=5)

# 1 — Rudder: yaw -> roll -> possible spiral
im,d=new_canvas("Rudder: Primary and Further Effects","The order matters: yaw first, then roll; an uncorrected imbalance can develop into a spiral dive.")
frames=[(75,220,515,850),(580,220,1020,850),(1085,220,1525,850)]
labels=[("1  PRIMARY","YAW"),("2  SECONDARY","ROLL"),("3  IF UNCORRECTED","SPIRAL DIVE")]
for i,b in enumerate(frames):
    box(d,b)
    center_text(d,((b[0]+b[2])/2,267),labels[i][0],font(18,True),MUTED)
    center_text(d,((b[0]+b[2])/2,307),labels[i][1],font(27,True),GOLD if i==0 else NAVY)
# frame 1
center_text(d,(295,385),"RUDDER INPUT",font(17,True),GOLD)
top_aircraft(d,295,535,0.9,angle_deg=16,accent=NAVY,rudder=True)
curved_arrow(d,(295,535),155,-78,-12,fill=GOLD,width=6,head=18)
center_text(d,(295,755),"Aircraft yaws about the vertical axis",font(17),MUTED)
# frame 2
center_text(d,(800,385),"ROLL DEVELOPS",font(17,True),NAVY)
front_aircraft(d,800,545,bank_deg=-22,highlight_ailerons=False)
curved_arrow(d,(800,545),145,200,330,fill=GOLD,width=6,head=18)
center_text(d,(800,705),"FRONT VIEW",font(15,True),MUTED)
center_text(d,(800,755),"The yaw-induced imbalance develops bank",font(17),MUTED)
# frame 3
center_text(d,(1305,385),"CONTINUED IMBALANCE",font(17,True),RED)
# spiral path
spir=[]
for i in range(80):
    a=0.22*i
    r=145-1.35*i
    spir.append((1305+r*math.cos(a),530+r*math.sin(a)*0.55))
polyline(d,spir,fill=RED,width=6); arrow(d,spir[-3],spir[-1],fill=RED,width=6,head=18)
top_aircraft(d,1325,520,0.72,angle_deg=35,bank=True,accent=NAVY)
arrow(d,(1390,595),(1425,680),fill=RED,width=6,head=18)
center_text(d,(1305,755),"May progress into a descending spiral",font(17),MUTED)
arrow(d,(520,535),(570,535),fill=MUTED,width=5,head=16); arrow(d,(1025,535),(1075,535),fill=MUTED,width=5,head=16)
box(d,(250,905,1350,988),fill=NAVY,outline=NAVY,width=1,radius=18)
center_text(d,(800,947),"RUDDER  →  YAW  →  ROLL  →  possible SPIRAL DIVE if not corrected",font(25,True),WHITE)
save_pair(im,"pof-rudder-further-effects")

# 2 — Aileron: roll -> yaw -> possible spiral
im,d=new_canvas("Aileron: Primary and Further Effects","Aileron produces roll first; secondary yaw follows, and a sustained imbalance can develop into a spiral dive.")
frames=[(75,220,515,850),(580,220,1020,850),(1085,220,1525,850)]
labels=[("1  PRIMARY","ROLL"),("2  SECONDARY","YAW"),("3  IF UNCORRECTED","SPIRAL DIVE")]
for i,b in enumerate(frames):
    box(d,b)
    center_text(d,((b[0]+b[2])/2,267),labels[i][0],font(18,True),MUTED)
    center_text(d,((b[0]+b[2])/2,307),labels[i][1],font(27,True),GOLD if i==0 else NAVY)
center_text(d,(295,385),"AILERON INPUT",font(17,True),GOLD)
front_aircraft(d,295,545,bank_deg=-24,highlight_ailerons=True)
curved_arrow(d,(295,545),145,200,330,fill=GOLD,width=6,head=18)
center_text(d,(295,705),"FRONT VIEW",font(15,True),MUTED)
center_text(d,(295,755),"Aileron input produces roll first",font(17),MUTED)
center_text(d,(800,385),"SECONDARY YAW",font(17,True),NAVY)
top_aircraft(d,800,535,0.9,angle_deg=15,bank=True,accent=NAVY)
curved_arrow(d,(800,535),150,-82,-18,fill=GOLD,width=6,head=18)
center_text(d,(800,755),"The rolled aircraft develops yaw",font(17),MUTED)
center_text(d,(1305,385),"CONTINUED IMBALANCE",font(17,True),RED)
spir=[]
for i in range(80):
    a=0.22*i; r=145-1.35*i
    spir.append((1305+r*math.cos(a),530+r*math.sin(a)*0.55))
polyline(d,spir,fill=RED,width=6); arrow(d,spir[-3],spir[-1],fill=RED,width=6,head=18)
top_aircraft(d,1325,520,0.72,angle_deg=35,bank=True,accent=NAVY)
arrow(d,(1390,595),(1425,680),fill=RED,width=6,head=18)
center_text(d,(1305,755),"May progress into a descending spiral",font(17),MUTED)
arrow(d,(520,535),(570,535),fill=MUTED,width=5,head=16); arrow(d,(1025,535),(1075,535),fill=MUTED,width=5,head=16)
box(d,(250,905,1350,988),fill=NAVY,outline=NAVY,width=1,radius=18)
center_text(d,(800,947),"AILERON  →  ROLL  →  YAW  →  possible SPIRAL DIVE if not corrected",font(25,True),WHITE)
save_pair(im,"pof-aileron-further-effects")

# 3 — Control column forward + left
im,d=new_canvas("Control Column Forward + Left","Two inputs act together: forward commands elevator DOWN; left commands left aileron UP and right aileron DOWN.")
box(d,(75,220,540,860)); box(d,(590,220,1525,860))
center_text(d,(307,270),"COCKPIT INPUT",font(23,True),NAVY)
# yoke / column
line(d,(307,395),(307,650),fill=NAVY,width=14)
d.ellipse((sc(237),sc(345),sc(377),sc(485)),outline=NAVY,width=sc(13))
line(d,(250,415),(365,385),fill=GOLD,width=12)
arrow(d,(307,520),(307,665),fill=GOLD,width=8,head=22)
arrow(d,(307,520),(205,520),fill=GOLD,width=8,head=22)
center_text(d,(307,710),"FORWARD",font(20,True),GOLD); center_text(d,(190,565),"LEFT",font(20,True),GOLD)
box(d,(135,765,480,825),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14)
center_text(d,(307,795),"COLUMN: FORWARD + LEFT",font(18,True),GOLD)
# aircraft top view with fixed labels
center_text(d,(1058,270),"RESULTING CONTROL-SURFACE MOVEMENTS",font(22,True),NAVY)
top_aircraft(d,1058,525,1.17,accent=NAVY,aileron=True)
# callout anchors: in top_aircraft left side of image is aircraft left wing for nose-up orientation
arrow(d,(875,485),(750,405),fill=GOLD,width=5,head=16)
box(d,(620,330,875,425),fill=PALE_GOLD,outline=GOLD,width=2,radius=14)
center_text(d,(747,365),"LEFT AILERON",font(17,True),GOLD); center_text(d,(747,398),"UP",font(23,True),GOLD)
arrow(d,(1240,485),(1365,405),fill=RED,width=5,head=16)
box(d,(1240,330,1490,425),fill="#F8EAEA",outline=RED,width=2,radius=14)
center_text(d,(1365,365),"RIGHT AILERON",font(17,True),RED); center_text(d,(1365,398),"DOWN",font(23,True),RED)
arrow(d,(1058,650),(1058,735),fill=GOLD,width=5,head=16)
box(d,(920,735,1196,825),fill=PALE_GOLD,outline=GOLD,width=2,radius=14)
center_text(d,(1058,767),"ELEVATOR",font(17,True),GOLD); center_text(d,(1058,798),"DOWN",font(23,True),GOLD)
# left/right labels
center_text(d,(778,545),"AIRCRAFT LEFT",font(15,True),MUTED); center_text(d,(1338,545),"AIRCRAFT RIGHT",font(15,True),MUTED)
box(d,(260,910,1340,990),fill=NAVY,outline=NAVY,width=1,radius=18)
center_text(d,(800,950),"FORWARD + LEFT  →  left aileron UP · right aileron DOWN · elevator DOWN",font(24,True),WHITE)
save_pair(im,"pof-control-column-forward-left")

# 4 — Aspect ratio and induced drag
im,d=new_canvas("Aspect Ratio & Induced Drag","Aspect ratio compares span with mean aerodynamic chord; a higher aspect ratio reduces induced drag for comparable lift conditions.")
box(d,(70,220,775,855)); box(d,(825,220,1530,855))
center_text(d,(422,270),"HIGH ASPECT RATIO",font(25,True),GOLD); center_text(d,(1177,270),"LOW ASPECT RATIO",font(25,True),NAVY)
# equal reference area planforms: long/narrow vs short/broad
# high AR wing top view
cx,cy=422,500
span1,chord1=560,115
d.rounded_rectangle((sc(cx-span1/2),sc(cy-chord1/2),sc(cx+span1/2),sc(cy+chord1/2)),radius=sc(18),fill=PALE_GOLD,outline=GOLD,width=sc(4))
d.rectangle((sc(cx-22),sc(cy-72),sc(cx+22),sc(cy+72)),fill=WHITE,outline=NAVY,width=sc(3))
line(d,(cx-span1/2,390),(cx+span1/2,390),fill=GOLD,width=4); line(d,(cx-span1/2,375),(cx-span1/2,405),fill=GOLD,width=3); line(d,(cx+span1/2,375),(cx+span1/2,405),fill=GOLD,width=3); center_text(d,(cx,360),"LONGER SPAN",font(17,True),GOLD)
line(d,(cx+315,cy-chord1/2),(cx+315,cy+chord1/2),fill=MUTED,width=3); center_text(d,(cx+315,cy+90),"short chord",font(15,True),MUTED)
# low AR
cx2,cy2=1177,500
span2,chord2=330,195
d.rounded_rectangle((sc(cx2-span2/2),sc(cy2-chord2/2),sc(cx2+span2/2),sc(cy2+chord2/2)),radius=sc(22),fill=PALE_NAVY,outline=NAVY,width=sc(4))
d.rectangle((sc(cx2-22),sc(cy2-120),sc(cx2+22),sc(cy2+120)),fill=WHITE,outline=NAVY,width=sc(3))
line(d,(cx2-span2/2,350),(cx2+span2/2,350),fill=NAVY,width=4); line(d,(cx2-span2/2,335),(cx2-span2/2,365),fill=NAVY,width=3); line(d,(cx2+span2/2,335),(cx2+span2/2,365),fill=NAVY,width=3); center_text(d,(cx2,320),"SHORTER SPAN",font(17,True),NAVY)
line(d,(cx2+205,cy2-chord2/2),(cx2+205,cy2+chord2/2),fill=MUTED,width=3); center_text(d,(cx2+205,cy2+125),"broader chord",font(15,True),MUTED)
# vortices / induced drag cue
for xx,yy,rr in [(180,690,34),(665,690,34)]: curved_arrow(d,(xx,yy),rr,20,330,fill=GREEN,width=4,head=12)
for xx,yy,rr in [(1012,690,53),(1342,690,53)]: curved_arrow(d,(xx,yy),rr,20,330,fill=RED,width=6,head=16)
center_text(d,(422,760),"weaker tip-vortex effect",font(16),MUTED); center_text(d,(1177,770),"stronger tip-vortex effect",font(16),MUTED)
box(d,(180,795,665,835),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=12); center_text(d,(422,815),"LESS INDUCED DRAG",font(20,True),GREEN)
box(d,(935,795,1420,835),fill="#F8EAEA",outline="#F8EAEA",width=1,radius=12); center_text(d,(1177,815),"MORE INDUCED DRAG",font(20,True),RED)
box(d,(245,905,1355,990),fill=NAVY,outline=NAVY,width=1,radius=18)
center_text(d,(800,938),"AR = span ÷ mean chord",font(22,True),WHITE); center_text(d,(800,970),"HIGH AR  →  relatively longer span + shorter chord  →  LESS induced drag",font(20,True),WHITE)
save_pair(im,"pof-aspect-ratio-induced-drag")

# 5 — Anhedral geometry
im,d=new_canvas("Anhedral: Wings Slope Downward from Root to Tip","Front-view geometry: each wingtip is lower than the wing root. Anhedral is the opposite geometric sense of dihedral.")
box(d,(80,220,1120,860)); box(d,(1160,220,1520,860),fill=WHITE)
center_text(d,(600,270),"FRONT VIEW — ANHEDRAL",font(26,True),GOLD)
# fuselage front
cx,root_y=600,500
d.ellipse((sc(cx-70),sc(root_y-75),sc(cx+70),sc(root_y+75)),fill=WHITE,outline=NAVY,width=sc(5))
# datum
line(d,(200,root_y),(1000,root_y),fill=MUTED,width=3)
d.text((sc(205),sc(root_y-38)),"horizontal root datum",font=font(15,True),fill=MUTED)
# downward wings from roots
left_root=(cx-65,root_y); right_root=(cx+65,root_y); left_tip=(220,650); right_tip=(980,650)
line(d,left_root,left_tip,fill=GOLD,width=16); line(d,right_root,right_tip,fill=GOLD,width=16)
# wing thickness second lines
line(d,(left_root[0],left_root[1]+18),(left_tip[0],left_tip[1]+18),fill=NAVY,width=3); line(d,(right_root[0],right_root[1]+18),(right_tip[0],right_tip[1]+18),fill=NAVY,width=3)
arrow(d,(345,555),(250,625),fill=GOLD,width=6,head=18); arrow(d,(855,555),(950,625),fill=GOLD,width=6,head=18)
center_text(d,(600,735),"ROOT  →  TIP:  DOWNWARD",font(27,True),GOLD)
center_text(d,(600,785),"Both wingtips sit below the wing roots",font(19),MUTED)
# contrast inset
center_text(d,(1340,270),"CONTRAST",font(19,True),MUTED); center_text(d,(1340,315),"DIHEDRAL",font(23,True),NAVY)
line(d,(1220,520),(1340,440),fill=NAVY,width=9); line(d,(1460,520),(1340,440),fill=NAVY,width=9)
line(d,(1200,520),(1480,520),fill=MUTED,width=2)
center_text(d,(1340,585),"tips ABOVE roots",font(16,True),MUTED)
center_text(d,(1340,645),"opposite slope",font(16),MUTED)
box(d,(230,910,1370,990),fill=NAVY,outline=NAVY,width=1,radius=18)
center_text(d,(800,950),"ANHEDRAL = wing slopes DOWN from root to tip when viewed from the front",font(25,True),WHITE)
save_pair(im,"pof-anhedral-wing-geometry")

print("Generated Batch 12: exactly five PNG + five WebP visual pairs.")
