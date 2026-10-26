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

Download the latest print files from **[Releases](https://github.com/MartyrZombie/Monopolitburo/releases/latest)**.

| File | What it is |
| --- | --- |
| `MONOPOLITBURO_vX.Y.Z_Complete.pdf` | Everything in one file. Page 1 is the checklist by paper type. |
| `Monopolitburo_vX.Y.Z_1_Decks.pdf` … `5_Rulebook.pdf` | The same pages split by component. |
| `Monopolitburo_v0.1.0_Board_Stickers.pdf` | Board stickers (unchanged since v0.1.0), also in [`print/board-stickers/`](print/board-stickers/). |

Print at **100% / Actual size**. Deeds and character cards are double-sided: print a FRONTS page, flip the
sheet on its long edge, then print the BACKS page that follows it.

## Building from source

```bash
pip install -r requirements.txt
python3 src/build_package.py
```

Everything lands in `out/`. All game numbers and card text live in [`src/game.py`](src/game.py); the version
lives in the [`VERSION`](VERSION) file and is stamped on every printed piece.

**Fonts** are not bundled:

- [Poppins](https://fonts.google.com/specimen/Poppins) Bold and Medium (SIL Open Font License). Set
  `POPPINS_DIR` if they aren't in `/usr/share/fonts/truetype/google-fonts/`.
- Courier 10 Pitch (Bitstream Type 1). On Debian and Ubuntu: `sudo apt install xfonts-scalable`. Set
  `TYPE1_DIR` if it isn't in `/usr/share/fonts/X11/Type1/`.

The board-sticker generator was not preserved between v0.1.0 and v0.2.0; the sticker PDF is provided as-is.

## Development and releases

- All work happens on the **`develop`** branch. `main` only receives finished releases.
- Every push to `develop` builds the PDFs in GitHub Actions. Download them from the run's **Artifacts** to
  test-print before releasing.
- Versions follow `MAJOR.MINOR.PATCH`. While in beta (0.x): a rules change bumps MINOR, a wording, art or
  layout fix bumps PATCH. 1.0.0 means out of beta.

To cut a release:

1. On `develop`, update [`VERSION`](VERSION) and add a `## vX.Y.Z` section to [`CHANGELOG.md`](CHANGELOG.md).
2. Merge `develop` into `main`.
3. On GitHub, **Releases → Draft a new release**, create tag `vX.Y.Z` on `main`, tick *Set as a pre-release*
   while in beta, and publish. Actions checks the tag matches `VERSION`, builds every PDF, attaches them to
   the release and fills in the notes from the changelog. Leave the notes blank; they get replaced.

## License

- **Code** in `src/` is under the [MIT License](LICENSE).
- **Game content** (rules, card text, flavor text, artwork, Comrade Kopeikin and the printed PDFs) is under
  [CC BY-NC-SA 4.0](LICENSE-CONTENT.md): share and remix with credit, non-commercially, under the same terms.

## Disclaimer

MONOPOLITBURO is an unofficial, non-commercial fan modification. MONOPOLY is a trademark of Hasbro, which
is not affiliated with and does not endorse this project. No Hasbro artwork, characters or logos are
reproduced. You need a retail copy of the game to play.

This is satire. The jokes are aimed at the system, never its victims. The history in the grey type is real.
