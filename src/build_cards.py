from common import *
from cards import *
def dup_note(side): return 'Print this side first.' if side == 'fronts' else 'Flip the sheet on its LONG edge and print this on the back.'

def portrait_sheet(c, items, title, n, total, side, stock):
    sheet_head(c, '%s  |  sheet %d of %d  |  %s' % (title, n, total, side.upper()), '%s cardstock, 100%% / Actual size. %s' % (stock, dup_note(side)))
    x0 = (W-3*CW)/2; y0 = H-48
    for i, pair in enumerate(items):
        col, row = i % 3, i // 3
        if side == 'backs': col = 2-col
        pair[0 if side == 'fronts' else 1](c, x0+col*CW, y0-(row+1)*CH)
    crop_marks(c, x0, y0-3*CH, 3*CW, 3*CH)

def deck_sheet(c, deck, cards, n, total, stock):
    sheet_head(c, '%s  |  sheet %d of %d' % (deck, n, total), 'Print on %s cardstock at 100%% / Actual size, one side only. Black ink only.' % stock)
    x0 = (W-2*LW)/2; y0 = H-70
    for i, d in enumerate(cards): deck_card(c, x0+(i % 2)*LW, y0-(i//2+1)*LH, deck, d)
    crop_marks(c, x0, y0-4*LH, 2*LW, 4*LH)

c = canvas.Canvas(outname('1_Decks'), pagesize=letter); c.setTitle('MONOPOLITBURO %s - card decks' % VERSION)
for deck, cards_, stock in (('Directives from Moscow', DIRECTIVES, 'ORANGE'), ('Kitchen Rumors', RUMORS, 'YELLOW')):
    for n in (0, 1): deck_sheet(c, deck, cards_[n*8:(n+1)*8], n+1, 2, stock); c.showPage()
c.save()

c = canvas.Canvas(outname('2_Deeds'), pagesize=letter); c.setTitle('MONOPOLITBURO %s - deeds' % VERSION)
chunks = [DEEDS[i:i+9] for i in range(0, 28, 9)]
for n, ch in enumerate(chunks):
    for side in ('fronts', 'backs'): portrait_sheet(c, ch, 'Deeds', n+1, len(chunks), side, 'White'); c.showPage()
c.save()

CH_PAIRS = [(lambda c, x, y, d=d: char_front(c, x, y, d), lambda c, x, y: char_back(c, x, y)) for d in CHARS]
c = canvas.Canvas(outname('3_Characters'), pagesize=letter); c.setTitle('MONOPOLITBURO %s - character cards' % VERSION)
for n, ch in enumerate([CH_PAIRS[0:9], CH_PAIRS[9:12]]):
    for side in ('fronts', 'backs'): portrait_sheet(c, ch, 'Character cards', n+1, 2, side, 'White'); c.showPage()
c.save(); print('ok')
