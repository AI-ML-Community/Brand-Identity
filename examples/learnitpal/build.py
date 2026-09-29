# Reference implementation from the LearnitPal identity. Set BRAND_OUT / BRAND_FONT to reuse it.
import os, subprocess
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = os.environ.get("BRAND_OUT", os.path.join(os.getcwd(), "learnitpal-brand"))
FONT = os.environ["BRAND_FONT"]  # e.g. PlusJakartaSans-Bold.ttf
INK, AMBER, PAPER, NIGHT = "#1B1712", "#E0962C", "#F9F5EF", "#14110D"
PAPER_ON_DARK = "#F3EEE6"

# ---------- the mark: a bookmark ribbon folded into an L, holding one amber pick ----------
# Grid 272 x 304. Stroke T, bookmark notch N at the top of the ribbon.
T, N, W, H = 92, 40, 272, 304
R_DOT = 62
DOT = (T + 84, H - T - 84)
def mark_paths(x=0, y=0, s=1.0):
    P = lambda px, py: f"{x + px * s:.2f} {y + py * s:.2f}"
    ribbon = (f"M{P(0,0)} L{P(T/2,N)} L{P(T,0)} L{P(T,H-T)} L{P(W,H-T)} "
              f"L{P(W,H)} L{P(0,H)} Z")
    cx, cy, r = x + DOT[0] * s, y + DOT[1] * s, R_DOT * s
    return ribbon, (cx, cy, r)

def mark_svg_elems(x, y, s, ink, dot):
    ribbon, (cx, cy, r) = mark_paths(x, y, s)
    return (f'<path d="{ribbon}" fill="{ink}"/>'
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{dot}"/>')

# ---------- the wordmark: "learnitpal" in Plus Jakarta Sans Bold, amber tittle ----------
font = TTFont(FONT)
gs = font.getGlyphSet()
blob = hb.Blob.from_file_path(FONT)
hbfont = hb.Font(hb.Face(blob))
TRACK = -14  # units per 1000: set a little tight, it's a display size

def glyph_contours(name):
    pen = DecomposingRecordingPen(gs); gs[name].draw(pen)
    contours, cur = [], []
    for op, args in pen.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            contours.append(cur); cur = []
    return contours

def bounds_of(ops):
    bp = BoundsPen(gs)
    for op, args in ops: getattr(bp, op)(*args)
    return bp.bounds

def wordmark(text="learnitpal"):
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": False})
    x, paths, dots = 0, [], []
    order = font.getGlyphOrder()
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        contours = glyph_contours(name)
        if name == "i":
            # The topmost contour is the tittle: swap it for a circle.
            tops = sorted(contours, key=lambda c: -bounds_of(c)[3])
            tittle, contours = tops[0], tops[1:]
            x0, y0, x1, y1 = bounds_of(tittle)
            dots.append((x + (x0 + x1) / 2, (y0 + y1) / 2, max(x1 - x0, y1 - y0) / 2 * 1.08))
        sp = SVGPathPen(gs)
        tp = TransformPen(sp, (1, 0, 0, -1, x + pos.x_offset, 0))
        for c in contours:
            for op, args in c: getattr(tp, op)(*args)
        paths.append(sp.getCommands())
        x += pos.x_advance + TRACK
    return " ".join(paths), dots, x - TRACK

WORD_D, WORD_DOTS, WORD_W = wordmark()
ASC = 757  # top of the l

def word_elems(x, baseline, s, ink, dot):
    d = f'<path transform="translate({x:.2f} {baseline:.2f}) scale({s:.5f})" d="{WORD_D}" fill="{ink}"/>'
    for cx, cy, r in WORD_DOTS:
        d += f'<circle cx="{x + cx * s:.2f}" cy="{baseline - cy * s:.2f}" r="{r * s:.2f}" fill="{dot}"/>'
    return d

def svg(w, h, body, bg=None, title="LearnitPal"):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{rect}{body}</svg>\n')

def write(name, content):
    with open(f"{OUT}/svg/{name}.svg", "w") as f: f.write(content)

# Mark alone, 1:1 grid with a quiet zone of 1/4 of T around it.
PAD = 46
MW, MH = W + PAD * 2, H + PAD * 2
schemes = {
    "": (INK, AMBER, None),
    "-reversed": (PAPER_ON_DARK, AMBER, None),
    "-mono": (INK, INK, None),
    "-mono-white": ("#FFFFFF", "#FFFFFF", None),
}
for suffix, (ink, dot, bg) in schemes.items():
    write(f"learnitpal-mark{suffix}", svg(MW, MH, mark_svg_elems(PAD, PAD, 1, ink, dot), bg))

# Wordmark alone: cap it at 200px of l-height.
WS = 200 / ASC
WPAD = 40
ww = WORD_W * WS + WPAD * 2
wh = (ASC + 240) * WS + WPAD * 2   # room for the p descender
for suffix, (ink, dot, bg) in schemes.items():
    write(f"learnitpal-wordmark{suffix}", svg(round(ww), round(wh), word_elems(WPAD, WPAD + ASC * WS, WS, ink, dot), bg))

# Horizontal lockup: mark sits on the baseline; its height is 1.3x the l.
def lockup(ink, dot, bg=None, word_l=200, pad=60):
    s_word = word_l / ASC
    s_mark = word_l * 1.16 / H
    gap = T * s_mark * 1.25
    mark_w = W * s_mark
    total_w = pad * 2 + mark_w + gap + WORD_W * s_word
    top = pad
    baseline = top + H * s_mark
    total_h = baseline + 240 * s_word + pad
    body = mark_svg_elems(pad, top, s_mark, ink, dot) + word_elems(pad + mark_w + gap, baseline, s_word, ink, dot)
    return round(total_w), round(total_h), body
for suffix, (ink, dot, bg) in schemes.items():
    w, h, body = lockup(ink, dot)
    write(f"learnitpal-lockup{suffix}", svg(w, h, body, bg))

# Stacked lockup, for the splash and print.
def stacked(ink, dot, cx, top, word_l=120):
    s_word = word_l / ASC
    s_mark = 1.0
    body = mark_svg_elems(cx - W / 2, top, s_mark, ink, dot)
    baseline = top + H + 90 + ASC * s_word
    body += word_elems(cx - WORD_W * s_word / 2, baseline, s_word, ink, dot)
    return body

# App icon (1024, square; the launcher applies its own mask). Mark is optically centred:
# the ribbon's visual mass sits left and low, so nudge it right and up a touch.
def icon(bg, ink, dot, size=1024, scale=1.72):
    mw, mh = W * scale, H * scale
    x = (size - mw) / 2 + 10
    y = (size - mh) / 2 - 6
    return svg(size, size, mark_svg_elems(x, y, scale, ink, dot), bg)
write("learnitpal-app-icon", icon(INK, PAPER_ON_DARK, AMBER))
write("learnitpal-app-icon-light", icon(PAPER, INK, AMBER))
# Android adaptive icon foreground: 108dp canvas, mark inside the 66dp safe circle.
write("learnitpal-adaptive-foreground", svg(432, 432,
      mark_svg_elems((432 - W * 0.72) / 2 + 4, (432 - H * 0.72) / 2 - 2, 0.72, PAPER_ON_DARK, AMBER)))

# Splash screens, phone portrait (1080 x 2400).
SW, SH = 1080, 2400
write("learnitpal-splash-light", svg(SW, SH, stacked(INK, AMBER, SW / 2, 820), PAPER))
write("learnitpal-splash-dark", svg(SW, SH, stacked(PAPER_ON_DARK, AMBER, SW / 2, 820), NIGHT))

# PNG previews
for name, width in [("learnitpal-mark", 512), ("learnitpal-mark-reversed", 512), ("learnitpal-lockup", 1600),
                    ("learnitpal-lockup-reversed", 1600), ("learnitpal-app-icon", 1024), ("learnitpal-app-icon-light", 1024),
                    ("learnitpal-splash-light", 540), ("learnitpal-splash-dark", 540), ("learnitpal-wordmark", 1200)]:
    subprocess.run(["rsvg-convert", "-w", str(width), f"{OUT}/svg/{name}.svg", "-o", f"{OUT}/png/{name}.png"], check=True)
for px in (16, 32, 48):
    subprocess.run(["rsvg-convert", "-w", str(px), f"{OUT}/svg/learnitpal-app-icon.svg", "-o", f"{OUT}/png/learnitpal-icon-{px}.png"], check=True)
print("word width", WORD_W, "dots", WORD_DOTS)
