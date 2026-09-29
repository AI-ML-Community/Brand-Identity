#!/usr/bin/env python3
"""Put several SVG marks side by side on one or more grounds, plus a tiny-size
strip, and render to PNG. This is how concepts and variants get *looked at*:
never judge a logo from its SVG code.

  python contact_sheet.py a.svg b.svg c.svg --out explore.png
  python contact_sheet.py v1.svg v2.svg v3.svg --grounds "#F9F5EF,#14110D" --tiny 48,24,16 --out refine.png

Each input SVG must have a viewBox. For a dark ground, pass reversed versions
of the marks (or use --swap "#1B1712=#F3EEE6" to recolour ink on dark rows).
"""
import argparse, re, subprocess, sys

def load(path):
    s = open(path).read()
    s = re.sub(r"<\?xml.*?\?>", "", s).strip()
    vb = re.search(r'viewBox="([^"]+)"', s)
    if not vb:
        sys.exit(f"{path}: needs a viewBox")
    inner = re.sub(r"^<svg[^>]*>", "", s, count=1)
    inner = re.sub(r"</svg>\s*$", "", inner)
    inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
    return vb.group(1), inner

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svgs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cell", type=int, default=400)
    ap.add_argument("--grounds", default="#F9F5EF")
    ap.add_argument("--swap", default="", help="OLD=NEW colour swaps applied on every ground after the first, comma separated")
    ap.add_argument("--tiny", default="", help="comma list of pixel sizes for a small-size strip, e.g. 48,32,16")
    a = ap.parse_args()

    marks = [load(p) for p in a.svgs]
    grounds = [g for g in a.grounds.split(",") if g]
    swaps = [tuple(x.split("=")) for x in a.swap.split(",") if "=" in x]
    tiny = [int(t) for t in a.tiny.split(",") if t]
    n, c = len(marks), a.cell
    tiny_h = (max(tiny) + 40) if tiny else 0
    W, H = n * c, len(grounds) * c + tiny_h
    body = ""
    for gi, g in enumerate(grounds):
        body += f'<rect x="0" y="{gi * c}" width="{W}" height="{c}" fill="{g}"/>'
        for i, (vb, inner) in enumerate(marks):
            if gi > 0:
                for old, new in swaps:
                    inner = inner.replace(old, new)
            m = c * 0.15
            body += f'<svg x="{i * c + m}" y="{gi * c + m}" width="{c - 2 * m}" height="{c - 2 * m}" viewBox="{vb}">{inner}</svg>'
    if tiny:
        y0 = len(grounds) * c
        body += f'<rect x="0" y="{y0}" width="{W}" height="{tiny_h}" fill="{grounds[0]}"/>'
        for i, (vb, inner) in enumerate(marks):
            x = i * c + 20
            for t in tiny:
                body += f'<svg x="{x}" y="{y0 + 20 + (max(tiny) - t)}" width="{t}" height="{t}" viewBox="{vb}">{inner}</svg>'
                x += t + 16
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'
    tmp = a.out.rsplit(".", 1)[0] + ".svg"
    open(tmp, "w").write(svg)
    subprocess.run(["rsvg-convert", tmp, "-o", a.out], check=True)
    print(a.out)

if __name__ == "__main__":
    main()
