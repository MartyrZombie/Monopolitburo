from common import *
COAT = Color(0.62, 0.50, 0.34); TROU = Color(0.40, 0.33, 0.24); GOLD = GOLDC; CHEEK = Color(0.95, 0.55, 0.55); ACC = RED
def set_palette(mono=False):
    global GOLD, CHEEK, ACC, COAT, TROU
    if mono: GOLD, CHEEK, ACC, COAT, TROU = white, Color(0.8, 0.8, 0.8), black, white, white
    else: GOLD, CHEEK, ACC, COAT, TROU = GOLDC, Color(0.95, 0.55, 0.55), RED, Color(0.62, 0.50, 0.34), Color(0.40, 0.33, 0.24)

def limb(c, pts, w, fill=white):
    c.saveState(); c.setLineCap(1); c.setLineJoin(1)
    for lw, col in [(w+2.4, black), (w, fill)]:
        c.setStrokeColor(col); c.setLineWidth(lw); p = c.beginPath(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()

def boot(c, knee, ankle, toe):
    kx, ky = knee; ax, ay = ankle; tl = math.hypot(*toe); tx, ty = toe[0]/tl, toe[1]/tl
    c.saveState(); c.setStrokeColor(black); c.setLineCap(1); c.setLineJoin(1)
    c.setLineWidth(11.4); c.line(kx+(ax-kx)*0.45, ky+(ay-ky)*0.45, ax, ay)
    c.setLineWidth(9.0); c.line(ax, ay, ax+tx*9.5, ay+ty*9.5); c.restoreState()

def mitten(c, x, y, r=5.2):
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1.2); c.circle(x, y, r, fill=1, stroke=1)

def head(c, x, y, look=0, mood='smile'):
    c.saveState(); c.translate(x, y); c.setStrokeColor(black); c.setLineWidth(1.3); c.setFillColor(white); c.circle(0, 0, 14, fill=1, stroke=1)
    dx = look*3.0
    c.setFillColor(CHEEK); c.circle(-8+dx, -5.5, 2.6, fill=1, stroke=0); c.circle(8+dx, -5.5, 2.6, fill=1, stroke=0)
    c.setFillColor(black); c.circle(-4.5+dx, -1.6, 1.4, fill=1, stroke=0); c.circle(4.5+dx, -1.6, 1.4, fill=1, stroke=0)
    c.setFillColor(white); c.setLineWidth(1.1); c.ellipse(-2.6+dx, -6.6, 2.6+dx, -2.2, fill=1, stroke=1)
    c.setLineWidth(1.1); c.setLineCap(1)
    if mood == 'smile': c.arc(-5+dx, -11.5, 5+dx, -4.5, startAng=200, extent=140)
    elif mood == 'worry': c.arc(-4+dx, -14.0, 4+dx, -8.5, startAng=20, extent=140)
    else: c.ellipse(-2+dx, -11.5, 2+dx, -8.0, fill=1, stroke=1)
    c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-13+dx, 6.0); p.curveTo(-9+dx, 1.0, 9+dx, 1.0, 13+dx, 6.0); p.curveTo(8+dx, 8.0, -8+dx, 8.0, -13+dx, 6.0); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(white); c.setLineWidth(0.8); c.arc(-7+dx, 2.2, 3+dx, 6.5, startAng=200, extent=70)
    c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(ACC)
    p = c.beginPath(); p.moveTo(-13.5, 6.0); p.lineTo(13.5, 6.0); p.lineTo(13.0, 12.0); p.lineTo(-13.0, 12.0); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(COAT)
    p = c.beginPath(); p.moveTo(-13.0, 12.0); p.curveTo(-20, 13, -19, 21, -10, 22.5); p.curveTo(-3, 25, 3, 25, 10, 22.5); p.curveTo(19, 21, 20, 13, 13.0, 12.0); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setLineWidth(0.7); c.arc(-14, 17.0, 14, 23.5, startAng=200, extent=140)
    star(c, dx*0.6, 9.0, 3.3, fill=GOLD, stroke=black, lw=0.5); c.restoreState()

def body(c, x, y):
    c.saveState(); c.translate(x, y); c.setStrokeColor(black); c.setLineWidth(1.4); c.setFillColor(COAT)
    p = c.beginPath(); p.moveTo(-12, 47); p.curveTo(-16, 46, -17, 40, -17, 34); p.lineTo(-23, 0); p.curveTo(-10, -4, 10, -4, 23, 0); p.lineTo(17, 34); p.curveTo(17, 40, 16, 46, 12, 47); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setLineWidth(0.9); c.line(0, 44, 0, -2.6); c.setFillColor(GOLD)
    for by in (38, 30, 14, 6): c.circle(-5, by, 1.5, fill=1, stroke=1); c.circle(5, by, 1.5, fill=1, stroke=1)
    c.setFillColor(black); c.rect(-18.6, 20, 37.2, 4.2, fill=1, stroke=0)
    c.setFillColor(GOLD); c.setLineWidth(0.7); c.rect(-3.4, 19.4, 6.8, 5.4, fill=1, stroke=1)
    c.setFillColor(ACC); c.setLineWidth(0.8)
    for sgn in (-1, 1):
        p = c.beginPath(); p.moveTo(sgn*1.5, 47); p.lineTo(sgn*10, 47.5); p.lineTo(sgn*7, 41); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.restoreState()

def suitcase(c, x, y, w=20, h=14):
    c.saveState(); c.setStrokeColor(black); c.setLineWidth(1.2); c.setFillColor(white); c.roundRect(x-w/2, y-h, w, h, 2, fill=1, stroke=1)
    c.setLineWidth(1.0); c.arc(x-4, y-3, x+4, y+4, startAng=0, extent=180); c.line(x-w/2, y-h*0.45, x+w/2, y-h*0.45)
    c.setFillColor(black); c.rect(x-w/2+3, y-h*0.45-1.5, 2, 3, fill=1, stroke=0); c.rect(x+w/2-5, y-h*0.45-1.5, 2, 3, fill=1, stroke=0); c.restoreState()

def paper(c, x, y, ang=0, w=13, h=17, stamp=True):
    c.saveState(); c.translate(x, y); c.rotate(ang); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white); c.rect(-w/2, -h/2, w, h, fill=1, stroke=1)
    c.setLineWidth(0.6)
    for i in range(4): c.line(-w/2+2, h/2-3-i*2.6, w/2-2, h/2-3-i*2.6)
    if stamp: c.setStrokeColor(ACC); c.setLineWidth(1.0); c.circle(1.5, -4.5, 3.0, fill=0, stroke=1)
    c.restoreState()

def kopeikin(c, x, y, s=1.0, pose='salute', mono=False):
    set_palette(mono); c.saveState(); c.translate(x, y); c.scale(s, s)
    def legs():
        for sg in (-1, 1): limb(c, [(sg*8, 18), (sg*9, 6)], 9, TROU); boot(c, (sg*8, 18), (sg*9, 5), (sg, 0))
    if pose == 'salute':
        legs(); limb(c, [(-16, 50), (-22, 38), (-20, 27)], 8.5, COAT); mitten(c, -20, 24); body(c, 0, 12); head(c, 0, 73)
        limb(c, [(16, 52), (28, 62), (17, 80)], 8.5, COAT); mitten(c, 15.5, 82, 4.8)
    elif pose == 'run':
        c.rotate(-10)
        limb(c, [(-7, 16), (-18, 7), (-31, 12)], 9, TROU); boot(c, (-18, 7), (-32, 12.5), (-5, -13))
        limb(c, [(7, 16), (19, 11), (28, 0)], 9, TROU); boot(c, (19, 11), (28.5, -1), (12, 7))
        limb(c, [(-16, 50), (-30, 46), (-36, 58)], 8.5, COAT); mitten(c, -37, 61); body(c, 0, 12); head(c, 0, 73, look=1, mood='open')
        limb(c, [(16, 50), (30, 44), (38, 50)], 8.5, COAT); mitten(c, 40, 51); c.rotate(10)
        c.setStrokeColor(black); c.setLineWidth(1.1); c.setLineCap(1)
        for yy, x0, x1 in [(62, -62, -46), (48, -68, -50), (34, -62, -46)]: c.line(x0, yy, x1, yy)
    elif pose == 'suitcase':
        legs(); limb(c, [(-16, 50), (-23, 38), (-24, 28)], 8.5, COAT); suitcase(c, -25, 22); mitten(c, -24.5, 25); body(c, 0, 12); head(c, 0, 73, look=-1, mood='worry')
        limb(c, [(16, 50), (25, 42), (30, 50)], 8.5, COAT); paper(c, 34, 56, ang=-12); mitten(c, 31, 50)
        c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(0.8); p = c.beginPath(); p.moveTo(19, 84); p.curveTo(16, 79, 22, 79, 19, 84); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.restoreState()
