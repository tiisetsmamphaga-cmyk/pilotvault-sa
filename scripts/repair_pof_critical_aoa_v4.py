#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/explanation-images/principles-of-flight/refined-batch-4'
MANIFEST = ROOT / 'data/pof-visual-manifest.json'
W,H = 1600,1050
NAVY='#071426'; BLUE='#204f7c'; GOLD='#f4b400'; RED='#c92b2b'; MUTED='#415979'; PALE='#f4f7fb'; LINE='#bfd0e4'; WHITE='#ffffff'

def font(size:int,bold:bool=False):
    name='DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    for p in [Path('/usr/share/fonts/truetype/dejavu')/name, Path('/usr/share/fonts/dejavu')/name]:
        if p.exists(): return ImageFont.truetype(str(p),size=size)
    return ImageFont.load_default()

def arrow(d,a,b,fill,width=8,head=20):
    d.line([a,b],fill=fill,width=width)
    ang=math.atan2(b[1]-a[1],b[0]-a[0])
    p1=(b[0]-head*math.cos(ang-math.pi/6),b[1]-head*math.sin(ang-math.pi/6))
    p2=(b[0]-head*math.cos(ang+math.pi/6),b[1]-head*math.sin(ang+math.pi/6))
    d.polygon([b,p1,p2],fill=fill)

def center(d,x,y,text,f,fill):
    box=d.textbbox((0,0),text,font=f)
    d.text((x-(box[2]-box[0])/2,y),text,font=f,fill=fill)

def aerofoil(d,cx,cy,scale,angle_deg,outline=NAVY):
    # Smooth symmetric teaching section with chord endpoints preserved.
    pts=[]
    for i in range(61):
        x=-1+2*i/60
        t=0.12/0.2*(0.2969*math.sqrt(max((x+1)/2,0))-0.1260*((x+1)/2)-0.3516*((x+1)/2)**2+0.2843*((x+1)/2)**3-0.1015*((x+1)/2)**4)
        pts.append((x, t))
    for i in range(60,-1,-1):
        x=-1+2*i/60
        t=0.12/0.2*(0.2969*math.sqrt(max((x+1)/2,0))-0.1260*((x+1)/2)-0.3516*((x+1)/2)**2+0.2843*((x+1)/2)**3-0.1015*((x+1)/2)**4)
        pts.append((x,-t))
    a=math.radians(angle_deg)
    out=[]
    for x,y in pts:
        X=x*scale; Y=-y*scale*1.65
        xr=X*math.cos(a)-Y*math.sin(a); yr=X*math.sin(a)+Y*math.cos(a)
        out.append((cx+xr,cy+yr))
    d.polygon(out,fill='#f7f9fc',outline=outline)
    # chord
    le=(cx-scale*math.cos(a),cy-scale*math.sin(a)); te=(cx+scale*math.cos(a),cy+scale*math.sin(a))
    d.line([le,te],fill=GOLD,width=5)
    return le,te

def flow_lines(d,x0,x1,y_values,fill,separated=False):
    for y in y_values:
        if not separated:
            pts=[(x0,y),(x0+110,y),(x0+240,y-14),(x0+390,y-10),(x1,y)]
        else:
            pts=[(x0,y),(x0+110,y),(x0+220,y-8),(x0+300,y+16),(x0+355,y-22),(x0+420,y+26),(x0+480,y-14),(x1,y+4)]
        d.line(pts,fill=fill,width=4)
        arrow(d,pts[0],(pts[0][0]+55,pts[0][1]),fill,width=3,head=10)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGB',(W,H),WHITE); d=ImageDraw.Draw(im)
    center(d,W/2,42,'CRITICAL ANGLE OF ATTACK',font(46,True),NAVY)
    center(d,W/2,100,'A stall occurs when the aerofoil reaches or exceeds its critical angle of attack.',font(27),MUTED)
    d.line([(800,165),(800,735)],fill=LINE,width=3)

    center(d,400,180,'BELOW CRITICAL AoA',font(32,True),NAVY)
    center(d,1200,180,'CRITICAL AoA / STALL',font(32,True),RED)

    # Left: attached flow, alpha below critical.
    flow_lines(d,85,705,[285,330,375,420],BLUE,False)
    aerofoil(d,405,515,245,9)
    d.arc((285,470,410,595),180,212,fill=RED,width=5)
    d.text((275,560),'α < αcrit',font=font(28,True),fill='#a66a00')
    arrow(d,(105,660),(700,660),BLUE,width=6,head=18)
    center(d,402,690,'RELATIVE AIRFLOW',font(23,True),BLUE)
    center(d,400,750,'Flow remains attached',font(25,True),NAVY)

    # Right: separated flow, alpha reaches/exceeds critical.
    flow_lines(d,895,1515,[285,330,375,420],RED,True)
    aerofoil(d,1205,520,245,18)
    d.arc((1068,442,1228,610),180,235,fill=RED,width=5)
    d.text((1040,575),'α ≥ αcrit',font=font(28,True),fill=RED)
    arrow(d,(905,660),(1500,660),BLUE,width=6,head=18)
    center(d,1202,690,'RELATIVE AIRFLOW',font(23,True),BLUE)
    center(d,1200,750,'Flow separation → lift loss / stall',font(25,True),RED)

    card=(125,820,1475,955)
    d.rounded_rectangle(card,radius=22,fill=PALE,outline=LINE,width=2)
    center(d,800,842,'For a given aerofoil/configuration, critical AoA is essentially fixed.',font(27,True),NAVY)
    center(d,800,888,'Speed, weight and bank change when αcrit is reached — not αcrit itself.',font(24),MUTED)
    center(d,800,930,'Source relationship: Principles of Flight — Fig. 1-16',font(17), '#8aa4c4')

    png=OUT/'pof-critical-aoa-stall-v4.png'; webp=OUT/'pof-critical-aoa-stall-v4.webp'
    im.save(png,'PNG',optimize=True); im.save(webp,'WEBP',quality=94,method=6)

    data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    v=next(x for x in data['visuals'] if x['visual_id']=='pof-critical-aoa-stall-001')
    if v.get('status')!='REFINING': raise SystemExit(f"Expected REFINING, got {v.get('status')}")
    v['assets']={'master_asset':'public/explanation-images/principles-of-flight/refined-batch-4/pof-critical-aoa-stall-v4.png','web_asset':'public/explanation-images/principles-of-flight/refined-batch-4/pof-critical-aoa-stall-v4.webp'}
    v['qa']={'technical':False,'teaching':False,'visual':False,'preview':False,'live':False}
    v['lock']={'approved':False,'replacement_reason':None}
    MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('Wrote critical-AoA v4 without fixed degree value')

if __name__=='__main__': main()
