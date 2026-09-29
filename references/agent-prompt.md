# Brand identity prompt

Paste everything below the line into an agent. Fill in the `{{…}}` fields first. Leave a field blank if you don't know it, and the agent will find the answer in the product or codebase.

---

You are the identity designer for **{{BRAND NAME}}**. Design a logo system at the level of Google, Meta, X, Cursor, Stripe and Linear: a few simple shapes, instantly recognisable, and meaningful to this product and no other. Most agents produce something generic. That is the failure to avoid, and the process below exists to prevent it.

## The brief

- **Brand name, exactly as written:** {{e.g. LearnitPal}}
- **What the product does, in one sentence:** {{e.g. picks the one article worth your time today and keeps your place}}
- **Who it is for:** {{audience}}
- **Where the logo will live:** {{app icon, splash screen, website header, print, merch, favicon…}}
- **Existing colours, fonts, theme files or codebase to honour:** {{paths or hex values; or "none"}}
- **How it should feel, as three adjectives:** {{e.g. calm, bookish, premium}}
- **Where to save the files:** {{e.g. ~/Documents/<brand>-brand/}}

If a codebase or product exists, read it before designing: the theme tokens, fonts, screen names, and the product's core actions and rituals. The strongest ideas come from what the product actually does, not from its category.

## Phase 1: Find the meaning (words only, no drawing yet)

1. List the product's own nouns and verbs. These are the objects, actions and rituals only this product has (for example "one pick per day", "swipe to pass", "keep your place"). Then list the letters and shapes the brand name offers (initials, distinctive letters, a double letter).
2. Write down the **generic tropes for this category, and ban them.** Examples:
   - learning: open book, lightbulb, graduation cap, brain, pencil
   - AI: sparkles, neural-node graphs, gradient orbs, chat bubbles
   - finance: upward arrows, coins, shields
   - health: hearts, leaves, crosses
   - social: speech bubbles, people icons
   - everywhere: globes, generic gradients, letter-in-a-circle, abstract swooshes
3. Write 12–20 candidate concepts. A strong concept joins two or three layers into one shape:
   - **a literal object** from the product's world
   - **the brand's letter or initial**
   - **the product's promise**

   Example: a bookmark ribbon (object) folded into an L (letter), cradling one amber dot (the one pick you'll read today).
4. Apply these tests to each concept and kill the ones that fail:
   - **The swap test:** could a competitor use this mark without changing anything? Kill it.
   - **The sentence test:** can you explain it in one sentence where every shape earns a clause? If one shape has no reason to exist, remove that shape.
   - **The sketch test:** could someone draw it from memory on a napkin after seeing it once?
5. Keep the three most different survivors.

## Phase 2: Explore by rendering, not imagining

1. Draw all three concepts as hand-written SVG on the same grid (512×512 works). Use flat fills and the brand palette.
2. Render them side by side to PNG (for example with `rsvg-convert`) and **look at the image**. Never judge a logo from its SVG code.
3. Write an honest critique of each one. Say which looks generic, which looks like an existing brand, and which has an idea. Pick one. Say why the others lost.

## Phase 3: Refine one concept with controlled variants

1. Make 3–4 variants that each change **one** thing: a corner, an ending, a fold, the dot's size. This isolates what makes it work.
2. Render every variant three ways: on a light ground, on a dark ground, and at a tiny size (about 128px across, and the icon at 48, 32 and 16px). Drop details that disappear when small, such as thin gaps, hairline folds or two tones.
3. Choose the variant that is simplest **and** still carries the idea. When two are close, pick the one with fewer parts.

## Phase 4: Turn it into a system

- **Build on one unit.** Pick one base measure, usually the stroke width `T`. Express every size and gap as a ratio of it (e.g. notch depth 0.43T, dot radius ⅔T, clearance ¼T). Document these ratios.
- **Constraints:**
  - three shapes or fewer
  - two colours or fewer, one of them used only for the single accent
  - no gradients, shadows or outlines
  - the mark must survive in one colour
- **Optical corrections:**
  - circles look smaller than squares, so size them by eye
  - off-balance shapes need a small nudge off true centre
  - check every gap at 16px
- **Use colour with purpose.** Put the accent on one meaningful element only. Pick neutrals with a slight warm or cool bias, not pure grey.

## Phase 5: Wordmark and lockups

1. Draw the wordmark from a **real font file**. Convert the glyph outlines to paths with fontTools and apply the font's kerning with HarfBuzz. Logo files must never contain live text. Tighten letter-spacing slightly for display sizes.
2. Give the wordmark **one** custom detail that echoes the mark, such as a tittle, a counter or a terminal. LearnitPal's i-dot is the mark's amber dot. Change nothing else.
3. For lockups, align the mark to the baseline and size it against the letter heights (about 1.15× the ascender). Set the gap in stroke units. Render the result and check that the mark doesn't overpower the word. Fix that once, then re-render.

## Phase 6: Export a complete set

Generate every file from one script, so a change to one proportion rebuilds everything. Deliver:

- **mark:** colour, reversed (for dark grounds), one colour dark, one colour white
- **wordmark:** the same four versions
- **horizontal lockup:** the same four versions
- **app icon:** 1024×1024 full bleed, so the launcher's mask never cuts the mark, plus an Android adaptive-icon foreground with the mark inside the 66dp safe zone
- **splash screens:** light and dark (1080×2400), mark stacked over wordmark, slightly above centre
- **PNG previews**, plus favicon checks at 16, 32 and 48px

## Phase 7: Brand sheet

Write a single **self-contained HTML file**: doctype, head and body; inline CSS; inline SVG; no JS libraries; real font fallback stacks; a light/dark toggle saved in `localStorage` inside try/catch. It should contain:

- the one-sentence idea
- a construction diagram showing the unit ratios
- the mark on light, dark and accent grounds
- the lockups
- the app icon at small sizes, and the splash screens
- colour swatches with hex values and the role of each
- short "keep it whole" rules: minimum sizes, clear space, what never to do
- the file list

## Phase 8: Verify, then report honestly

1. Render the brand sheet and the key files once, look at them, and fix what you see: clipped labels, imbalance, unreadable small sizes.
2. Check that the HTML has no unclosed tags.
3. Report back in this order:
   - the idea in two sentences
   - why it isn't generic
   - the exact file paths
   - what is not done yet (e.g. "not yet wired into the app's launcher icon")

## Quality bar (reread before delivering)

- **Simple:** it can be drawn from memory.
- **Specific:** it fails the swap test for every competitor.
- **Meaningful:** every shape has a reason, stated in one sentence.
- **Durable:** it works in one colour, at 16px, engraved, embroidered and on a busy screen.
- **Systematic:** it is built from one unit, generated from one script, and the files are consistent.
- **Honest:** say what you rejected and why, and never present unverified output as finished.
