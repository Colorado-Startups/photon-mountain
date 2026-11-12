#!/usr/bin/env python3
# ============================================================================
# PHOTON MOUNTAIN, launch infographic. Single US Letter page, portrait.
# Public / LinkedIn audience. Photon Mountain identity (Alpenglow accent).
# Built 2026-06-18; content reworked 2026-06-21 to match photon_mountain.html:
#   - Fort Collins removed; corridor shown as two tiers (Core + Greater).
#   - Core = Boulder, Golden, Arvada, Denver. Greater = Lafayette, Louisville,
#     Broomfield, Westminster, Longmont.
#   - "What is Photon Mountain" explainer added.
#   - Third pillar is RENEWABLE ENERGY (laser-fusion pillar dropped); pillars
#     run chips / renewable energy / quantum (canonical Lead order).
#   - The stat band was removed to keep the piece strictly the AI compute economy.
#   - Comparison trimmed to four rows (the "Powered by / grid" row removed).
#   - Energy framing is renewable energy (the "clean grid" framing was retired
#     project-wide 2026-06-21).
# Honesty guardrails (per 02_substance/corridor_facts_and_sources.md and
# 02_substance/energy_why_and_how.md):
#   NIST Boulder = an OPERATING cleanroom for integrated photonics; the Quantum
#   Commons (Arvada) fab is TARGETED for 2026 and the CU Boulder nanofab for 2028; "(formerly NREL)" for NLR; the 100%
#   figure is labeled a 2040 GOAL (Polis roadmap), never stated as current.
# Output: photon_mountain.pdf next to this script.
# ============================================================================
import math, os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

BASE = os.path.dirname(os.path.abspath(__file__))

# ---------------- BRAND PALETTE (Photon Mountain v1, locked 2026-07-05) ------
# Every value comes from 04_tools/brand_tokens.py, which is checked against
# 01_doctrine/brand_identity.md by its own --self-test. Nothing is hardcoded
# here, so the palette has exactly one definition.
sys.path.insert(0, os.path.join(BASE, '..', '..', '04_tools'))
import brand_tokens as BT

_c = lambda k: HexColor(BT.ROLE[k])
PAPER      = _c('surface_light')            # Snowfield
WHITE      = _c('surface_paper')
INK        = _c('text_primary')             # Summit Night
STONE      = _c('text_secondary')           # Granite
MIST       = _c('rule_hairline')            # hairline rules on light
DARKPANEL  = _c('surface_dark')             # Summit Night panels
PAPERDIM   = _c('text_dim_on_dark')         # body copy on a dark panel
STONELIGHT = _c('text_secondary_on_dark')   # secondary labels on dark
ACCENT     = _c('accent')                   # Alpenglow, the one loud thing
ACCENT_INK = _c('accent_text_on_light')     # Alpenglow as text on light
ACCENT2    = _c('accent2')                  # Laser Violet, data and secondary
ACCENT2_INK= _c('accent2_text_on_light')    # Violet as text on light
TINT       = _c('surface_tint')             # Dawn Tint

# Compatibility aliases for the layout code below, which was written against
# the retired Colorado AI palette. Each maps to its Photon Mountain role.
# ACCENT2_ON_DARK is deliberately not aliased to the old TURQ name: the
# captions it colors sit on a Summit Night panel, and the on-light violet
# scores 2.37 against that ground, well under AA.
GOLD = ACCENT; GOLDINK = ACCENT_INK; EVER = DARKPANEL; PINE = DARKPANEL
ACCENT2_ON_DARK = _c('accent2_text_on_dark')   # Violet Bright, 5.03 on Summit Night

# ---------------- FONTS ----------------
# Space Grotesk for display, Inter for body, Space Mono for data, per the
# Typography table in brand_identity.md. Paths come from brand_tokens so the
# font set has one definition too. A missing file falls back to a core PDF
# font and flips BRAND_FONTS, which the footer reports.
def _reg(name, role, fallback):
    try:
        pdfmetrics.registerFont(TTFont(name, BT.font_path(role)))
        return name, True
    except Exception:
        return fallback, False

# Display roles (formerly IBM Plex Serif) now take Space Grotesk. The brand
# has no italic, so the old italic role maps to Medium.
SERIF,   s1 = _reg('PMDisplay',     'display_medium', 'Helvetica')
SERIF_SB,s2 = _reg('PMDisplayB',    'display_bold',   'Helvetica-Bold')
SERIF_B, s3 = SERIF_SB, s2
SERIF_I, s4 = SERIF, s1
# Body roles (formerly Work Sans) now take Inter. SemiBold 600 is the heaviest
# weight the spec names, so it serves both the old SB and B roles.
SANS,    n1 = _reg('PMBody',        'body_regular',   'Helvetica')
SANS_M,  n2 = _reg('PMBodyM',       'body_medium',    'Helvetica')
SANS_SB, n3 = _reg('PMBodySB',      'body_semibold',  'Helvetica-Bold')
SANS_B,  n4 = SANS_SB, n3
MONO,    m1 = _reg('PMMono',        'mono_regular',   'Courier')
BRAND_FONTS=all([s1,s2,n1,n2,n3,m1])

# ---------------- PAGE / OPS ----------------
PAGE_W=612; PAGE_H=792; M=30; CX=M; CW=PAGE_W-2*M; BOTTOM=PAGE_H-M
pages=[]; CUR=None; y=M
def newpage():
    global CUR,y; CUR=[]; pages.append(CUR); y=M
def rrect(x,yy,w,h,r=0,fill=None,stroke=None,sw=1): CUR.append(('rrect',x,yy,w,h,r,fill,stroke,sw))
def rect(x,yy,w,h,fill=None,stroke=None,sw=1): CUR.append(('rrect',x,yy,w,h,0,fill,stroke,sw))
def line(x1,y1,x2,y2,color,sw=1): CUR.append(('line',x1,y1,x2,y2,color,sw))
def txt(x,yb,s,font,size,color,align='left'): CUR.append(('text',x,yb,s,font,size,color,align))
def poly(pts,fill=None,stroke=None,sw=1): CUR.append(('poly',pts,fill,stroke,sw))
def circle(cx,cy,r,fill=None,stroke=None,sw=1): CUR.append(('circle',cx,cy,r,fill,stroke,sw))
def arc(cx,cy,r,lw,color,start,extent): CUR.append(('arc',cx,cy,r,lw,color,start,extent))
def insert_rect(idx,x,yy,w,h,r,fill,stroke=None,sw=1): CUR.insert(idx,('rrect',x,yy,w,h,r,fill,stroke,sw))

def wrap(s,font,size,maxw):
    words=s.split(); lines=[]; cur=''
    for w in words:
        t=w if not cur else cur+' '+w
        if stringWidth(t,font,size)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def para(x,yy,s,font,size,color,maxw,leading,align='left'):
    for ln in wrap(s,font,size,maxw):
        txt(x,yy+size*0.80,ln,font,size,color,align); yy+=leading
    return yy

# ---------------- BRAND MARK + GLYPHS ----------------
def summit_sun(x,yy,h,disc=None,peak=None):
    """The Summit Sun mark: a peak in front of a rising light.

    Construction is the locked spec in 01_doctrine/brand_identity.md: a solid
    disc, an isosceles triangle in front of it with base 1.27x the disc
    diameter, apex on the disc's vertical center line and a quarter radius
    above the disc center, so the disc's top rim stays visible above the apex
    and its lower rim is hidden. On light surfaces the disc is Alpenglow and
    the peak is Summit Night. Never inverted: the peak is always in front.

    x, yy is the TOP-left of the mark's box and h is its total height. Note
    this module's y axis increases downward (every primitive renders at
    PAGE_H-y), so "above" here means a smaller y.

    Returns the drawn width.
    """
    disc = ACCENT if disc is None else disc
    peak = INK if peak is None else peak
    r    = h/2.6                    # disc radius
    cy   = yy + r                   # disc top rim sits on the box top edge
    base = 1.27*(2*r)               # triangle base, 1.27x the disc diameter
    cx   = x + base/2               # disc and apex share the center line
    apex = cy - r*0.25              # apex a quarter radius above disc center
    circle(cx,cy,r,fill=disc)
    # Baseline at the box bottom, below the disc's lower rim (yy+2r), so the
    # peak hides that rim while the top rim stays visible above the apex.
    poly([(cx-base/2, yy+h), (cx+base/2, yy+h), (cx, apex)], fill=peak)
    return base
def photon(cx,cy,r,color):           # a photon: a dot
    circle(cx,cy,r,fill=color)
def ray(x1,y1,x2,y2,color,sw=1.1):   # a light ray
    line(x1,y1,x2,y2,color,sw)
def chip_glyph(x,yy,s,color):        # photonic chip: square + pins
    rrect(x,yy,s,s,r=s*0.16,stroke=color,sw=1.4)
    rrect(x+s*0.28,yy+s*0.28,s*0.44,s*0.44,r=s*0.06,fill=color)
    for i in range(3):
        gx=x+s*0.30+i*s*0.20
        line(gx,yy-2.5,gx,yy,color,1.2); line(gx,yy+s,gx,yy+s+2.5,color,1.2)
        line(x-2.5,yy+s*0.30+i*s*0.20,x,yy+s*0.30+i*s*0.20,color,1.2)
        line(x+s,yy+s*0.30+i*s*0.20,x+s+2.5,yy+s*0.30+i*s*0.20,color,1.2)
def atom_glyph(cx,cy,r,color):       # quantum: nucleus + ring + electrons
    circle(cx,cy,r*0.22,fill=color)
    circle(cx,cy,r,stroke=color,sw=1.0)
    for ang in (90,210,330):
        a=math.radians(ang); ex=cx+r*math.cos(a); ey=cy+r*math.sin(a); circle(ex,ey,r*0.13,fill=color)
def sun_glyph(cx,cy,r,color):        # renewable energy: a sun (disc + outer rays)
    circle(cx,cy,r*0.55,fill=color)
    for i in range(8):
        a=math.radians(i*45)
        line(cx+r*0.78*math.cos(a),cy+r*0.78*math.sin(a),cx+r*1.18*math.cos(a),cy+r*1.18*math.sin(a),color,1.4)
def fusion_glyph(cx,cy,r,color):     # (kept for reference; unused)
    for i in range(8):
        a=math.radians(i*45); line(cx,cy,cx+r*math.cos(a),cy+r*math.sin(a),color,1.3)
    circle(cx,cy,r*0.30,fill=color)
def ridge(x,yy,w,h,color):           # mountain-ridge silhouette
    pts=[(x,yy+h)]
    peaks=[(0.0,0.55),(0.12,0.18),(0.24,0.50),(0.38,0.05),(0.52,0.42),(0.66,0.12),
           (0.80,0.46),(0.90,0.22),(1.0,0.50)]
    for fx,fy in peaks: pts.append((x+fx*w,yy+fy*h))
    pts.append((x+w,yy+h))
    poly(pts,fill=color)
def tier_tag(x,yy,label,filled):     # gold pill tag (Core filled, Greater outlined)
    w=stringWidth(label,SANS_B,7.5)+14; h=13
    if filled:
        rrect(x,yy,w,h,r=6.5,fill=GOLD); txt(x+7,yy+h-4,label,SANS_B,7.5,EVER)
    else:
        rrect(x,yy,w,h,r=6.5,stroke=GOLD,sw=1.0); txt(x+7,yy+h-4,label,SANS_B,7.5,GOLD)
    return w

# ============================================================================
# CONTENT
# ============================================================================
def header():
    global y
    pad=16; hx=CX+pad; hw=CW-2*pad; st=len(CUR); hy=y+pad
    txt(hx,hy+8,"COLORADO  ·  THE NEXT ERA OF COMPUTE",SANS_B,9.5,GOLD); hy+=20
    txt(hx,hy+12,"Silicon Valley",SANS_SB,12,STONELIGHT)
    aw=stringWidth("Silicon Valley  ",SANS_SB,12)
    txt(hx+aw,hy+12,">",SANS_B,12,GOLD)
    txt(hx+aw+stringWidth(">  ",SANS_B,12),hy+12,"Photon Mountain",SANS_SB,12,PAPER); hy+=24
    hy=para(hx,hy,"Photon Mountain",SERIF_SB,34,PAPER,hw,37); hy+=4
    hy=para(hx,hy,"Silicon Valley was named for the material of the last era. Photon Mountain is named for the medium of the next, light. Along Colorado's Front Range, one corridor is building the AI age out of photons: light-based chips, renewable energy, and quantum systems.",
        SERIF,12.5,PAPERDIM,hw,16.5)
    hy+=pad; insert_rect(st,CX,y,CW,hy-y,16,INK); y=hy

def corridor():
    global y
    pad=14; top=y; bx=CX; bw=CW; inw=bw-2*pad; tagw=62
    explainer=("Photon Mountain is a real place, the Front Range corridor where Colorado builds the "
               "AI age out of light. A photon is the particle of light, so the name holds both the "
               "photonic chips Colorado can make and the quantum science it can run. Two rings: a "
               "dense core of labs and fabs, and a greater ring of cities.")
    core_def="The dense Boulder, Golden, Arvada, and Denver cluster: the labs, the fabs, and the metro hub."
    greater_def="The Front Range ring around the core, where the corridor's companies and workforce spread out."
    exp_lines=wrap(explainer,SANS,9.5,inw)
    cdef_lines=wrap(core_def,SANS,8.5,inw-tagw)
    gdef_lines=wrap(greater_def,SANS,8.5,inw-tagw)
    # ---- vertical plan (compute height first) ----
    yy=top+pad
    label_y=yy+8; yy+=18
    exp_y=yy; yy+=len(exp_lines)*12.0+8
    core_head_y=yy; yy+=max(13,len(cdef_lines)*11)+8
    core_row_y=yy+22
    yy=core_row_y+28+10
    greater_head_y=yy; yy+=max(13,len(gdef_lines)*11)+6
    cities_y=yy+8; yy+=18
    H=(yy-top)+pad
    # ---- draw: panel, ridge (behind), then content (on top) ----
    rrect(bx,top,bw,H,r=14,fill=EVER)
    ridge(bx,top+H-26,bw,26,PINE)
    txt(bx+pad,label_y,"WHAT IS PHOTON MOUNTAIN",SANS_B,9.5,GOLD)
    ey=exp_y
    for ln in exp_lines: txt(bx+pad,ey+8,ln,SANS,9.5,PAPERDIM); ey+=12.0
    # CORE tier
    tier_tag(bx+pad,core_head_y,"CORE",True)
    dy=core_head_y
    for ln in cdef_lines: txt(bx+pad+tagw,dy+9,ln,SANS,8.5,PAPERDIM); dy+=11
    cities=[("Boulder","Light science + chip fab"),("Golden","Quantum minds + renewable energy"),
            ("Arvada","Photonic-chip fab · 2026"),("Denver","The hub")]
    n=len(cities); x0=bx+pad+26; x1=bx+bw-pad-26
    xs=[x0+(x1-x0)*i/(n-1) for i in range(n)]
    rowY=core_row_y
    for i in range(n-1): ray(xs[i]+8,rowY,xs[i+1]-8,rowY,GOLD,1.2)
    for i,(city,role) in enumerate(cities):
        cx=xs[i]; circle(cx,rowY,6,fill=GOLD); circle(cx,rowY,2.4,fill=EVER)
        for a in (35,145,225,315):
            ar=math.radians(a); line(cx+6.5*math.cos(ar),rowY+6.5*math.sin(ar),cx+10*math.cos(ar),rowY+10*math.sin(ar),GOLD,0.8)
        txt(cx,rowY-12,city,SANS_B,9,PAPER,'center')
        # 84pt keeps the outermost caption inside the page margin. Inter is
        # wider than the font this layout was first set in, and at 118 the
        # Boulder caption stayed one line and overran the left margin.
        for j,ln in enumerate(wrap(role,SANS,7.5,84)[:2]): txt(cx,rowY+16+j*9,ln,SANS,7.5,ACCENT2_ON_DARK,'center')
    # GREATER tier
    tier_tag(bx+pad,greater_head_y,"GREATER",False)
    gy=greater_head_y
    for ln in gdef_lines: txt(bx+pad+tagw,gy+9,ln,SANS,8.5,PAPERDIM); gy+=11
    txt(bx+pad,cities_y+8,"Lafayette   ·   Louisville   ·   Broomfield   ·   Westminster   ·   Longmont",SANS_B,9.5,PAPER)
    y=top+H

def pillars():
    global y
    gap=10; cw=(CW-2*gap)/3.0; h=132; top=y
    data=[("PHOTONIC CHIPS","Chips that compute and move data with light, at far lower power. Colorado fabricates them today at NIST Boulder.",">$10B","2034 market, per analyst forecasts",chip_glyph),
          ("RENEWABLE ENERGY","Power is the constraint on the AI build. Golden's National Laboratory of the Rockies (formerly NREL) is a Department of Energy national lab.","100%","renewable-electricity goal by 2040 (Polis roadmap)",sun_glyph),
          ("QUANTUM SYSTEMS","The Elevate Quantum hub, and Colorado School of Mines' first-in-nation quantum systems engineering bachelor's.","$127M+","federal and state funding awarded, 2024",atom_glyph)]
    for i,(title,body,stat,lab,glyph) in enumerate(data):
        x=CX+i*(cw+gap)
        rrect(x,top,cw,h,r=10,fill=WHITE,stroke=MIST,sw=1)
        if glyph is chip_glyph: chip_glyph(x+15,top+17,15,GOLDINK)
        elif glyph is sun_glyph: sun_glyph(x+23,top+25,9,GOLDINK)
        else: atom_glyph(x+22,top+25,8.5,GOLDINK)
        txt(x+14,top+50,title,SANS_B,9.5,INK)
        yy=top+58
        for ln in wrap(body,SANS,8.3,cw-28)[:4]:
            txt(x+14,yy+8,ln,SANS,8.3,STONE); yy+=10.5
        txt(x+14,top+h-20,stat,SERIF_B,17,GOLDINK)
        sw_=stringWidth(stat+" ",SERIF_B,17)
        for j,ln in enumerate(wrap(lab,SANS,7.5,cw-28-sw_)[:2]):
            txt(x+14+sw_,top+h-26+j*9.5,ln,SANS,7.5,STONE)
    y=top+h

def comparison():
    global y
    top=y; pad=12; h=92
    rrect(CX,top,CW,h,r=10,fill=PAPER,stroke=STONE,sw=1)
    rect(CX,top,4,h,fill=GOLD)
    midx=CX+CW*0.50
    txt(CX+pad+6,top+pad+8,"SILICON VALLEY",SANS_B,9,STONE)
    txt(midx+pad,top+pad+8,"PHOTON MOUNTAIN",SANS_B,9,GOLDINK)
    rows=[("Era","The computer age","The AI age"),
          ("Named for","Silicon, the material","Photon, the light"),
          ("The place","San Jose to Menlo Park","Denver to Boulder"),
          ("Builds","Microchips","Photonic chips, renewable energy, quantum")]
    ry=top+pad+24; rh=(h-pad-28)/len(rows)
    for k,(lab,a,b) in enumerate(rows):
        txt(CX+pad+6,ry+8,a,SANS_M,8.7,STONE)
        txt(midx+pad,ry+8,b,SANS_SB,8.7,INK)
        if k>0: line(CX+pad,ry-2,CX+CW-pad,ry-2,MIST,0.7)
        ry+=rh
    line(midx,top+8,midx,top+h-8,MIST,0.8)
    y=top+h

def footer():
    global y
    line(CX,y,CX+CW,y,ACCENT,1); y+=10
    txt(PAGE_W/2,y+9,"Silicon Valley built the last era out of silicon. Photon Mountain builds the next out of light.",SERIF_I,12.5,INK,'center'); y+=18
    cw0=summit_sun(PAGE_W/2-64,y,14); txt(PAGE_W/2-64+cw0+9,y+11,"Build with light.",SANS_B,11,INK); y+=21
    # Two entities, no individual: the collaboration is the stronger signal,
    # and a personal address would read as one person's side project. No
    # domain here until photonmountain.org is actually live.
    txt(PAGE_W/2,y+7,"Photon Mountain  ·  a Colorado Startups project in collaboration with Colorado AI",SANS,9,STONE,'center'); y+=11
    src="Sources: NIST; Elevate Quantum / Colorado OEDIT; Colorado School of Mines; National Laboratory of the Rockies (formerly NREL); Colorado Energy Office; Xcel; IMARC, Precedence and other analysts. NIST Boulder runs an operating photonics cleanroom; the Arvada fab is targeted for 2026, CU's nanofab for 2028. The 100% renewable-electricity target is a 2040 goal."
    for ln in wrap(src,MONO,7,CW-20):
        txt(PAGE_W/2,y+7,ln,MONO,7,STONE,'center'); y+=9.0

# ---- LAYOUT ----
newpage()
header(); y+=7
corridor(); y+=7
pillars(); y+=7
comparison(); y+=9
footer()

# ---- RENDER ----
PATH=os.path.join(BASE,"photon_mountain.pdf")
c=canvas.Canvas(PATH,pagesize=(PAGE_W,PAGE_H))
overflow=[]
for pi,opl in enumerate(pages):
    c.setFillColor(PAPER); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
    for op in opl:
        k=op[0]
        if k=='rrect':
            _,x,yy,w,h,r,fill,stroke,sw=op; ry=PAGE_H-(yy+h)
            if fill is not None: c.setFillColor(fill)
            if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(sw)
            c.roundRect(x,ry,w,h,r if r>0 else 0,fill=1 if fill is not None else 0,stroke=1 if stroke is not None else 0)
            if yy+h>BOTTOM+1: overflow.append((pi+1,round(yy+h)))
        elif k=='line':
            _,x1,y1,x2,y2,color,sw=op; c.setStrokeColor(color); c.setLineWidth(sw); c.line(x1,PAGE_H-y1,x2,PAGE_H-y2)
        elif k=='text':
            _,x,yb,s,font,size,color,align=op; c.setFont(font,size); c.setFillColor(color); ry=PAGE_H-yb
            if align=='center': c.drawCentredString(x,ry,s)
            elif align=='right': c.drawRightString(x,ry,s)
            else: c.drawString(x,ry,s)
            if yb>BOTTOM+2: overflow.append((pi+1,round(yb)))
        elif k=='poly':
            _,pts,fill,stroke,sw=op; p=c.beginPath(); fst=True
            for (px,py) in pts:
                if fst: p.moveTo(px,PAGE_H-py); fst=False
                else: p.lineTo(px,PAGE_H-py)
            p.close()
            if fill is not None: c.setFillColor(fill)
            if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(sw)
            c.drawPath(p,fill=1 if fill is not None else 0,stroke=1 if stroke is not None else 0)
        elif k=='circle':
            _,cx,cy,r,fill,stroke,sw=op
            if fill is not None: c.setFillColor(fill)
            if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(sw)
            c.circle(cx,PAGE_H-cy,r,fill=1 if fill is not None else 0,stroke=1 if stroke is not None else 0)
        elif k=='arc':
            _,cx,cy,r,lw,color,start,extent=op
            p=c.beginPath(); p.arc(cx-r,PAGE_H-(cy+r),cx+r,PAGE_H-(cy-r),start,extent)
            c.setStrokeColor(color); c.setLineWidth(lw); c.setLineCap(0)
            c.drawPath(p,fill=0,stroke=1); c.setLineCap(1)
    c.showPage()
c.save()
print("PAGES",len(pages),"| brand_fonts=",BRAND_FONTS)
print("OVERFLOW",sorted(set(overflow)) if overflow else "none","(bottom limit =",BOTTOM,")")
print("PDF",PATH)
