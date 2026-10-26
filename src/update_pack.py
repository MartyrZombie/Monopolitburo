"""Update pack: only the pages a returning player has to reprint.

    python3 src/update_pack.py PREV_DIR PREV_TAG

PREV_DIR holds the previous release's component PDFs. The current build must already be in out/.
Writes out/MONOPOLITBURO_<VERSION>_Update_from_<PREV_TAG>.pdf and out/update-notes.md.

A page is "changed" when the printed pieces on it differ from the same page in the previous release, judged on
text and on rendered pixels. Version stamps and the printing instructions at the very top and bottom of each sheet
are ignored, because they change every release but are never cut out and used.

- Double-sided parts (deeds, characters) are included a full sheet at a time: front and back together.
- The rulebook is one object: if any page changed, the whole rulebook is included.
- A component that is new, or whose page count changed, is included whole.
"""
import os, re, sys, glob, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import *
from pypdf import PdfReader, PdfWriter
from PIL import Image, ImageChops, ImageDraw
import pdfplumber
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

TOP_BAND, BOTTOM_BAND = 46, 30          # points: sheet instructions and footers, never cut out
VER = re.compile(r'v\d+\.\d+\.\d+')
DPI = 50
DUPLEX = {'deeds', 'characters'}
WHOLE = {'rulebook'}
NAMES = {'board_stickers': 'Board stickers', 'decks': 'Card decks', 'deeds': 'Deeds', 'characters': 'Character cards',
         'table_pieces': 'Aids, trackers, chits, Year sticker', 'rulebook': 'Rulebook'}

def component(path):
    """'Monopolitburo_v0.2.0_2_Deeds.pdf' and 'Monopolitburo_v0.1.0_Board_Stickers.pdf' -> 'deeds', 'board_stickers'."""
    b = os.path.basename(path)
    if 'Complete' in b or 'Update_from' in b: return None
    b = re.sub(r'^Monopolitburo_v\d+\.\d+\.\d+_', '', b, flags=re.I)
    return re.sub(r'^\d+_', '', b[:-4]).lower()

def components(folder):
    return {k: f for f in glob.glob(os.path.join(folder, '*.pdf')) if (k := component(f))}

def page_text(pl_page):
    h = pl_page.height
    crop = pl_page.within_bbox((0, TOP_BAND, pl_page.width, h - BOTTOM_BAND))
    lines = (crop.extract_text() or '').splitlines()
    return [VER.sub('vX', ' '.join(l.split())) for l in lines if l.strip()]

def version_boxes(pl_page):
    return [(w['x0'] - 2, w['top'] - 2, w['x1'] + 2, w['bottom'] + 2) for w in pl_page.extract_words() if VER.fullmatch(w['text'])]

def render(pdf, folder, tag):
    subprocess.run(['pdftoppm', '-r', str(DPI), '-gray', pdf, os.path.join(folder, tag)], check=True)
    return sorted(glob.glob(os.path.join(folder, tag + '-*.pgm')))

def masked(img, boxes, w_pt, h_pt):
    s = img.width / w_pt; d = ImageDraw.Draw(img)
    d.rectangle((0, 0, img.width, TOP_BAND*s), fill=255); d.rectangle((0, img.height - BOTTOM_BAND*s, img.width, img.height), fill=255)
    for x0, t, x1, b in boxes: d.rectangle((x0*s, t*s, x1*s, b*s), fill=255)
    return img

def regions(mask, cell=6, min_px=6):
    """Separate clusters of changed pixels, as bounding boxes in pixels."""
    w, h = mask.size; gw, gh = -(-w // cell), -(-h // cell)
    small = mask.resize((gw, gh), Image.BOX).point(lambda v: 255 if v > 0 else 0)
    px = small.load(); seen = set(); boxes = []
    for y in range(gh):
        for x in range(gw):
            if px[x, y] and (x, y) not in seen:
                stack = [(x, y)]; seen.add((x, y)); x0 = x1 = x; y0 = y1 = y
                while stack:
                    cx, cy = stack.pop()
                    x0, x1, y0, y1 = min(x0, cx), max(x1, cx), min(y0, cy), max(y1, cy)
                    for nx in range(cx-2, cx+3):           # join cells up to 2 apart: one piece, one box
                        for ny in range(cy-2, cy+3):
                            if 0 <= nx < gw and 0 <= ny < gh and px[nx, ny] and (nx, ny) not in seen:
                                seen.add((nx, ny)); stack.append((nx, ny))
                box = (x0*cell, y0*cell, (x1+1)*cell, (y1+1)*cell)
                if mask.crop(box).histogram()[255] >= min_px: boxes.append(box)
    return boxes

def words(pl_page):
    crop = pl_page.within_bbox((0, TOP_BAND, pl_page.width, pl_page.height - BOTTOM_BAND))
    return [VER.sub('vX', w['text']) for w in crop.extract_words()]

def diff_part(old, new, tmp):
    """Per page: (changed?, words added on the new page, changed regions in pixels) for pages present in both."""
    out = []
    with pdfplumber.open(old) as po, pdfplumber.open(new) as pn:
        ro, rn = render(old, tmp, 'o'), render(new, tmp, 'n')
        for i, (a, b) in enumerate(zip(po.pages, pn.pages)):
            ta, tb = page_text(a), page_text(b)
            wa = set(words(a)); added = [x for x in dict.fromkeys(words(b)) if x not in wa]
            boxes = version_boxes(a) + version_boxes(b)
            ia = masked(Image.open(ro[i]), boxes, a.width, a.height); ib = masked(Image.open(rn[i]), boxes, b.width, b.height)
            if ia.size == ib.size:
                boxes_px = regions(ImageChops.difference(ia, ib).point(lambda v: 255 if v > 48 else 0))
            else:
                boxes_px = [(0, 0, ib.width, ib.height)]
            out.append((ta != tb or bool(boxes_px), added, boxes_px))
        for f in glob.glob(os.path.join(tmp, '*.pgm')): os.remove(f)
    return out

def plan(prev_dir):
    prev, cur = components(prev_dir), components(OUT)
    entries = []          # (component, page_index, reason, added_words, changed_regions_px)
    with tempfile.TemporaryDirectory() as tmp:
        for k in sorted(cur, key=lambda k: os.path.basename(cur[k])):
            new = cur[k]; n_new = len(PdfReader(new).pages)
            if k not in prev:
                entries += [(k, i, 'new component', [], None) for i in range(n_new)]; continue
            old = prev[k]; n_old = len(PdfReader(old).pages)
            if n_old != n_new and k not in WHOLE:
                entries += [(k, i, 'page count changed (%d to %d)' % (n_old, n_new), [], None) for i in range(n_new)]; continue
            res = diff_part(old, new, tmp)
            changed = {i for i, (c, _, _) in enumerate(res) if c}
            if k in WHOLE:
                if changed or n_old != n_new:
                    entries += [(k, i, 'rulebook changed: reprint all of it', [], None) for i in range(n_new)]
                continue
            if k in DUPLEX:
                changed |= {i ^ 1 for i in changed if (i ^ 1) < n_new}
            for i in sorted(changed):
                c, added, bbox = res[i] if i < len(res) else (True, [], None)
                reason = 'changed' if c else 'back of a changed sheet'
                entries.append((k, i, reason, added, bbox))
    return cur, entries

def paper_for(k, i):
    """Paper for page i of component k, taken from the checklist plan."""
    import checklist
    for paper, part, sl, *_ in checklist.PLAN:
        if component('Monopolitburo_v0.0.0_' + part + '.pdf') == k:
            a, b = sl if sl else (0, 10**6)
            if a <= i < b: return paper
    return 'Plain paper'

def thumbnail(pdf, i, regions_px, tmp):
    subprocess.run(['pdftoppm', '-r', '48', '-f', str(i+1), '-l', str(i+1), '-png', pdf, os.path.join(tmp, 't')], check=True)
    img = Image.open(glob.glob(os.path.join(tmp, 't*.png'))[0]).convert('RGB')
    for f in glob.glob(os.path.join(tmp, 't*.png')): os.remove(f)
    s = 48.0 / DPI; d = ImageDraw.Draw(img)
    for x0, y0, x1, y1 in regions_px or []:
        for k in range(3): d.rectangle((x0*s-3-k, y0*s-3-k, x1*s+3+k, y1*s+3+k), outline=(204, 18, 26))
    return img

def draw_guide(path, prev_tag, groups, thumbs, first):
    """The guide pages. Returns how many pages it took, so pack page numbers can be checked."""
    st = ParagraphStyle('c', fontName='Mono', fontSize=8.2, leading=10); sb = ParagraphStyle('cb', fontName='MonoB', fontSize=8.4, leading=10)
    sh = ParagraphStyle('h', parent=sb, textColor=white)
    c = canvas.Canvas(path, pagesize=letter)
    def foot():
        c.setFont('Mono', 7.5); c.setFillColor(GREY); c.drawCentredString(W/2, 24, 'Update guide, page %d  |  MONOPOLITBURO %s' % (c.getPageNumber(), VERSION))
    c.setFillColor(RED); c.rect(40, H-78, W-80, 38, fill=1, stroke=0); hdraw(c, 'MONOPOLITBURO', 52, H-66, 'HeadB', 20, color=white, anchor='l', ucyr=True)
    c.setFillColor(white); c.setFont('MonoB', 9.5); c.drawRightString(W-86, H-63, '%s UPDATE FROM %s' % (VERSION, prev_tag)); hammer_sickle(c, W-62, H-59, 12, color=GOLDC)
    y = para(c, 'Already have %s printed? Print only the pages listed below: they hold every piece that changed, and this file contains '
                'nothing else. Pages are grouped by paper. Red boxes on the thumbnails mark what changed, so you can cut just those pieces '
                'and keep the rest of your set. Print at 100%% / Actual size.' % prev_tag, 40, H-90, W-80, 'Mono', 9, leading=11.4)
    data = [[Paragraph(h, sh) for h in ('Paper', 'Pages in this file', 'Component', 'Was page', 'What changed')]]
    pos = first
    for paper, k, es in groups:
        a, b = pos, pos + len(es) - 1
        reason = es[0][2] if all(x[2] == es[0][2] for x in es) else 'changed'
        added = list(dict.fromkeys(x for e in es for x in e[3]))
        nbox = sum(len(e[4] or []) for e in es)
        if k in WHOLE or reason.startswith(('new', 'page count')): what = reason
        else:
            what = '%d change%s, boxed in red below.' % (nbox, '' if nbox == 1 else 's')
            what += (' New words: ' + ' '.join(added[:12]) + (' ...' if len(added) > 12 else '')) if added else ' Artwork or lettering only.'
        data.append([Paragraph(paper, sb), Paragraph(str(a) if a == b else '%d-%d' % (a, b), sb), Paragraph(NAMES.get(k, k), st),
                     Paragraph(', '.join(str(e[1]+1) for e in es), st), Paragraph(what, st)])
        pos = b + 1
    t = Table(data, colWidths=[108, 58, 96, 52, 218])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), black), ('GRID', (0, 0), (-1, -1), 0.5, black), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]))
    _, th_ = t.wrapOn(c, W-80, 600); t.drawOn(c, 40, y-10-th_); y = y-10-th_-12
    if any(g[1] in DUPLEX for g in groups):
        y = para(c, 'Deeds and character cards are double-sided: print a front page, flip the sheet on its long edge, then print the page after it.', 40, y, W-80, 'Mono', 8.6, leading=10.8) - 4
    tw, th, per_row, col, pos = 164, 212, 3, 0, first
    for e, img in thumbs:
        if col == 0:
            if y - th - 22 < 40: foot(); c.showPage(); y = H-40
            y -= th + 20
        x = 40 + col*(tw + 16); iw, ih = img.size; s = min(tw/iw, th/ih)
        c.drawImage(ImageReader(img), x, y, iw*s, ih*s); c.setStrokeColor(GREY); c.setLineWidth(0.4); c.rect(x, y, iw*s, ih*s)
        c.setFont('MonoB', 7); c.setFillColor(black); c.drawString(x, y-9, 'Page %d: %s p.%d' % (pos, NAMES.get(e[0], e[0]), e[1]+1))
        pos += 1; col = (col + 1) % per_row
    foot(); c.save()
    return len(PdfReader(path).pages)

def build(prev_dir, prev_tag):
    cur, entries = plan(prev_dir)
    name = 'MONOPOLITBURO_%s_Update_from_%s.pdf' % (VERSION, prev_tag)
    notes = os.path.join(OUT, 'update-notes.md')
    if not entries:
        open(notes, 'w').write('**Updating from %s?** Nothing to reprint: no printed piece changed.\n' % prev_tag)
        print('no printed pieces changed since', prev_tag); return None
    papers = []
    for e in entries:
        if paper_for(e[0], e[1]) not in papers: papers.append(paper_for(e[0], e[1]))
    ordered = [e for p in papers for e in entries if paper_for(e[0], e[1]) == p]
    groups = []
    for e in ordered:
        p = paper_for(e[0], e[1])
        if groups and groups[-1][0] == p and groups[-1][1] == e[0]: groups[-1][2].append(e)
        else: groups.append([p, e[0], [e]])
    with tempfile.TemporaryDirectory() as tmp:
        thumbs = [(e, thumbnail(cur[e[0]], e[1], e[4], tmp)) for e in ordered]
    guide = os.path.join(OUT, 'update-guide.pdf')
    n = draw_guide(guide, prev_tag, groups, thumbs, 2)
    if n != 1: n = draw_guide(guide, prev_tag, groups, thumbs, n + 1)    # renumber now the guide length is known
    w = PdfWriter(); w.append(guide)
    for e in ordered: w.append(cur[e[0]], pages=(e[1], e[1]+1))
    path = os.path.join(OUT, name)
    with open(path, 'wb') as f: w.write(f)
    os.remove(guide)
    sheets = {}
    for paper, k, es in groups:
        sheets[paper] = sheets.get(paper, 0) + ((len(es)+1)//2 if k in DUPLEX or k in WHOLE else len(es))
    sheets['Plain paper'] = sheets.get('Plain paper', 0) + n        # the guide
    lines = ['**Updating from %s?** Print only `%s`: %d page(s) of changed pieces plus a %d-page guide. It holds:' % (prev_tag, name, len(ordered), n), '']
    for paper, k, es in groups:
        total = len(PdfReader(cur[k]).pages)
        lines.append('- %s: %s, page%s %s of %d' % (paper, NAMES.get(k, k), 's' if len(es) > 1 else '', ', '.join(str(e[1]+1) for e in es), total))
    lines += ['', 'Paper: ' + ', '.join('%d %s' % (v, k.replace(', 65 lb', '').lower()) for k, v in sheets.items()) + '.']
    open(notes, 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines)); print('wrote', path, len(w.pages), 'pages')
    return path

if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
