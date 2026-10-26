# MONOPOLITBURO

A Stalinist themed Monopoly! Created in part with Claude. Experience the joy of Soviet living!

*Five-Year Plan in Four Years!*

A satirical re-theme of Monopoly set in Stalin's Soviet Union, for 3 to 6 players, in 90 to 120 minutes.
One player is the **Party Secretary**, who runs the bank and must pay Moscow a rising quota every Year.
Everyone else is a **citizen**, getting rich while trying not to look rich. Denounce your rivals, bribe the
Secretary, and keep an eye on your Suspicion: at 5, the black car comes and you become someone else.

> **Beta: v0.2.0.** Every printed piece carries its version number. See [CHANGELOG.md](CHANGELOG.md).

## What you need

- A **retail copy of classic US Monopoly**. MONOPOLITBURO is a modification kit: you keep the board,
  money (10s and up), dice, tokens, houses and hotels, and cover parts of the board with stickers.
- 65 lb cardstock in orange, yellow, white and ivory, plus matte full-sheet sticker paper.
- About 10 black glass beads and a third die for 6-player games.
- A home printer. Everything prints on 8.5 x 11 in at **100% / Actual size**.

## Printing

| File | What it is |
| --- | --- |
| [`print/v0.2.0/MONOPOLITBURO_v0.2.0_Complete.pdf`](print/v0.2.0/MONOPOLITBURO_v0.2.0_Complete.pdf) | Everything for v0.2.0 in one file. Page 1 is the checklist by paper type. |
| [`print/v0.2.0/`](print/v0.2.0/) | The same pages split into decks, deeds, characters, table pieces and rulebook. |
| [`print/board-stickers/`](print/board-stickers/) | Board stickers (unchanged since v0.1.0): name patches, full spaces, corners, deck labels, title banner, maker's mark. |

Deeds and character cards are double-sided: print a FRONTS page, flip the sheet on its long edge,
then print the BACKS page that follows it.

## Building from source

The `src/` folder holds the Python scripts that generate every PDF in `print/v0.2.0/`.

```bash
pip install reportlab
mkdir -p out && cd src
python3 build_cards.py      # decks, deeds, characters
python3 build_table.py      # aids, Suspicion trackers, Blat chits, Year track sticker
python3 rulebook.py         # rulebook with glossary and change log
```

All game numbers and card text live in [`src/game.py`](src/game.py). The version string lives in
[`src/common.py`](src/common.py).

**Fonts** are not bundled. The scripts expect:

- [Poppins](https://fonts.google.com/specimen/Poppins) Bold and Medium (SIL Open Font License) at
  `/usr/share/fonts/truetype/google-fonts/`
- Courier 10 Pitch (Bitstream Type 1) at `/usr/share/fonts/X11/Type1/`. On Debian and Ubuntu:
  `sudo apt install xfonts-scalable`

Adjust the paths at the top of `src/common.py` for your system.

The board-sticker generator was not preserved between v0.1.0 and v0.2.0; the sticker PDF is provided as-is.

## License

- **Code** in `src/` is under the [MIT License](LICENSE).
- **Game content** (rules, card text, flavor text, artwork, Comrade Kopeikin and the printed PDFs) is under
  [CC BY-NC-SA 4.0](LICENSE-CONTENT.md): share and remix with credit, non-commercially, under the same terms.

## Disclaimer

MONOPOLITBURO is an unofficial, non-commercial fan modification. MONOPOLY is a trademark of Hasbro, which
is not affiliated with and does not endorse this project. No Hasbro artwork, characters or logos are
reproduced. You need a retail copy of the game to play.

This is satire. The jokes are aimed at the system, never its victims. The history in the grey type is real.
