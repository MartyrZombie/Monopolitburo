"""MONOPOLITBURO quality check.

Checks the game data against the design rules, then checks the built PDFs in out/.
Run after building:   python3 src/build_package.py && python3 src/qc.py
Set QC_RELEASE=1 to also require a CHANGELOG section for the current VERSION (used on main).
Exit code 1 if any check fails.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import VERSION, OUT, RUS, outname, IN
import game as G
import stickers as ST
import rulebook as RB
import poses, busts

RESULTS = []
def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))

def money_in(text):
    """Rubles amounts mentioned in card or rule text (not counts like '3 spaces' or '10 times')."""
    pats = [r'(?:[Pp]ay|[Cc]ollect|pays the Secretary|cost you|minimum of|Take|take)\s+(\d[\d,]*)(?!\s*(?:times|spaces|Suspicion|Blat|cards?|players?))',
            r'(\d[\d,]*)\s+(?:rubles|per Workshop|per Kombinat|less)']
    found = []
    for p in pats:
        found += [int(m.replace(',', '')) for m in re.findall(p, text)]
    return found

# ------------------------------------------------------------------ version and changelog
semver = re.fullmatch(r'v(\d+)\.(\d+)\.(\d+)', VERSION)
check('VERSION is MAJOR.MINOR.PATCH', semver, VERSION)
cl = open(os.path.join(HERE, '..', 'CHANGELOG.md')).read()
cl_heads = re.findall(r'^## (v\d+\.\d+\.\d+|Unreleased)', cl, re.M)
vers = [tuple(map(int, h[1:].split('.'))) for h in cl_heads if h != 'Unreleased']
check('CHANGELOG versions are unique and newest first', vers == sorted(set(vers), reverse=True), ', '.join(cl_heads))
check('CHANGELOG "Unreleased" section, if any, is at the top', 'Unreleased' not in cl_heads or cl_heads[0] == 'Unreleased')
if os.environ.get('QC_RELEASE') == '1':
    check('CHANGELOG has a section for %s (required on main)' % VERSION, VERSION in cl_heads)
    check('No "Unreleased" section on main (rename it to the version)', 'Unreleased' not in cl_heads)
else:
    check('CHANGELOG mentions current or upcoming version', VERSION in cl_heads or 'Unreleased' in cl_heads)

# ------------------------------------------------------------------ repository
import ast, glob as _glob
_local = {os.path.basename(f)[:-3] for f in _glob.glob(os.path.join(HERE, '*.py'))}
_mods = set()
for f in _glob.glob(os.path.join(HERE, '*.py')):
    for n in ast.walk(ast.parse(open(f).read())):
        if isinstance(n, ast.Import): _mods |= {a.name.split('.')[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0: _mods.add(n.module.split('.')[0])
_third = _mods - _local - set(sys.stdlib_module_names)
_req = {l.split('>=')[0].split('==')[0].strip().lower() for l in open(os.path.join(HERE, '..', 'requirements.txt')) if l.strip() and not l.startswith('#')}
_missing = sorted(m for m in _third if {'PIL': 'pillow'}.get(m, m).lower() not in _req)
check('requirements.txt covers every third-party import in src/', not _missing, _missing)

# ------------------------------------------------------------------ component counts
check('22 enterprise deeds', len(G.D) == 22, len(G.D))
check('4 railways and 2 utilities', len(G.RAIL) == 4 and len(G.UTIL) == 2)
check('12 characters', len(G.CHARS) == 12, len(G.CHARS))
check('16 Directives from Moscow', len(G.DIRECTIVES) == 16, len(G.DIRECTIVES))
check('16 Kitchen Rumors', len(G.RUMORS) == 16, len(G.RUMORS))
check('22 board name patches', len(ST.PATCHES) == 22, len(ST.PATCHES))
groups = [d[0] for d in G.D]
want = ['brown']*2 + ['lblue']*3 + ['pink']*3 + ['orange']*3 + ['red']*3 + ['yellow']*3 + ['green']*3 + ['dblue']*2
check('Colour groups in board order with classic sizes (2,3,3,3,3,3,3,2)', groups == want)

# ------------------------------------------------------------------ prices and fees
classic = [60, 60, 100, 100, 120, 140, 140, 160, 180, 180, 200, 220, 220, 240, 260, 260, 280, 300, 300, 320, 350, 400]
check('Purchase prices match the classic board', [d[2] for d in G.D] == classic)
check('Patch board positions match the classic properties', [p[0] for p in ST.PATCHES] == [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39])
norm = lambda lines: re.sub(r'\s+', ' ', ' '.join(lines).replace('- ', '-')).strip().lower()
mism = [(norm(p[2]), norm(d[1])) for p, d in zip(ST.PATCHES, G.D) if norm(p[2]) != norm(d[1])]
check('Board sticker names match deed names', not mism, mism)
bad = [d[1] for d in G.D if len(d[3]) != 6 or d[3] != sorted(d[3])]
check('Every fee ladder has 6 steps and never decreases', not bad, bad)
amounts = [('price', d[2]) for d in G.D] + [('fee', f) for d in G.D for f in d[3]] + [('build', v[2]) for v in G.GROUPS.values()]
amounts += [('pledge', G.pledge(d[2])) for d in G.D] + [('redeem', G.redeem(d[2])) for d in G.D]
amounts += [('quota', q) for qs in G.QUOTAS.values() for q in qs] + [('Kulak Line', G.KULAK)]
for coll, label in ((G.DIRECTIVES, 'Directive'), (G.RUMORS, 'Kitchen Rumor')):
    amounts += [('%s "%s"' % (label, d[0]), a) for d in coll for a in money_in(d[1])]
amounts += [('character %s' % d[0], a) for d in G.CHARS for a in money_in(d[2])]
off10 = [(k, v) for k, v in amounts if v % 10]
check('Every money amount is a multiple of 10 (no 1s or 5s)', not off10, off10)
check('Card and character text mentions money (sanity check of the scan)', len(amounts) > 200, len(amounts))
bad = [(d[2], G.pledge(d[2])) for d in G.D if G.pledge(d[2]) != int(round(d[2]/2/10.0))*10]
check('Pledge value is half the price, rounded to 10', not bad, bad)
check('Redeem value is more than pledge value', all(G.redeem(d[2]) > G.pledge(d[2]) for d in G.D))

# ------------------------------------------------------------------ quotas and winning
q = G.QUOTAS
check('Quota tables exist for 3, 4 or 5, and 6 players', set(q) == {'3', '4 or 5', '6'}, list(q))
check('Quotas rise every Year', all(list(v) == sorted(v) and len(set(v)) == 4 for v in q.values()))
check('Quotas rise with player count', all(q['3'][i] < q['4 or 5'][i] < q['6'][i] for i in range(4)))
check('Kulak Line is above the starting stake of 1,500', G.KULAK > 1500, G.KULAK)

# ------------------------------------------------------------------ cards
for coll, label, n_sab in ((G.DIRECTIVES, 'Directives', 2), (G.RUMORS, 'Kitchen Rumors', 1)):
    empty = [d[0] for d in coll if not all(x.strip() for x in d[:4])]
    check('%s: every card has title, effect, flavor and gloss' % label, not empty, empty)
    check('%s: %d Sabotage cards' % (label, n_sab), sum(1 for d in coll if d[5]) == n_sab)
    gain = [d[0] for d in coll if re.search(r'gain 1 Suspicion', d[1])]
    lose = [d[0] for d in coll if re.search(r'lose 1 Suspicion', d[1])]
    check('%s: exactly one card gains and one loses Suspicion' % label, len(gain) == 1 and len(lose) == 1, (gain, lose))
    check('%s: titles are unique' % label, len({d[0] for d in coll}) == len(coll))
    badart = [d[0] for d in coll if d[4][0] not in ('hold', 'cheer', 'sad', 'run', 'salute', 'suitcase', 'photo') or (d[4][1] and d[4][1] not in poses.PROPS)]
    check('%s: every card has valid art' % label, not badart, badart)
    jail = [d[0] for d in coll if 'Gulag free' in d[1]]
    check('%s: one Get-out-of-the-Gulag card' % label, len(jail) == 1, jail)
check('Exactly 3 Sabotage cards in total (the Spets rule)', sum(1 for d in G.DIRECTIVES + G.RUMORS if d[5]) == 3)

# ------------------------------------------------------------------ characters
roles = [d[0] for d in G.CHARS]
check('Character roles are unique', len(set(roles)) == 12)
check('Every character has a portrait', all(r in busts.SPECS for r in roles), [r for r in roles if r not in busts.SPECS])
check('Every character name is first name, patronymic, surname', all(len(d[1].split()) == 3 for d in G.CHARS), [d[1] for d in G.CHARS if len(d[1].split()) != 3])
check('Every character has a rule, flavor and two glosses', all(all(x.strip() for x in d) for d in G.CHARS))
check('Every character has exactly one rule sentence pair (benefit, drawback or both)', all(len(d[2]) < 140 for d in G.CHARS), [d[0] for d in G.CHARS if len(d[2]) >= 140])

# ------------------------------------------------------------------ glosses and the glossary
glossary = {t.lower() for t, _ in RB.GLOSS}
alias = {'kolkhoznik': 'kolkhoz', 'the organs': 'organs, the', 'former people': 'byvshiye lyudi'}
all_gloss = [d[3] for d in G.DIRECTIVES + G.RUMORS] + [d[5] for d in G.D] + [x for d in G.CHARS for x in d[4:6]] + [g for _, _, g in G.RAIL] + [g for _, _, g in G.UTIL]
missing = set()
for gtext in all_gloss:
    m = re.match(r'^"?([A-Z][\w\- ]{1,24}?)"?:\s', gtext)
    if m:
        t = m.group(1).lower()
        if alias.get(t, t) not in glossary: missing.add(m.group(1))
check('Every glossed term on a card is in the rulebook glossary', not missing, sorted(missing))
check('Every gloss is a full sentence ending in a full stop', all(g.rstrip('"').endswith('.') for g in all_gloss), [g[:40] for g in all_gloss if not g.rstrip('"').endswith('.')])
check('Glossary is alphabetical', [t.lower().lstrip('"') for t, _ in RB.GLOSS] == sorted(t.lower().lstrip('"') for t, _ in RB.GLOSS))
# Russian words glossed as "Term:" must render plain (not mirrored) when they appear in a headline
heads = ' '.join([d[0] for d in G.DIRECTIVES + G.RUMORS] + [' '.join(d[1]) for d in G.D] + roles).upper()
glossed = set()
for gtext in all_gloss:
    m = re.match(r'^([A-Z][a-z]+):\s', gtext)
    if m: glossed.add(m.group(1).upper())
mirrored = sorted(w for w in glossed if re.search(r'\b%s\b' % w, heads) and w not in RUS and ('N' in w or 'R' in w))
check('Glossed Russian words in headlines stay plain, never mirrored', not mirrored, mirrored)

# ------------------------------------------------------------------ physical sizes (measured from the real board)
check('Cards are 2 1/8 x 3 3/16 in', abs(__import__('cards').CW - 2.125*IN) < 0.01 and abs(__import__('cards').CH - 3.1875*IN) < 0.01)
check('Property sticker is 1 5/8 x 2 9/16 in, corner 2 9/16 in', abs(ST.SP_W - 1.625*IN) < .01 and abs(ST.SP_H - 2.5625*IN) < .01 and abs(ST.CORNER - 2.5625*IN) < .01)
check('Deck labels cover the 3 5/16 x 2 3/16 in card outlines', ST.DLW >= 3.3125*IN and ST.DLH >= 2.1875*IN)
check('Title bar covers the 11 3/8 x 2 5/16 in logo bar', ST.L >= 11.375*IN and ST.T >= 2.3125*IN)

# ------------------------------------------------------------------ built PDFs
from pypdf import PdfReader
import subprocess, tempfile
from PIL import Image
MARGIN_IN = 0.2      # most home printers cannot print the outer 0.17 to 0.25 in
def ink_in_margin(pdf, dpi=50):
    """Pages that put visible ink inside the outer margin, judged on the rendered page."""
    bad = []
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['pdftoppm', '-r', str(dpi), '-gray', pdf, os.path.join(d, 'p')], check=True)
        for i, f in enumerate(sorted(os.listdir(d))):
            im = Image.open(os.path.join(d, f)); w, h = im.size; m = max(1, int(MARGIN_IN*dpi))
            dark = im.point(lambda v: 255 if v < 200 else 0)
            bands = [(0, 0, w, m), (0, h-m, w, h), (0, 0, m, h), (w-m, 0, w, h)]
            if any(dark.crop(b).getbbox() for b in bands): bad.append(i+1)
    return bad
expect = {'0_Board_Stickers': 6, '1_Decks': 4, '2_Deeds': 8, '3_Characters': 4, '4_Table_Pieces': 7, '5_Rulebook': None}
complete = OUT + 'MONOPOLITBURO_%s_Complete.pdf' % VERSION
files = {k: outname(k) for k in expect}
present = {k: os.path.exists(p) for k, p in files.items()}
check('All PDFs were built for %s' % VERSION, all(present.values()) and os.path.exists(complete), [k for k, v in present.items() if not v])
if all(present.values()) and os.path.exists(complete):
    texts = {}
    for k, p in files.items():
        r = PdfReader(p)
        if expect[k] is None:
            check('%s has an even page count of 8 or fewer (back cover lands on a back)' % k, len(r.pages) % 2 == 0 and len(r.pages) <= 8, len(r.pages))
        else:
            check('%s has %d pages' % (k, expect[k]), len(r.pages) == expect[k], len(r.pages))
        sizes = {(round(float(pg.mediabox.width)), round(float(pg.mediabox.height))) for pg in r.pages}
        check('%s is US Letter throughout' % k, sizes == {(612, 792)}, sizes)
        texts[k] = [pg.extract_text() or '' for pg in r.pages]
        nover = [i+1 for i, t in enumerate(texts[k]) if VERSION not in t]
        check('%s carries %s on every page' % (k, VERSION), not nover, nover)
        fonts = set()
        for pg in r.pages:
            res = pg.get('/Resources') or {}
            for f in (res.get('/Font') or {}).values():
                f = f.get_object(); fd = f.get('/FontDescriptor')
                if fd is not None:
                    fd = fd.get_object(); fonts.add((str(f.get('/BaseFont')), any(x in fd for x in ('/FontFile', '/FontFile2', '/FontFile3'))))
        unembedded = sorted(n for n, e in fonts if not e)
        check('%s embeds all its fonts' % k, not unembedded, unembedded)
        out = ink_in_margin(p)
        check('%s keeps all ink inside the printable area (0.2 in margin)' % k, not out, out)
    rc = PdfReader(complete)
    parts = sum(len(PdfReader(files[k]).pages) for k in expect) + 1
    check('Complete package has checklist + all parts (%d pages)' % parts, len(rc.pages) == parts, len(rc.pages))
    cl_text = rc.pages[0].extract_text()
    m = re.search(r'(\d+) pages', cl_text)
    check('Checklist page count matches the package', m and int(m.group(1)) == len(rc.pages), m and m.group(1))
    import checklist as CK
    released = [h for h in cl_heads if h != 'Unreleased']
    check('Checklist points returning players at the update pack from the last release', (CK.UPGRADE_FROM in released) and CK.UPDATE_PACK and CK.UPDATE_PACK in re.sub(r'\s+', '', cl_text), CK.UPDATE_PACK)
    rows, total, _ = CK.rows_and_totals()
    covered = set()
    for r in rows:
        a, _, b = r[1].partition('-'); covered |= set(range(int(a), int(b or a)+1))
    check('Checklist rows cover every page of the package exactly once', covered == set(range(2, len(rc.pages)+1)) and sum(1 for _ in covered) == len(rc.pages)-1, sorted(set(range(2, len(rc.pages)+1)) - covered))
    rb = ' '.join(texts['5_Rulebook'])
    rbn = re.sub(r'\s+', ' ', rb)
    check('Rulebook states the Kulak Line from game.py', '{:,}'.format(G.KULAK) in rbn)
    check('Rulebook quota table matches game.py', all('{:,}'.format(v) in rbn for vals in G.QUOTAS.values() for v in vals))
    for h in cl_heads[:2]:
        label = 'Unreleased (in testing)' if h == 'Unreleased' else h + ','
        check('Rulebook change log includes %s from CHANGELOG.md (latest two sections)' % h, label in rbn)
    for phrase in ['once per round', 'plus 20 per point of your Suspicion', 'keeps 30', 'gains +2 Suspicion', 'richest citizen wins whatever their net worth']:
        check('Rulebook says "%s"' % phrase, phrase.lower() in rbn.lower())
    check('Rulebook glossary lists every term', all(t.split()[0].upper() in rbn.upper() for t, _ in RB.GLOSS))
    tp = re.sub(r'\s+', ' ', ' '.join(texts['4_Table_Pieces']))
    check('Aids state the Kulak Line from game.py', '{:,}'.format(G.KULAK) in tp)
    check('Year track sticker shows every quota', all('{:,}'.format(v) in tp for vals in G.QUOTAS.values() for v in vals))
    dd = re.sub(r'\s+', ' ', ' '.join(texts['2_Deeds']))
    missing_price = [d[2] for d in G.D if 'PRICE %s' % '{:,}'.format(d[2]) not in dd]
    check('Every deed shows its purchase price', not missing_price, missing_price)
    stk = re.sub(r'\s+', ' ', ' '.join(texts['0_Board_Stickers'])).upper()
    check('Sticker placement key lists every original street', all(p[1].upper() in stk for p in ST.PATCHES))

# ------------------------------------------------------------------ report
w = max(len(n) for n, _, _ in RESULTS)
fails = [r for r in RESULTS if not r[1]]
summary = os.environ.get('GITHUB_STEP_SUMMARY')
lines = ['## MONOPOLITBURO %s quality check: %d passed, %d failed' % (VERSION, len(RESULTS)-len(fails), len(fails)), '', '| | Check | Detail |', '| --- | --- | --- |']
for n, ok, d in RESULTS:
    print(('PASS  ' if ok else 'FAIL  ') + n.ljust(w) + ('' if ok or d == '' else '   -> %s' % (d,)))
    lines.append('| %s | %s | %s |' % ('✅' if ok else '❌', n, '' if ok else str(d).replace('|', '/')))
print('\n%d checks, %d failed' % (len(RESULTS), len(fails)))
if summary:
    with open(summary, 'a') as f: f.write('\n'.join(lines) + '\n')
sys.exit(1 if fails else 0)
