from common import *
from mascot import limb
KHAKI = Color(0.62, 0.50, 0.34)
def _poly(c, pts, fill=1, stroke=1):
    p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, fill=fill, stroke=stroke)
def gear(c, cx, cy, r, teeth=8):
    c.setFillColor(black)
    for i in range(teeth):
        a = 2*math.pi*i/teeth; c.saveState(); c.translate(cx+r*math.cos(a), cy+r*math.sin(a)); c.rotate(math.degrees(a)); c.rect(-r*0.22, -r*0.2, r*0.44, r*0.4, fill=1, stroke=0); c.restoreState()
    c.circle(cx, cy, r, fill=1, stroke=0); c.setFillColor(white); c.circle(cx, cy, r*0.42, fill=1, stroke=0)

def bust(c, cx, cy, s, spec):
    g = spec.get; c.saveState(); c.translate(cx, cy); c.scale(s, s); c.setLineJoin(1); c.setLineCap(1); c.setStrokeColor(black); c.setLineWidth(1.2)
    if g('desk'): c.line(-46, 0, 46, 0)
    if g('back'): g('back')(c)
    c.setFillColor(g('coat', white))
    p = c.beginPath(); p.moveTo(-26, 0); p.curveTo(-26, 18, -14, 22, 0, 22); p.curveTo(14, 22, 26, 18, 26, 0); p.close(); c.drawPath(p, fill=1, stroke=1)
    col = g('collar')
    if col == 'tie': c.setFillColor(black); _poly(c, [(-2.5, 21), (2.5, 21), (3.5, 4), (0, 0.5), (-3.5, 4)], stroke=0); c.line(-9, 21.5, -2, 10); c.line(9, 21.5, 2, 10)
    elif col == 'bowtie': c.setFillColor(black); _poly(c, [(0, 17), (-8, 21), (-8, 13)], stroke=0); _poly(c, [(0, 17), (8, 21), (8, 13)], stroke=0); c.line(-9, 21.5, -3, 8); c.line(9, 21.5, 3, 8)
    elif col == 'scarf':
        c.setFillColor(white); c.roundRect(-11, 16, 22, 7, 3, fill=1, stroke=1); c.rect(3, 0.6, 7, 17, fill=1, stroke=1)
        for yy in (4, 8, 12): c.line(3, yy, 10, yy)
    elif col == 'pearls':
        c.setFillColor(white)
        for i in range(9): a = math.radians(200+i*17.5); c.circle(11*math.cos(a), 24+9*math.sin(a), 1.7, fill=1, stroke=1)
    elif col == 'tunic':
        c.line(0, 21, 0, 0.6); c.setFillColor(RED); _poly(c, [(-1.5, 22), (-10, 22), (-7, 16)]); _poly(c, [(1.5, 22), (10, 22), (7, 16)]); c.setFillColor(black)
        for yy in (14, 8): c.circle(-4, yy, 1, fill=1, stroke=0); c.circle(4, yy, 1, fill=1, stroke=0)
    elif col == 'apron': c.setFillColor(white); c.rect(-10, 0.6, 20, 17, fill=1, stroke=1); c.line(-10, 17.6, -6, 22); c.line(10, 17.6, 6, 22)
    elif col == 'work': c.line(-8, 21.5, 0, 12); c.line(8, 21.5, 0, 12); c.line(0, 12, 0, 0.6)
    if g('medal'): star(c, -13, 9, 4.2, fill=RED, stroke=black, lw=0.7); c.line(-13, 13.5, -13, 17)
    hat = g('hat')
    if hat == 'kerchief':
        c.setFillColor(g('kcolor', RED)); c.circle(0, 35, 14.8, fill=1, stroke=1); _poly(c, [(-4, 21.5), (4, 21.5), (7, 14), (0, 18), (-7, 14)])
        c.setFillColor(white); c.ellipse(-9.5, 22.5, 9.5, 43, fill=1, stroke=1)
        if g('dots'):
            c.setFillColor(black)
            for (dx, dy) in [(-11, 40), (-7, 46.5), (0, 48.5), (7, 46.5), (11, 40), (-12.5, 32), (12.5, 32)]: c.circle(dx, dy, 0.9, fill=1, stroke=0)
    else: c.setFillColor(white); c.circle(0, 34, 12.5, fill=1, stroke=1)
    hair = g('hair'); c.setFillColor(black)
    if hair == 'short': p = c.beginPath(); p.moveTo(-12.3, 37); p.curveTo(-11, 48, 9, 50, 12.3, 38); p.curveTo(6, 43, -4, 44, -12.3, 37); p.close(); c.drawPath(p, fill=1, stroke=0)
    elif hair == 'bald': c.circle(-12, 32, 2.6, fill=1, stroke=0); c.circle(12, 32, 2.6, fill=1, stroke=0)
    elif hair == 'wild':
        pts = []
        for i in range(15): a = math.radians(-10+i*200/14); r = 19 if i % 2 else 12.2; pts.append((r*math.cos(a), 35+r*math.sin(a)))
        _poly(c, pts, stroke=0); c.setFillColor(white); c.ellipse(-10.5, 23, 10.5, 42, fill=1, stroke=0); c.setFillColor(black)
    elif hair == 'bun':
        p = c.beginPath(); p.moveTo(-12.4, 33); p.curveTo(-13, 50, 13, 50, 12.4, 33); p.curveTo(8, 42, -8, 42, -12.4, 33); p.close(); c.drawPath(p, fill=1, stroke=0); c.circle(0, 50, 4.6, fill=1, stroke=0)
    elif hair == 'waves': p = c.beginPath(); p.moveTo(-12.6, 26); p.curveTo(-16, 46, 16, 46, 12.6, 26); p.curveTo(11, 40, -11, 40, -12.6, 26); p.close(); c.drawPath(p, fill=1, stroke=0)
    sm = g('mouth', 'smile'); c.setLineWidth(1.0)
    if g('glasses'):
        c.setFillColor(white); c.circle(-4.6, 33, 3.6, fill=1, stroke=1); c.circle(4.6, 33, 3.6, fill=1, stroke=1); c.line(-1, 33.5, 1, 33.5)
        c.setFillColor(black); c.circle(-4.6, 33, 0.9, fill=1, stroke=0); c.circle(4.6, 33, 0.9, fill=1, stroke=0)
    else:
        c.setFillColor(black); c.circle(-4.4, 33.5, 1.2, fill=1, stroke=0); c.circle(4.4, 33.5, 1.2, fill=1, stroke=0)
        if g('lashes'): c.setLineWidth(0.7); c.line(-6.2, 34.6, -7.6, 36); c.line(6.2, 34.6, 7.6, 36); c.setLineWidth(1.0)
    if g('beard'): c.setFillColor(white); p = c.beginPath(); p.moveTo(-10.5, 31); p.curveTo(-11, 14, 11, 14, 10.5, 31); p.curveTo(6, 25, -6, 25, -10.5, 31); p.close(); c.drawPath(p, fill=1, stroke=1)
    if sm == 'smile': c.arc(-4.5, 25.5, 4.5, 31.5, startAng=200, extent=140)
    elif sm == 'smirk': c.arc(-2, 25.5, 6, 30.5, startAng=210, extent=120)
    elif sm == 'o': c.ellipse(-1.8, 25.5, 1.8, 29, fill=0, stroke=1)
    else: c.line(-3.5, 27, 3.5, 27)
    c.setLineWidth(1.2)
    if hat == 'flatcap': c.setFillColor(black); p = c.beginPath(); p.moveTo(-13.5, 40); p.curveTo(-14, 52, 12, 53, 14, 42); p.lineTo(20, 40); p.lineTo(13, 38.5); p.close(); c.drawPath(p, fill=1, stroke=0)
    elif hat == 'fedora':
        c.setFillColor(black); c.ellipse(-19, 39, 19, 45, fill=1, stroke=0); _poly(c, [(-11, 42), (-9, 55), (9, 55), (11, 42)], stroke=0)
        c.setStrokeColor(white); c.setLineWidth(1.6); c.line(-10.6, 45.6, 10.6, 45.6); c.setStrokeColor(black); c.setLineWidth(1.2)
    elif hat == 'budenovka':
        c.setFillColor(KHAKI); p = c.beginPath(); p.moveTo(-13.5, 36); p.curveTo(-13, 50, -4, 52, 0, 62); p.curveTo(4, 52, 13, 50, 13.5, 36); p.curveTo(6, 40, -6, 40, -13.5, 36); p.close(); c.drawPath(p, fill=1, stroke=1)
        _poly(c, [(-13.5, 36), (-15.5, 24), (-11.5, 27)]); _poly(c, [(13.5, 36), (15.5, 24), (11.5, 27)]); star(c, 0, 45, 4.4, fill=RED, stroke=black, lw=0.6)
    elif hat == 'shopcap': c.setFillColor(white); p = c.beginPath(); p.moveTo(-10, 43.5); p.lineTo(-11, 53); p.curveTo(-4, 56, 4, 56, 11, 53); p.lineTo(10, 43.5); p.curveTo(4, 46, -4, 46, -10, 43.5); p.close(); c.drawPath(p, fill=1, stroke=1)
    elif hat == 'ladyhat':
        c.setFillColor(black); c.ellipse(-21, 40, 21, 47, fill=1, stroke=0); c.ellipse(-10, 42, 10, 54, fill=1, stroke=0)
        c.setFillColor(white); c.setLineWidth(1.0); p = c.beginPath(); p.moveTo(8, 50); p.curveTo(14, 66, 28, 62, 26, 50); p.curveTo(22, 56, 16, 56, 12, 48); p.close(); c.drawPath(p, fill=1, stroke=1); c.setLineWidth(1.2)
    if g('ear'): c.setFillColor(white); c.ellipse(11, 27, 21, 41, fill=1, stroke=1); c.arc(13.5, 30, 18.5, 38, startAng=-60, extent=200)
    if g('prop'): g('prop')(c)
    c.restoreState()

def pr_hammer(c):
    limb(c, [(22, 12), (32, 22), (30, 36)], 6.5); c.setStrokeColor(black); c.setLineWidth(2.6); c.line(30, 30, 30, 56)
    c.setFillColor(black); c.rect(22, 52, 18, 8, fill=1, stroke=0); c.setFillColor(white); c.setLineWidth(1.0); c.circle(30, 38, 4.2, fill=1, stroke=1)
def bk_factory(c):
    c.setFillColor(black); c.rect(-46, 0, 16, 26, fill=1, stroke=0); c.rect(-42, 26, 5, 18, fill=1, stroke=0); c.rect(30, 0, 16, 20, fill=1, stroke=0); c.rect(36, 20, 5, 20, fill=1, stroke=0)
    c.setFillColor(white); c.setLineWidth(0.9)
    for (x, y, r) in [(-38, 50, 4), (-32, 56, 5.5), (40, 46, 4), (46, 52, 5.5)]: c.circle(x, y, r, fill=1, stroke=1)
def pr_turnip(c):
    limb(c, [(22, 12), (31, 16)], 6.5); c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(36, 12); p.curveTo(24, 14, 26, 32, 36, 32); p.curveTo(46, 32, 48, 14, 36, 12); p.close(); c.drawPath(p, fill=1, stroke=1); c.line(36, 12, 36, 6); c.setFillColor(black)
    for a in (-30, 0, 30): c.saveState(); c.translate(36, 32); c.rotate(a); c.ellipse(-2.6, 0, 2.6, 14, fill=1, stroke=0); c.restoreState()
    c.setFillColor(white); c.circle(31, 17, 4.2, fill=1, stroke=1)
def pr_watches(c):
    c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(white); _poly(c, [(6, 20), (24, 12), (22, 0.6), (6, 0.6)])
    for (x, y) in [(11, 14), (17, 10), (11, 6), (17, 3.6)]: c.setFillColor(white); c.circle(x, y, 2.3, fill=1, stroke=1); c.setLineWidth(0.6); c.line(x, y, x, y+1.5); c.line(x, y, x+1.2, y); c.setLineWidth(1.1)
def pr_notebook(c):
    limb(c, [(-22, 12), (-31, 18)], 6.5); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white); c.saveState(); c.translate(-38, 22); c.rotate(12); c.rect(-7, -9, 14, 18, fill=1, stroke=1)
    for i in range(4): c.line(-4.5, 5-i*3.4, 4.5, 5-i*3.4)
    c.restoreState(); c.circle(-31, 18, 4.2, fill=1, stroke=1)
def pr_gear(c):
    gear(c, 38, 30, 9); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white); c.saveState(); c.translate(-36, 22); c.rotate(-18); c.rect(-14, -3, 28, 6, fill=1, stroke=1)
    for i in range(9): c.line(-12+i*3, 3, -12+i*3, 0.5 if i % 2 else -0.8)
    c.rect(-3, -4.5, 6, 9, fill=0, stroke=1); c.restoreState()
def pr_quill(c):
    limb(c, [(22, 12), (31, 18)], 6.5); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(30, 16); p.curveTo(34, 34, 46, 44, 50, 52); p.curveTo(40, 48, 32, 38, 30, 16); p.close(); c.drawPath(p, fill=1, stroke=1); c.line(30, 16, 46, 46)
    c.circle(31, 18, 4.2, fill=1, stroke=1); c.saveState(); c.translate(-36, 14); c.rotate(-8); c.rect(-9, -11, 18, 22, fill=1, stroke=1)
    for i in range(5): c.line(-6, 7-i*3.6, 6 if i % 2 else 3, 7-i*3.6)
    c.restoreState()
def pr_sabre(c):
    c.setStrokeColor(black); c.setLineWidth(2.2); p = c.beginPath(); p.moveTo(30, 4); p.curveTo(40, 22, 44, 40, 40, 58); c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(3.4); c.line(27, 0.5, 31, 8); c.setLineWidth(1.4); c.arc(24, 2, 36, 12, startAng=200, extent=160)
def pr_stamp(c):
    c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(white)
    for i in range(5): c.rect(-44, 0.8+i*2.6, 17, 2.6, fill=1, stroke=1)
    c.rect(22, 0.8, 20, 2.2, fill=1, stroke=1); limb(c, [(21, 14), (31, 16)], 6.5)
    c.setFillColor(black); c.rect(27, 3.4, 9, 4, fill=1, stroke=0); c.rect(30, 7, 3, 6, fill=1, stroke=0); c.setFillColor(white); c.setLineWidth(1.0); c.circle(31.5, 15.5, 4.2, fill=1, stroke=1)
def pr_scales(c):
    c.setStrokeColor(black); c.setLineWidth(1.4); c.line(36, 0.6, 36, 26); c.line(26, 24, 46, 28); c.setLineWidth(0.8)
    for (x, y) in [(26, 24), (46, 28)]: c.line(x, y, x-4, y-9); c.line(x, y, x+4, y-9); c.setFillColor(white); c.arc(x-5, y-13, x+5, y-5, startAng=180, extent=180); c.line(x-5, y-9, x+5, y-9)
    c.setFillColor(white); c.setLineWidth(1.0); c.rect(-44, 0.8, 14, 10, fill=1, stroke=1); c.rect(-42, 10.8, 10, 8, fill=1, stroke=1)
def pr_typewriter(c):
    c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(black); _poly(c, [(24, 0.8), (46, 0.8), (43, 12), (27, 12)], stroke=0)
    c.setFillColor(white); c.rect(28, 12, 14, 12, fill=1, stroke=1); c.line(30, 20, 40, 20); c.line(30, 16.5, 38, 16.5)
    for i in range(5): c.circle(29+i*3.2, 5, 1, fill=1, stroke=0)
    for i in range(4): c.circle(30.6+i*3.2, 8.5, 1, fill=1, stroke=0)

SPECS = {
 'Stakhanovite': dict(hat='kerchief', kcolor=RED, lashes=True, collar='work', prop=pr_hammer, medal=True),
 'Red Director': dict(hat='flatcap', collar='tie', mouth='flat', back=bk_factory),
 'Kolkhoznik': dict(hat='kerchief', kcolor=white, dots=True, lashes=True, collar='apron', prop=pr_turnip),
 'Spekulant': dict(hat='fedora', mouth='smirk', collar='work', prop=pr_watches),
 'Seksot': dict(hair='bun', glasses=True, mouth='flat', ear=True, collar='work', prop=pr_notebook),
 'Old Bolshevik': dict(hair='bald', glasses=True, beard=True, collar='tie', medal=True),
 'Spets': dict(hair='short', glasses=True, collar='bowtie', mouth='o', prop=pr_gear),
 'Poet': dict(hair='wild', collar='scarf', prop=pr_quill),
 'Red Army Officer': dict(hat='budenovka', coat=KHAKI, collar='tunic', mouth='flat', prop=pr_sabre),
 'Apparatchik': dict(hair='short', glasses=True, collar='tie', mouth='flat', desk=True, prop=pr_stamp),
 'Prodavets': dict(hair='waves', hat='shopcap', lashes=True, collar='apron', mouth='smirk', desk=True, prop=pr_scales),
 'Former Person': dict(hair='waves', hat='ladyhat', lashes=True, collar='pearls', mouth='flat', desk=True, prop=pr_typewriter),
}
