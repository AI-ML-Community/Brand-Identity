# LearnitPal exploration stage: writes SVG next to the working directory; render with rsvg-convert or ../../scripts/contact_sheet.py.
# Three candidate marks on the same 512 grid, rendered side by side to judge.
INK="#1B1712"; AMBER="#E0962C"; PAPER="#F9F5EF"

def nook(x=0,y=0):
    # A bookmark ribbon folded into an L, cradling one amber dot.
    s=f'<g transform="translate({x},{y})">'
    s+=f'<path fill="{INK}" d="M112 96 L164 140 L216 96 V312 H400 L356 364 L400 416 H112 Z"/>'
    s+=f'<circle cx="302" cy="226" r="58" fill="{AMBER}"/></g>'
    return s

def page(x=0,y=0):
    # A page with its corner folded down; the fold is amber: the one worth keeping.
    s=f'<g transform="translate({x},{y})">'
    s+=f'<path fill="{INK}" d="M128 96 H300 L384 180 V416 H128 Z"/>'
    s+=f'<path fill="{AMBER}" d="M300 96 V180 H384 Z"/></g>'
    return s

def spark(x=0,y=0):
    # One line highlighted among three.
    s=f'<g transform="translate({x},{y})">'
    for i,(w,c) in enumerate([(288,INK),(220,AMBER),(160,INK)]):
        s+=f'<rect x="112" y="{150+i*80}" width="{w}" height="48" rx="24" fill="{c}"/>'
    s+='</g>'
    return s

svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="512" viewBox="0 0 1536 512"><rect width="1536" height="512" fill="{PAPER}"/>{nook()}{page(512)}{spark(1024)}</svg>'
open('explore.svg','w').write(svg)
