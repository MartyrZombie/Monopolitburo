# MONOPOLITBURO

A satirical re-theme of classic US Monopoly set in Stalin's Soviet Union. It is a print-and-play kit:
players keep a retail Monopoly board, money, dice, tokens, houses and hotels, cover parts of the board with
stickers, and print new cards, deeds, aids and a rulebook on a home printer. In beta.

The owner is MartyrZombie. Work in short reviewable chunks and propose changes before building them.

## Layout

| Path | What it is |
| --- | --- |
| `VERSION` | The version, `MAJOR.MINOR.PATCH`. Stamped on every printed piece and in every filename. |
| `CHANGELOG.md` | Release notes. The rulebook's change log and the GitHub Release notes are generated from it. |
| `src/game.py` | **Source of truth** for all game numbers and card text: deeds, fees, quotas, Kulak Line, characters, both decks. |
| `src/stickers.py` | Board sticker pieces and the 22 name patches (`PATCHES`). |
| `src/rulebook.py` | Rules text and the glossary (`GLOSS`). |
| `src/checklist.py` | Page 1 of the package. Page ranges, paper counts and the previous release are all computed. |
| `src/common.py` | Fonts, colours, faux-Cyrillic headlines, hammer and sickle, version stamp, output paths. |
| `src/mascot.py`, `poses.py`, `busts.py` | Comrade Kopeikin and the character portraits, all original line art. |
| `src/cards.py`, `table.py` | Card, deed, aid, tracker, chit and Year-track renderers. |
| `src/build_*.py`, `build_package.py` | Builders. `build_package.py` runs them all and assembles the complete PDF. |
| `src/qc.py` | Quality check: the design rules below, as code, plus checks on the built PDFs. |
| `src/update_pack.py` | Update pack: only the pages that changed since the previous release, with a guide. |
| `src/pdfdiff.py` | Page-by-page text and pixel comparison of two builds. |
| `out/` | Build output. Git-ignored; never commit PDFs. Releases carry them. |

## Build and check

```bash
pip install -r requirements.txt          # reportlab, pypdf, Pillow; poppler-utils for pdftoppm
python3 src/build_package.py             # everything into out/
python3 src/qc.py                        # must print "0 failed" before you push
python3 src/update_pack.py PREV_DIR vA.B.C   # optional: update pack against a previous release's PDFs
python3 src/pdfdiff.py OLD_DIR out       # optional: page-by-page comparison of two builds
```

Fonts are not bundled: Poppins Bold and Medium (`POPPINS_DIR`, default `/usr/share/fonts/truetype/google-fonts`)
and Courier 10 Pitch from Debian's `xfonts-scalable` (`TYPE1_DIR`, default `/usr/share/fonts/X11/Type1`).

## Design rules

These are the owner's decisions. `src/qc.py` enforces every one it can; when you add a rule, add a check.

**Tone and content**
- Satire aimed at the system (bureaucracy, paranoia, doublespeak), never at its victims, in text or art.
- Every Russian word or Soviet term gets a short, accurate, straight-faced gloss, and every glossed term is in
  the rulebook glossary. Jokes go in flavor text, facts go in glosses; never mix them.
- No real people pictured or named on cards. Characters are invented, with a first name, patronymic and a
  "speaking" surname whose root is glossed. Stalin appears in text references only.
- Comrade Kopeikin is the mascot: an original cartoon Red Army officer in a furazhka (khaki crown, red band, gold
  star, black visor), khaki greatcoat, tall black boots. He replaces the Monopoly man wherever that figure would
  appear. Never reproduce Hasbro artwork, characters or logos.
- Hammer and sickle and red are used freely for theming.

**Look**
- Copy the Monopoly house style: white spaces, thin black rules, colour bars, centred capitals, simple line art.
- Headlines: Poppins Bold/Medium with faux Cyrillic made by mirroring N and R (and a tailed U in the title only).
  Mirroring applies to English words only. Russian words stay plain: add them to `RUS` in `common.py`.
- Body: Courier 10 Pitch typewriter. Text needed to play is black; flavor text and glosses are dark grey (`FLAV`).
- Board stickers use board green chip G (`#BFDDC8`), matched to the owner's board.
- "Flair" means professional colour, layout and typography, never emojis or doodles.

**Numbers**
- Every money amount is a multiple of 10. The 1 and 5 notes are retired.
- Prices and colour groups follow the classic board. Fee ladders never decrease.
- Pledge value is half the price rounded to 10. Redeem is pledge + 20 (under 200), + 30 (under 300), + 40.
- Quotas rise every Year and with player count. Kulak Line is in `game.py` and printed from there.
- Each deck has exactly one card that gains and one that loses Suspicion, and one get-out-of-the-Gulag card.
  There are exactly 3 Sabotage cards (2 Directives, 1 Kitchen Rumor) because the Spets depends on them.

**Physical**
- Measured board: property space 1 5/8 x 2 9/16 in, corners 2 9/16 in, logo bar 11 3/8 x 2 5/16 in,
  card outlines 3 5/16 x 2 3/16 in, cards 2 1/8 x 3 3/16 in.
- Everything prints on US Letter at 100%. Keep ink at least 0.2 in from every page edge.
- Paper: orange cardstock (Directives), yellow (Kitchen Rumors), white (deeds, characters, chits), ivory (aids,
  trackers), matte full-sheet sticker paper, plain paper (rulebook). All cardstock 65 lb.
- Double-sided pieces are printed by hand-flipping on the long edge, so back pages are mirrored left to right.
- Aids are postcard-brief and single-sided. Suspicion and the Year are tracked with black glass beads on separate
  trackers and a board sticker. Blat stays as cardstock chits.
- The rulebook has an even page count of 8 or fewer so its back cover lands on the back of a sheet.
- Returning players reprint as little as possible. Every release ships an update pack with only the pages whose
  printed pieces changed. Double-sided sheets go in front and back together; the rulebook is one object and goes in
  whole if any page changed. Version stamps and the printing notes at the top and bottom of sheets don't count as
  changes. Keep piece positions stable between releases so an edit touches as few sheets as possible.

## Branches, versions and releases

- All work goes on `develop`. `main` only receives releases.
- Versions follow `MAJOR.MINOR.PATCH`. In beta (0.x): a rules change bumps MINOR; a wording, art, layout or
  print fix bumps PATCH. 1.0.0 means out of beta.
- Record changes under `## Unreleased` at the top of `CHANGELOG.md` as you make them.
- To release:
  1. On `develop`: set `VERSION` and rename `## Unreleased` to `## vX.Y.Z (Month YYYY)`. Run the build and QC.
  2. Merge `develop` into `main` (fast-forward) and push.
  3. GitHub Actions runs QC in release mode, builds every PDF, builds the update pack against the previous release,
     tags the commit and publishes a pre-release with all PDFs attached. The notes say what to reprint, then quote
     the changelog section. Nothing else to do.

## Continuous integration

- `.github/workflows/quality.yml`: on every push and PR to `develop` and `main`, builds and runs `src/qc.py`.
  On `main` it runs with `QC_RELEASE=1`, which requires a changelog section for `VERSION` and no `Unreleased`.
  It also builds a preview update pack against the latest release: what to reprint goes in the run summary and
  the pack is uploaded as the `update-pack-preview` artifact.
- `.github/workflows/build.yml`: builds on every push, uploads the PDFs as a run artifact, and on `main` publishes
  the release when `VERSION` has none yet. The QC gate runs before publishing.

## Working here as Claude

- Commit as `Claude <noreply@anthropic.com>` so commits show as verified.
- These sessions can push branches but cannot push tags, create releases, or change repo settings (description,
  topics, default branch). Releases come from Actions; settings are for the owner to change.
- Sessions do not keep files between conversations. Everything needed to rebuild lives in this repo.
- When a QC check fails, fix the content, not the check, unless the owner has changed the rule. Report anything a
  returning player would need to reprint.
