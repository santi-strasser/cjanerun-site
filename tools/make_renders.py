"""Renders the 3D pack shots (stick packs + cartons) into public/assets/images.

tools/render3d/index.html draws every shot with three.js; this script serves
the repo, opens that page in headless Edge, collects the PNGs it posts back and
saves them as trimmed, downsized WebP files.

    python tools/make_renders.py                  # render the site images
    python tools/make_renders.py --export DIR     # also save full-size PNGs and flat label art to DIR
"""
import subprocess
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "public" / "assets" / "images"
OUT = ROOT / "tools" / "render3d" / "out"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 8792
MAX_SIDE = 1400      # longest edge of the saved WebP, in pixels
done = threading.Event()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def log_message(self, *a):
        pass

    def do_POST(self):
        url = urlparse(self.path)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if url.path == "/save":
            name = parse_qs(url.query)["name"][0]
            if not name.replace("-", "").isalnum():
                self.send_error(400)
                return
            OUT.mkdir(parents=True, exist_ok=True)
            (OUT / f"{name}.png").write_bytes(body)
            print("rendered", name)
        elif url.path == "/done":
            done.set()
        self.send_response(204)
        self.end_headers()


def trimmed(png):
    im = Image.open(png).convert("RGBA")
    box = im.getchannel("A").point(lambda a: 255 if a > 6 else 0).getbbox()
    if box:
        pad = 24
        box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
        im = im.crop(box)
    return im


def finish(png):
    """Trim the empty margin, downsize the 2x render and save as WebP."""
    im = trimmed(png)
    scale = min(1, MAX_SIDE / max(im.size))
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    out = IMG / f"{png.stem}.webp"
    im.save(out, "WEBP", quality=88, method=6)
    print(f"wrote {out.name}  {im.width}x{im.height}  {out.stat().st_size // 1024} KB")


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    edge = subprocess.Popen(
        [EDGE, "--headless=new", "--hide-scrollbars", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
         "--window-size=1800,1600", f"http://127.0.0.1:{PORT}/tools/render3d/index.html"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    ok = done.wait(timeout=600)
    edge.terminate()
    server.shutdown()
    if not ok:
        sys.exit("render page never finished – open tools/render3d/index.html?preview=pack-before-hero to debug")
    export = Path(sys.argv[sys.argv.index("--export") + 1]).resolve() if "--export" in sys.argv else None
    for png in sorted(OUT.glob("*.png")):
        label = png.stem.startswith("label-")
        if export:
            dest = export / ("label-art" if label else "renders")
            dest.mkdir(parents=True, exist_ok=True)
            (Image.open(png) if label else trimmed(png)).save(dest / png.name, optimize=True)
        if not label:
            finish(png)
        png.unlink()
    if export:
        print("exported full-size PNGs to", export)


if __name__ == "__main__":
    main()
