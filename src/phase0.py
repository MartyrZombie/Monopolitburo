from common import *
from cards import *
from table import *

def heading(c, text, sub):
    c.setFillColor(RED); c.rect(36, H-66, W-72, 28, fill=1, stroke=0); hdraw(c, text, 46, H-58, 'HeadB', 15, color=white, anchor='l')
    para(c, sub, 36, H-72, W-72, 'Mono', 9, leading=11.5)
def foot(c, t): c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawCentredString(W/2, 22, 'MONOPOLITBURO %s  |  Phase 0  |  %s  |  Print at 100%% / Actual size' % (VERSION, t))

out = '../out/Monopolitburo_v0.2.0_Phase0_Samples.pdf'
c = canvas.Canvas(out, pagesize=letter); c.setTitle('MONOPOLITBURO %s - Phase 0 samples' % VERSION)
# page 1: year sticker + tracker + chit
heading(c, 'Year track sticker and Suspicion tracker', 'Print on plain paper first. Lay the Year track in the centre of the board, between the title banner and the Community Chest outline, and tell me if it needs to grow or shrink.')
year_sticker(c, (W-YW)/2, H-100-YH); c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawString((W-YW)/2, H-100-YH-11, 'Year track sticker, 7.5 x 1.6 in, board green. One bead marks the Year.')
suspicion_tracker(c, (W-6*IN)/2, H-100-YH-50-1.75*IN); c.drawString((W-6*IN)/2, H-100-YH-50-1.75*IN-11, 'Suspicion tracker, 6 x 1.75 in, one per citizen. One bead in the dashed circle.')
blat_chit(c, (W-6*IN)/2, H-100-YH-50-1.75*IN-40-IN); c.drawString((W-6*IN)/2+IN+8, H-100-YH-50-1.75*IN-40-IN+30, 'Blat chit, unchanged from v0.1.0.')
foot(c, 'Table pieces'); c.showPage()
# page 2: aids
heading(c, 'Player aids, single-sided', 'Rewritten for v0.2.0 with the auction box and the Secretary\'s powers and limits. Still 6 x 4 in.')
secretary_aid(c, (W-AW)/2, H-96-AH); citizen_aid(c, (W-AW)/2, H-96-AH-14-AH); foot(c, 'Aids'); c.showPage()
# page 3: cards
heading(c, 'Card samples', 'A deed with its price line, a character with the new Officer rule, a changed Directive, and the version footer on each.')
DEEDS[0][0](c, 60, H-110-CH); DEEDS[21][0](c, 60+CW+16, H-110-CH); char_front(c, 60+2*CW+32, H-110-CH, CHARS[8])
deck_card(c, 60, H-110-CH-30-LH, 'Directives from Moscow', DIRECTIVES[12]); DEEDS[0][1](c, 60+LW+20, H-110-CH-30-CH)
foot(c, 'Cards'); c.showPage(); c.save(); print('ok')
