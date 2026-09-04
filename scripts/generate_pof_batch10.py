from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, hashlib

OUT = Path("public/explanation-images/principles-of-flight/refined-batch-10")
OUT.mkdir(parents=True, exist_ok=True)

W,H=1600,1050
S=2
NAVY="#0B1F33"
GOLD="#C9942E"
WHITE="#FFFFFF"
BG="#F6F8FA"
INK="#162A3D"
MUTED="#5E6C7A"
LIGHT="#E7ECF1"
PALE_GOLD="#F6EBD2"
PALE_NAVY="#E7EEF5"
RED="#A84646"
GREEN="#2F6E5A"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz,bold=False): return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(sz*S))
def sc(v): return int(round(v*S))
def pts(points): return [(sc(x),sc(y)) for x,y in points]
def new_canvas(title, subtitle=None):
    im=Image.new("RGB",(W*S,H*S),BG); d=ImageDraw.Draw(im)
    d.rounded_rectangle((sc(70),sc(48),sc(1530),sc(54)), radius=sc(3), fill=GOLD)
    d.text((sc(76),sc(82)), title, font=font(46,True), fill=NAVY)
    if subtitle: d.text((sc(78),sc(142)), subtitle, font=font(22), fill=MUTED)
    return im,d

def rounded_box(d, box, fill=WHITE, outline=LIGHT, width=2, radius=22):
    d.rounded_rectangle(tuple(sc(v) for v in box), radius=sc(radius), fill=fill, outline=outline, width=sc(width))
def text_center(d, xy, text, fnt, fill=INK):
    bbox=d.textbbox((0,0),text,font=fnt); x=sc(xy[0])-(bbox[2]-bbox[0])//2; y=sc(xy[1])-(bbox[3]-bbox[1])//2
    d.text((x,y),text,font=fnt,fill=fill)
def arrow(d, start, end, fill=NAVY, width=8, head=20):
    x1,y1=map(sc,start); x2,y2=map(sc,end); d.line((x1,y1,x2,y2),fill=fill,width=sc(width)); ang=math.atan2(y2-y1,x2-x1); h=sc(head)
    p1=(x2+h*math.cos(ang+math.pi*0.84),y2+h*math.sin(ang+math.pi*0.84)); p2=(x2+h*math.cos(ang-math.pi*0.84),y2+h*math.sin(ang-math.pi*0.84)); d.polygon([(x2,y2),p1,p2],fill=fill)
def line(d,start,end,fill=NAVY,width=4): d.line((*map(sc,start),*map(sc,end)),fill=fill,width=sc(width))
def wrap_text(d,xy,text,max_width,fnt,fill=INK,spacing=7):
    words=text.split(); lines=[]; cur=""
    for w in words:
        cand=(cur+" "+w).strip(); bb=d.textbbox((0,0),cand,font=fnt)
        if bb[2]-bb[0]<=sc(max_width) or not cur: cur=cand
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    d.multiline_text((sc(xy[0]),sc(xy[1])),"\n".join(lines),font=fnt,fill=fill,spacing=sc(spacing))
def airfoil_polygon(cx,cy,chord=650,thickness=0.16,camber=0.05,n=120):
    xs=[i/(n-1) for i in range(n)]; upper=[]; lower=[]
    for x in xs:
        yt=5*thickness*(0.2969*math.sqrt(max(x,1e-6))-0.1260*x-0.3516*x*x+0.2843*x**3-0.1015*x**4); cam=camber*math.sin(math.pi*x)
        upper.append((cx+(x-0.5)*chord,cy-(cam+yt)*chord)); lower.append((cx+(x-0.5)*chord,cy-(cam-yt)*chord))
    return upper+lower[::-1]
def save_pair(im,stem):
    im2=im.resize((W,H),Image.Resampling.LANCZOS); png=OUT/f"{stem}-v1.png"; webp=OUT/f"{stem}-v1.webp"
    im2.save(png,optimize=True); im2.save(webp,"WEBP",quality=92,method=6)

# 1. Pressure distribution
im,d=new_canvas("Pressure Distribution Creates Lift","The pressure imbalance across a lifting aerofoil produces a net upward force.")
rounded_box(d,(80,205,1520,900)); poly=airfoil_polygon(800,520,760,0.13,0.045); d.polygon(pts(poly),fill=WHITE,outline=NAVY); line(d,(420,520),(1180,520),fill="#A9B4BF",width=2)
for y in [340,390,440]: arrow(d,(250,y),(520,y-20),fill=NAVY,width=3,head=10); arrow(d,(1080,y-20),(1350,y),fill=NAVY,width=3,head=10)
for y in [610,660,710]: arrow(d,(250,y),(520,y+5),fill=NAVY,width=3,head=10); arrow(d,(1080,y+5),(1350,y),fill=NAVY,width=3,head=10)
rounded_box(d,(180,250,500,330),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=16); d.text((sc(215),sc(270)),"LOW PRESSURE",font=font(26,True),fill=NAVY)
for x in [560,680,800,920,1040]:
    xn=(x-420)/760; ysurf=520-(0.045*math.sin(math.pi*xn)+5*0.13*(0.2969*math.sqrt(max(xn,1e-6))-0.1260*xn-0.3516*xn*xn+0.2843*xn**3-0.1015*xn**4))*760
    arrow(d,(x,ysurf-6),(x,ysurf-75),fill=NAVY,width=4,head=12)
rounded_box(d,(180,740,510,820),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=16); d.text((sc(205),sc(760)),"HIGH PRESSURE",font=font(26,True),fill=GOLD)
for x in [560,680,800,920,1040]:
    xn=(x-420)/760; yt=5*0.13*(0.2969*math.sqrt(max(xn,1e-6))-0.1260*xn-0.3516*xn*xn+0.2843*xn**3-0.1015*xn**4); cam=0.045*math.sin(math.pi*xn); ysurf=520-(cam-yt)*760
    arrow(d,(x,ysurf+78),(x,ysurf+8),fill=GOLD,width=4,head=12)
arrow(d,(800,480),(800,255),fill=GOLD,width=11,head=28); rounded_box(d,(650,835,950,885),fill=NAVY,outline=NAVY,width=1,radius=14); text_center(d,(800,860),"NET LIFT ↑",font(24,True),WHITE)
rounded_box(d,(280,925,1320,1000),fill=WHITE,outline=GOLD,width=2,radius=18); text_center(d,(800,962),"Lower P above  +  Higher P below  =  Net upward lift",font(25,True),NAVY); save_pair(im,"pof-pressure-distribution-lift")

# 2. Adverse yaw versus AoA
im,d=new_canvas("Why Adverse Yaw Is Stronger at High AoA","The down-going aileron adds local AoA, lift and induced drag — more strongly when baseline AoA is already high.")
for box,title in [((80,210,770,865),"LOW ANGLE OF ATTACK"),((830,210,1520,865),"HIGH ANGLE OF ATTACK")]: rounded_box(d,box); text_center(d,((box[0]+box[2])/2,250),title,font(25,True),NAVY if "LOW" in title else GOLD)
def draw_top_aircraft(d,cx,cy,high=False):
    d.rounded_rectangle((sc(cx-22),sc(cy-170),sc(cx+22),sc(cy+170)),radius=sc(18),fill=PALE_NAVY,outline=NAVY,width=sc(3))
    wing=[(cx-275,cy-45),(cx-25,cy-80),(cx+25,cy-80),(cx+275,cy-45),(cx+275,cy+10),(cx+28,cy+50),(cx-28,cy+50),(cx-275,cy+10)]; d.polygon(pts(wing),fill=WHITE,outline=NAVY)
    tail=[(cx-95,cy+125),(cx-20,cy+100),(cx+20,cy+100),(cx+95,cy+125),(cx+90,cy+150),(cx-90,cy+150)]; d.polygon(pts(tail),fill=WHITE,outline=NAVY)
    d.rounded_rectangle((sc(cx-250),sc(cy-15),sc(cx-150),sc(cy+15)),radius=sc(5),fill=PALE_NAVY,outline=NAVY,width=sc(2)); d.rounded_rectangle((sc(cx+150),sc(cy-12),sc(cx+250),sc(cy+22)),radius=sc(5),fill=PALE_GOLD,outline=GOLD,width=sc(2))
    d.text((sc(cx-250),sc(cy+26)),"UP",font=font(16,True),fill=NAVY); d.text((sc(cx+185),sc(cy+32)),"DOWN",font=font(16,True),fill=GOLD)
    arrow_end_y=cy+140 if not high else cy+185; arrow(d,(cx+210,cy+45),(cx+210,arrow_end_y),fill=GOLD,width=5 if not high else 8,head=18)
    label="Induced drag" if not high else "LARGER\ninduced drag"; d.multiline_text((sc(cx+35),sc(cy+110 if not high else cy+120)),label,font=font(17,True),fill=GOLD,spacing=sc(3))
    arrow(d,(cx-60,cy-145),(cx+(115 if not high else 155),cy-145),fill=RED,width=5 if not high else 8,head=18); d.text((sc(cx-95),sc(cy-205)),"Adverse yaw → RIGHT",font=font(18,True),fill=RED)
draw_top_aircraft(d,425,520,False); draw_top_aircraft(d,1175,520,True)
rounded_box(d,(185,735,665,815),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=14); text_center(d,(425,762),"Lower baseline AoA",font(20,True),NAVY); text_center(d,(425,792),"smaller drag imbalance → weaker adverse yaw",font(17),MUTED)
rounded_box(d,(935,735,1415,815),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); text_center(d,(1175,762),"Higher baseline AoA",font(20,True),GOLD); text_center(d,(1175,792),"larger drag imbalance → stronger adverse yaw",font(17),MUTED)
rounded_box(d,(300,900,1300,985),fill=WHITE,outline=GOLD,width=2,radius=18); text_center(d,(800,932),"Same left-roll input",font(20,True),NAVY); text_center(d,(800,965),"Higher AoA → more induced drag → stronger adverse yaw",font(25,True),NAVY); save_pair(im,"pof-adverse-yaw-high-aoa")

# 3. Venturi continuity + Bernoulli
im,d=new_canvas("Venturi: Continuity + Bernoulli","In subsonic flow, a smaller passage means higher velocity and lower static pressure — with mass flow conserved.")
rounded_box(d,(90,220,1510,865)); top=[(190,380),(500,380),(700,470),(900,470),(1100,380),(1410,380)]; bot=[(190,700),(500,700),(700,610),(900,610),(1100,700),(1410,700)]; d.line(pts(top),fill=NAVY,width=sc(8)); d.line(pts(bot),fill=NAVY,width=sc(8))
for y in [460,540,620]: arrow(d,(245,y),(450,y),fill=NAVY,width=5,head=16); arrow(d,(1110,y),(1340,y),fill=NAVY,width=5,head=16)
for y in [515,565]: arrow(d,(700,y),(900,y),fill=GOLD,width=8,head=20)
arrow(d,(510,395),(510,685),fill=MUTED,width=3,head=12); arrow(d,(690,595),(690,485),fill=MUTED,width=3,head=12); d.text((sc(365),sc(320)),"WIDE SECTION",font=font(24,True),fill=NAVY); d.text((sc(735),sc(410)),"THROAT",font=font(24,True),fill=GOLD)
rounded_box(d,(175,745,585,840),fill=PALE_NAVY,outline=PALE_NAVY,width=1,radius=15); d.text((sc(205),sc(765)),"A larger   •   V lower   •   P higher",font=font(22,True),fill=NAVY); d.text((sc(205),sc(805)),"Static pressure is higher here",font=font(18),fill=MUTED)
rounded_box(d,(650,745,1050,840),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=15); d.text((sc(680),sc(765)),"A smaller  •  V higher  •  P lower",font=font(22,True),fill=GOLD); d.text((sc(680),sc(805)),"Maximum speed at the throat",font=font(18),fill=MUTED)
rounded_box(d,(1115,745,1430,840),fill=WHITE,outline=LIGHT,width=1,radius=15); text_center(d,(1272,782),"Mass flow",font(20,True),NAVY); text_center(d,(1272,817),"REMAINS CONSTANT",font(19,True),GOLD)
rounded_box(d,(320,910,1280,990),fill=NAVY,outline=NAVY,width=1,radius=18); text_center(d,(800,950),"Area ↓  →  Velocity ↑  →  Static pressure ↓",font(28,True),WHITE); save_pair(im,"pof-venturi-continuity")

# 4. Level-turn force balance
im,d=new_canvas("Level Turn: Where the Turning Force Comes From","Bank tilts the lift vector. Its vertical component holds altitude; its horizontal component turns the aeroplane.")
rounded_box(d,(70,210,1030,900)); cx,cy=545,570; ang=-math.radians(30)
def rot(p,c=(cx,cy),a=ang):
    x,y=p; ox,oy=c; dx,dy=x-ox,y-oy; return (ox+dx*math.cos(a)-dy*math.sin(a),oy+dx*math.sin(a)+dy*math.cos(a))
wing=[(cx-300,cy-22),(cx-32,cy-42),(cx+32,cy-42),(cx+300,cy-22),(cx+300,cy+18),(cx+35,cy+40),(cx-35,cy+40),(cx-300,cy+18)]; d.polygon(pts([rot(p) for p in wing]),fill=WHITE,outline=NAVY)
fuse=[(cx-28,cy-90),(cx+28,cy-90),(cx+28,cy+95),(cx-28,cy+95)]; d.polygon(pts([rot(p) for p in fuse]),fill=PALE_NAVY,outline=NAVY)
arrow(d,(cx,cy),(cx-220,cy-380),fill=GOLD,width=11,head=28); arrow(d,(cx,cy),(cx,cy+285),fill=NAVY,width=9,head=24); arrow(d,(cx,cy),(cx,cy-310),fill=GREEN,width=7,head=20); arrow(d,(cx,cy),(cx-220,cy),fill=RED,width=7,head=20)
for y in range(int(cy-310),int(cy),18): line(d,(cx-2,y),(cx+2,y),fill="#9DAAB6",width=2)
rounded_box(d,(120,285,430,350),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); text_center(d,(275,317),"TOTAL LIFT",font(22,True),GOLD)
rounded_box(d,(605,265,940,350),fill="#E1F1EB",outline="#E1F1EB",width=1,radius=14); text_center(d,(772,292),"VERTICAL COMPONENT",font(18,True),GREEN); text_center(d,(772,322),"supports WEIGHT",font(18,True),GREEN)
rounded_box(d,(110,520,400,605),fill="#F6E3E3",outline="#F6E3E3",width=1,radius=14); text_center(d,(255,547),"HORIZONTAL COMPONENT",font(17,True),RED); text_center(d,(255,577),"= CENTRIPETAL FORCE",font(18,True),RED); d.text((sc(570),sc(730)),"WEIGHT",font=font(21,True),fill=NAVY)
rounded_box(d,(150,805,950,875),fill=WHITE,outline=GOLD,width=2,radius=16); text_center(d,(550,840),"Hold altitude → increase AoA / total lift until vertical lift = weight",font(21,True),NAVY)
rounded_box(d,(1080,210,1530,900)); text_center(d,(1305,255),"APPARENT LOAD — AIRCRAFT FRAME",font(20,True),NAVY); wrap_text(d,(1120,295),"The pilot feels the resultant of weight and outward centrifugal effect. Wing lift must oppose that resultant.",360,font(17),MUTED,6)
icx,icy=1300,570; arrow(d,(icx,icy),(icx,icy+170),fill=NAVY,width=7,head=20); arrow(d,(icx,icy),(icx+165,icy),fill=RED,width=7,head=20); arrow(d,(icx,icy),(icx+165,icy+170),fill=GOLD,width=9,head=24)
d.text((sc(icx-55),sc(icy+185)),"Weight",font=font(17,True),fill=NAVY); d.text((sc(icx+105),sc(icy-42)),"Centrifugal",font=font(17,True),fill=RED); d.text((sc(icx+80),sc(icy+155)),"Resultant\nload",font=font(18,True),fill=GOLD)
rounded_box(d,(1130,785,1480,860),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); text_center(d,(1305,815),"More bank → higher load factor",font(18,True),GOLD); text_center(d,(1305,842),"60° level bank = 2.0 G",font(17,True),NAVY); save_pair(im,"pof-level-turn-force-balance")

# 5. Propeller left-turning tendencies
im,d=new_canvas("Propeller Left-Turning Tendencies","For a conventional propeller rotating clockwise as seen from the cockpit, torque and P-factor create different left tendencies.")
for box,title in [((75,210,780,880),"1  TORQUE REACTION = ROLL"),((820,210,1525,880),"2  P-FACTOR = YAW")]: rounded_box(d,box); text_center(d,((box[0]+box[2])/2,255),title,font(24,True),NAVY if box[0]<100 else GOLD)
cx,cy=425,525; rounded_box(d,(280,292,570,340),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=12); text_center(d,(425,316),"PROP: CLOCKWISE",font(18,True),GOLD)
d.ellipse((sc(cx-150),sc(cy-150),sc(cx+150),sc(cy+150)),outline="#B9C4CF",width=sc(3)); d.rounded_rectangle((sc(cx-18),sc(cy-140),sc(cx+18),sc(cy+140)),radius=sc(16),fill=NAVY); d.rounded_rectangle((sc(cx-138),sc(cy-16),sc(cx+138),sc(cy+16)),radius=sc(14),fill=NAVY); d.ellipse((sc(cx-30),sc(cy-30),sc(cx+30),sc(cy+30)),fill=GOLD)
d.arc((sc(cx-190),sc(cy-190),sc(cx+190),sc(cy+190)),start=205,end=515,fill=GOLD,width=sc(8)); arrow(d,(cx+168,cy-45),(cx+184,cy+5),fill=GOLD,width=7,head=18); d.arc((sc(210),sc(620),sc(640),sc(830)),start=195,end=345,fill=RED,width=sc(9)); arrow(d,(248,735),(230,700),fill=RED,width=8,head=22); text_center(d,(425,770),"AIRCRAFT REACTS OPPOSITE",font(17,True),MUTED); text_center(d,(425,810),"ROLLS LEFT",font(28,True),RED)
cx2,cy2=1170,510; d.ellipse((sc(cx2-160),sc(cy2-160),sc(cx2+160),sc(cy2+160)),outline="#B9C4CF",width=sc(3)); line(d,(cx2,cy2-145),(cx2,cy2+145),fill=NAVY,width=16); d.ellipse((sc(cx2-25),sc(cy2-25),sc(cx2+25),sc(cy2+25)),fill=GOLD); arrow(d,(cx2+95,cy2-110),(cx2+95,cy2+85),fill=GOLD,width=7,head=20)
d.text((sc(cx2+120),sc(cy2-35)),"Descending blade",font=font(17,True),fill=GOLD); d.text((sc(cx2+120),sc(cy2-2)),"more thrust",font=font(17,True),fill=GOLD); arrow(d,(cx2+180,cy2+200),(cx2-170,cy2+200),fill=RED,width=9,head=24); text_center(d,(1170,750),"NOSE YAWS LEFT",font(26,True),RED)
rounded_box(d,(955,790,1385,850),fill=PALE_GOLD,outline=PALE_GOLD,width=1,radius=14); text_center(d,(1170,820),"Correct with RIGHT RUDDER",font(21,True),GOLD); rounded_box(d,(240,910,1360,995),fill=NAVY,outline=NAVY,width=1,radius=18); text_center(d,(800,940),"High power + low speed + high AoA → left-turning tendency is strongest",font(22,True),WHITE); text_center(d,(800,972),"Remember: TORQUE = ROLL   •   P-FACTOR = YAW",font(24,True),GOLD); save_pair(im,"pof-propeller-left-turning-tendencies")

EXPECTED={
'pof-adverse-yaw-high-aoa-v1.png':'32e57e76ea477978fe6202c384664b67266567fee099df74b075d72d15ab64fe','pof-adverse-yaw-high-aoa-v1.webp':'14cdc9e8dc02a826bf9b7773bbb1e0b9c7567407d43c7dbb6e8b9db21ba8cc8b',
'pof-level-turn-force-balance-v1.png':'36f93395967c48163632f52fc28d998af80819f83c7d24a9115a656c658265bd','pof-level-turn-force-balance-v1.webp':'ec9237b41719489b38a8e0dd891234a4bc049a9e06f71b884e63aa028e0cfafb',
'pof-pressure-distribution-lift-v1.png':'e0d22722ec916f1092a0591587b7941ff3543115fd41481f025eb6850245d2a1','pof-pressure-distribution-lift-v1.webp':'4efe961788de4286b2bb94dbd27ffc43d1284647de813fe6685b3c000bfcb11b',
'pof-propeller-left-turning-tendencies-v1.png':'767eecd8c610195620dc677d728a1661f26239e7db6e09c7a675f52db04f3466','pof-propeller-left-turning-tendencies-v1.webp':'ed13656bc97e6894360bc162e430c6a105eca44c7e7d2e96b64930761fdc4908',
'pof-venturi-continuity-v1.png':'bb016bf0288df50f9fbb6cb87b7602c6c8917d4ddd91f87606d8880126248f23','pof-venturi-continuity-v1.webp':'b7f861b52639cd76677c1b3c9a4aaef95c625f3b4cb5790acb790b14ecb39b1a'}
for name,expected in EXPECTED.items():
    path=OUT/name
    assert path.exists(),f'missing generated asset: {path}'
    with Image.open(path) as check: assert check.size==(1600,1050),f'{name}: wrong size {check.size}'
    actual=hashlib.sha256(path.read_bytes()).hexdigest(); assert actual==expected,f'{name}: SHA256 mismatch {actual} != {expected}'
print(f'Batch 10 asset generation verified: {len(EXPECTED)} assets')
