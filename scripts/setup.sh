#!/usr/bin/env bash
# One-time toolchain for the brand-identity skill.
#   fonttools + uharfbuzz  -> outline real font glyphs with real kerning
#   rsvg-convert           -> render SVG to PNG so the work can be looked at
# Prints the python to use. Safe to re-run.
set -euo pipefail
VENV="${BRAND_VENV:-$HOME/.cache/brand-identity/venv}"
if [ ! -x "$VENV/bin/python" ]; then
  mkdir -p "$(dirname "$VENV")"
  python3 -m venv "$VENV"
fi
"$VENV/bin/python" -c "import fontTools, uharfbuzz" 2>/dev/null || "$VENV/bin/pip" install -q --disable-pip-version-check fonttools uharfbuzz
if ! command -v rsvg-convert >/dev/null 2>&1; then
  if command -v brew >/dev/null 2>&1; then brew install librsvg; else
    echo "rsvg-convert missing: install librsvg (apt install librsvg2-bin / brew install librsvg)" >&2; exit 1; fi
fi
echo "$VENV/bin/python"
