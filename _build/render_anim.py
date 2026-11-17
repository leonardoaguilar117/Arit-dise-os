"""Render the mini PC assembly loop: N frames from exploded (t=1) to assembled (t=0) with a fixed camera.
Output: assets/anim/ensamble-{palette}-NN.png. Usage: python render_anim.py [palette] [frames] [width]"""
import base64, sys, math, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
pal = sys.argv[1] if len(sys.argv) > 1 else "red"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1300
OUT = HERE / "assets" / "anim"
OUT.mkdir(parents=True, exist_ok=True)


def ease(x):  # easeInOutCubic
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
port = httpd.server_address[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page()
    pg.on("pageerror", lambda e: print("pageerror:", e))

    def render(t, fix=None):
        qs = f"palette={pal}&w={W}&t={t:.4f}" + (f"&fix={fix}" if fix else "")
        pg.goto(f"http://127.0.0.1:{port}/render.html?{qs}")
        pg.wait_for_function("window.__result", timeout=90000)
        return pg.evaluate("window.__result")

    first = render(1.0)
    fix = ",".join(f"{v:.3f}" for v in first["frame"])
    for i in range(N):
        t = 1 - ease(i / (N - 1))
        r = render(t, fix)
        (OUT / f"ensamble-{pal}-{i:02d}.png").write_bytes(base64.b64decode(r["png"].split(",", 1)[1]))
    print("frames", N, r["w"], r["h"])
    b.close()
httpd.shutdown()
