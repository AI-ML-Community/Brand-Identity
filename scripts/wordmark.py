#!/usr/bin/env python3
"""Outline a wordmark from a real font file, with the font's own kerning.

Logo files must never contain live text. This shapes the text with HarfBuzz,
converts every glyph to a path with fontTools, and can lift the dot off i/j so
it can be replaced with a detail that echoes the mark (a circle in the accent).

  python wordmark.py --font Bold.ttf --text learnitpal --track -14 \
      --echo-dots circle --json out.json --svg preview.svg

JSON output (font units, baseline at y=0, y grows DOWN like SVG):
  d          path data for all letters (without lifted dots)
  dots       [{cx, cy, r}] circles replacing lifted dots (cy negative = above baseline)
  advance    total width
  ascender   height of the tallest glyph top above baseline
  descender  depth of the lowest glyph bottom below baseline (positive)
  unitsPerEm, xHeight, capHeight
Scale by (target_px / ascender) or (target_px / xHeight) when placing it.
"""
import argparse, json
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

DOTTED = {"i", "j"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--track", type=float, default=0, help="extra space per glyph, font units (negative = tighter)")
    ap.add_argument("--echo-dots", choices=["none", "circle"], default="none",
                    help="lift the dots of i/j and return them as circles")
    ap.add_argument("--dot-scale", type=float, default=1.08, help="circle size vs the original dot (circles read smaller)")
    ap.add_argument("--features", default="kern", help="comma list of OpenType features to enable")
    ap.add_argument("--json", help="write geometry JSON here")
    ap.add_argument("--svg", help="write a preview SVG here")
    ap.add_argument("--ink", default="#1B1712")
    ap.add_argument("--accent", default="#E0962C")
    ap.add_argument("--bg", default="", help="preview background colour (default transparent)")
    a = ap.parse_args()

    font = TTFont(a.font)
    gs = font.getGlyphSet()
    order = font.getGlyphOrder()
    hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(a.font)))
    buf = hb.Buffer(); buf.add_str(a.text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {f: True for f in a.features.split(",") if f} | {"liga": False})

    def bounds(ops):
        bp = BoundsPen(gs)
        for op, args in ops:
            getattr(bp, op)(*args)
        return bp.bounds

    x, paths, dots = 0.0, [], []
    top, bottom = 0.0, 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        pen = DecomposingRecordingPen(gs); gs[name].draw(pen)
        contours, cur = [], []
        for op, args in pen.value:
            cur.append((op, args))
            if op in ("closePath", "endPath"):
                contours.append(cur); cur = []
        b = bounds(pen.value)
        if b:
            top, bottom = max(top, b[3]), min(bottom, b[1])
        if a.echo_dots == "circle" and name in DOTTED and len(contours) > 1:
            contours.sort(key=lambda c: -bounds(c)[3])
            dot, contours = contours[0], contours[1:]
            x0, y0, x1, y1 = bounds(dot)
            dots.append({"cx": round(x + pos.x_offset + (x0 + x1) / 2, 2), "cy": round(-(y0 + y1) / 2, 2),
                         "r": round(max(x1 - x0, y1 - y0) / 2 * a.dot_scale, 2)})
        sp = SVGPathPen(gs)
        tp = TransformPen(sp, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset))
        for c in contours:
            for op, args in c:
                getattr(tp, op)(*args)
        paths.append(sp.getCommands())
        x += pos.x_advance + a.track
    advance = x - a.track
    os2 = font["OS/2"]
    out = {"d": " ".join(p for p in paths if p), "dots": dots, "advance": round(advance, 2),
           "ascender": top, "descender": -bottom, "unitsPerEm": font["head"].unitsPerEm,
           "xHeight": getattr(os2, "sxHeight", None), "capHeight": getattr(os2, "sCapHeight", None)}
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f)
    if a.svg:
        pad = 60
        w, h = advance + pad * 2, top - bottom + pad * 2
        body = f'<path transform="translate({pad} {pad + top})" d="{out["d"]}" fill="{a.ink}"/>'
        for d in dots:
            body += f'<circle cx="{pad + d["cx"]}" cy="{pad + top + d["cy"]}" r="{d["r"]}" fill="{a.accent}"/>'
        bg = f'<rect width="100%" height="100%" fill="{a.bg}"/>' if a.bg else ""
        with open(a.svg, "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}">'
                    f"{bg}{body}</svg>\n")
    if not a.json and not a.svg:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
