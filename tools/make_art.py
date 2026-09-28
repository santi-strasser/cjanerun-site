"""Generates the product mockup SVGs in public/assets/images.

The runner path is read from runner.svg so every illustration uses the same
traced logo mark. Re-run after changing colors or shapes:
    python tools/make_art.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "assets" / "images"

NAVY = "#1B2030"
RUNNER_PINK = "#E3A2AB"
FONT = "Montserrat, 'Segoe UI', Arial, sans-serif"

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


def crimp(x, y, w, h, color):
    lines = "".join(
        f'<line x1="{x + i}" y1="{y + 2}" x2="{x + i}" y2="{y + h - 2}"/>'
        for i in range(4, w, 5)
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>'
        f'<g stroke="#fff" stroke-opacity=".28" stroke-width="1.2">{lines}</g>'
    )


def stick(name, body, crimp_color, word, ink):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 320" role="img" aria-label="CJane Run {word.lower()} stick pack mockup">
  <rect x="8" y="10" width="84" height="300" rx="5" fill="{body}"/>
  {crimp(8, 10, 84, 26, crimp_color)}
  {crimp(8, 284, 84, 26, crimp_color)}
  <path d="M8 44l6 4-6 4zM92 44l-6 4 6 4z" fill="{crimp_color}"/>
  <rect x="8" y="36" width="22" height="248" fill="#fff" opacity=".13"/>
  <text x="50" y="66" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="9.5" letter-spacing="2.2" fill="{ink}">CJANE RUN</text>
  <text transform="translate(58.5 158) rotate(-90)" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="25" letter-spacing="4" fill="{ink}">{word}</text>
  {badge(50, 256, 16)}
</svg>
"""
    (IMG / name).write_text(svg, encoding="utf-8")


def pouch():
    balls = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#9A6A45"/>'
        f'<circle cx="{x - r * .35:.1f}" cy="{y - r * .4:.1f}" r="{r * .35:.1f}" fill="#fff" opacity=".12"/>'
        + "".join(
            f'<circle cx="{x + dx}" cy="{y + dy}" r="1.6" fill="#E9D6BF"/>'
            for dx, dy in ((-6, 4), (5, -5), (8, 6), (-2, -9), (1, 10))
        )
        for x, y, r in ((92, 164, 21), (128, 158, 21), (110, 190, 21))
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 290" role="img" aria-label="CJane Run protein balls pouch mockup">
  <path d="M26 30h168l6 222c0 14-10 26-24 26H44c-14 0-24-12-24-26z" fill="#7BA894"/>
  {crimp(26, 18, 168, 24, "#66917E")}
  <rect x="26" y="42" width="40" height="232" fill="#fff" opacity=".1"/>
  <text x="110" y="76" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="13" letter-spacing="4" fill="{NAVY}">CJANE RUN</text>
  <circle cx="110" cy="172" r="52" fill="#F6F5F1"/>
  <clipPath id="w"><circle cx="110" cy="172" r="48"/></clipPath>
  <g clip-path="url(#w)"><rect x="60" y="120" width="100" height="110" fill="#EFE7DA"/>{balls}</g>
  <text x="110" y="254" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="20" letter-spacing="5" fill="{NAVY}">SNACK</text>
</svg>
"""
    (IMG / "pouch-snack.svg").write_text(svg, encoding="utf-8")


def bottle(name, liquid, liquid_edge, flavor1, flavor2, word, accent):
    body = "M50 62C50 82 22 90 22 120V312q0 20 20 20h56q20 0 20-20V120c0-30-28-38-28-58z"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 340" role="img" aria-label="CJane Run {flavor1.lower()} {flavor2.lower()} bottle mockup">
  <clipPath id="b"><path d="{body}"/></clipPath>
  <path d="{body}" fill="#EEF0F2"/>
  <g clip-path="url(#b)">
    <rect x="0" y="92" width="140" height="260" fill="{liquid}"/>
    <path d="M0 92q35 -6 70 0t70 0v6H0z" fill="#fff" opacity=".35"/>
  </g>
  <path d="{body}" fill="none" stroke="{liquid_edge}" stroke-width="2"/>
  <rect x="48" y="46" width="44" height="18" fill="#DDE1E5" stroke="{liquid_edge}" stroke-width="1.5"/>
  <rect x="42" y="8" width="56" height="42" rx="7" fill="#F6F5F1" stroke="{NAVY}" stroke-opacity=".22" stroke-width="1.5"/>
  <g stroke="{NAVY}" stroke-opacity=".14" stroke-width="2">{"".join(f'<line x1="{x}" y1="14" x2="{x}" y2="44"/>' for x in range(50, 96, 6))}</g>
  <rect x="22" y="168" width="96" height="116" fill="{NAVY}"/>
  <text x="70" y="190" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="9" letter-spacing="2.4" fill="#fff">CJANE RUN</text>
  {badge(70, 214, 13)}
  <text x="70" y="252" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="11" letter-spacing="1" fill="{accent}">{flavor1}</text>
  <text x="70" y="268" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="11" letter-spacing="1" fill="{accent}">{flavor2}</text>
  <text x="70" y="306" text-anchor="middle" font-family="{FONT}" font-weight="700" font-size="11" letter-spacing="3" fill="{NAVY}" opacity=".75">{word}</text>
  <rect x="30" y="112" width="7" height="190" rx="3.5" fill="#fff" opacity=".4"/>
</svg>
"""
    (IMG / name).write_text(svg, encoding="utf-8")


stick("stick-before.svg", "#E07A93", "#C9627C", "BEFORE", "#fff")
stick("stick-after.svg", "#B3A9D6", "#9A8FC4", "AFTER", NAVY)
pouch()
bottle("bottle-before.svg", "#F4C3CC", "#E3A2AB", "STRAWBERRY", "CREAM", "BEFORE", "#F4C3CC")
bottle("bottle-after.svg", "#B9CF8E", "#98B36A", "MATCHA", "CREAM", "AFTER", "#B9CF8E")
print("wrote", sorted(p.name for p in IMG.glob("*.svg")))
