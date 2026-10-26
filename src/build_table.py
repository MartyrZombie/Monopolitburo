from common import *
from table import *
c = canvas.Canvas(outname('4_Table_Pieces'), pagesize=letter); c.setTitle('MONOPOLITBURO %s - aids, trackers, chits' % VERSION)
# aids: 3 sheets single-sided -> 1 secretary + 5 citizen
for n, (a, b) in enumerate([(secretary_aid, citizen_aid), (citizen_aid, citizen_aid), (citizen_aid, citizen_aid)]):
    sheet_head(c, 'Player aids  |  sheet %d of 3' % (n+1), 'Ivory cardstock, 100% / Actual size, one side. Each aid is 6 x 4 in.')
    x0 = (W-AW)/2; y0 = H-60
    for i, fn in enumerate((a, b)): fn(c, x0, y0-(i+1)*AH-i*14); crop_marks(c, x0, y0-(i+1)*AH-i*14, AW, AH)
    c.showPage()
# suspicion trackers: 6 on one sheet
sheet_head(c, 'Suspicion trackers  |  1 to 5 of 6', 'Ivory cardstock, 100% / Actual size, one side. One per citizen. A black glass bead marks your Suspicion.')
x0 = (W-6*IN)/2; y0 = H-56
for i in range(5): suspicion_tracker(c, x0, y0-(i+1)*1.75*IN-i*6); crop_marks(c, x0, y0-(i+1)*1.75*IN-i*6, 6*IN, 1.75*IN)
c.showPage()
sheet_head(c, 'Suspicion trackers  |  6 of 6, plus a spare', 'Ivory cardstock, 100% / Actual size, one side.')
for i in range(2): suspicion_tracker(c, x0, y0-(i+1)*1.75*IN-i*6); crop_marks(c, x0, y0-(i+1)*1.75*IN-i*6, 6*IN, 1.75*IN)
c.showPage()
# chits
sheet_head(c, 'Blat chits  |  20 chits: 15 for play, 5 spares', 'White cardstock, 100% / Actual size, one side. Each chit is 1 in square. Cut the grid in strips.')
x0 = (W-5*IN)/2; y0 = H-70
for i in range(20): blat_chit(c, x0+(i % 5)*IN, y0-(i//5+1)*IN)
crop_marks(c, x0, y0-4*IN, 5*IN, 4*IN)
yy = rich(c, 40, y0-4*IN-24, W-80, 'Blat: spend one to cancel a single payment of up to 200 rubles, or to block 1 Suspicion as you gain it. Hold 3 at most.', size=8.5)
rich(c, 40, yy-4, W-80, "Blat was the informal economy of favors and connections that got you what rubles couldn't.", size=8, color=FLAV)
c.showPage()
# year sticker
sheet_head(c, 'Year track sticker', 'Sticker paper, 100% / Actual size. Apply in the centre of the board, below the title banner.')
year_sticker(c, (W-YW)/2, H-80-YH); year_sticker(c, (W-YW)/2, H-80-YH-20-YH)
c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawCentredString(W/2, H-80-2*YH-32, 'Two copies: one to apply, one spare.')
c.showPage(); c.save(); print('ok')
