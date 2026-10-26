"""Build every printable PDF and assemble the complete print package.

Run from anywhere:  python3 src/build_package.py
Output goes to out/.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
for script in ('build_cards.py', 'build_table.py', 'rulebook.py', 'checklist.py'):
    print('building', script, flush=True)
    subprocess.run([sys.executable, script], check=True)

from common import OUT, VERSION, outname
from pypdf import PdfWriter
parts = [OUT + 'checklist.pdf'] + [outname(p) for p in ('1_Decks', '2_Deeds', '3_Characters', '4_Table_Pieces', '5_Rulebook')]
w = PdfWriter()
for p in parts:
    w.append(p)
pkg = OUT + 'MONOPOLITBURO_%s_Complete.pdf' % VERSION
with open(pkg, 'wb') as f:
    w.write(f)
os.remove(OUT + 'checklist.pdf')
print('package', pkg, len(w.pages), 'pages')
