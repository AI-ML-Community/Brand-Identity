---
name: brand-identity
description: >
  Design a memorable, non-generic logo system and brand identity (mark, wordmark, lockups,
  app icon, splash screens, print-ready SVGs, standalone brand sheet) at the level of Google,
  Meta, X, Cursor, Stripe or Linear. Use when the user asks for a logo, brand mark, wordmark,
  app icon, splash screen, favicon, brand identity or brand guidelines for any product, app
  or website, or wants a prompt that makes other agents produce that calibre of identity work.
---

# Brand identity

The goal is a mark that is **simple** (drawable from memory), **specific** (no competitor could use it), **meaningful** (every shape has a reason) and **durable** (works in one colour, at 16px, in print).

Most generated logos fail for one reason: they are designed from the product's *category* ("a learning app"), so they reuse the category's clichés. Design from the *product* instead, and judge only what you have rendered and looked at, never the SVG code.

Everything this skill needs lives in this folder (`~/.claude/skills/brand-identity/`):

| Path | What it is |
|---|---|
| `scripts/setup.sh` | One-time toolchain (fonttools, uharfbuzz, rsvg-convert). Prints the python to use. |
| `scripts/wordmark.py` | Outlines text from a real font file with its kerning; can lift the i/j dots to use as an echo detail. |
| `scripts/contact_sheet.py` | Renders several SVG marks side by side on light and dark grounds, with a tiny-size strip, to PNG. |
| `scripts/check_html.py` | Checks a standalone brand sheet: skeleton, tags, theme toggle, no external assets. |
| `references/case-study-learnitpal.md` | The worked example: every decision and why. Read it before starting. |
| `references/cliches.md` | Ban lists of generic tropes by category. |
| `references/deliverables.md` | The exact export set, sizes, Android/iOS/web notes, brand sheet spec. |
| `references/agent-prompt.md` | A self-contained prompt to give *other* agents or tools. |
| `examples/learnitpal/` | The real scripts (`explore.py`, `refine.py`, `build.py`, `sheet.py`), all final SVGs, renders of each stage, and the finished brand sheet. Use them as a reference implementation. |

If the user asks for **a prompt** for another agent, give them `references/agent-prompt.md` (copy it to where they want it). Otherwise, carry out the process below yourself.

## 0. Set up and gather the brief

Run `~/.claude/skills/brand-identity/scripts/setup.sh` and use the python it prints. Work in the session scratchpad. Deliver final files where the user asks, or else in `~/Documents/<brand>-brand/`.

Pin down the brief. Answer these from the codebase or product wherever you can, and ask only for what you can't find:
- the brand name, spelled and capitalised exactly
- what the product does, in one sentence
- the audience
- where the logo will live: app icon, splash, web header, print, merch
- existing colours, fonts or theme tokens (search for theme or tailwind files, `colors.xml`, font folders)
- three adjectives for how it should feel

**Honour an existing system.** If the product already has colours and fonts, the identity uses them.

## 1. Find the meaning (words only, no drawing)

1. List the product's own nouns, verbs and rituals: the things only this product has. From LearnitPal: "one pick a day", "keeps your place", "swipe to pass". Also list what the brand name gives you: its initial, distinctive letters, doubled letters.
2. Open `references/cliches.md`. Write down the banned tropes for this category, plus any the product's world adds.
3. Write 12–20 concepts. A strong concept joins **an object from the product's world + a letter of the name + the product's promise** into one shape. LearnitPal's: a bookmark ribbon folded into an L, cradling one amber dot, the pick that keeps your place.
4. Kill any concept that fails a test:
   - **Swap:** a competitor could use it unchanged.
   - **Sentence:** it can't be explained in one sentence where every shape earns a clause.
   - **Napkin:** it can't be drawn from memory after one look.
5. Keep the **three most different** survivors.

## 2. Explore by rendering

1. Hand-write each of the three as SVG on one grid (512×512, flat fills, brand palette).
2. Render them with `scripts/contact_sheet.py a.svg b.svg c.svg --out explore.png`, then **Read the PNG**.
3. Critique each in writing: generic, derivative of an existing brand, or carrying a real idea. Pick one and say why the others lost.

## 3. Refine one concept

1. Make 3–4 variants that each change **one** thing (a corner, a terminal, a fold, the accent's size).
2. Render them on light and dark grounds with a tiny-size strip:
   `contact_sheet.py v1.svg v2.svg v3.svg --grounds "#F9F5EF,#14110D" --swap "#1B1712=#F3EEE6" --tiny 48,32,16 --out refine.png`
3. Drop details that vanish at small sizes: thin gaps, hairline creases, two tones. When two variants are close, choose the one with fewer parts.

## 4. Systematise

- **Build on one unit.** Choose a base unit, usually the stroke width `T`. Every measure is a ratio of `T`, and you record the ratios (for LearnitPal: notch 0.43T, dot radius ⅔T, clearance ¼T, clear space ½T).
- **Constraints:**
  - three shapes or fewer
  - two colours or fewer, with the accent on one meaningful element only
  - no gradients, shadows, outlines or thin strokes
  - the mark must survive in one colour
- **Optical corrections:**
  - circles read smaller than squares, so size them up slightly
  - nudge asymmetric marks off true centre so they look centred
  - check every gap at 16px
- **Neutrals:** give them a slight hue bias. Never use pure grey.

## 5. Wordmark and lockups

1. Outline the wordmark from the brand's font. Never use live text in logo files:
   `wordmark.py --font Bold.ttf --text <name> --track -14 --echo-dots circle --json word.json --svg word.svg`
   Slightly tight tracking suits display sizes.
2. Give the wordmark **one** detail that echoes the mark: a tittle, a counter or a terminal. LearnitPal's i-dot is the mark's amber dot. One echo looks intentional; two looks like a gimmick.
3. For the horizontal lockup, put the mark's base on the text baseline and make the mark about **1.15× the ascender** tall. Set the gap at about 1.25T at the mark's scale.
4. Render the lockup and look at it. If the mark overpowers the word, scale the mark down. Re-render once.

## 6. Generate the full set from one script

Write a single `build.py` that defines the geometry once and writes every file, so changing one ratio rebuilds everything consistently. Use `examples/learnitpal/build.py` as the model. The exact export list is in `references/deliverables.md`:
- mark, wordmark and lockup, each in colour, reversed, mono dark and mono white
- the app icon, full bleed at 1024
- the Android adaptive-icon foreground
- light and dark splash screens
- PNG previews and a favicon check

## 7. Brand sheet

Generate a **standalone HTML** brand sheet from the same SVG files; `examples/learnitpal/sheet.py` is the model, and `references/deliverables.md` has the spec. It must contain:
- the one-sentence idea
- a construction diagram showing the unit ratios
- the logo on light, dark and accent grounds
- the lockups
- the app icon at 48, 32 and 16px, and the splash screens
- swatches with hex values and the role of each
- "keep it whole" rules and minimum sizes
- the file list
- a light/dark toggle saved to localStorage inside try/catch

Run `scripts/check_html.py` on it.

## 8. Verify, then report

1. Screenshot the sheet once. With Chrome headless: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --window-size=1280,2600 --screenshot=out.png file://<path>`.
2. Read the screenshot. Fix what you see (clipped labels, imbalance, unreadable small sizes), then stop polishing.
3. Report in this order:
   - the idea in two sentences
   - why it isn't generic, including what you rejected
   - exact file paths
   - what isn't done yet (e.g. "not yet wired into the launcher icon")

   Offer to wire the icon and splash into the app as a separate step.

## Quality bar (reread before delivering)

- [ ] Drawable from memory; three shapes or fewer; two colours or fewer.
- [ ] Fails the swap test for every competitor, and uses nothing from the cliché list.
- [ ] Every shape earns a clause in the one-sentence story.
- [ ] Holds up in one colour, on dark, and at 16px. You rendered and looked at all three.
- [ ] Built on one unit, generated by one script, and the files are consistent.
- [ ] The wordmark is outlined from a real font, with exactly one echo detail.
- [ ] The report is honest: rejected directions, file paths, what's unfinished.
