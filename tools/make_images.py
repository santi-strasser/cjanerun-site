"""Renders the favicons and the Open Graph share image with headless Edge.

    python tools/make_images.py
"""
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "assets" / "images"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

runner = (IMG / "runner.svg").read_text()
runner_body = re.search(r"<symbol[^>]*>(.*?)</symbol>", runner, re.S).group(1)

FONTS = '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Montserrat:wght@600;700&display=block" rel="stylesheet">'


def badge(size, text=True):
    arcs = ""
    if text:
        arcs = """<defs><path id="t" d="M34 100A66 66 0 0 1 166 100"/><path id="b" d="M16 100A84 84 0 0 0 184 100"/></defs>
        <g font-family="Montserrat" font-weight="600" font-size="25" letter-spacing="7" fill="#fff">
        <text><textPath href="#t" startOffset="50%" text-anchor="middle">CJANE</textPath></text>
        <text><textPath href="#b" startOffset="50%" text-anchor="middle">RUN</textPath></text></g>"""
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 200 200">
      <circle cx="100" cy="100" r="96" fill="#1B2030" stroke="#E3A2AB" stroke-opacity=".35" stroke-width="2"/>
      <g color="#E3A2AB">{runner_body}</g>{arcs}</svg>"""


def shoot(html, w, h, out):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        page = Path(f.name)
    subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
         "--virtual-time-budget=5000", f"--window-size={w},{h}", f"--screenshot={out}", page.as_uri()],
        capture_output=True,
    )
    page.unlink()


art = lambda n: (IMG / n).as_uri()

og = f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;width:1200px;height:630px;background:#1B2030;color:#fff;font-family:'DM Sans';display:flex;align-items:center;overflow:hidden;position:relative}}
.txt{{padding-left:80px;width:560px}}
h1{{font-family:Montserrat;font-weight:700;font-size:92px;line-height:1.02;margin:28px 0 0;letter-spacing:-1px}}
h1 span{{color:#E07A93}}
p{{font-size:28px;color:#C9CCD8;margin:22px 0 0;line-height:1.35}}
.url{{font-family:Montserrat;font-weight:700;font-size:20px;letter-spacing:.2em;color:#E3A2AB;margin-top:34px}}
.art{{position:absolute;right:40px;bottom:40px;width:470px;height:520px}}
.art img{{position:absolute;bottom:0;filter:drop-shadow(0 18px 24px rgba(0,0,0,.4))}}
.glow{{position:absolute;inset:10% 0 0;border-radius:50%;background:radial-gradient(closest-side,rgba(224,122,147,.3),transparent)}}
</style></head><body>
<div class="txt">{badge(120)}<h1>Fuel what’s <span>next.</span></h1>
<p>Great-tasting sports nutrition built around how you actually train.</p>
<div class="url">JOIN THE WAITLIST · CJANERUN.STORE</div></div>
<div class="art"><div class="glow"></div>
<img src="{art('stick-before.svg')}" style="height:440px;left:70px;transform:rotate(-9deg)">
<img src="{art('stick-after.svg')}" style="height:440px;left:230px;transform:rotate(6deg)">
</div></body></html>"""

EVERYDAY_FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=block" rel="stylesheet">'
EVERYDAY_MARK = """<svg width="{size}" height="{size}" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#2BA8B8"/>
<path d="M11 22c3-4 6-4 9 0s6 4 9 0" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>"""

og_everyday = f"""<!doctype html><html><head><meta charset="utf-8">{EVERYDAY_FONTS}<style>
body{{margin:0;width:1200px;height:630px;background:#12414D;color:#fff;font-family:Inter;display:flex;align-items:center;overflow:hidden;position:relative}}
.txt{{padding-left:80px;width:560px}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:700;font-size:40px}}
h1{{font-weight:700;font-size:84px;line-height:1.04;margin:34px 0 0;letter-spacing:-2px}}
h1 span{{color:#E9783E}}
p{{font-size:28px;color:#CFE3E8;margin:22px 0 0;line-height:1.35}}
.url{{font-weight:700;font-size:20px;letter-spacing:.14em;color:#F5B48F;margin-top:34px}}
.art{{position:absolute;right:40px;bottom:40px;width:470px;height:520px}}
.art img{{position:absolute;bottom:0;filter:drop-shadow(0 18px 24px rgba(0,0,0,.35))}}
.glow{{position:absolute;inset:10% 0 0;border-radius:50%;background:radial-gradient(closest-side,rgba(43,168,184,.35),transparent)}}
</style></head><body>
<div class="txt"><div class="brand">{EVERYDAY_MARK.format(size=56)}everyday</div>
<h1>Simple, everyday <span>essentials.</span></h1>
<p>Easy drink mixes for hydration and recovery.</p>
<div class="url">JOIN THE WAITLIST</div></div>
<div class="art"><div class="glow"></div>
<img src="{art('stick-everyday-hydration.svg')}" style="height:440px;left:70px;transform:rotate(-9deg)">
<img src="{art('stick-everyday-recovery.svg')}" style="height:440px;left:230px;transform:rotate(6deg)">
</div></body></html>"""


def make_icons(mark_html, bg, favicon_name, touch_name):
    page = f"""<!doctype html><html><head><style>body{{margin:0;background:transparent}}svg{{display:block}}</style></head>
<body>{mark_html}</body></html>"""
    tmp = IMG / "icon-512.png"
    shoot(page, 512, 512, tmp)
    # Round the square screenshot into a transparent circle, then size the icons.
    src = Image.open(tmp).convert("RGBA")
    mask = Image.new("L", src.size, 0)
    ImageDraw.Draw(mask).ellipse((1, 1, 510, 510), fill=255)
    src.putalpha(mask)
    src.resize((32, 32), Image.LANCZOS).save(IMG / favicon_name)
    # Apple touch icons shouldn't be transparent – put the mark on the brand color.
    touch = Image.new("RGBA", (512, 512), bg)
    touch.alpha_composite(src)
    touch.convert("RGB").resize((180, 180), Image.LANCZOS).save(IMG / touch_name)
    tmp.unlink()


def save_og(html, name):
    shoot(html, 1200, 630, IMG / name)
    Image.open(IMG / name).convert("RGB").save(IMG / name, optimize=True)


save_og(og, "og-share.png")
save_og(og_everyday, "og-everyday.png")
make_icons(badge(512, text=False), "#1B2030", "favicon-32.png", "apple-touch-icon.png")
make_icons(EVERYDAY_MARK.format(size=512), "#12414D", "everyday-favicon-32.png", "everyday-touch-icon.png")
print("wrote OG images and favicons for CJane Run and Everyday")
