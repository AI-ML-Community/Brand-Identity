# Brand Identity

A practical skill for designing durable, distinctive logo systems—not generic category icons. It guides an identity from a product brief to a tested, production-ready set of marks, wordmarks, lockups, app icons, splash screens, and an offline brand sheet.

The standard is simple: the mark should be memorable enough to draw from memory, specific enough that a competitor could not adopt it, meaningful enough that every shape has a reason, and robust enough to work in one colour and at 16 px.

## What it does

The workflow helps you:

- derive concepts from a product’s own rituals, language, and name instead of category clichés;
- explore multiple SVG directions and judge rendered output on light, dark, and tiny-size backgrounds;
- refine one direction with controlled, single-change variants;
- express the final mark as a small system of ratios built on one base unit;
- create outlined wordmarks with real font kerning and one detail that echoes the mark;
- generate consistent SVG exports, preview PNGs, app-icon assets, splash screens, and a self-contained HTML brand sheet from one build script;
- validate the brand sheet and visually inspect the final output before delivery.

It is designed for product logos, app icons, favicons, splash screens, visual identities, and brand-guideline deliverables.

## Design principles

Start with the product, not its market category. Identify the product’s distinctive objects, actions, and promises; combine them with useful letterforms from the name; then reject concepts that fail these tests:

- **Swap test:** a competitor could use it unchanged.
- **Sentence test:** it cannot be explained in one sentence where each shape earns a clause.
- **Sketch test:** it cannot be redrawn from memory after one look.

The final system keeps to three shapes or fewer, two colours or fewer, a single purposeful accent, and no gradients, shadows, outlines, or live text in logo files. See [the full skill instructions](SKILL.md), [category cliché ban lists](references/cliches.md), and [the LearnitPal case study](references/case-study-learnitpal.md) for the rationale.

## Workflow

1. Gather the brief: exact brand name, product purpose, audience, applications, existing visual tokens, and desired character.
2. Write 12–20 product-specific concepts and keep the three most distinct survivors.
3. Draw and render the three concepts together; select one based on what is visible, not SVG source code.
4. Produce three or four single-change refinements; test each on light and dark grounds and at 48, 32, and 16 px.
5. Define the chosen mark’s geometry with one base unit (`T`), then create an outlined wordmark and horizontal lockup.
6. Generate the complete export set from one `build.py` script.
7. Create and check a standalone HTML brand sheet, then inspect a screenshot and correct visible issues.

## Included tools

| Tool | Purpose |
| --- | --- |
| [`scripts/setup.sh`](scripts/setup.sh) | Creates the Python environment and installs/checks `fonttools`, `uharfbuzz`, and `rsvg-convert`. Prints the Python executable to use. |
| [`scripts/contact_sheet.py`](scripts/contact_sheet.py) | Renders several SVG concepts or variants side by side, including light/dark grounds and a tiny-size strip. |
| [`scripts/wordmark.py`](scripts/wordmark.py) | Shapes a real font with HarfBuzz, converts glyphs to SVG paths, and can replace `i`/`j` dots with an accent echo detail. |
| [`scripts/check_html.py`](scripts/check_html.py) | Checks an offline brand sheet for its document skeleton, balanced tags, safe persisted theme toggle, and external assets. |

Run setup once from the repository root:

```bash
BRAND_PY=$(./scripts/setup.sh)
```

Use the returned executable for the Python utilities:

```bash
"$BRAND_PY" scripts/contact_sheet.py concept-a.svg concept-b.svg concept-c.svg \
  --out renders/explore.png

"$BRAND_PY" scripts/contact_sheet.py variant-a.svg variant-b.svg variant-c.svg \
  --grounds "#F9F5EF,#14110D" \
  --swap "#1B1712=#F3EEE6" \
  --tiny 48,32,16 \
  --out renders/refine.png

"$BRAND_PY" scripts/wordmark.py \
  --font /path/to/Brand-Bold.ttf \
  --text "Brand Name" \
  --track -14 \
  --echo-dots circle \
  --json wordmark.json \
  --svg wordmark-preview.svg

"$BRAND_PY" scripts/check_html.py brand-sheet.html
```

`rsvg-convert` is required for SVG rendering. On macOS, the setup script can install it through Homebrew if it is missing.

## Expected deliverables

Generate these from a single script so every variant shares the same geometry:

- colour, reversed, mono-dark, and mono-white versions of the mark, wordmark, and horizontal lockup;
- a full-bleed 1024 px app icon and Android adaptive-icon foreground;
- light and dark 1080 × 2400 splash screens;
- PNG previews, including 48 px, 32 px, and 16 px icon checks;
- an offline `brand-sheet.html` with the concept, construction ratios, colour roles, logo applications, usage rules, and all SVG files.

The exact naming, dimensions, platform notes, and brand-sheet requirements are in [references/deliverables.md](references/deliverables.md).

## Reference implementation

[`examples/learnitpal`](examples/learnitpal) is a complete worked example. It includes exploration, refinement, a reusable build script, generated SVG assets, PNG renders, and the finished brand sheet.

To study or adapt it:

```bash
cd examples/learnitpal
mkdir -p out/svg out/png
BRAND_FONT=/path/to/Brand-Bold.ttf BRAND_OUT="$PWD/out" "$BRAND_PY" build.py
BRAND_OUT="$PWD/out" "$BRAND_PY" sheet.py
```

For a ready-to-fill brief you can give another agent or designer, use [references/agent-prompt.md](references/agent-prompt.md).

## Repository layout

```text
SKILL.md                         Complete workflow and quality bar
scripts/                         Setup, rendering, wordmark, and HTML-check utilities
references/                      Deliverables, cliché lists, worked case study, and agent brief
examples/learnitpal/             Reference implementation and finished assets
```

## Final review checklist

- The mark survives the swap, sentence, and sketch tests.
- It has three shapes or fewer and two colours or fewer.
- It is legible in one colour, on dark backgrounds, and at 16 px.
- The wordmark uses outlined glyphs from a real font, with only one intentional echo detail.
- All exported files come from shared geometry and have been rendered and inspected.
- The brand sheet opens offline and passes `check_html.py`.
