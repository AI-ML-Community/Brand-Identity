# LearnitPal exploration stage: writes SVG next to the working directory; render with rsvg-convert or ../../scripts/contact_sheet.py.
INK="#1B1712"; AMBER="#E0962C"; PAPER="#F9F5EF"
T=92  # stroke weight

def frame(x, body):
    return f'<g transform="translate({x},0)">{body}</g>'

def dot(cx, cy, r): return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{AMBER}"/>'

# Geometry: L occupies x 120..392, y 104..408 (centred on 256).
L, R, TOP, BOT = 120, 392, 104, 408
N = 40  # notch depth
def a_notch_square():
    d=f'M{L} {TOP} L{L+T/2} {TOP+N} L{L+T} {TOP} V{BOT-T} H{R} V{BOT} H{L} Z'
    return f'<path fill="{INK}" d="{d}"/>' + dot(L+T+22+62, BOT-T-22-62, 62)

def b_notch_round():
    r=T/2
    d=f'M{L} {TOP} L{L+T/2} {TOP+N} L{L+T} {TOP} V{BOT-T} H{R-r} A{r} {r} 0 0 1 {R-r} {BOT} H{L} Z'
    return f'<path fill="{INK}" d="{d}"/>' + dot(L+T+22+62, BOT-T-22-62, 62)

def d_folded():
    # Two halves of one ribbon meeting at a 45° crease through the corner.
    g=7  # crease gap
    vert=f'M{L} {TOP} L{L+T/2} {TOP+N} L{L+T} {TOP} V{BOT-T-g*0.7} L{L} {BOT-g*0.7-T+T} Z'
    # vertical piece: from top down to the diagonal line joining outer corner (L,BOT) and inner corner (L+T,BOT-T)
    vert=f'M{L} {TOP} L{L+T/2} {TOP+N} L{L+T} {TOP} V{BOT-T-g} L{L} {BOT-g} Z'
    horiz=f'M{L+g} {BOT} L{L+T+g} {BOT-T} H{R} V{BOT} Z'
    return f'<path fill="{INK}" d="{vert}"/><path fill="{INK}" d="{horiz}"/>' + dot(L+T+22+62, BOT-T-22-62, 62)

def e_folded_amberfold():
    # The horizontal half is the ribbon's underside: a shade lighter.
    g=0
    vert=f'M{L} {TOP} L{L+T/2} {TOP+N} L{L+T} {TOP} V{BOT-T} L{L} {BOT} Z'
    horiz=f'M{L} {BOT} L{L+T} {BOT-T} H{R} V{BOT} Z'
    return f'<path fill="{INK}" d="{vert}"/><path fill="#4A4238" d="{horiz}"/>' + dot(L+T+22+62, BOT-T-22-62, 62)

cells=[a_notch_square(), b_notch_round(), d_folded(), e_folded_amberfold()]
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{512*len(cells)}" height="512"><rect width="100%" height="100%" fill="{PAPER}"/>'+''.join(frame(i*512,c) for i,c in enumerate(cells))+'</svg>'
open('refine.svg','w').write(svg)
# Small-size test: the same marks at 32px, as a favicon or notification icon.
small=f'<svg xmlns="http://www.w3.org/2000/svg" width="{512*len(cells)}" height="512" viewBox="0 0 {512*len(cells)} 512"><rect width="100%" height="100%" fill="#0C0B0A"/>'+''.join(frame(i*512,c.replace(INK,"#F3EEE6").replace("#4A4238","#B9B2A8")) for i,c in enumerate(cells))+'</svg>'
open('refine-dark.svg','w').write(small)
