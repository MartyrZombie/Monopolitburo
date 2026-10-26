from common import *
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
st = ParagraphStyle('c', fontName='Mono', fontSize=8.6, leading=10.6); sb = ParagraphStyle('cb', fontName='MonoB', fontSize=8.8, leading=10.6); sh = ParagraphStyle('h', parent=sb, textColor=white)
rows = [('ORANGE cardstock, 65 lb', '2-3', '2', 'Directives from Moscow, 16 cards.', 'One side. Black ink only.'),
 ('YELLOW cardstock, 65 lb', '4-5', '2', 'Kitchen Rumors, 16 cards.', 'One side. Black ink only.'),
 ('WHITE cardstock, 65 lb', '6-13', '4', 'Deeds, 28 cards. Pages alternate fronts, backs.', 'Double-sided: print a FRONTS page, flip the sheet on its long edge, print the BACKS page that follows.'),
 ('WHITE cardstock, 65 lb', '14-17', '2', 'Character cards, 12. Pages alternate fronts, backs.', 'Double-sided, same routine.'),
 ('IVORY cardstock, 65 lb', '18-20', '3', 'Player aids: 1 Secretary, 5 citizens.', 'One side.'),
 ('IVORY cardstock, 65 lb', '21-22', '2', 'Suspicion trackers, 6 plus a spare.', 'One side.'),
 ('WHITE cardstock, 65 lb', '23', '1', 'Blat chits, 20.', 'One side.'),
 ('Matte sticker paper', '24', '1', 'Year track sticker, 2 copies.', 'One side. The only new sticker.'),
 ('Plain paper', '25-30', '3', 'Rules of Play, 6 pages, with the change log.', 'Double-sided. Staple the corner.')]
c = canvas.Canvas(OUT + 'checklist.pdf', pagesize=letter)
c.setFillColor(RED); c.rect(40, H-78, W-80, 38, fill=1, stroke=0); hdraw(c, 'MONOPOLITBURO', 52, H-66, 'HeadB', 20, color=white, anchor='l', ucyr=True)
c.setFillColor(white); c.setFont('MonoB', 9.5); c.drawRightString(W-86, H-63, VERSION + '  UPDATE CHECKLIST'); hammer_sickle(c, W-62, H-59, 12, color=GOLDC)
y = para(c, 'This is the %s update, 30 pages. It replaces every card, aid and tracker from v0.1.0 and adds one board sticker. The board stickers you already applied stay as they are. Print every page at 100%% / Actual size.' % VERSION, 40, H-90, W-80, 'Mono', 9.4, leading=12)
data = [[Paragraph(h, sh) for h in ('Paper', 'Pages', 'Sheets', 'What prints', 'How')]] + [[Paragraph(a, sb), Paragraph(b, sb), Paragraph(d, st), Paragraph(e, st), Paragraph(f, st)] for a, b, d, e, f in rows]
t = Table(data, colWidths=[122, 44, 48, 184, 134])
t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), black), ('GRID', (0, 0), (-1, -1), 0.5, black), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('BACKGROUND', (0, 1), (-1, 1), Color(1, 0.86, 0.72)), ('BACKGROUND', (0, 2), (-1, 2), Color(1, 0.96, 0.7)), ('BACKGROUND', (0, 5), (-1, 6), Color(0.99, 0.97, 0.9)), ('BACKGROUND', (0, 8), (-1, 8), Color(0.9, 0.95, 0.9))]))
tw, th = t.wrapOn(c, W-80, 600); t.drawOn(c, 40, y-14-th); y = y-14-th-16
hdraw(c, 'What to replace from v0.1.0', 40, y-10, 'HeadB', 11, color=RED, anchor='l'); y -= 16
for ln in ['Replace: both card decks, all 28 deeds, all 12 character cards, both aids, the rulebook. Every one changed.', 'Retire: the old double-sided aids with their track backs, the 1 and 5 ruble notes, the spare houses and hotel used as markers.',
           'Keep: every board sticker already on the board, the Blat chits (reprint only if yours are worn), the money from 10 up, the houses and hotels in play.', 'Add: the Year track sticker, 6 Suspicion trackers, about 10 black glass beads, a third die for 6 players.']:
    y = para(c, '- ' + ln, 40, y, W-80, 'Mono', 9.2, leading=11.8) - 3
y -= 10; hdraw(c, 'Paper to buy', 40, y-10, 'HeadB', 11, color=RED, anchor='l'); y -= 16
y = para(c, '- 2 orange, 2 yellow, 7 white and 5 ivory sheets of 65 lb cardstock, 1 sheet of matte sticker paper, 3 plain. Buy a few spares for test prints.', 40, y, W-80, 'Mono', 9.2, leading=11.8)
c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawCentredString(W/2, 24, 'Page 1 of 30  |  plain paper  |  MONOPOLITBURO ' + VERSION); c.save(); print('ok')
