"""Generates the stick-pack mockup SVGs in public/assets/images.

CJane Run sticks carry the traced runner badge (read from runner.svg). The
"Everyday" sticks are the neutral control brand for the Meta test – same
format and size, plain mass-market look. Re-run after changing colors/shapes:
    python tools/make_art.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "assets" / "images"

NAVY = "#1B2030"
RUNNER_PINK = "#E3A2AB"
FONT = "Montserrat, 'Segoe UI', Arial, sans-serif"
PLAIN_FONT = "Inter, 'Segoe UI', Arial, sans-serif"

EVERYDAY_INK = "#12414D"

runner_d = re.search(r'd="(M[^"]+)"', (IMG / "runner.svg").read_text()).group(1)


def badge(cx, cy, r):
    """Small navy badge with the runner mark (no arc text – too small to read)."""
    s = r / 96
    return (
        f'<g transform="translate({cx - 100 * s:.2f} {cy - 100 * s:.2f}) scale({s:.4f})">'
        f'<circle cx="100" cy="100" r="96" fill="{NAVY}"/>'
        f'<path fill="{RUNNER_PINK}" d="{runner_d}"/>'
        f'<path stroke="{RUNNER_PINK}" stroke-width="3" stroke-linecap="round" d="M24 108.5H54M146 108.5H176"/>'
        "</g>"
    )


# Simple icons for the Everyday sticks, drawn in a 24x24 box.
DROP = '<path d="M12 3c3.5 4.6 6 8 6 11a6 6 0 0 1-12 0c0-3 2.5-6.4 6-11z"/>'
LEAF = '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14zM5 19l7-7"/>'


def icon(cx, cy, r, glyph, bg, ink):
    s = r * 1.1 / 12
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
        f'<g transform="translate({cx - 12 * s:.2f} {cy - 12 * s:.2f}) scale({s:.3f})" fill="none" '
        f'stroke="{ink}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>'
    )


def crimp(x, y, w, h, color):
    lines = "".join(
        f'<line x1="{x + i}" y1="{y + 2}" x2="{x + i}" y2="{y + h - 2}"/>'
        for i in range(4, w, 5)
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'
        f'<g stroke="#fff" stroke-opacity=".28" stroke-width="1.2">{lines}</g>'
    )


def shell(body, crimp_color):
    return f"""<rect x="8" y="10" width="84" height="300" rx="5" fill="{body}"/>
  {crimp(8, 10, 84, 26, crimp_color)}
  {crimp(8, 284, 84, 26, crimp_color)}
  <path d="M8 44l6 4-6 4zM92 44l-6 4 6 4z" fill="{crimp_color}"/>
  <rect x="8" y="36" width="22" height="248" fill="#fff" opacity=".13"/>"""


def cjr_stick(name, body, crimp_color, word, ink):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 320" role="img" aria-label="CJane Run {word.lower()} stick pack mockup">
  {shell(body, crimp_color)}
  <text x="50" y="66" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="9.5" letter-spacing="2.2" fill="{ink}">CJANE RUN</text>
  <text transform="translate(58.5 158) rotate(-90)" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="25" letter-spacing="4" fill="{ink}">{word}</text>
  {badge(50, 256, 16)}
</svg>
"""
    (IMG / name).write_text(svg, encoding="utf-8")


def everyday_stick(name, body, crimp_color, word, glyph):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 320" role="img" aria-label="Everyday {word.lower()} mix stick pack mockup">
  {shell(body, crimp_color)}
  <text x="50" y="68" text-anchor="middle" font-family="{PLAIN_FONT}" font-weight="700" font-size="15" fill="{EVERYDAY_INK}">everyday</text>
  <text transform="translate(57 150) rotate(-90)" text-anchor="middle" font-family="{PLAIN_FONT}" font-weight="700" font-size="19" letter-spacing="1.5" fill="{EVERYDAY_INK}">{word}</text>
  {icon(50, 256, 16, glyph, "#fff", EVERYDAY_INK)}
</svg>
"""
    (IMG / name).write_text(svg, encoding="utf-8")


cjr_stick("stick-before.svg", "#E07A93", "#C9627C", "BEFORE", "#fff")
cjr_stick("stick-after.svg", "#B3A9D6", "#9A8FC4", "AFTER", NAVY)
everyday_stick("stick-everyday-hydration.svg", "#9AD3E0", "#7DBFCF", "HYDRATION", DROP)
everyday_stick("stick-everyday-recovery.svg", "#E9CFA8", "#D8B887", "RECOVERY", LEAF)
print("wrote", sorted(p.name for p in IMG.glob("stick-*.svg")))
