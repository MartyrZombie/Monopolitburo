"""Board stickers: name patches, full spaces, corners, deck labels, title banner and maker's mark.

Recreated from the v0.1.0 generator. Sizes are measured from a classic US board (see CLAUDE.md).
"""
from common import *
from mascot import kopeikin

SP_W, SP_H, CORNER = 1.625*IN, 2.5625*IN, 2.5625*IN
SW, SH, CS = SP_W, SP_H, CORNER
PW, PH = 1.5*IN, 1.0*IN                         # name patch
DLW, DLH = 3.45*IN, 2.3*IN                      # deck label
L, T = 11.6*IN, 2.5*IN                          # title bar
BELOW, ABOVE = 0.65*IN, 0.5*IN
MX0, MX1, MH = 3.9*IN, 8.05*IN, 2.4*IN          # mascot piece, measured from the bar's left end

# board position, original name, new name lines
PATCHES = [(1, 'Mediterranean Ave', ['Kolkhoz', '"Red Dawn"']), (3, 'Baltic Ave', ['Machine-', 'Tractor', 'Station']),
    (6, 'Oriental Ave', ["Workers'", 'Barracks']), (8, 'Vermont Ave', ['Kommunalka', 'No. 5']), (9, 'Connecticut Ave', ['Factory', 'Stolovaya']),
    (11, 'St. Charles Place', ['Ivanovo', 'Textile Mill']), (13, 'States Ave', ['State Vodka', 'Distillery']), (14, 'Virginia Ave', ['Red October', 'Chocolate', 'Factory']),
    (16, 'St. James Place', ['Stalingrad', 'Tractor Plant']), (18, 'Tennessee Ave', ['GAZ', 'Automobile', 'Plant']), (19, 'New York Ave', ['Magnitogorsk', 'Steel Works']),
    (21, 'Kentucky Ave', ['Pravda', 'Printing', 'House']), (23, 'Indiana Ave', ['Mosfilm', 'Studio']), (24, 'Illinois Ave', ['Bolshoi', 'Theatre']),
    (26, 'Atlantic Ave', ['Gosplan']), (27, 'Ventnor Ave', ['Narkomat of', 'Heavy', 'Industry']), (29, 'Marvin Gardens', ['Glavlit']),
    (31, 'Pacific Ave', ['Torgsin', 'Store']), (32, 'North Carolina Ave', ['Hotel', 'Moskva']), (34, 'Pennsylvania Ave', ['House on the', 'Embankment']),
    (37, 'Park Place', ['Kuntsevo', 'Dacha']), (39, 'Boardwalk', ['The Kremlin'])]

def heading(c, text, sub=None):
    c.setFillColor(RED); c.rect(36, H-66, W-72, 28, fill=1, stroke=0)
    hdraw(c, text, 46, H-58, 'HeadB', 15, color=white, anchor='l')
    if sub: para(c, sub, 36, H-72, W-72, 'Mono', 9, leading=11.5)

def foot(c, label):
    c.setFont('Mono', 7.5); c.setFillColor(GREY)
    c.drawCentredString(W/2, 20, 'MONOPOLITBURO %s  |  Board stickers  |  %s  |  Sticker paper, 100%% / Actual size' % (VERSION, label))

# ---------------------------------------------------------------- art
def loco(c, cx, cy, s=1.0):
    c.saveState(); c.translate(cx, cy); c.scale(s, s); c.setFillColor(black)
    c.rect(-30, 0, 42, 16, fill=1, stroke=0); c.rect(12, 0, 20, 27, fill=1, stroke=0)
    c.setFillColor(MINT); c.rect(17, 13, 10, 9, fill=1, stroke=0)
    c.setFillColor(black); c.rect(-24, 16, 7, 12, fill=1, stroke=0); c.rect(-26, 27, 11, 3, fill=1, stroke=0); c.circle(-8, 18, 4, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(-30, 0); p.lineTo(-42, -8); p.lineTo(-30, -8); p.close(); c.drawPath(p, fill=1, stroke=0)
    for wx, r in [(-20, 7), (-3, 7), (20, 9)]:
        c.setFillColor(black); c.circle(wx, -6, r, fill=1, stroke=0); c.setFillColor(MINT); c.circle(wx, -6, r*0.45, fill=1, stroke=0)
    star(c, -34, 8, 5.5, fill=RED, stroke=white, lw=0.6)
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(0.9)
    for (sx, sy, r) in [(-20, 38, 5), (-10, 46, 7), (4, 52, 8)]: c.circle(sx, sy, r, fill=1, stroke=1)
    c.restoreState()

def art_dam(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(black); c.setLineWidth(1.3); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(-40, -18); p.lineTo(-40, 12); p.lineTo(40, 22); p.lineTo(40, -18); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(black)
    for i in range(6): c.rect(-33+i*12.5, -18, 6, 18+i*1.6, fill=1, stroke=0)
    c.setLineWidth(1.1)
    for k in range(3):
        p = c.beginPath(); p.moveTo(-42, -24-k*5)
        for j in range(7): p.curveTo(-42+j*12+3, -21-k*5, -42+j*12+9, -27-k*5, -42+(j+1)*12, -24-k*5)
        c.drawPath(p, fill=0, stroke=1)
    c.setFillColor(YEL); p = c.beginPath()
    for i, (px, py) in enumerate([(2, 50), (-12, 26), (-2, 26), (-8, 6), (14, 34), (3, 34), (10, 50)]): (p.moveTo if i == 0 else p.lineTo)(px, py)
    p.close(); c.drawPath(p, fill=1, stroke=1); c.restoreState()

def art_canal(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(black); c.setLineWidth(1.3); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(-42, 8); p.lineTo(-20, 8); p.lineTo(-12, -22); p.lineTo(12, -22); p.lineTo(20, 8); p.lineTo(42, 8); c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(1.0)
    for k in range(2):
        p = c.beginPath(); x0 = -13+k*2; p.moveTo(x0, -10-k*6)
        for j in range(3): p.curveTo(x0+j*8+2, -7-k*6, x0+j*8+6, -13-k*6, x0+(j+1)*8, -10-k*6)
        c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(3.2); c.setLineCap(1); c.line(-16, 16, 16, 52); c.line(16, 16, -16, 52)
    c.setLineWidth(1.2); c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-23, 9); p.curveTo(-27, 16, -22, 23, -14, 21); p.lineTo(-11, 14); p.close(); c.drawPath(p, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(4, 56); p.curveTo(12, 60, 24, 56, 30, 46); p.lineTo(27, 44); p.curveTo(22, 52, 13, 54, 6, 52); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.restoreState()

def art_bond(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.rotate(-6); c.setStrokeColor(black); c.setFillColor(white); c.setLineWidth(1.3)
    c.rect(-36, -24, 72, 48, fill=1, stroke=1); c.setLineWidth(0.7); c.rect(-32, -20, 64, 40, fill=0, stroke=1)
    c.setFillColor(black); c.setFont('HeadB', 7); c.drawCentredString(0, 9, 'STATE BOND')
    c.setFont('MonoB', 5.2); c.drawCentredString(0, 1, 'entirely voluntary')
    c.setLineWidth(0.6); c.line(-24, -9, 8, -9); c.line(-24, -14, 2, -14)
    star(c, 21, -10, 7, fill=RED, stroke=black, lw=0.6); c.restoreState()

def art_partycard(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.rotate(8); c.setStrokeColor(black); c.setLineWidth(1.3)
    c.setFillColor(Color(0.55, 0.05, 0.08)); c.roundRect(-22, -30, 47, 62, 3, fill=1, stroke=1)
    c.setFillColor(RED); c.roundRect(-25, -28, 47, 62, 3, fill=1, stroke=1)
    hammer_sickle(c, -1.5, 10, 11, color=GOLDC)
    c.setFillColor(GOLDC); c.setFont('HeadB', 6.2); c.drawCentredString(-1.5, -13, 'PARTBILET')
    c.setFont('MonoB', 4.6); c.drawCentredString(-1.5, -20, 'do not lose'); c.restoreState()

def art_bang(c, cx, cy):
    c.saveState(); t = c.beginText(); c.setFillColor(ORANGE); c.setStrokeColor(black); c.setLineWidth(1.6)
    size = 96; w = sw('!', 'HeadB', size)
    t.setTextOrigin(cx-w/2, cy-32); t.setFont('HeadB', size); t.setTextRenderMode(2); t.textOut('!'); t.setTextRenderMode(0); c.drawText(t); c.restoreState()
    star(c, cx+25, cy+28, 7, fill=RED, stroke=black, lw=0.7)

def art_teapot(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(black); c.setLineWidth(1.4); c.setFillColor(YEL)
    p = c.beginPath(); p.moveTo(22, 2); p.curveTo(34, 6, 36, 20, 44, 22); p.lineTo(46, 17); p.curveTo(40, 14, 40, -6, 24, -10); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(MINT); c.setLineWidth(4.2); c.arc(-42, -14, -12, 16, startAng=75, extent=210); c.setLineWidth(1.4)
    c.setFillColor(YEL); c.ellipse(-28, -24, 28, 20, fill=1, stroke=1)
    c.rect(-16, -28, 32, 5, fill=1, stroke=1)
    c.ellipse(-13, 16, 13, 24, fill=1, stroke=1); c.circle(0, 27, 3.4, fill=1, stroke=1)
    c.setLineWidth(1.2); c.setLineCap(1)
    for sx in (36, 46, 56):
        p = c.beginPath(); p.moveTo(sx-8, 30); p.curveTo(sx-14, 38, sx-2, 42, sx-8, 50); c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

def person(c, x, y, s=1.0, hat=False, scarf=False):
    c.saveState(); c.translate(x, y); c.scale(s, s); c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-8, 0); p.lineTo(-6, 26); p.curveTo(-5, 32, 5, 32, 6, 26); p.lineTo(8, 0); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.circle(0, 38, 6.5, fill=1, stroke=0)
    if hat: c.rect(-8, 41, 16, 3, fill=1, stroke=0); c.rect(-5, 43, 10, 6, fill=1, stroke=0)
    if scarf:
        p = c.beginPath(); p.moveTo(-7.5, 40); p.curveTo(-6, 49, 6, 49, 7.5, 40); p.lineTo(8, 33); p.lineTo(-8, 33); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

def car(c, cx, cy, s=1.0):
    c.saveState(); c.translate(cx, cy); c.scale(s, s); c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-40, 0); p.lineTo(-40, 14); p.curveTo(-38, 18, -30, 18, -26, 18); p.lineTo(-18, 34); p.lineTo(14, 34); p.lineTo(22, 18)
    p.lineTo(36, 16); p.curveTo(42, 15, 43, 8, 43, 0); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(MINT)
    p = c.beginPath(); p.moveTo(-21, 19); p.lineTo(-15, 31); p.lineTo(-4, 31); p.lineTo(-4, 19); p.close(); c.drawPath(p, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(-1, 19); p.lineTo(-1, 31); p.lineTo(12, 31); p.lineTo(18, 19); p.close(); c.drawPath(p, fill=1, stroke=0)
    for wx in (-24, 26):
        c.setFillColor(black); c.circle(wx, 0, 9, fill=1, stroke=0); c.setFillColor(MINT); c.circle(wx, 0, 3.6, fill=1, stroke=0)
    c.setFillColor(YEL); c.setStrokeColor(black); c.setLineWidth(0.8); c.circle(42, 9, 3, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(46, 11); p.lineTo(66, 17); p.lineTo(66, 1); p.lineTo(46, 7); p.close(); c.setFillColor(Color(0.98, 0.84, 0.25, alpha=0.55)); c.drawPath(p, fill=1, stroke=0)
    c.restoreState()

# ---------------------------------------------------------------- pieces
def name_patch(c, x, y, lines):
    c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, PW, PH, fill=1, stroke=1)
    for i, ln in enumerate(lines): hfit(c, ln, x+PW/2, y+PH-22-i*12.5, PW-8, 'HeadM', 9.5)

def space_base(c, x, y, lines, bottom, size=10):
    c.setFillColor(MINT); c.setStrokeColor(black); c.setLineWidth(1.6); c.rect(x, y, SW, SH, fill=1, stroke=1)
    for i, ln in enumerate(lines): hfit(c, ln, x+SW/2, y+SH-23-i*12.5, SW-14, 'HeadM', size)
    c.setFillColor(black); c.setFont('HeadM', 9); c.drawCentredString(x+SW/2, y+11, bottom)

def rail(name):
    def f(c, x, y): space_base(c, x, y, name, '200'); loco(c, x+SW/2+4, y+SH*0.40, 1.1)
    return f
def util(lines, art):
    def f(c, x, y): space_base(c, x, y, lines, '150', size=9.5); art(c, x+SW/2, y+SH*0.40)
    return f
def tax(lines, art, pay):
    def f(c, x, y): space_base(c, x, y, lines, pay, size=9); art(c, x+SW/2, y+SH*0.36)
    return f
def cardspace(lines, art):
    def f(c, x, y): space_base(c, x, y, lines, '', size=9.5); art(c, x+SW/2, y+SH*0.36)
    return f

def corner_box(c, x, y):
    c.setFillColor(MINT); c.setStrokeColor(black); c.setLineWidth(1.6); c.rect(x, y, CS, CS, fill=1, stroke=1)

def corner_poluchka(c, x, y):
    corner_box(c, x, y); s = CS
    c.saveState(); c.translate(x+s/2, y+s/2); c.rotate(45)
    c.setFillColor(black); c.setFont('MonoB', 7.8)
    c.drawCentredString(0, 60, 'COLLECT 200 RUBLES'); c.drawCentredString(0, 50.5, 'WAGES AS YOU PASS')
    hdraw(c, 'POLUCHKA', 0, 17, 'HeadB', 25, color=RED)
    c.setFillColor(black); c.setFont('MonoB', 9); c.drawCentredString(0, 4, '(PAYDAY)')
    c.restoreState()
    kopeikin(c, x+s*0.70, y+s*0.11, 0.62, 'run')
    c.setFillColor(RED); c.setStrokeColor(black); c.setLineWidth(0.8)
    p = c.beginPath(); ax, ay = x+11, y+17
    p.moveTo(ax, ay); p.lineTo(ax+22, ay+11); p.lineTo(ax+22, ay+4.5); p.lineTo(ax+80, ay+4.5)
    p.lineTo(ax+80, ay-4.5); p.lineTo(ax+22, ay-4.5); p.lineTo(ax+22, ay-11); p.close(); c.drawPath(p, fill=1, stroke=1)

def corner_gulag(c, x, y):
    corner_box(c, x, y)
    b = 1.78*IN; bx, by = x+CS-b, y+CS-b
    c.setFillColor(Color(0.72, 0.74, 0.76)); c.setStrokeColor(black); c.setLineWidth(1.4); c.rect(bx, by, b, b, fill=1, stroke=1)
    hdraw(c, 'The Gulag', bx+b/2, by+b-19, 'HeadB', 13, color=black)
    wx, wy, ww, wh = bx+22, by+14, b-44, b-46
    c.setFillColor(white); c.rect(wx, wy, ww, wh, fill=1, stroke=1)
    c.saveState(); cp = c.beginPath(); cp.rect(wx, wy, ww, wh); c.clipPath(cp, stroke=0, fill=0)
    kopeikin(c, wx+ww/2, wy-52, 1.15, 'suitcase'); c.restoreState()
    c.setStrokeColor(black); c.setLineWidth(3.0)
    for i in range(1, 5): c.line(wx+i*ww/5, wy, wx+i*ww/5, wy+wh)
    c.setLineWidth(1.4); c.rect(wx, wy, ww, wh, fill=0, stroke=1)
    c.saveState(); c.translate(x+(CS-b)/2+4, y+(CS-b)+b/2); c.rotate(90); hdraw(c, 'Visiting', 0, 0, 'HeadM', 11); c.restoreState()
    hdraw(c, 'A Relative', x+(CS-b)+b/2, y+(CS-b)/2-4, 'HeadM', 11)

def corner_ochered(c, x, y):
    corner_box(c, x, y)
    c.saveState(); c.translate(x+CS/2, y+CS/2); c.rotate(45)
    hdraw(c, 'Ochered', 0, 52, 'HeadB', 19, color=RED)
    c.setStrokeColor(black); c.setLineWidth(1.3); c.setFillColor(white); c.rect(40, -30, 30, 50, fill=1, stroke=1)
    c.setFillColor(black); c.rect(47, -30, 16, 30, fill=1, stroke=0)
    c.setFont('HeadB', 6); c.drawCentredString(55, 8, 'SHOP')
    c.setFont('MonoB', 4.5); c.drawCentredString(55, 2.5, 'CLOSED')
    for i, (hat, scarf) in enumerate([(False, True), (True, False), (False, False), (True, False), (False, True)]):
        person(c, 24-i*19, -30, 0.92, hat, scarf)
    c.setFillColor(black); c.setFont('MonoB', 9); c.drawCentredString(0, -48, '(THE QUEUE)')
    c.setFont('MonoB', 6.6); c.drawCentredString(0, -60, 'SKIP A TURN, TAKE 1 BLAT')
    c.restoreState()

def corner_knock(c, x, y):
    corner_box(c, x, y)
    c.saveState(); c.translate(x+CS/2, y+CS/2); c.rotate(45)
    hdraw(c, 'The Midnight', 0, 54, 'HeadB', 14.5, color=black)
    car(c, -8, -12, 1.12)
    c.setFillColor(YEL); c.setStrokeColor(black); c.setLineWidth(0.9); c.circle(48, 34, 9, fill=1, stroke=1)
    c.setFillColor(MINT); c.circle(52, 37, 8, fill=1, stroke=0)
    hdraw(c, 'Knock', 0, -46, 'HeadB', 22, color=RED)
    c.setFillColor(black); c.setFont('MonoB', 6.6); c.drawCentredString(0, -58, 'GO DIRECTLY TO THE GULAG')
    c.restoreState()

def deck_label(c, x, y, title, fill, ink, art):
    c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, DLW, DLH, fill=1, stroke=1)
    c.setFillColor(fill); c.setStrokeColor(black); c.setLineWidth(1.0); c.roundRect(x+0.2*IN, y+0.2*IN, DLW-0.4*IN, DLH-0.4*IN, 6, fill=1, stroke=1)
    art(c, x+DLW/2, y+DLH/2+14)
    hfit(c, title, x+DLW/2, y+0.2*IN+15, DLW-0.4*IN-20, 'HeadB', 12, color=ink)

# ---------------------------------------------------------------- title banner
def title_size():
    size = 92
    while sw('MONOPOLITBURO', 'HeadB', size) > L*0.76: size -= 0.5
    return size

def bar_art(c):
    c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.4); c.rect(0, -BELOW, L, T+BELOW+ABOVE, fill=1, stroke=1)
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1.2); c.rect(0, 0, L, T, fill=1, stroke=1)
    ins = 0.10*IN; c.setFillColor(RED); c.rect(ins, ins, L-2*ins, T-2*ins, fill=1, stroke=0)
    size = title_size(); ty = T/2 - size*0.35
    hdraw(c, 'MONOPOLITBURO', L/2+3.5, ty-3.5, 'HeadB', size, color=black, ucyr=True)
    hdraw(c, 'MONOPOLITBURO', L/2, ty, 'HeadB', size, color=white, ucyr=True)
    hammer_sickle(c, L*0.056, T/2, T*0.21, color=GOLDC); hammer_sickle(c, L*0.944, T/2, T*0.21, color=GOLDC)
    c.setFillColor(black); c.setFont('MonoB', 17); c.drawCentredString(L/2, -BELOW+15, 'FIVE-YEAR PLAN IN FOUR YEARS!')
    c.setStrokeColor(GREY); c.setLineWidth(0.6)
    for mx in (MX0, MX1): c.line(mx, T+2, mx, T+ABOVE-2)

def split_x():
    size = title_size(); x = L/2 - sw('MONOPOLITBURO', 'HeadB', size)/2; gaps = []
    for ch in 'MONOPOLITBURO':
        x += sw(ch, 'HeadB', size); gaps.append(x)
    return min(gaps, key=lambda g: abs(g - L/2))

def mascot_piece(c, x, y):
    w = MX1-MX0
    c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.4); c.rect(x, y, w, MH, fill=1, stroke=1)
    c.saveState(); cp = c.beginPath(); cp.rect(x, y, w, MH); c.clipPath(cp, stroke=0, fill=0)
    kopeikin(c, x + (L/2 - MX0), y-92, 2.05, 'salute'); c.restoreState()
