# Deliverables spec

Generate every file from a single `build.py` that defines the geometry once. `../examples/learnitpal/build.py` is the reference implementation. Use the brand name as the file prefix.

## SVG set (`svg/`)

| File | Content |
|---|---|
| `<b>-mark.svg` | Colour mark on a transparent ground, with a quiet zone of ½T |
| `<b>-mark-reversed.svg` | For dark grounds: ink swapped to a warm off-white, accent unchanged |
| `<b>-mark-mono.svg` | Every shape in ink, for single-colour print and stamping |
| `<b>-mark-mono-white.svg` | Every shape in white, for photos and colour grounds |
| `<b>-wordmark[-reversed\|-mono\|-mono-white].svg` | Outlined wordmark with its echo detail, in the same four versions |
| `<b>-lockup[-reversed\|-mono\|-mono-white].svg` | Horizontal lockup: mark on the baseline at ~1.15× ascender, gap ~1.25T |
| `<b>-app-icon.svg` | 1024×1024, **full bleed** ground, mark at ~55% width, optically centred |
| `<b>-app-icon-light.svg` | The same icon on the light ground |
| `<b>-adaptive-foreground.svg` | Android adaptive icon: 108dp canvas (432 units), mark inside the central 66dp safe circle |
| `<b>-splash-light.svg` / `-dark.svg` | 1080×2400, mark stacked over wordmark, block centred slightly above the middle |

**Rules for the SVGs:**
- Every file has a `viewBox`, `role="img"` and a `<title>`.
- No live `<text>`, no strokes (outline everything), no filters, no gradients.
- Coordinates rounded to 2 decimals.

## PNG previews (`png/`)

Render with `rsvg-convert -w <px> in.svg -o out.png`:
- mark at 512
- lockup at 1600
- app icon at 1024
- splash at 540
- icon at **48, 32 and 16** (the favicon test)

Read at least the lockup, the app icon, one splash and the 48px icon before delivering.

## Platform wiring (offer it separately; don't do it unasked)

**Android**
- Launcher: `mipmap-anydpi-v26/ic_launcher.xml` with a `<background>` colour and a `<foreground>` vector drawable made from the adaptive foreground. Legacy PNGs go in mdpi 48, hdpi 72, xhdpi 96, xxhdpi 144 and xxxhdpi 192 (plus `ic_launcher_round`).
- Splash (Android 12+ `SplashScreen` API): `windowSplashScreenBackground` set to the ground colour. `windowSplashScreenAnimatedIcon` is the mark inside a 240dp icon with a 160dp safe circle. Define a `values-night` variant for dark.
- Convert SVG to a vector drawable by hand or with Android Studio's Vector Asset tool. Keep paths flat.

**iOS:** a 1024 AppIcon with no transparency and no pre-rounded corners. `LaunchScreen.storyboard` with the ground colour and a centred mark image (PDF or SVG asset, "Preserve Vector Data").

**Web:**
- `favicon.svg` with a `prefers-color-scheme` media query inside it for dark tabs
- `favicon.ico` at 16 and 32
- `apple-touch-icon.png` at 180
- `icon-192.png` / `icon-512.png` plus a maskable version with 20% padding
- `og-image` at 1200×630 using the lockup

## Brand sheet (`index.html`)

A **standalone** file that opens offline in any browser:
- `<!doctype html>`, `<html lang>`, head with charset and viewport, body
- base reset: `color-scheme`, `body{margin:0}`, `img{max-width:100%}`, `[hidden]{display:none!important}`
- light palette tokens on `:root`, the dark palette under `@media (prefers-color-scheme: dark)` guarded with `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]`
- a theme toggle that cycles system, light and dark, saved in `localStorage` inside try/catch
- inline CSS and inline SVG; no JS libraries; real font fallback stacks (a Google Fonts link is optional; never embed fonts as data URIs unless asked)

Sections, in order:
1. **Hero:** the mark large, next to the one-sentence idea ("A bookmark, folded into an L, keeping your place.") and a short paragraph on what each shape means.
2. **Construction:** an SVG diagram of the mark on a grid, with dimension lines labelled in units of T, and a note on clear space.
3. **On every ground:** the mark on light, dark and accent grounds (mono on accent), and the lockup on light, dark and white (mono).
4. **App icon and splash:** why the icon is full bleed; the icon at 48, 32 and 16px; both splash screens in phone frames.
5. **Colour:** swatches with name, hex value and role ("Amber: only ever the dot").
6. **Keep it whole:** 6 rules at most, covering accent usage, no rounding or softening, no moving the key element, no effects, minimum sizes (e.g. mark 16px / 5mm, lockup 96px / 20mm), wordmark never retyped.
7. **Files:** a list of every SVG.

Run `../scripts/check_html.py index.html`, take one screenshot, fix what it shows, and deliver.
