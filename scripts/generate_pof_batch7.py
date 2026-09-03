from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import hashlib, json, math

W,H,S=1600,1050,2
WW,HH=W*S,H*S
OUT=Path('public/explanation-images/principles-of-flight/refined-batch-7')
OUT.mkdir(parents=True,exist_ok=True)
BG='#F6F7F9'; CARD='#FFFFFF'; NAVY='#0B1B31'; TEXT='#1D2735'; MUTED='#64748B'; GOLD='#D4A017'; LINE='#D7DEE8'; BLUE='#356A9A'; BLUE2='#7EA6C8'; RED='#B84335'; GREEN='#2F7D5A'; YELLOW='#D8A315'; BLACK='#141A22'; WHITE='#FFFFFF'; AIR='#5D7893'
REG='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def sc(v): return int(round(v*S))
def pts(a): return [(sc(x),sc(y)) for x,y in a]
def F(size,bold=False): return ImageFont.truetype(BOLD if bold else REG,int(size*S))
def canvas(): return Image.new('RGB',(WW,HH),BG)
def txt(d,xy,t,size,fill=TEXT,bold=False,anchor=None): d.text((sc(xy[0]),sc(xy[1])),t,font=F(size,bold),fill=fill,anchor=anchor)
def title(d,main,sub):
    txt(d,(70,65),main,37,NAVY,True); txt(d,(72,112),sub,18,MUTED); d.line((sc(70),sc(150),sc(1530),sc(150)),fill=LINE,width=sc(2))
def box(d,x,y,w,h,head,body='',accent=GOLD,hs=24,bs=19):
    d.rounded_rectangle((sc(x),sc(y),sc(x+w),sc(y+h)),radius=sc(18),fill=CARD,outline=LINE,width=sc(2))
    d.rounded_rectangle((sc(x+18),sc(y+18),sc(x+26),sc(y+h-18)),radius=sc(4),fill=accent)
    txt(d,(x+46,y+22),head,hs,NAVY,True)
    yy=y+58
    for line in body.split('\n') if body else []:
        txt(d,(x+46,yy),line,bs,MUTED); yy+=bs+9
def arrow(d,start,end,fill=GOLD,width=6,head=18):
    x1,y1=map(sc,start); x2,y2=map(sc,end); d.line((x1,y1,x2,y2),fill=fill,width=sc(width))
    ang=math.atan2(y2-y1,x2-x1); L=sc(head); a=math.radians(28)
    p1=(x2-int(L*math.cos(ang-a)),y2-int(L*math.sin(ang-a))); p2=(x2-int(L*math.cos(ang+a)),y2-int(L*math.sin(ang+a)))
    d.polygon([(x2,y2),p1,p2],fill=fill)
def curved(d,c,r,a1,a2,fill=RED,width=6,head=18):
    d.arc((sc(c[0]-r),sc(c[1]-r),sc(c[0]+r),sc(c[1]+r)),start=a1,end=a2,fill=fill,width=sc(width))
    a=math.radians(a2); ex=c[0]+r*math.cos(a); ey=c[1]+r*math.sin(a); tang=math.radians(a2+90)
    p1=(ex-head*math.cos(tang-math.radians(28)),ey-head*math.sin(tang-math.radians(28))); p2=(ex-head*math.cos(tang+math.radians(28)),ey-head*math.sin(tang+math.radians(28)))
    d.polygon(pts([(ex,ey),p1,p2]),fill=fill)
def airfoil(d,x,y,w,h,angle=0):
    top=[]; bot=[]
    for i in range(61):
        xx=i/60; yt=5*.12*(.2969*math.sqrt(max(xx,1e-6))-.1260*xx-.3516*xx**2+.2843*xx**3-.1015*xx**4); top.append((xx,yt)); bot.append((xx,-yt))
    cx=x+w/2; cy=y; th=math.radians(angle); out=[]
    for xx,yy in top+bot[::-1]:
        px=x+xx*w; py=y-yy*h*3.5; dx=px-cx; dy=py-cy; out.append((cx+dx*math.cos(th)-dy*math.sin(th),cy+dx*math.sin(th)+dy*math.cos(th)))
    d.polygon(pts(out),fill='#E9EDF2',outline=NAVY)
    def rot(px,py):
        dx=px-cx; dy=py-cy; return (cx+dx*math.cos(th)-dy*math.sin(th),cy+dx*math.sin(th)+dy*math.cos(th))
    a,b=rot(x,y),rot(x+w,y); d.line((*pts([a,b])[0],*pts([a,b])[1]),fill=MUTED,width=sc(2))
def plane_top(cx,cy,l=500,span=650):
    return [(cx,cy-l*.5),(cx+42,cy-l*.34),(cx+55,cy-l*.10),(cx+span*.5,cy+20),(cx+span*.48,cy+65),(cx+60,cy+55),(cx+43,cy+l*.32),(cx+span*.19,cy+l*.39),(cx+span*.17,cy+l*.45),(cx+26,cy+l*.39),(cx+18,cy+l*.5),(cx-18,cy+l*.5),(cx-26,cy+l*.39),(cx-span*.17,cy+l*.45),(cx-span*.19,cy+l*.39),(cx-43,cy+l*.32),(cx-span*.48,cy+65),(cx-span*.5,cy+20),(cx-55,cy-l*.10),(cx-42,cy-l*.34)]
def save(im,name):
    im=im.resize((W,H),Image.Resampling.LANCZOS); im.save(OUT/f'{name}.png',optimize=True); im.save(OUT/f'{name}.webp','WEBP',quality=94,method=6)

# ASI
im=canvas(); d=ImageDraw.Draw(im); title(d,'AIRSPEED LIMITS ON THE ASI','Read VFE, VNO and VNE from the standard colour-coded operating ranges')
d.rounded_rectangle((sc(80),sc(190),sc(940),sc(930)),radius=sc(28),fill=CARD,outline=LINE,width=sc(2)); cx,cy,R=510,565,295
d.ellipse((sc(cx-R),sc(cy-R),sc(cx+R),sc(cy+R)),fill='#FAFBFC',outline=NAVY,width=sc(8))
for i in range(11):
    a=math.radians(135+270*i/10); p1=(cx+(R-35)*math.cos(a),cy+(R-35)*math.sin(a)); p2=(cx+(R-10)*math.cos(a),cy+(R-10)*math.sin(a)); d.line((*pts([p1,p2])[0],*pts([p1,p2])[1]),fill=MUTED,width=sc(3))
def arc(a0,a1,c,w=20,r=225): d.arc((sc(cx-r),sc(cy-r),sc(cx+r),sc(cy+r)),start=a0,end=a1,fill=c,width=sc(w))
arc(145,225,'#AEB8C5',26,250); arc(145,225,WHITE,18,250); arc(180,315,GREEN,20,225); arc(315,378,YELLOW,20,225)
a=math.radians(378); p1=(cx+(R-75)*math.cos(a),cy+(R-75)*math.sin(a)); p2=(cx+(R-10)*math.cos(a),cy+(R-10)*math.sin(a)); d.line((*pts([p1,p2])[0],*pts([p1,p2])[1]),fill=RED,width=sc(9))
for lab,ang,col in [('VFE',225,GOLD),('VNO',315,GOLD),('VNE',378,RED)]:
    a=math.radians(ang); txt(d,(cx+(R+55)*math.cos(a),cy+(R+55)*math.sin(a)),lab,24,col,True,'mm')
d.ellipse((sc(cx-17),sc(cy-17),sc(cx+17),sc(cy+17)),fill=NAVY); a=math.radians(275); arrow(d,(cx,cy),(cx+150*math.cos(a),cy+150*math.sin(a)),NAVY,7,16); txt(d,(cx,cy+110),'STANDARD ASI',19,MUTED,True,'mm')
box(d,990,220,520,185,'VFE — MAXIMUM FLAPS EXTENDED','Upper limit of the WHITE ARC\nAbove VFE, flap loads may be excessive',GOLD); box(d,990,445,520,185,'VNO — MAX STRUCTURAL CRUISE','Upper limit of the GREEN ARC\nAbove VNO: caution / smooth air only',GREEN); box(d,990,670,520,185,'VNE — NEVER EXCEED','RED LINE\nMust not be intentionally exceeded',RED); txt(d,(1000,885),'No aircraft-specific speeds shown — read the LIMIT POSITIONS.',17,MUTED)
save(im,'pof-airspeed-indicator-limits-v1')

# Skin friction
im=canvas(); d=ImageDraw.Draw(im); title(d,'SKIN FRICTION AT THE WING SURFACE','The air touching the surface is slowed by viscosity — skin friction is parasite drag')
d.rounded_rectangle((sc(70),sc(190),sc(1530),sc(835)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); airfoil(d,210,575,980,170,0)
for yy,ll in [(510,90),(475,150),(435,225),(390,310),(345,390)]: arrow(d,(270,yy),(270+ll,yy),AIR,4,13)
for yy in [285,320]: arrow(d,(250,yy),(1150,yy),BLUE,4,13)
txt(d,(260,245),'OUTER AIRFLOW',18,BLUE,True); d.line((sc(235),sc(330),sc(235),sc(530)),fill=GOLD,width=sc(4)); d.line((sc(225),sc(330),sc(250),sc(330)),fill=GOLD,width=sc(4)); d.line((sc(225),sc(530),sc(250),sc(530)),fill=GOLD,width=sc(4)); txt(d,(130,430),'SLOWED\nSURFACE\nLAYER',20,GOLD,True,'mm')
for x in [500,555,620,690]: d.ellipse((sc(x-5),sc(540),sc(x+5),sc(550)),fill='#6F5A3A')
txt(d,(565,635),'dust can remain close to the surface',17,MUTED,False,'mm'); arrow(d,(1030,675),(740,675),RED,6,18); txt(d,(885,715),'SKIN-FRICTION DRAG',21,RED,True,'mm'); box(d,1010,375,430,180,'WHY THE NEAR-SURFACE AIR IS SLOWER','Viscous shear opposes motion\nat the aircraft surface.',GOLD,20,18); box(d,75,875,760,105,'KEY IDEA','Near-surface air is slower than the free stream.',BLUE,20,18); box(d,865,875,665,105,'CLASSIFICATION','Skin friction = PARASITE DRAG',GOLD,20,18)
save(im,'pof-skin-friction-boundary-layer-v1')

# Induced drag vs speed/AoA
im=canvas(); d=ImageDraw.Draw(im); title(d,'WHY INDUCED DRAG RISES AS SPEED FALLS','In steady level flight: lower speed → higher required angle of attack → more induced drag')
d.rounded_rectangle((sc(70),sc(195),sc(820),sc(900)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); txt(d,(110,235),'INDUCED DRAG vs SPEED',23,NAVY,True); x0,y0=160,790; d.line((sc(x0),sc(y0),sc(750),sc(y0)),fill=NAVY,width=sc(4)); d.line((sc(x0),sc(y0),sc(x0),sc(300)),fill=NAVY,width=sc(4)); txt(d,(455,830),'AIRSPEED',18,MUTED,True,'mm'); txt(d,(105,540),'INDUCED\nDRAG',18,MUTED,True,'mm')
curve=[]
for i in range(101):
    t=i/100; curve.append((x0+40+t*500,y0-430/(1+4.8*t)))
d.line(pts(curve),fill=BLUE,width=sc(8),joint='curve'); lp,hp=curve[9],curve[80]
for p,c in [(lp,GOLD),(hp,BLUE2)]: d.ellipse((sc(p[0]-9),sc(p[1]-9),sc(p[0]+9),sc(p[1]+9)),fill=c,outline=WHITE,width=sc(3))
d.line((sc(lp[0]),sc(lp[1]),sc(lp[0]),sc(y0)),fill=GOLD,width=sc(3)); d.line((sc(lp[0]),sc(lp[1]),sc(x0),sc(lp[1])),fill=GOLD,width=sc(3)); txt(d,(lp[0]+20,lp[1]-38),'LOW SPEED',18,GOLD,True); txt(d,(lp[0]+20,lp[1]-12),'HIGH INDUCED DRAG',16,TEXT,True); txt(d,(hp[0]-30,hp[1]-45),'HIGHER SPEED',16,MUTED,True)
d.rounded_rectangle((sc(860),sc(195),sc(1530),sc(900)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); txt(d,(900,235),'LEVEL-FLIGHT WING STATES',23,NAVY,True); d.line((sc(1195),sc(285),sc(1195),sc(840)),fill=LINE,width=sc(2)); txt(d,(1025,305),'LOW SPEED',22,GOLD,True,'mm'); txt(d,(1025,343),'higher required AoA',17,MUTED,False,'mm'); arrow(d,(915,610),(1130,610),BLUE,4,13); txt(d,(1015,640),'relative airflow',15,MUTED,False,'mm'); airfoil(d,915,535,235,80,12); d.arc((sc(900),sc(545),sc(1000),sc(645)),start=265,end=350,fill=GOLD,width=sc(4)); txt(d,(968,580),'AoA ↑',17,GOLD,True); arrow(d,(1045,485),(1045,380),GREEN,5,15); txt(d,(1070,420),'required lift',15,GREEN,True); arrow(d,(990,500),(1130,530),RED,5,15); txt(d,(1020,465),'induced drag ↑',16,RED,True); txt(d,(1360,305),'HIGHER SPEED',22,BLUE,True,'mm'); txt(d,(1360,343),'lower required AoA',17,MUTED,False,'mm'); arrow(d,(1245,610),(1470,610),BLUE,4,13); airfoil(d,1245,535,235,80,4); txt(d,(1360,680),'smaller induced-drag requirement',16,MUTED,False,'mm'); box(d,300,925,1000,90,'LEVEL FLIGHT CHAIN','SPEED ↓  →  AoA required ↑  →  INDUCED DRAG ↑',GOLD,19,18)
save(im,'pof-induced-drag-speed-aoa-v1')

# Density
im=canvas(); d=ImageDraw.Draw(im); title(d,'AIR DENSITY & AIRCRAFT PERFORMANCE','Hotter, higher or more humid air is less dense — and lower density reduces performance')
for i,(a,b) in enumerate([('ALTITUDE ↑','pressure / density ↓'),('TEMPERATURE ↑','air expands'),('HUMIDITY ↑','water vapour displaces denser dry air')]): box(d,70+i*505,200,460,135,a,b,GOLD,23,16)
d.rounded_rectangle((sc(145),sc(385),sc(760),sc(760)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); txt(d,(452,420),'SAME VOLUME OF AIR',22,NAVY,True,'mm'); d.rounded_rectangle((sc(190),sc(485),sc(420),sc(680)),radius=sc(18),fill='#EEF4F8',outline=BLUE2,width=sc(2)); txt(d,(305,455),'DENSER AIR',18,BLUE,True,'mm'); d.rounded_rectangle((sc(485),sc(485),sc(715),sc(680)),radius=sc(18),fill='#F6F8FA',outline=LINE,width=sc(2)); txt(d,(600,455),'LESS DENSE AIR',18,GOLD,True,'mm')
for x,y in [(220,520),(265,515),(315,535),(360,510),(395,550),(230,585),(285,575),(340,595),(390,620),(245,645),(310,635),(365,655)]: d.ellipse((sc(x-9),sc(y-9),sc(x+9),sc(y+9)),fill=BLUE)
for x,y in [(520,520),(600,545),(675,515),(545,610),(635,630),(690,585)]: d.ellipse((sc(x-9),sc(y-9),sc(x+9),sc(y+9)),fill=GOLD)
arrow(d,(430,585),(475,585),GOLD,6,16); txt(d,(452,715),'density ↓',22,GOLD,True,'mm'); d.rounded_rectangle((sc(820),sc(385),sc(1530),sc(835)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); txt(d,(1175,420),'LOWER DENSITY → LOWER PERFORMANCE',22,NAVY,True,'mm'); d.rectangle((sc(900),sc(685),sc(1445),sc(755)),fill='#D9DEE5')
for x in range(930,1420,90): d.rectangle((sc(x),sc(716),sc(x+42),sc(724)),fill=WHITE)
d.polygon(pts([(1010,650),(1085,630),(1230,635),(1280,650),(1230,665),(1085,668)]),fill='#DCE3EA',outline=NAVY); d.polygon(pts([(1150,640),(1215,575),(1240,585),(1205,642)]),fill='#DCE3EA',outline=NAVY); d.polygon(pts([(1085,638),(1145,598),(1160,605),(1135,642)]),fill='#DCE3EA',outline=NAVY); arrow(d,(1270,620),(1420,500),GREEN,6,18); arrow(d,(930,790),(1390,790),RED,6,18); txt(d,(1160,820),'take-off run ↑',18,RED,True,'mm'); txt(d,(1390,485),'climb performance ↓',17,GREEN,True,'mm'); box(d,840,850,210,120,'LIFT','↓',BLUE,20,24); box(d,1075,850,210,120,'ENGINE POWER','↓',BLUE,20,24); box(d,1310,850,210,120,'PROP EFFICIENCY','↓',BLUE,18,24); txt(d,(800,350),'HIGH / HOT / HUMID  →  DENSITY ↓',23,GOLD,True,'mm')
save(im,'pof-air-density-performance-v1')

# Adverse yaw
im=canvas(); d=ImageDraw.Draw(im); title(d,'ADVERSE YAW DURING A LEFT ROLL','The down-going right aileron creates more lift and induced drag — the nose initially yaws right')
d.rounded_rectangle((sc(70),sc(190),sc(1080),sc(900)),radius=sc(26),fill=CARD,outline=LINE,width=sc(2)); cx,cy=565,555; d.polygon(pts(plane_top(cx,cy)),fill='#E9EDF2',outline=NAVY); d.line((sc(cx),sc(300),sc(cx),sc(815)),fill='#B6C0CC',width=sc(2)); d.ellipse((sc(cx-10),sc(cy-10),sc(cx+10),sc(cy+10)),fill=NAVY); txt(d,(cx+22,cy+2),'CG',16,NAVY,True,'lm')
d.rounded_rectangle((sc(355),sc(270),sc(600),sc(325)),radius=sc(14),fill='#EEF7F2',outline='#B9D8C8',width=sc(2)); txt(d,(477,297),'LEFT ROLL COMMAND',17,GREEN,True,'mm'); d.line((sc(650),sc(300),sc(765),sc(325)),fill=GREEN,width=sc(6)); d.line((sc(707),sc(275),sc(707),sc(350)),fill=LINE,width=sc(2)); txt(d,(785,325),'left wing down',14,MUTED,False,'lm'); d.polygon(pts([(265,545),(335,535),(350,575),(280,595)]),fill=BLUE2,outline=NAVY); d.polygon(pts([(780,535),(855,545),(840,595),(770,575)]),fill=GOLD,outline=NAVY); txt(d,(310,510),'LEFT AILERON ↑',16,BLUE,True,'mm'); txt(d,(815,510),'RIGHT AILERON ↓',16,GOLD,True,'mm'); arrow(d,(320,600),(320,705),MUTED,5,15); arrow(d,(815,600),(815,790),RED,9,22); txt(d,(860,720),'MORE INDUCED DRAG',17,RED,True,'lm'); curved(d,(565,555),250,225,320,RED,7,21); txt(d,(780,355),'INITIAL YAW RIGHT',20,RED,True,'mm'); d.polygon(pts([(555,772),(575,810),(548,840),(530,805)]),fill=GOLD,outline=NAVY); d.line((sc(548),sc(830),sc(685),sc(850)),fill=GOLD,width=sc(4)); txt(d,(700,852),'LEFT RUDDER coordinates',16,GOLD,True,'lm'); box(d,1120,225,410,175,'1  LOWERED RIGHT AILERON','Local AoA ↑\nLocal lift ↑',GOLD,21,18); box(d,1120,435,410,175,'2  INDUCED DRAG INCREASES','More lift / higher AoA\nmeans more induced drag.',RED,21,18); box(d,1120,645,410,175,'3  DRAG PULLS THE NOSE RIGHT','Yaw is opposite the\nintended left roll.',RED,21,18); txt(d,(1125,875),'Correction: coordinated LEFT RUDDER.',20,NAVY,True)
save(im,'pof-adverse-yaw-aileron-drag-v1')

# Update only asset paths; keep stage REFINING and QA flags false.
manifest_path=Path('data/pof-visual-manifest.json'); m=json.loads(manifest_path.read_text())
assets={
'pof-airspeed-indicator-limits-001':'pof-airspeed-indicator-limits-v1',
'pof-skin-friction-boundary-layer-001':'pof-skin-friction-boundary-layer-v1',
'pof-induced-drag-speed-aoa-001':'pof-induced-drag-speed-aoa-v1',
'pof-air-density-performance-001':'pof-air-density-performance-v1',
'pof-adverse-yaw-aileron-drag-001':'pof-adverse-yaw-aileron-drag-v1'}
seen=set()
for v in m['visuals']:
    if v['visual_id'] in assets:
        if v.get('status')!='REFINING': raise SystemExit(f"{v['visual_id']} not REFINING")
        stem=assets[v['visual_id']]; v['assets']={'master_asset':f'public/explanation-images/principles-of-flight/refined-batch-7/{stem}.png','web_asset':f'public/explanation-images/principles-of-flight/refined-batch-7/{stem}.webp'}; seen.add(v['visual_id'])
if seen!=set(assets): raise SystemExit(f'missing manifest ids: {set(assets)-seen}')
manifest_path.write_text(json.dumps(m,indent=2)+'\n')

# Integrity checks.
files=sorted(OUT.glob('*')); assert len(files)==10
hashes=[]
for p in files:
    im=Image.open(p); assert im.size==(1600,1050); assert im.format in {'PNG','WEBP'}; hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
assert len(set(hashes))==10
print('Batch 7 generated: 5 PNG + 5 WebP, all 1600x1050, unique hashes')
