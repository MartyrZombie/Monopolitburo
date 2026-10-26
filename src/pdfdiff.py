"""Compare PDFs page by page: page count, page size, extracted text and rendered pixels.

  python3 src/pdfdiff.py OLD_DIR NEW_DIR          compare every component in two folders
  python3 src/pdfdiff.py "label|old.pdf|new.pdf"  compare one pair, exit 1 if different
"""
import sys, subprocess, tempfile, os
from pypdf import PdfReader
from PIL import Image, ImageChops

def texts(p):
    out = []
    for pg in PdfReader(p).pages:
        out.append(' '.join((pg.extract_text() or '').split()))
    return out

def render(p, d, tag, dpi=40):
    subprocess.run(['pdftoppm', '-r', str(dpi), '-gray', p, os.path.join(d, tag)], check=True)
    return sorted(f for f in os.listdir(d) if f.startswith(tag))

def compare(a, b, label):
    ra, rb = PdfReader(a), PdfReader(b)
    res = {'label': label, 'pages': (len(ra.pages), len(rb.pages)), 'size_mismatch': [], 'text_diff': [], 'pixel_diff': []}
    for i, (pa, pb) in enumerate(zip(ra.pages, rb.pages)):
        if [round(float(x)) for x in pa.mediabox] != [round(float(x)) for x in pb.mediabox]:
            res['size_mismatch'].append(i+1)
    ta, tb = texts(a), texts(b)
    for i, (x, y) in enumerate(zip(ta, tb)):
        if x != y: res['text_diff'].append(i+1)
    with tempfile.TemporaryDirectory() as d:
        fa, fb = render(a, d, 'a'), render(b, d, 'b')
        for i, (x, y) in enumerate(zip(fa, fb)):
            ia, ib = Image.open(os.path.join(d, x)), Image.open(os.path.join(d, y))
            if ia.size != ib.size: res['pixel_diff'].append((i+1, 'size')); continue
            diff = ImageChops.difference(ia, ib)
            n = diff.point(lambda v: 255 if v > 40 else 0).histogram()[255]
            pct = 100.0 * n / (ia.size[0]*ia.size[1])
            if pct > 0.01: res['pixel_diff'].append((i+1, round(pct, 3)))
    ok = res['pages'][0] == res['pages'][1] and not (res['size_mismatch'] or res['text_diff'] or res['pixel_diff'])
    print(('MATCH   ' if ok else 'DIFFERS ') + label, '| pages %d vs %d' % res['pages'],
          '| text diffs on pages:', res['text_diff'] or 'none', '| pixel diffs:', res['pixel_diff'] or 'none',
          '| page size mismatches:', res['size_mismatch'] or 'none')
    return ok

def compare_dirs(old, new):
    """Match files by component (the part after the version) and compare each pair."""
    import re, glob
    key = lambda f: re.sub(r'_v\d+\.\d+\.\d+_', '_', os.path.basename(f)).lower()
    olds = {key(f): f for f in glob.glob(os.path.join(old, '*.pdf'))}
    news = {key(f): f for f in glob.glob(os.path.join(new, '*.pdf'))}
    for k in sorted(set(olds) | set(news)):
        if k not in olds: print('NEW     ' + os.path.basename(news[k]))
        elif k not in news: print('GONE    ' + os.path.basename(olds[k]))
        else: compare(olds[k], news[k], os.path.basename(news[k]))

if __name__ == '__main__':
    if len(sys.argv) == 3 and os.path.isdir(sys.argv[1]):
        compare_dirs(sys.argv[1], sys.argv[2])     # informational: never fails
    else:
        pairs = [l.split('|') for l in sys.argv[1:]]
        results = [compare(a, b, lbl) for lbl, a, b in pairs]
        sys.exit(0 if all(results) else 1)
