from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color, black, white
from reportlab.lib.fonts import addMapping
import math

import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
VERSION = 'v' + open(_os.path.join(_ROOT, 'VERSION')).read().strip()
OUT = _os.path.join(_ROOT, 'out') + _os.sep
_os.makedirs(OUT, exist_ok=True)
def outname(part): return OUT + 'Monopolitburo_%s_%s.pdf' % (VERSION, part)
IN = 72.0
W, H = letter
RED = Color(0.80, 0.07, 0.10)
GREY = Color(0.55, 0.55, 0.55)
FLAV = Color(0.36, 0.36, 0.36)
MINT = Color(0xBF/255, 0xDD/255, 0xC8/255)      # chip G
GOLDC = Color(1, 0.85, 0.2)
ORANGE = Color(0.95, 0.52, 0.20)
YEL = Color(0.98, 0.84, 0.25)

G = _os.environ.get('POPPINS_DIR', '/usr/share/fonts/truetype/google-fonts').rstrip('/') + '/'
pdfmetrics.registerFont(TTFont('HeadB', G+'Poppins-Bold.ttf'))
pdfmetrics.registerFont(TTFont('HeadM', G+'Poppins-Medium.ttf'))
T1 = _os.environ.get('TYPE1_DIR', '/usr/share/fonts/X11/Type1').rstrip('/') + '/'
for name, stem in [('Mono', 'c0419bt_'), ('MonoB', 'c0583bt_'), ('MonoI', 'c0582bt_'), ('MonoBI', 'c0611bt_')]:
    face = pdfmetrics.EmbeddedType1Face(T1+stem+'.afm', T1+stem+'.pfb')
    pdfmetrics.registerTypeFace(face)
    pdfmetrics.registerFont(pdfmetrics.Font(name, face.name, 'WinAnsiEncoding'))
    for b in (0, 1):
        for i in (0, 1): addMapping(name, b, i, name)

RUS = {'KOLKHOZ', 'NARKOMAT', 'APPARATCHIK', 'POLUCHKA', 'KOPEIKIN', 'OCHERED', 'GULAG', 'KOMMUNALKA', 'STOLOVAYA', 'PRAVDA',
       'BOLSHOI', 'GOSPLAN', 'GLAVLIT', 'TORGSIN', 'DACHA', 'TURKSIB', 'DNIPROHES', 'BELOMORKANAL', 'MOSFILM', 'GAZ', 'MOSKVA',
       'KOLKHOZNIK', 'SPEKULANT', 'SEKSOT', 'SPETS', 'PRODAVETS', 'DOSKA', 'POCHYOTA', 'KOMANDIROVKA', 'PROPISKA', 'SUBBOTNIK',
       'SHTURMOVSHCHINA', 'PUTYOVKA', 'DONOS', 'PREMIYA', 'TOLKUCHKA', 'GOSSTRAKH', 'BRAK', 'SHABASHKA', 'KUNTSEVO', 'BLAT', 'KOMBINAT'}

def sw(s, font, size): return pdfmetrics.stringWidth(s, font, size)
hwidth = sw

def hdraw(c, s, x, y, font, size, color=black, anchor='c', fx=True, ucyr=False):
    """Headline text with mirrored N and R on English words (faux Cyrillic)."""
    s = s.upper(); w = sw(s, font, size)
    cx = x - w/2 if anchor == 'c' else x - w if anchor == 'r' else x
    c.setFillColor(color); c.setFont(font, size)
    for word in s.split(' '):
        plain = (not fx) or word.strip('"\',.!-:()') in RUS
        for ch in word:
            cw = sw(ch, font, size)
            if ch in 'NR' and not plain:
                c.saveState(); c.translate(cx+cw, y); c.scale(-1, 1); c.setFillColor(color); c.setFont(font, size); c.drawString(0, 0, ch); c.restoreState()
            else:
                c.drawString(cx, y, ch)
                if ch == 'U' and ucyr: c.rect(cx+cw*0.80, y-size*0.17, size*0.105, size*0.26, fill=1, stroke=0)
            cx += cw
        cx += sw(' ', font, size)
    return w

def hfit(c, s, x, y, width, font, size, **kw):
    while sw(s.upper(), font, size) > width and size > 4: size -= 0.25
    hdraw(c, s, x, y, font, size, **kw); return size

def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if sw(t, font, size) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def para(c, text, x, y, width, font, size, leading=None, align='left', color=black):
    leading = leading or size*1.18
    c.setFillColor(color); c.setFont(font, size)
    for ln in wrap(text, font, size, width):
        y -= leading
        (c.drawCentredString(x+width/2, y, ln) if align == 'center' else c.drawString(x, y, ln))
    return y

def fit_center(c, text, cx, y, width, font, size, color=black, minsize=4):
    while sw(text, font, size) > width and size > minsize: size -= 0.25
    c.setFillColor(color); c.setFont(font, size); c.drawCentredString(cx, y, text); return size

def star(c, cx, cy, r, fill=RED, stroke=None, lw=0.6):
    p = c.beginPath()
    for i in range(10):
        ang = math.pi/2 + i*math.pi/5; rr = r if i % 2 == 0 else r*0.40
        (p.moveTo if i == 0 else p.lineTo)(cx+rr*math.cos(ang), cy+rr*math.sin(ang))
    p.close(); c.setFillColor(fill)
    if stroke: c.setStrokeColor(stroke); c.setLineWidth(lw); c.drawPath(p, fill=1, stroke=1)
    else: c.drawPath(p, fill=1, stroke=0)

def hammer_sickle(c, cx, cy, s, color=RED):
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(color); c.setFillColor(color); c.setLineCap(1)
    c.saveState(); clip = c.beginPath(); clip.moveTo(0, 0)
    for a in (214, 250, 290, 330, 10, 50, 90, 126): clip.lineTo(3*s*math.cos(math.radians(a)), 3*s*math.sin(math.radians(a)))
    clip.close(); c.clipPath(clip, stroke=0, fill=0)
    ring = c.beginPath(); ring.circle(0, 0, s); ring.circle(-0.115*s, 0.165*s, 0.79*s); c.drawPath(ring, stroke=0, fill=1, fillMode=0)
    c.restoreState()
    c.setLineWidth(s*0.24); c.line(-0.72*s, -0.56*s, -1.02*s, -0.90*s)
    c.setLineWidth(s*0.20); c.line(0.86*s, -0.92*s, -0.30*s, 0.36*s)
    c.saveState(); c.translate(-0.36*s, 0.43*s); c.rotate(42); c.rect(-0.46*s, -0.17*s, 0.92*s, 0.34*s, fill=1, stroke=0); c.restoreState()
    c.restoreState()

def crop_marks(c, x, y, w, h, l=8, gap=3):
    c.saveState(); c.setStrokeColor(black); c.setLineWidth(0.4)
    for (px, py, dx, dy) in [(x, y, -1, -1), (x+w, y, 1, -1), (x, y+h, -1, 1), (x+w, y+h, 1, 1)]:
        c.line(px+dx*gap, py, px+dx*(gap+l), py); c.line(px, py+dy*gap, px, py+dy*(gap+l))
    c.restoreState()

def vstamp(c, x, y, size=4.6, color=GREY):
    c.setFillColor(color); c.setFont('Mono', size); c.drawRightString(x, y, 'MONOPOLITBURO ' + VERSION)

def sheet_head(c, title, note):
    c.setFillColor(black); c.setFont('MonoB', 9); c.drawString(40, H-26, 'MONOPOLITBURO %s  |  %s' % (VERSION, title))
    size = 8
    while sw(note, 'Mono', size) > W-80 and size > 6: size -= 0.25
    c.setFont('Mono', size); c.drawString(40, H-38, note)

def ddr_logo(c, cx, cy, oval=True):
    w, h = 1.7*IN, 1.0*IN
    c.setFillColor(black)
    (c.ellipse(cx-w/2, cy-h/2, cx+w/2, cy+h/2, fill=1, stroke=0) if oval else c.roundRect(cx-w/2, cy-h/2, w, h, 9, fill=1, stroke=0))
    c.setStrokeColor(white); c.setLineWidth(0.9)
    (c.ellipse(cx-w/2+4, cy-h/2+4, cx+w/2-4, cy+h/2-4, fill=0, stroke=1) if oval else c.roundRect(cx-w/2+4, cy-h/2+4, w-8, h-8, 6, fill=0, stroke=1))
    hdraw(c, 'Made in', cx, cy+9, 'HeadM', 8.5, color=white, fx=False); hdraw(c, 'East Germany', cx, cy-5, 'HeadB', 11.5, color=white, fx=False)
    c.setFillColor(white); c.setFont('MonoB', 5.6); c.drawCentredString(cx, cy-17, 'VEB SPIELWAREN'); star(c, cx, cy+25 if oval else cy+27, 3.6, fill=white)
