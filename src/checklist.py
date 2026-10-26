"""Page 1 of the complete package: what prints on which paper, computed from the built PDFs."""
from common import *
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader

def previous_release():
    """The release a returning player has printed, read from CHANGELOG.md."""
    import os, re
    text = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'CHANGELOG.md')).read()
    heads = re.findall(r'^## (v\d+\.\d+\.\d+|Unreleased)', text, re.M)
    versions = [h for h in heads if h != 'Unreleased']
    released = versions if 'Unreleased' in heads else [h for h in versions if h != VERSION]
    return released[0] if released else None

UPGRADE_FROM = previous_release()
UPDATE_PACK = 'MONOPOLITBURO_%s_Update_from_%s.pdf' % (VERSION, UPGRADE_FROM) if UPGRADE_FROM else None

def pages(part): return len(PdfReader(outname(part)).pages)

# (paper, part, page slice within that part or None for all, what prints, how, duplex)
PLAN = [
    ('Matte sticker paper', '0_Board_Stickers', None, 'Board stickers: name patches, full spaces, deck labels, corners, title banner, maker\'s mark.', 'One side.', False),
    ('ORANGE cardstock, 65 lb', '1_Decks', (0, 2), 'Directives from Moscow, 16 cards.', 'One side. Black ink only.', False),
    ('YELLOW cardstock, 65 lb', '1_Decks', (2, 4), 'Kitchen Rumors, 16 cards.', 'One side. Black ink only.', False),
    ('WHITE cardstock, 65 lb', '2_Deeds', None, 'Deeds, 28 cards. Pages alternate fronts, backs.', 'Double-sided: print a FRONTS page, flip the sheet on its long edge, print the BACKS page that follows.', True),
    ('WHITE cardstock, 65 lb', '3_Characters', None, 'Character cards, 12. Pages alternate fronts, backs.', 'Double-sided, same routine.', True),
    ('IVORY cardstock, 65 lb', '4_Table_Pieces', (0, 3), 'Player aids: 1 Secretary, 5 citizens.', 'One side.', False),
    ('IVORY cardstock, 65 lb', '4_Table_Pieces', (3, 5), 'Suspicion trackers, 6 plus a spare.', 'One side.', False),
    ('WHITE cardstock, 65 lb', '4_Table_Pieces', (5, 6), 'Blat chits, 20.', 'One side.', False),
    ('Matte sticker paper', '4_Table_Pieces', (6, 7), 'Year track sticker, 2 copies.', 'One side.', False),
    ('Plain paper', '5_Rulebook', None, 'Rules of Play, with glossary and change log.', 'Double-sided. Staple the corner.', True),
]
# The package order (after this checklist page) is the part order below; stickers print first.
ORDER = ['0_Board_Stickers', '1_Decks', '2_Deeds', '3_Characters', '4_Table_Pieces', '5_Rulebook']

def rows_and_totals():
    start, n = {}, 2                         # page 1 is this checklist
    for part in ORDER: start[part] = n; n += pages(part)
    total = n - 1
    rows, sheets = [], {}
    for paper, part, sl, what, how, duplex in PLAN:
        a, b = sl if sl else (0, pages(part))
        p0, p1 = start[part] + a, start[part] + b - 1
        cnt = (b - a + 1)//2 if duplex else (b - a)
        rows.append((paper, str(p0) if p0 == p1 else '%d-%d' % (p0, p1), str(cnt), what, how))
        key = paper.split(',')[0].replace(' cardstock', '').title() if 'cardstock' in paper else paper
        sheets[key] = sheets.get(key, 0) + cnt
    sheets['Plain paper'] = sheets.get('Plain paper', 0) + 1    # this checklist
    return rows, total, sheets

def build():
    rows, total, sheets = rows_and_totals()
    st = ParagraphStyle('c', fontName='Mono', fontSize=8.4, leading=10.2); sb = ParagraphStyle('cb', fontName='MonoB', fontSize=8.6, leading=10.2); sh = ParagraphStyle('h', parent=sb, textColor=white)
    c = canvas.Canvas(OUT + 'checklist.pdf', pagesize=letter)
    c.setFillColor(RED); c.rect(40, H-78, W-80, 38, fill=1, stroke=0); hdraw(c, 'MONOPOLITBURO', 52, H-66, 'HeadB', 20, color=white, anchor='l', ucyr=True)
    c.setFillColor(white); c.setFont('MonoB', 9.5); c.drawRightString(W-86, H-63, VERSION + '  PRINT CHECKLIST'); hammer_sickle(c, W-62, H-59, 12, color=GOLDC)
    y = para(c, 'The complete MONOPOLITBURO %s print set, %d pages, grouped by paper. Print every page at 100%% / Actual size, never "fit to page." You also need a retail copy of classic US Monopoly.' % (VERSION, total), 40, H-90, W-80, 'Mono', 9.2, leading=11.6)
    data = [[Paragraph(h, sh) for h in ('Paper', 'Pages', 'Sheets', 'What prints', 'How')]] + [[Paragraph(a, sb), Paragraph(b, sb), Paragraph(d, st), Paragraph(e, st), Paragraph(f, st)] for a, b, d, e, f in rows]
    t = Table(data, colWidths=[118, 46, 44, 188, 136])
    tint = {'ORANGE': Color(1, 0.86, 0.72), 'YELLOW': Color(1, 0.96, 0.7), 'IVORY': Color(0.99, 0.97, 0.9), 'Matte': Color(0.86, 0.93, 0.88)}
    style = [('BACKGROUND', (0, 0), (-1, 0), black), ('GRID', (0, 0), (-1, -1), 0.5, black), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    for i, r in enumerate(rows):
        for k, col in tint.items():
            if r[0].startswith(k): style.append(('BACKGROUND', (0, i+1), (-1, i+1), col))
    t.setStyle(TableStyle(style))
    tw, th = t.wrapOn(c, W-80, 600); t.drawOn(c, 40, y-12-th); y = y-12-th-14
    if UPGRADE_FROM:
        hdraw(c, 'Already have %s?' % UPGRADE_FROM, 40, y-10, 'HeadB', 11, color=RED, anchor='l'); y -= 15
        y = para(c, "- Don't print all of this. Print %s from the same release instead: it holds only the pages that changed, "
                    "with a guide marking which pieces to cut. Keep everything else you have." % UPDATE_PACK, 40, y, W-80, 'Mono', 9, leading=11.4) - 2
        y -= 8
    hdraw(c, 'Paper to buy for a full set', 40, y-10, 'HeadB', 11, color=RED, anchor='l'); y -= 15
    parts = ['%d %s' % (v, k.lower()) for k, v in sheets.items() if k not in ('Matte sticker paper', 'Plain paper')]
    y = para(c, '- %s sheets of 65 lb cardstock, %d sheets of matte full-sheet sticker paper, %d plain. Buy a few spares for test prints.' % (', '.join(parts), sheets.get('Matte sticker paper', 0), sheets['Plain paper']), 40, y, W-80, 'Mono', 9, leading=11.4)
    y = para(c, '- From your Monopoly set: the board, the money from 10 up, dice, tokens, 20 houses and 8 hotels. Add about 10 black glass beads, and a third die for 6 players.', 40, y-2, W-80, 'Mono', 9, leading=11.4)
    c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawCentredString(W/2, 24, 'Page 1 of %d  |  plain paper  |  MONOPOLITBURO %s' % (total, VERSION)); c.save()
    return total

if __name__ == '__main__':
    print('ok', build())
