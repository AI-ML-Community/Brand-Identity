# LearnitPal: the worked example

Everything produced when the LearnitPal identity was designed. Read `../../references/case-study-learnitpal.md` for the reasoning behind each step.

| Stage | Files |
|---|---|
| 1. Explore: three concepts on one grid | `explore.py`, `renders/1-explore.png` |
| 2. Refine: single-change variants, light, dark and tiny | `refine.py`, `renders/2-refine.png`, `renders/2-refine-tiny.png` |
| 3. Build: the mark from unit T, the outlined wordmark, the full export set | `build.py`, `svg/`, `renders/3-lockup.png`, `renders/3-app-icon.png` |
| 4. Brand sheet | `sheet.py`, `brand-sheet.html`, `renders/4-brand-sheet.png` |

To re-run the build for another brand, copy `build.py` and `sheet.py` into the scratchpad and change the geometry constants and colours. Then:

```bash
PY=$(~/.claude/skills/brand-identity/scripts/setup.sh)
BRAND_FONT=/path/to/Brand-Bold.ttf BRAND_OUT=$PWD/out $PY build.py
BRAND_OUT=$PWD/out $PY sheet.py
```

`build.py` expects `$BRAND_OUT/svg` and `$BRAND_OUT/png` to exist (`mkdir -p out/svg out/png`).
