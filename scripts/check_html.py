#!/usr/bin/env python3
"""Sanity-check a standalone brand sheet before handing it over:
doctype/head/body skeleton, balanced tags, a theme toggle that persists safely,
and no external assets other than an optional Google Fonts stylesheet.

  python check_html.py path/to/index.html
"""
import re, sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SVG_SELF = {"path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "use", "stop"}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
    def handle_startendtag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif tag in SVG_SELF:
            return
        else:
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> but open is {self.stack[-1] if self.stack else None}")

src = open(sys.argv[1]).read()
problems = []
if not src.lstrip().lower().startswith("<!doctype html>"):
    problems.append("missing <!doctype html>")
for t in ("<html", "<head", "<body", 'name="viewport"', "charset"):
    if t not in src:
        problems.append(f"missing {t}")
if "localStorage" not in src or "try" not in src:
    problems.append("no persisted light/dark toggle (localStorage in try/catch)")
if 'data-theme="dark"' not in src and "[data-theme=\"dark\"]" not in src:
    problems.append("no [data-theme=\"dark\"] token block")
for m in re.finditer(r'(?:src|href)="(https?://[^"]+)"', src):
    if "fonts.googleapis.com" not in m.group(1) and "fonts.gstatic.com" not in m.group(1):
        problems.append(f"external asset: {m.group(1)}")
c = Checker(); c.feed(src)
problems += c.errors
problems += [f"unclosed <{t}> from line {l}" for t, l in c.stack]
if problems:
    print("PROBLEMS:\n  " + "\n  ".join(problems)); sys.exit(1)
print(f"ok: {len(src) // 1024} KB, skeleton, toggle and tags all fine")
