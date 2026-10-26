from common import *
import mascot as M
from mascot import limb, boot, mitten, head, body, suitcase, paper

def p_money(c):
    c.setStrokeColor(black); c.setLineWidth(0.9)
    for a in (28, 8, -12):
        c.saveState(); c.rotate(a); c.setFillColor(white); c.rect(-3, 2, 9, 17, fill=1, stroke=1); c.setFillColor(black); c.circle(1.5, 10.5, 2.2, fill=1, stroke=0); c.restoreState()
def p_paper(c): paper(c, 3, 8, ang=-12)
def p_ticket(c):
    c.saveState(); c.rotate(-15); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white); c.rect(-4, 2, 20, 10, fill=1, stroke=1)
    c.setDash(1.5, 1.5); c.line(10, 2, 10, 12); c.setDash(); star(c, 3, 7, 2.6, fill=black); c.restoreState()
def p_letter(c):
    c.saveState(); c.rotate(-10); c.setStrokeColor(black); c.setLineWidth(1.0); c.setFillColor(white); c.rect(-5, 2, 22, 14, fill=1, stroke=1); c.line(-5, 16, 6, 8); c.line(17, 16, 6, 8); c.restoreState()
def p_key(c):
    c.saveState(); c.rotate(20); c.setStrokeColor(black); c.setLineWidth(2.2); c.setLineCap(1); c.circle(2, 20, 4.5, fill=0, stroke=1); c.line(2, 15, 2, 0); c.line(2, 2, 7, 2); c.line(2, 6, 6, 6); c.restoreState()
def p_shovel(c):
    c.saveState(); c.rotate(-8); c.setStrokeColor(black); c.setLineWidth(2.6); c.setLineCap(1); c.line(2, -34, 2, 22)
    c.setFillColor(black); p = c.beginPath(); p.moveTo(-5, -34); p.lineTo(9, -34); p.lineTo(8, -46); p.curveTo(5, -52, -1, -52, -4, -46); p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()
def p_boot(c):
    c.saveState(); c.translate(6, 10); c.setFillColor(black); c.roundRect(-5, 0, 10, 15, 3, fill=1, stroke=0); c.ellipse(-16, -5, 6, 5, fill=1, stroke=0); c.setFont('MonoB', 7); c.drawString(8, 12, 'L'); c.restoreState()
def p_wrench(c):
    c.saveState(); c.rotate(-25); c.setStrokeColor(black); c.setLineWidth(3.2); c.setLineCap(1); c.line(2, 0, 2, 20); c.setLineWidth(3.0); c.arc(-4, 17, 8, 29, startAng=130, extent=280); c.restoreState()
def p_brush(c):
    c.saveState(); c.rotate(-20); c.setStrokeColor(black); c.setLineWidth(2.4); c.setLineCap(1); c.line(2, 0, 2, 16)
    c.setFillColor(black); c.rect(-3, 16, 10, 5, fill=1, stroke=0); c.setFillColor(white); c.setLineWidth(1.0); c.rect(-3, 21, 10, 8, fill=1, stroke=1); c.restoreState()
    c.setStrokeColor(black); c.setFillColor(white); c.setLineWidth(1.1)
    p = c.beginPath(); p.moveTo(10, -60); p.lineTo(28, -60); p.lineTo(30, -44); p.lineTo(8, -44); p.close(); c.drawPath(p, fill=1, stroke=1); c.arc(9, -50, 29, -34, startAng=0, extent=180)
def p_parcel(c):
    c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(white); c.rect(-6, 2, 24, 18, fill=1, stroke=1); c.line(6, 2, 6, 20); c.line(-6, 11, 18, 11)
    c.arc(1, 18, 7, 26, startAng=0, extent=360); c.arc(5, 18, 11, 26, startAng=0, extent=360)
def p_coat(c):
    c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(-2, 8); p.lineTo(14, 8); p.lineTo(20, -2); p.lineTo(15, -5); p.lineTo(14, -30); p.lineTo(-2, -30); p.lineTo(-3, -5); p.lineTo(-8, -2); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.line(6, 8, 6, -30); c.setFillColor(black)
    for yy in (0, -9, -18): c.circle(9, yy, 1, fill=1, stroke=0)
def p_pot(c):
    c.saveState(); c.translate(7, 12); c.setStrokeColor(black); c.setLineWidth(1.1); c.setFillColor(white)
    c.arc(-22, -7, -8, 7, startAng=75, extent=210); c.ellipse(-13, -10, 13, 9, fill=1, stroke=1); c.ellipse(-6, 7, 6, 11, fill=1, stroke=1); c.circle(0, 13, 1.8, fill=1, stroke=1)
    c.setFont('MonoB', 9); c.setFillColor(black); c.drawString(15, -2, '?'); c.restoreState()
def _frame(c):
    c.setStrokeColor(black); c.setLineWidth(1.8); c.setFillColor(white); c.rect(-10, 0, 30, 36, fill=1, stroke=1); c.setLineWidth(0.7); c.rect(-7, 3, 24, 30, fill=0, stroke=1)
def p_portrait(c):
    _frame(c); c.setFillColor(black); c.circle(5, 22, 5.5, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(-6, 4); p.curveTo(-6, 16, 16, 16, 16, 4); p.close(); c.drawPath(p, fill=1, stroke=0)
def p_selfportrait(c):
    _frame(c); c.saveState(); cp = c.beginPath(); cp.rect(-7, 3, 24, 30); c.clipPath(cp, stroke=0, fill=0); c.translate(5, 14); c.scale(0.52, 0.52); head(c, 0, 0); c.restoreState()
def p_medal(c): pass
PROPS = dict(money=p_money, paper=p_paper, ticket=p_ticket, letter=p_letter, key=p_key, shovel=p_shovel, boot=p_boot, wrench=p_wrench,
             brush=p_brush, parcel=p_parcel, coat=p_coat, pot=p_pot, portrait=p_portrait, selfportrait=p_selfportrait, medal=p_medal)

def kop(c, x, y, s=1.0, pose='hold', prop=None, mood='smile', mono=True):
    if pose in ('salute', 'run', 'suitcase'): M.kopeikin(c, x, y, s, pose, mono=mono); return
    M.set_palette(mono); c.saveState(); c.translate(x, y); c.scale(s, s)
    for sg in (-1, 1): limb(c, [(sg*8, 18), (sg*9, 6)], 9, M.TROU); boot(c, (sg*8, 18), (sg*9, 5), (sg, 0))
    if pose == 'cheer':
        body(c, 0, 12); head(c, 0, 73, mood=mood)
        limb(c, [(-16, 52), (-29, 62), (-31, 79)], 8.5, M.COAT); mitten(c, -31, 82); limb(c, [(16, 52), (29, 62), (31, 79)], 8.5, M.COAT)
        if prop: c.saveState(); c.translate(31, 82); PROPS[prop](c); c.restoreState()
        mitten(c, 31, 82)
    elif pose == 'sad':
        limb(c, [(-16, 50), (-23, 38), (-22, 26)], 8.5, M.COAT); mitten(c, -22, 23); limb(c, [(16, 50), (23, 38), (22, 26)], 8.5, M.COAT)
        body(c, 0, 12); head(c, 0, 71, mood='worry')
        if prop: c.saveState(); c.translate(24, 22); PROPS[prop](c); c.restoreState()
        mitten(c, 22, 23)
    else:
        limb(c, [(-16, 50), (-23, 38), (-21, 27)], 8.5, M.COAT); mitten(c, -21, 24); body(c, 0, 12); head(c, 0, 73, mood=mood)
        limb(c, [(16, 50), (27, 43), (35, 50)], 8.5, M.COAT)
        if prop: c.saveState(); c.translate(36, 52); PROPS[prop](c); c.restoreState()
        mitten(c, 36, 52)
    if prop == 'medal': star(c, -8, 50, 5.5, fill=white, stroke=black, lw=1.0); c.setStrokeColor(black); c.setLineWidth(1.0); c.line(-8, 56, -8, 60)
    if mood == 'worry' and pose != 'sad':
        c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(0.8); p = c.beginPath(); p.moveTo(19, 84); p.curveTo(16, 79, 22, 79, 19, 84); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.restoreState()
