from common import *
from game import *
from poses import kop
from busts import bust, SPECS
CW, CH = 2.125*IN, 3.1875*IN

def _col(t): return Color(*t)

def frame(c, x, y, w, h):
    c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); c.setStrokeColor(black); c.setLineWidth(0.8); c.rect(x+6, y+6, w-12, h-12)

def header(c, x, y, w, h, lines, fill, ink, price):
    c.setFillColor(fill); c.setStrokeColor(black); c.setLineWidth(0.8); c.rect(x+10, y+h-52, w-20, 42, fill=1, stroke=1)
    c.setFillColor(ink); c.setFont('MonoB', 5.8); c.drawCentredString(x+w/2, y+h-19.5, "DIRECTOR'S APPOINTMENT")
    if len(lines) == 1: hfit(c, lines[0], x+w/2, y+h-40, w-28, 'HeadB', 12.5, color=ink)
    else: hfit(c, lines[0], x+w/2, y+h-33, w-28, 'HeadB', 10.5, color=ink); hfit(c, lines[1], x+w/2, y+h-45.5, w-28, 'HeadB', 10.5, color=ink)
    c.setFillColor(black); c.setFont('MonoB', 7.6); c.drawCentredString(x+w/2, y+h-62, 'PRICE %s' % fmt(price))

def flavor_block(c, x, y, w, top, text, bottom=14):
    fs = 7.6; t = text if text.startswith('[') else '"'+text+'"'
    while len(wrap(t, 'MonoI', fs, w-28))*fs*1.2 > top-(y+bottom) and fs > 5.6: fs -= 0.2
    para(c, t, x+14, top, w-28, 'MonoI', fs, leading=fs*1.2, align='center', color=FLAV)

def deed_front(c, x, y, d):
    g, lines, price, fees, flavor, gloss = d; fill, ink, build = GROUPS[g]; fill = _col(fill); ink = white if ink == 'w' else black; w, h = CW, CH
    frame(c, x, y, w, h); header(c, x, y, w, h, lines, fill, ink, price)
    labels = ['FEE', 'With 1 Workshop', 'With 2 Workshops', 'With 3 Workshops', 'With 4 Workshops', 'With KOMBINAT']; yy = y+h-76
    for i, (a, b) in enumerate(zip(labels, fees)):
        c.setFillColor(black); c.setFont('MonoB' if i in (0, 5) else 'Mono', 8.2); c.drawString(x+14, yy, a); c.drawRightString(x+w-14, yy, fmt(b)); yy -= 10.4
    yy = para(c, 'Whole group, unbuilt: double fee.', x+14, yy+7, w-28, 'Mono', 6.4, leading=7.6, align='center')
    yy -= 5; c.setStrokeColor(black); c.setLineWidth(0.5); c.line(x+14, yy, x+w-14, yy); yy -= 10
    c.setFillColor(black); c.setFont('Mono', 7.4)
    for a, b in [('Pledge / redeem', '%s / %s' % (fmt(pledge(price)), fmt(redeem(price)))), ('Workshop', '%d each' % build), ('Kombinat', '%d + 4 W.' % build)]:
        c.drawString(x+14, yy, a); c.drawRightString(x+w-14, yy, b); yy -= 9.6
    c.line(x+14, yy+4, x+w-14, yy+4); flavor_block(c, x, y, w, yy+2, flavor); vstamp(c, x+w-9, y+8)

def loco(c, cx, cy, s=1.0, bg=white):
    c.saveState(); c.translate(cx, cy); c.scale(s, s); c.setFillColor(black)
    c.rect(-30, 0, 42, 16, fill=1, stroke=0); c.rect(12, 0, 20, 27, fill=1, stroke=0); c.setFillColor(bg); c.rect(17, 13, 10, 9, fill=1, stroke=0)
    c.setFillColor(black); c.rect(-24, 16, 7, 12, fill=1, stroke=0); c.rect(-26, 27, 11, 3, fill=1, stroke=0); c.circle(-8, 18, 4, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(-30, 0); p.lineTo(-42, -8); p.lineTo(-30, -8); p.close(); c.drawPath(p, fill=1, stroke=0)
    for wx, r in [(-20, 7), (-3, 7), (20, 9)]: c.setFillColor(black); c.circle(wx, -6, r, fill=1, stroke=0); c.setFillColor(bg); c.circle(wx, -6, r*0.45, fill=1, stroke=0)
    star(c, -34, 8, 5.5, fill=RED, stroke=white, lw=0.6); c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(0.9)
    for (sx, sy, r) in [(-20, 38, 5), (-10, 46, 7), (4, 52, 8)]: c.circle(sx, sy, r, fill=1, stroke=1)
    c.restoreState()

def art_dam(c, cx, cy):
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(black); c.setLineWidth(1.3); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(-40, -18); p.lineTo(-40, 12); p.lineTo(40, 22); p.lineTo(40, -18); p.close(); c.drawPath(p, fill=1, stroke=1); c.setFillColor(black)
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
    c.saveState(); c.translate(cx, cy); c.setStrokeColor(black); c.setLineWidth(1.3)
    p = c.beginPath(); p.moveTo(-42, 8); p.lineTo(-20, 8); p.lineTo(-12, -22); p.lineTo(12, -22); p.lineTo(20, 8); p.lineTo(42, 8); c.drawPath(p, fill=0, stroke=1); c.setLineWidth(1.0)
    for k in range(2):
        p = c.beginPath(); x0 = -13+k*2; p.moveTo(x0, -10-k*6)
        for j in range(3): p.curveTo(x0+j*8+2, -7-k*6, x0+j*8+6, -13-k*6, x0+(j+1)*8, -10-k*6)
        c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(3.2); c.setLineCap(1); c.line(-16, 16, 16, 52); c.line(16, 16, -16, 52); c.setLineWidth(1.2); c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-23, 9); p.curveTo(-27, 16, -22, 23, -14, 21); p.lineTo(-11, 14); p.close(); c.drawPath(p, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(4, 56); p.curveTo(12, 60, 24, 56, 30, 46); p.lineTo(27, 44); p.curveTo(22, 52, 13, 54, 6, 52); p.close(); c.drawPath(p, fill=1, stroke=1); c.restoreState()

def special_front(c, x, y, lines, art, rows, note, price, flavor):
    w, h = CW, CH; frame(c, x, y, w, h); header(c, x, y, w, h, lines, white, black, price); art(c, x+w/2, y+h-100); yy = y+h-134
    for a, b in rows: c.setFillColor(black); c.setFont('Mono', 7.6); c.drawString(x+14, yy, a); c.drawRightString(x+w-14, yy, b); yy -= 10
    if note: yy = para(c, note, x+14, yy+8, w-28, 'Mono', 7.2, leading=8.8) - 9
    c.setStrokeColor(black); c.setLineWidth(0.5); c.line(x+14, yy+3, x+w-14, yy+3); yy -= 7
    c.setFillColor(black); c.setFont('Mono', 7.2); c.drawString(x+14, yy, 'Pledge / redeem'); c.drawRightString(x+w-14, yy, '%s / %s' % (fmt(pledge(price)), fmt(redeem(price)))); yy -= 5
    c.line(x+14, yy, x+w-14, yy); flavor_block(c, x, y, w, yy-2, flavor); vstamp(c, x+w-9, y+8)

def deed_back(c, x, y, lines, price, gloss):
    w, h = CW, CH; c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); c.setStrokeColor(RED); c.setLineWidth(1.2); c.rect(x+12, y+12, w-24, h-24)
    hdraw(c, 'Pledged', x+w/2, y+h-40, 'HeadB', 13, color=RED); hdraw(c, 'to the State', x+w/2, y+h-52, 'HeadB', 8, color=RED); hammer_sickle(c, x+w/2, y+h-84, 14)
    c.setFillColor(black); fit_center(c, ' '.join(lines).upper(), x+w/2, y+h-114, w-34, 'MonoB', 7.6)
    c.setFont('Mono', 7.4); c.drawCentredString(x+w/2, y+h-126, 'Pledged for %s' % fmt(pledge(price))); c.drawCentredString(x+w/2, y+h-136, 'Redeem for %s' % fmt(redeem(price)))
    c.setStrokeColor(FLAV); c.setLineWidth(0.4); c.line(x+40, y+h-143, x+w-40, y+h-143); fs = 7.2
    while len(wrap(gloss, 'Mono', fs, w-40))*fs*1.18 > (h-148)-18 and fs > 5.2: fs -= 0.2
    para(c, gloss, x+20, y+h-146, w-40, 'Mono', fs, leading=fs*1.18, align='center', color=FLAV); vstamp(c, x+w-14, y+15)

DEEDS = []
for d in D: DEEDS.append((lambda c, x, y, d=d: deed_front(c, x, y, d), lambda c, x, y, d=d: deed_back(c, x, y, d[1], d[2], d[5])))
for lines, fl, gl in RAIL:
    rows = [('FEE', '30'), ('If 2 railways directed', '50'), ('If 3 railways directed', '100'), ('If 4 railways directed', '200')]
    DEEDS.append((lambda c, x, y, l=lines, f=fl, r=rows: special_front(c, x, y, l, lambda cc, cx, cy: loco(cc, cx+3, cy-10, 0.75), r, None, 200, f), lambda c, x, y, l=lines, g=gl: deed_back(c, x, y, l, 200, g)))
for (lines, fl, gl), art in zip(UTIL, (art_dam, art_canal)):
    note = 'If one utility is directed, the fee is 4 times the dice roll. If both are directed, 10 times the dice roll.'
    DEEDS.append((lambda c, x, y, l=lines, a=art, f=fl, n=note: special_front(c, x, y, l, lambda cc, cx, cy: (cc.saveState(), cc.translate(cx, cy-4), cc.scale(0.72, 0.72), a(cc, 0, 0), cc.restoreState()), [], n, 150, f), lambda c, x, y, l=lines, g=gl: deed_back(c, x, y, [l[0]], 150, g)))

def lines_h(t, f, s, w, lead): return len(wrap(t, f, s, w))*s*lead

def char_front(c, x, y, d):
    role, name, rule, flavor, g1, g2 = d; w, h = CW, CH
    c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); c.setFillColor(RED); c.rect(x+6, y+h-32, w-12, 26, fill=1, stroke=0)
    hfit(c, role, x+w/2, y+h-24.5, w-22, 'HeadB', 13, color=white); c.setStrokeColor(black); c.setLineWidth(0.8); c.rect(x+6, y+6, w-12, h-12)
    c.setFillColor(black); fit_center(c, name, x+w/2, y+h-43, w-18, 'MonoB', 7.8)
    tw = w-22; top_text_max = y+h-104; bottom = y+14; k = 1.0
    def total(k): return (lines_h(rule, 'MonoB', 8.4*k, tw, 1.18) + 5 + lines_h('"'+flavor+'"', 'MonoI', 7.0*k, tw, 1.2) + 9 + lines_h(g1, 'Mono', 6.1*k, tw, 1.17) + 3 + lines_h(g2, 'Mono', 6.1*k, tw, 1.17))
    while total(k) > (top_text_max-bottom) and k > 0.8: k -= 0.02
    text_top = max(min(top_text_max, bottom+total(k)+2), bottom+total(k)); art_room = (y+h-48)-text_top; s = min(1.2, max(0.62, (art_room-6)/64.0))
    bust(c, x+w/2, text_top+5, s, SPECS[role]); yy = text_top; c.setStrokeColor(black); c.setLineWidth(0.5); c.line(x+12, yy, x+w-12, yy)
    yy = para(c, rule, x+11, yy-2, tw, 'MonoB', 8.4*k, leading=8.4*k*1.18, align='center')
    yy = para(c, '"'+flavor+'"', x+11, yy-4, tw, 'MonoI', 7.0*k, leading=7.0*k*1.2, align='center', color=FLAV)
    yy -= 5; c.setStrokeColor(FLAV); c.setLineWidth(0.4); c.line(x+34, yy, x+w-34, yy)
    yy = para(c, g1, x+11, yy-2, tw, 'Mono', 6.1*k, leading=6.1*k*1.17, align='center', color=FLAV)
    para(c, g2, x+11, yy-3, tw, 'Mono', 6.1*k, leading=6.1*k*1.17, align='center', color=FLAV); vstamp(c, x+w-9, y+8)

def char_back(c, x, y):
    w, h = CW, CH; c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); c.setFillColor(RED); c.rect(x+6, y+6, w-12, h-12, fill=1, stroke=0)
    c.setStrokeColor(GOLDC); c.setLineWidth(1.2); c.rect(x+13, y+13, w-26, h-26); hammer_sickle(c, x+w/2, y+h/2+18, 26, color=GOLDC)
    hdraw(c, 'Citizen', x+w/2, y+h/2-38, 'HeadB', 14, color=white); c.setFillColor(white); c.setFont('MonoB', 6.8); c.drawCentredString(x+w/2, y+h/2-50, 'PAPERS, PLEASE')
    vstamp(c, x+w-16, y+16, color=Color(1, 0.85, 0.85))

# ---- landscape deck cards ----
LW, LH = CH, CW
def person(c, x, y, s=1.0, hat=False, scarf=False):
    c.saveState(); c.translate(x, y); c.scale(s, s); c.setFillColor(black)
    p = c.beginPath(); p.moveTo(-8, 0); p.lineTo(-6, 26); p.curveTo(-5, 32, 5, 32, 6, 26); p.lineTo(8, 0); p.close(); c.drawPath(p, fill=1, stroke=0); c.circle(0, 38, 6.5, fill=1, stroke=0)
    if hat: c.rect(-8, 41, 16, 3, fill=1, stroke=0); c.rect(-5, 43, 10, 6, fill=1, stroke=0)
    if scarf: p = c.beginPath(); p.moveTo(-7.5, 40); p.curveTo(-6, 49, 6, 49, 7.5, 40); p.lineTo(8, 33); p.lineTo(-8, 33); p.close(); c.drawPath(p, fill=1, stroke=0)
    c.restoreState()
def photo_gag(c, cx, by):
    c.setStrokeColor(black); c.setLineWidth(1.6); c.setFillColor(white); c.rect(cx-31, by, 62, 62, fill=1, stroke=1); c.setLineWidth(0.6); c.rect(cx-28, by+3, 56, 56, fill=0, stroke=1)
    person(c, cx-17, by+6, 0.95, hat=True); person(c, cx+17, by+6, 0.95, scarf=True)
    c.saveState(); c.translate(cx, by+6); c.scale(0.95, 0.95); c.setDash(2, 2); c.setLineWidth(1.0); c.setStrokeColor(black)
    p = c.beginPath(); p.moveTo(-8, 0); p.lineTo(-6, 26); p.curveTo(-5, 32, 5, 32, 6, 26); p.lineTo(8, 0); c.drawPath(p, fill=0, stroke=1); c.circle(0, 38, 6.5, fill=0, stroke=1); c.restoreState()

def deck_card(c, x, y, deck, data):
    title, effect, flavor, gloss, art, sabotage = data; w, h = LW, LH
    c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); hdraw(c, deck, x+w/2, y+h-15, 'HeadB', 8)
    c.setStrokeColor(black); c.setLineWidth(0.8); c.line(x+10, y+h-20, x+w-10, y+h-20)
    if sabotage:
        tw = sw('SABOTAGE', 'HeadB', 6)+8; c.setFillColor(black); c.rect(x+w-10-tw, y+h-18.5, tw, 10, fill=1, stroke=0); hdraw(c, 'Sabotage', x+w-10-tw/2, y+h-16, 'HeadB', 6, color=white, fx=False)
    gs = 6.2; gl = wrap(gloss, 'Mono', gs, w-20)
    if len(gl) > 3: gs = 5.8; gl = wrap(gloss, 'Mono', gs, w-20)
    gtop = y+10+len(gl)*gs*1.18; para(c, gloss, x+10, gtop, w-20, 'Mono', gs, leading=gs*1.18, color=FLAV)
    c.setStrokeColor(FLAV); c.setLineWidth(0.4); c.line(x+10, gtop+3.5, x+w-10, gtop+3.5)
    tx, tw_ = x+84, w-84-10; top = y+h-25; avail = top-(gtop+7); ts, es, fs = 10.5, 7.8, 7.2
    def total(ts, es, fs):
        tl = 1 if sw(title.upper(), 'HeadB', ts) <= tw_ else 2
        return tl*ts*1.12 + 3 + lines_h(effect, 'MonoB', es, tw_, 1.17) + 4 + lines_h(flavor, 'MonoI', fs, tw_, 1.18), tl
    tot, tl = total(ts, es, fs)
    while tot > avail and es > 6.2: es -= 0.2; fs -= 0.2; ts = max(8.5, ts-0.25); tot, tl = total(ts, es, fs)
    yy = top
    if tl == 1: yy -= ts*1.12; hdraw(c, title, tx, yy+1, 'HeadB', ts, anchor='l')
    else:
        words = title.split(); best = 1
        for k in range(1, len(words)):
            if sw(' '.join(words[:k]).upper(), 'HeadB', ts) <= tw_: best = k
        for part in (' '.join(words[:best]), ' '.join(words[best:])): yy -= ts*1.12; hfit(c, part, tx, yy+1, tw_, 'HeadB', ts, anchor='l')
    yy = para(c, effect, tx, yy-3, tw_, 'MonoB', es, leading=es*1.17)
    para(c, '"'+flavor+'"', tx, yy-4, tw_, 'MonoI', fs, leading=fs*1.18, color=FLAV)
    mid = (top+gtop+7)/2
    if art[0] == 'photo': photo_gag(c, x+42, mid-33)
    else: s = 0.68; kop(c, x+{'hold': 33, 'run': 52, 'cheer': 40}.get(art[0], 40), mid-52*s-5, s, art[0], art[1], art[2] or 'smile', mono=True)
    vstamp(c, x+w-10, y+3)
