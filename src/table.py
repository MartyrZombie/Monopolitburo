from common import *
from game import *
from mascot import kopeikin
AW, AH = 6*IN, 4*IN
YW, YH = 7.5*IN, 1.6*IN       # Year track sticker

def rich(c, x, y, w, text, size=9.0, lead=1.2, bullet=False, color=black):
    indent = 9 if bullet else 0; pre = ''
    if ':' in text[:34] and not text.startswith('('): pre = text[:text.index(':')+1]
    lines = wrap(text, 'Mono', size, w-indent)
    if bullet: c.setFillColor(RED); c.rect(x+1, y-size*lead+1.6, 3.2, 3.2, fill=1, stroke=0)
    for i, ln in enumerate(lines):
        y -= size*lead; c.setFillColor(color)
        if i == 0 and pre and ln.startswith(pre):
            c.setFont('MonoB', size); c.drawString(x+indent, y, pre); c.setFont('Mono', size); c.drawString(x+indent+sw(pre, 'Mono', size), y, ln[len(pre):])
        else: c.setFont('Mono', size); c.drawString(x+indent, y, ln)
    return y

def label(c, x, y, text): hdraw(c, text, x, y-10, 'HeadB', 9.6, color=RED, anchor='l'); return y-12

def aid_frame(c, x, y, title, sub):
    c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, AW, AH); c.setFillColor(RED); c.rect(x+8, y+AH-40, AW-16, 32, fill=1, stroke=0)
    hdraw(c, title, x+20, y+AH-30, 'HeadB', 15, color=white, anchor='l'); c.setFillColor(white); c.setFont('MonoB', 7.2); c.drawRightString(x+AW-52, y+AH-27, sub)
    hammer_sickle(c, x+AW-30, y+AH-24, 10.5, color=GOLDC); c.setStrokeColor(black); c.setLineWidth(0.8); c.rect(x+8, y+8, AW-16, AH-16); vstamp(c, x+AW-12, y+11, size=5)

def quota_table(c, x, y, w, size=8.4):
    rows = [('Players', 'Y1', 'Y2', 'Y3', 'Y4')] + [(k,) + tuple(fmt(v) for v in vals) for k, vals in QUOTAS.items()]
    cw = [w*0.30] + [w*0.175]*4; rh = 13
    for r, row in enumerate(rows):
        xx = x
        for k, cell in enumerate(row):
            if r == 0: c.setFillColor(black); c.rect(xx, y-rh*(r+1), cw[k], rh, fill=1, stroke=0)
            c.setStrokeColor(black); c.setLineWidth(0.5); c.rect(xx, y-rh*(r+1), cw[k], rh, fill=0, stroke=1)
            c.setFillColor(white if r == 0 else black); c.setFont('MonoB' if r == 0 or k == 0 else 'Mono', size); c.drawCentredString(xx+cw[k]/2, y-rh*(r+1)+3.8, cell); xx += cw[k]
    return y-rh*len(rows)

def auction_box(c, x, y, w):
    c.setFillColor(Color(0.95, 0.95, 0.95)); c.setStrokeColor(black); c.setLineWidth(0.6); c.rect(x, y-62, w, 62, fill=1, stroke=1)
    hdraw(c, 'Running an auction', x+6, y-12, 'HeadB', 8.2, color=black, anchor='l')
    yy = y-14
    for t in ['Opens at 10. Anyone bids, up in 10s.', 'Secretary never bids. Winner pays now.', 'Secretary keeps 30. Rest to the bank.', 'Winner adds 20 per Suspicion point.']:
        yy = rich(c, x+6, yy, w-12, t, size=7.2, lead=1.25)
    return y-62

def secretary_aid(c, x, y):
    aid_frame(c, x, y, 'Party Secretary', 'PLAYER AID'); lx, rx, cwid = x+18, x+AW/2+8, AW/2-26; top = y+AH-46
    yy = label(c, lx, top, 'Goal'); yy = rich(c, lx, yy, cwid, 'Pay all four quotas and keep every citizen at or under %s rubles.' % fmt(KULAK), size=8.2)
    yy = label(c, lx, yy-4, 'Your turn (last each round)'); yy = rich(c, lx, yy, cwid, 'Roll two dice, no doubles bonus. 6 players: roll three, keep two.', size=8.2)
    for b in ['Directed enterprise: Inspection. Director pays a bribe equal to the fee, or takes +2 Suspicion.', 'Unowned enterprise: auction it.', 'The Midnight Knock: one citizen +1 Suspicion.',
              'Once per round: denounce one citizen free.', 'Passing Poluchka: the Year ends.']:
        yy = rich(c, lx, yy-1.5, cwid, b, bullet=True, size=7.8)
    auction_box(c, lx, yy-6, cwid)
    yy = label(c, rx, top, 'Year end'); yy = rich(c, rx, yy, cwid, 'Richest citizen +2 Suspicion, second richest +1. Then pay the quota or be purged.', size=8.2)
    yy = quota_table(c, rx, yy-5, cwid, size=8)
    yy = label(c, rx, yy-7, 'You may'); yy = rich(c, rx, yy, cwid, 'Set any bribe. Sell pardons, release, Blat and papers at any price. Pick the reverting enterprise. Settle shortages. Decide where the rules are silent.', size=7.6)
    yy = label(c, rx, yy-4, 'You may not'); rich(c, rx, yy, cwid, 'Change fees, prices or quotas. Refuse an auction. Take from the bank. Hide the Fund: it stays face up.', size=7.6)

def citizen_aid(c, x, y):
    aid_frame(c, x, y, 'Citizen', 'PLAYER AID'); lx, rx, cwid = x+18, x+AW/2+8, AW/2-26; top = y+AH-46
    yy = label(c, lx, top, 'Goal'); yy = rich(c, lx, yy, cwid, 'Be the richest citizen at the end of Year 4 with more than %s rubles. If nobody clears it, the Secretary wins.' % fmt(KULAK), size=8.4)
    yy = label(c, lx, yy-4, 'On your turn'); yy = rich(c, lx, yy, cwid, 'Roll, move, buy or pay. Collect 200 at Poluchka. Appointments cost 20 extra per point of your Suspicion.', size=8.4)
    for b in ['Denounce: once per round, pay the Secretary 50 to give a rival +1 Suspicion.', 'Subbotnik: skip buying and building, pay 100 to drop 1 Suspicion.', 'Forged papers: pay 150 to draw a new character and drop 2.']:
        yy = rich(c, lx, yy-1.5, cwid, b, bullet=True, size=8.2)
    yy = label(c, rx, top, 'Suspicion'); yy = rich(c, rx, yy, cwid, 'At 5 you are disappeared: Gulag, lose an enterprise, new character.', size=8.4)
    for b in ['Up: denounced +1, refuse a bribe +2, richest at year end +2, second +1, some cards.', 'Down: your denunciation jails someone -1, visit the Gulag corner -1, Subbotnik, papers, some cards.', 'Blat: spend one to cancel a payment up to 200 or block 1 Suspicion. Hold 3.']:
        yy = rich(c, rx, yy-1.5, cwid, b, bullet=True, size=8.2)
    yy = label(c, rx, yy-4, 'Gulag'); yy = rich(c, rx, yy, cwid, 'Leave with doubles, 50 rubles, a card or a deal. No fees inside. Visiting drops 1 Suspicion.', size=8.2)
    yy = label(c, rx, yy-4, 'Broke?'); rich(c, rx, yy, cwid, 'New character, 500 rubles, keep playing.', size=8.2)

def suspicion_tracker(c, x, y):
    w, h = 6*IN, 1.75*IN
    c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h); c.setStrokeColor(black); c.setLineWidth(0.8); c.rect(x+6, y+6, w-12, h-12)
    hdraw(c, 'Suspicion', x+16, y+h-22, 'HeadB', 11, color=RED, anchor='l'); c.setFillColor(FLAV); c.setFont('MonoI', 6.8); c.drawRightString(x+w-16, y+h-21, 'Your file. One black bead marks where you stand.')
    labels = ['Model citizen', 'Noted', 'A file exists', 'The file is thick', 'Neighbors avoid you', 'Disappeared']
    bw, bh, gap = 0.86*IN, 1.05*IN, 0.06*IN; bx = x+(w-(6*bw+5*gap))/2; by = y+12
    for i, t in enumerate(labels):
        xx = bx+i*(bw+gap); last = i == 5
        c.setFillColor(black if last else white); c.setStrokeColor(black); c.setLineWidth(0.9); c.rect(xx, by, bw, bh, fill=1, stroke=1)
        hdraw(c, str(i), xx+bw/2, by+bh-24, 'HeadB', 20, color=RED if i == 4 else (white if last else black))
        c.setFillColor(white if last else FLAV); c.setFont('MonoI', 5.8)
        for k, ln in enumerate(wrap(t, 'MonoI', 5.8, bw-6)): c.drawCentredString(xx+bw/2, by+bh-33-k*7, ln)
        c.setStrokeColor(white if last else GREY); c.setDash(2, 2); c.setLineWidth(0.6); c.circle(xx+bw/2, by+14, 9, fill=0, stroke=1); c.setDash()
    vstamp(c, x+w-12, y+9, size=4.6)

def year_sticker(c, x, y):
    w, h = YW, YH
    c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, w, h, fill=1, stroke=1)
    bw, gap = 1.3*IN, 0.08*IN; bh = h-22; bx = x+10; by = y+8
    hdraw(c, 'The Plan', x+12, y+h-11, 'HeadB', 8.5, color=black, anchor='l'); c.setFillColor(black); c.setFont('Mono', 5.8); c.drawString(x+12+sw('THE PLAN', 'HeadB', 8.5)+8, y+h-11, 'Move the bead each time the Secretary passes Poluchka. The District Fund sits here, face up.')
    for i in range(4):
        xx = bx+i*(bw+gap)
        c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(1.0); c.rect(xx, by, bw, bh, fill=1, stroke=1); c.setFillColor(black); c.rect(xx, by+bh-15, bw, 15, fill=1, stroke=0)
        hdraw(c, 'Year %d' % (i+1), xx+bw/2, by+bh-11, 'HeadB', 9, color=white)
        c.setFillColor(FLAV); c.setFont('Mono', 5.2); c.drawCentredString(xx+bw/2, by+bh-23, 'QUOTA DUE AT YEAR END')
        for k, (pl, vals) in enumerate(QUOTAS.items()):
            c.setFillColor(black); c.setFont('Mono', 6.2); c.drawString(xx+5, by+bh-34-k*9, pl+' players'); c.setFont('MonoB', 7.2); c.drawRightString(xx+bw-5, by+bh-34-k*9, fmt(vals[i]))
        c.setStrokeColor(GREY); c.setDash(2, 2); c.setLineWidth(0.6); c.circle(xx+bw*0.5, by+13, 9, fill=0, stroke=1); c.setDash()
    ex = bx+4*(bw+gap); ew = x+w-10-ex
    c.setFillColor(RED); c.setStrokeColor(black); c.setLineWidth(1.0); c.rect(ex, by, ew, bh, fill=1, stroke=1)
    hdraw(c, 'Plan', ex+ew/2, by+bh-20, 'HeadB', 11, color=white); hdraw(c, 'complete!', ex+ew/2, by+bh-32, 'HeadB', 7.6, color=white); star(c, ex+ew/2, by+bh/2-8, 11, fill=GOLDC)
    c.setFillColor(white); c.setFont('MonoB', 5.2); c.drawCentredString(ex+ew/2, by+5, 'CHECK THE KULAK LINE')
    vstamp(c, x+w-12, y+3, size=4.2)

def blat_chit(c, x, y):
    s = 1.0*IN; c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, s, s); c.setStrokeColor(RED); c.setLineWidth(1.6); c.rect(x+5, y+5, s-10, s-10)
    c.setFillColor(black); c.setFont('MonoB', 6.2); c.drawCentredString(x+s/2, y+s-17, 'GOOD FOR'); hdraw(c, 'Blat', x+s/2, y+s/2-8, 'HeadB', 22, color=RED)
    c.setFillColor(black); c.setFont('MonoB', 6.2); c.drawCentredString(x+s/2, y+13, 'ONE FAVOR')
