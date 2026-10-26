"""Build the board sticker sheets: python3 build_stickers.py  (output in out/)."""
from stickers import *

def page_patches(c):
    heading(c, 'Name patches (22)', 'Each patch is 1.5 x 1 in. Tuck its top edge against the colour bar. Patches share cut lines, so cut the grid in strips. Three blank spares are included.')
    x0, y0 = (W-5*PW)/2, H-112
    for i in range(25):
        x, y = x0+(i % 5)*PW, y0-(i//5+1)*PH
        if i < 22:
            name_patch(c, x, y, PATCHES[i][2])
            c.setFont('Mono', 5); c.setFillColor(GREY); c.drawRightString(x+PW-3, y+3, str(PATCHES[i][0]))
        else:
            c.setFillColor(MINT); c.setStrokeColor(GREY); c.setLineWidth(0.3); c.rect(x, y, PW, PH, fill=1, stroke=1)
    ky = y0-5*PH-18
    hdraw(c, 'Placement key', 36, ky, 'HeadB', 10, color=RED, anchor='l'); ky -= 5
    c.setFont('Mono', 7.6); c.setFillColor(black)
    for i, (n, old, new) in enumerate(PATCHES):
        col, row = i // 11, i % 11
        c.drawString(36+col*3.75*IN, ky-11-row*10.6, '%2d  %-19s ->  %s' % (n, old, ' '.join(new).replace('- ', '-')))
    para(c, 'The small grey number on each patch is its board position (GO = 0, counting clockwise). It sits at the patch edge and can be trimmed off.', 36, ky-11*10.6-6, W-72, 'Mono', 7, leading=8.6, color=GREY)
    foot(c, 'Name patches')

def grid_spaces(c, items, y_top, per_row=4, gap=0.22*IN):
    x0 = (W - per_row*SW - (per_row-1)*gap)/2
    for i, (cap, fn) in enumerate(items):
        x = x0+(i % per_row)*(SW+gap); y = y_top-(i//per_row)*(SH+26)-SH
        fn(c, x, y); c.setFont('Mono', 7); c.setFillColor(GREY); c.drawCentredString(x+SW/2, y-10, cap)

def page_spaces1(c):
    heading(c, 'Full-space stickers, sheet 1 of 2', 'Each is 1 5/8 x 2 9/16 in with its own black border. The caption under each names the space it covers.')
    items = [('5  Reading Railroad', rail(['Trans-Siberian', 'Railway'])), ('15  Pennsylvania Railroad', rail(['October', 'Railway'])),
             ('25  B. & O. Railroad', rail(['Turksib'])), ('35  Short Line', rail(['Moscow', 'Metro'])),
             ('12  Electric Company', util(['DniproHES', '(Dnieper Dam)'], art_dam)), ('28  Water Works', util(['Belomorkanal', '(White Sea Canal)'], art_canal)),
             ('4  Income Tax', tax(['"Voluntary"', 'State Bond', 'Subscription'], art_bond, 'PAY 200')), ('38  Luxury Tax', tax(['Party Dues'], art_partycard, 'PAY 100'))]
    grid_spaces(c, items, H-112); foot(c, 'Full spaces 1/2')

def page_spaces2(c):
    heading(c, 'Full-space stickers, sheet 2 of 2, and deck labels', 'Three Directives spaces, three Kitchen Rumors spaces, and the two labels that cover the card outlines in the middle of the board.')
    d = cardspace(['Directives', 'from Moscow'], art_bang); k = cardspace(['Kitchen', 'Rumors'], art_teapot)
    items = [('7  Chance', d), ('22  Chance', d), ('36  Chance', d), ('2  Community Chest', k), ('17  Community Chest', k), ('33  Community Chest', k)]
    grid_spaces(c, items, H-112)
    y = H-112-2*(SH+26)-DLH-8
    deck_label(c, 40, y, 'Directives from Moscow', ORANGE, white, lambda c, x, yy: hammer_sickle(c, x, yy, 24, color=white))
    deck_label(c, 40+DLW+16, y, 'Kitchen Rumors', YEL, black, lambda c, x, yy: art_teapot(c, x-6, yy-2))
    c.setFont('Mono', 7); c.setFillColor(GREY); c.drawString(40, y-10, 'Covers the orange Chance outline'); c.drawString(40+DLW+16, y-10, 'Covers the blue Community Chest outline')
    foot(c, 'Full spaces 2/2')

def page_corners(c):
    heading(c, "Corner stickers (4) and maker's mark", 'Each corner is 2 9/16 in square. Turn each one so its words face the middle of the board, the way the originals do.')
    g = 0.3*IN; x0 = (W-2*CS-g)/2; y1 = H-116-CS; y2 = y1-CS-30
    corner_poluchka(c, x0, y1); corner_gulag(c, x0+CS+g, y1); corner_ochered(c, x0, y2); corner_knock(c, x0+CS+g, y2)
    c.setFont('Mono', 7); c.setFillColor(GREY)
    for (t, xx, yy) in [('0  GO', x0, y1), ('10  Jail / Just Visiting', x0+CS+g, y1), ('20  Free Parking', x0, y2), ('30  Go To Jail', x0+CS+g, y2)]:
        c.drawCentredString(xx+CS/2, yy-10, t)
    ly = y2-0.5*IN-34
    ddr_logo(c, W/2-1.1*IN, ly, True); ddr_logo(c, W/2+1.1*IN, ly, False)
    c.drawCentredString(W/2, ly-0.5*IN-12, "Maker's mark: covers the Hasbro Gaming oval. Oval, or the easier-to-cut rounded rectangle.")
    foot(c, 'Corners')

def page_bar(c):
    heading(c, 'Title banner - bar, two pieces', 'Apply these first. Piece A goes on the left, piece B butts against it. Both are plain rectangles, so they cut with a ruler and knife.')
    sx = split_x(); tot = T+BELOW+ABOVE
    ay = H-112-ABOVE-T
    c.saveState(); c.translate(36, ay); cp = c.beginPath(); cp.rect(-1, -BELOW-1, sx+1, tot+2); c.clipPath(cp, stroke=0, fill=0); bar_art(c); c.restoreState()
    c.setStrokeColor(GREY); c.setLineWidth(0.4); c.line(36+sx, ay-BELOW, 36+sx, ay+T+ABOVE)
    c.setFont('Mono', 8); c.setFillColor(GREY); c.drawString(36, ay-BELOW-11, 'Piece A (left), %.2f in long' % (sx/IN))
    by = ay - BELOW - 26 - ABOVE - T
    c.saveState(); c.translate(36-sx, by); cp = c.beginPath(); cp.rect(sx, -BELOW-1, L-sx+1, tot+2); c.clipPath(cp, stroke=0, fill=0); bar_art(c); c.restoreState()
    c.setStrokeColor(GREY); c.line(36, by-BELOW, 36, by+T+ABOVE)
    c.drawString(36, by-BELOW-11, 'Piece B (right), %.2f in long. The small grey ticks above the bar show where the mascot piece sits.' % ((L-sx)/IN))
    foot(c, 'Title bar')

def page_mascot_piece(c):
    heading(c, 'Title banner - mascot piece', "Apply last, bottom edge on the bar's top black line, between the grey ticks.")
    mascot_piece(c, 36, H-110-MH); foot(c, 'Banner mascot piece')

PAGES = (page_patches, page_spaces1, page_spaces2, page_corners, page_bar, page_mascot_piece)
if __name__ == '__main__':
    c = canvas.Canvas(outname('0_Board_Stickers'), pagesize=letter); c.setTitle('MONOPOLITBURO %s - board stickers' % VERSION)
    for fn in PAGES: fn(c); c.showPage()
    c.save(); print('ok')
