# Reference implementation from the LearnitPal identity. Set BRAND_OUT / BRAND_FONT to reuse it.
import os, re
OUT = os.environ.get("BRAND_OUT", os.path.join(os.getcwd(), "learnitpal-brand"))
def inline(name, cls=""):
    s = open(f"{OUT}/svg/{name}.svg").read().strip()
    s = re.sub(r' width="[\d.]+" height="[\d.]+"', "", s, count=1)
    s = re.sub(r'<title>.*?</title>', "", s)
    return s.replace("<svg ", f'<svg class="{cls}" ', 1)

# Mark with fills driven by CSS tokens so it follows the theme.
def themed_mark(cls):
    s = inline("learnitpal-mark", cls)
    return s.replace('fill="#1B1712"', 'fill="var(--ink)"').replace('fill="#E0962C"', 'fill="var(--amber)"')
def themed_lockup(cls):
    s = inline("learnitpal-lockup", cls)
    return s.replace('fill="#1B1712"', 'fill="var(--ink)"').replace('fill="#E0962C"', 'fill="var(--amber)"')

T, N, W, H, R = 92, 40, 272, 304, 62
construction = f'''<svg class="construct" viewBox="-120 -60 470 430" role="img" aria-label="Construction of the mark on a grid of stroke units">
  <defs><pattern id="g" width="23" height="23" patternUnits="userSpaceOnUse"><path d="M23 0H0V23" fill="none" stroke="var(--grid)" stroke-width="1"/></pattern></defs>
  <rect x="0" y="0" width="{W}" height="{H}" fill="url(#g)"/>
  <path d="M0 0 L{T/2} {N} L{T} 0 L{T} {H-T} L{W} {H-T} L{W} {H} L0 {H} Z" fill="var(--ink)" fill-opacity=".9"/>
  <circle cx="{T+84}" cy="{H-T-84}" r="{R}" fill="var(--amber)"/>
  <circle cx="{T+84}" cy="{H-T-84}" r="3" fill="var(--ink)"/>
  <g stroke="var(--note)" stroke-width="1.5" fill="none">
    <path d="M0 -28 H{T}"/><path d="M0 -34 V-22 M{T} -34 V-22"/>
    <path d="M-28 0 V{N}"/><path d="M-34 0 H-22 M-34 {N} H-22"/>
    <path d="M{T} {H-T-84} H{T+22}"/>
    <path d="M{T+84} {H-T} V{H-T-22}"/>
    <path d="M{T+84} {H-T-84} L{T+84+R*0.707:.1f} {H-T-84-R*0.707:.1f}"/>
    <path d="M{W+28} {H-T} V{H}"/><path d="M{W+22} {H-T} H{W+34} M{W+22} {H} H{W+34}"/>
  </g>
  <g class="lbl" fill="var(--note)">
    <text x="{T/2}" y="-40" text-anchor="middle">T</text>
    <text x="-40" y="{N/2+5}" text-anchor="end">0.43T</text>
    <text x="{T+11}" y="{H-T-92}" text-anchor="middle">¼T</text>
    <text x="{T+100}" y="{H-T-6}" text-anchor="start">¼T</text>
    <text x="{T+84+R*0.707+6:.0f}" y="{H-T-84-R*0.707-6:.0f}">⅔T</text>
    <text x="{W+40}" y="{H-T/2+5}">T</text>
    <text x="{W/2}" y="{H+44}" text-anchor="middle">3T wide · 3.3T tall</text>
  </g>
</svg>'''

swatches = [("Ink", "#1B1712", "Ribbon, wordmark, text"), ("Amber", "#E0962C", "The pick. Only ever the dot."),
            ("Paper", "#F9F5EF", "Light ground"), ("Night", "#14110D", "Dark ground"), ("Paper on dark", "#F3EEE6", "Ribbon on Night")]
sw_html = "".join(f'<li><span class="chip" style="background:{h}"></span><b>{n}</b><code>{h}</code><small>{d}</small></li>' for n, h, d in swatches)

files = sorted(os.listdir(f"{OUT}/svg"))
file_rows = "".join(f"<li><code>svg/{f}</code></li>" for f in files)

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LearnitPal Mark</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap">
<style>
:root{{color-scheme:light dark;
  --bg:#F9F5EF;--surface:#F1EBE2;--ink:#1B1712;--muted:#6E655A;--line:#E2DACE;--amber:#E0962C;--grid:#E4DCD0;--note:#9A6A22;
  --sans:"Plus Jakarta Sans",ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --serif:"Newsreader",Georgia,"Iowan Old Style","Times New Roman",serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#14110D;--surface:#1E1A15;--ink:#F3EEE6;--muted:#A69C8F;--line:#2E2821;--amber:#F0AE45;--grid:#2A241D;--note:#E7B35F}}}}
:root[data-theme="dark"]{{--bg:#14110D;--surface:#1E1A15;--ink:#F3EEE6;--muted:#A69C8F;--line:#2E2821;--amber:#F0AE45;--grid:#2A241D;--note:#E7B35F}}
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans)}}
img,svg{{max-width:100%}}
[hidden]{{display:none!important}}
.wrap{{max-width:1080px;margin:0 auto;padding-inline:24px;padding-block:28px 96px}}
header.top{{display:flex;justify-content:space-between;align-items:center;gap:16px}}
header.top .lock{{height:32px;width:auto}}
button.theme{{font:600 13px/1 var(--sans);color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:999px;padding:9px 14px;cursor:pointer}}
button.theme:focus-visible{{outline:2px solid var(--amber);outline-offset:2px}}
.hero{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:48px;align-items:center;padding-block:72px 56px;border-bottom:1px solid var(--line)}}
.hero .big{{width:100%;max-width:380px;height:auto;justify-self:center}}
h1{{font:500 clamp(34px,5vw,54px)/1.08 var(--serif);letter-spacing:-.01em;margin:0 0 18px;text-wrap:balance}}
h2{{font:700 12px/1 var(--sans);text-transform:uppercase;letter-spacing:.14em;color:var(--muted);margin:0 0 20px}}
p{{margin:0 0 14px;max-width:62ch}}
.lede{{font-size:18px;color:var(--muted)}}
.lede b{{color:var(--ink);font-weight:600}}
section{{padding-block:56px;border-bottom:1px solid var(--line)}}
.two{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;align-items:center}}
.construct{{width:100%;height:auto}}
.construct .lbl{{font:600 15px var(--mono)}}
.grounds{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.ground{{border-radius:14px;aspect-ratio:4/3;display:grid;place-items:center;padding:24px;border:1px solid var(--line)}}
.ground svg{{width:46%;height:auto}}
.ground.wide svg{{width:86%}}
.cap{{font-size:13px;color:var(--muted);margin-top:8px}}
.sizes{{display:flex;align-items:flex-end;gap:28px;flex-wrap:wrap}}
.sizes figure{{margin:0;display:flex;flex-direction:column;align-items:center;gap:8px}}
.sizes figcaption{{font:13px var(--mono);color:var(--muted)}}
.phones{{display:flex;gap:24px;flex-wrap:wrap}}
.phone{{width:min(220px,44%);border-radius:28px;overflow:hidden;border:1px solid var(--line)}}
.phone svg{{display:block;width:100%;height:auto}}
ul.sw{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:20px}}
ul.sw li{{display:grid;grid-template-columns:44px 1fr;column-gap:12px;align-items:center}}
.chip{{grid-row:span 3;width:44px;height:44px;border-radius:50%;border:1px solid var(--line)}}
ul.sw code{{font:13px var(--mono);color:var(--muted)}}
ul.sw small{{font-size:13px;color:var(--muted);line-height:1.35}}
.rules{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 48px;padding:0;margin:0;list-style:none}}
.rules li{{padding-left:22px;position:relative}}
.rules li::before{{content:"";position:absolute;left:0;top:.62em;width:8px;height:8px;border-radius:50%;background:var(--amber)}}
ul.files{{columns:2;column-gap:48px;padding:0;margin:0;list-style:none}}
ul.files code{{font:13px/2 var(--mono);color:var(--muted)}}
@media (max-width:720px){{.hero,.two{{grid-template-columns:1fr}}.grounds{{grid-template-columns:1fr}}.rules{{grid-template-columns:1fr}}ul.files{{columns:1}}.hero{{padding-block:40px}}}}
</style>
</head>
<body>
<div class="wrap">
<header class="top">
  {themed_lockup("lock")}
  <button class="theme" id="theme-toggle" type="button" aria-label="Switch light or dark">Theme: system</button>
</header>

<div class="hero">
  {themed_mark("big")}
  <div>
    <h1>A bookmark, folded into an L, keeping your place.</h1>
    <p class="lede">The ribbon has the <b>V-notch of a bookmark</b> and turns a corner to make the <b>L</b> of LearnitPal. Resting in that corner is the <b>amber dot</b>: the one article picked for you today. It is the whole product in three shapes.</p>
    <p class="lede">The same dot is the tittle on the i of the wordmark, so the name and the symbol carry the same idea.</p>
  </div>
</div>

<section class="two">
  <div>
    <h2>Construction</h2>
    <p>Every measure comes from the stroke width, <b>T</b>. The notch is cut 0.43T deep at the midpoint. The dot's radius is two thirds of T, and it sits a quarter T clear of both arms, so it rests in the corner without touching either.</p>
    <p>There are no curves in the ribbon and no gradients anywhere. It prints in one colour, engraves, embroiders and stamps.</p>
    <p class="cap">Clear space: half a T on every side. No other element comes inside it.</p>
  </div>
  {construction}
</section>

<section>
  <h2>On every ground</h2>
  <div class="grounds">
    <div><div class="ground" style="background:#F9F5EF">{inline("learnitpal-mark")}</div><p class="cap">Primary, on Paper</p></div>
    <div><div class="ground" style="background:#14110D">{inline("learnitpal-mark-reversed")}</div><p class="cap">Reversed, on Night</p></div>
    <div><div class="ground" style="background:#E0962C">{inline("learnitpal-mark-mono")}</div><p class="cap">One colour. On amber the dot goes Ink too.</p></div>
    <div><div class="ground wide" style="background:#F9F5EF">{inline("learnitpal-lockup")}</div><p class="cap">Horizontal lockup</p></div>
    <div><div class="ground wide" style="background:#14110D">{inline("learnitpal-lockup-reversed")}</div><p class="cap">Lockup, reversed</p></div>
    <div><div class="ground wide" style="background:#FFFFFF">{inline("learnitpal-lockup-mono")}</div><p class="cap">Lockup, one colour, for print and fax-grade copies</p></div>
  </div>
</section>

<section class="two">
  <div>
    <h2>App icon and splash</h2>
    <p>The icon is the reversed mark on Night, full bleed, so Android's launcher masks (circle, squircle, teardrop) cut the ground and never the mark. The adaptive foreground keeps the mark inside the 66dp safe zone.</p>
    <p>The splash stacks the mark over the wordmark, centred slightly above the middle of the screen, where the eye lands first.</p>
    <div class="sizes" aria-label="The icon at small sizes">
      <figure><img src="png/learnitpal-icon-48.png" width="48" height="48" alt="Icon at 48 pixels"><figcaption>48</figcaption></figure>
      <figure><img src="png/learnitpal-icon-32.png" width="32" height="32" alt="Icon at 32 pixels"><figcaption>32</figcaption></figure>
      <figure><img src="png/learnitpal-icon-16.png" width="16" height="16" alt="Icon at 16 pixels"><figcaption>16</figcaption></figure>
    </div>
  </div>
  <div class="phones">
    <div class="phone">{inline("learnitpal-splash-light")}</div>
    <div class="phone">{inline("learnitpal-splash-dark")}</div>
  </div>
</section>

<section>
  <h2>Colour</h2>
  <ul class="sw">{sw_html}</ul>
</section>

<section>
  <h2>Keep it whole</h2>
  <ul class="rules">
    <li>Amber is only ever the dot. Never colour the ribbon amber on a light ground.</li>
    <li>Never round the ribbon's corners or soften the notch. The hard corners are the point.</li>
    <li>Never move the dot out of the corner, outline it, or turn it into another shape.</li>
    <li>Never rotate, skew, add shadows, or put the mark on a busy photo without a solid ground.</li>
    <li>Smallest mark: 16px on screen, 5mm in print. Smallest lockup: 96px or 20mm wide.</li>
    <li>The wordmark is always lowercase, set as drawn. Never retype it in another font.</li>
  </ul>
</section>

<section>
  <h2>Files</h2>
  <p>Everything here is vector. PNG previews are in <code>png/</code>.</p>
  <ul class="files">{file_rows}</ul>
</section>
</div>
<script>
(function(){{
  var KEY="learnitpal.brand.theme", order=["system","light","dark"], root=document.documentElement, btn=document.getElementById("theme-toggle");
  function read(){{try{{return localStorage.getItem(KEY)||"system"}}catch(e){{return "system"}}}}
  function apply(mode){{
    if(mode==="system"){{root.removeAttribute("data-theme")}}else{{root.setAttribute("data-theme",mode)}}
    btn.textContent="Theme: "+mode;
  }}
  var mode=read(); apply(mode);
  btn.addEventListener("click",function(){{
    mode=order[(order.indexOf(mode)+1)%order.length]; apply(mode);
    try{{localStorage.setItem(KEY,mode)}}catch(e){{}}
  }});
}})();
</script>
</body>
</html>
'''
open(f"{OUT}/index.html", "w").write(html)
