"""Render isometric scenes (scenes.html) per palette. Usage: python render_scenes.py eco:red office:neutral ..."""
import base64, json, sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "assets"
specs = sys.argv[1:] or ["eco:red", "eco:neutral", "office:red", "office:neutral"]

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
port = httpd.server_address[1]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page()
    pg.on("pageerror", lambda e: print("pageerror:", e))
    for spec in specs:
        scene, pal = spec.split(":")
        pg.goto(f"http://127.0.0.1:{port}/scenes.html?scene={scene}&palette={pal}")
        pg.wait_for_function("window.__result", timeout=90000)
        r = pg.evaluate("window.__result")
        name = f"scene-{scene}-{pal}"
        (OUT / f"{name}.png").write_bytes(base64.b64decode(r["png"].split(",", 1)[1]))
        (OUT / f"{name}.json").write_text(json.dumps({"w": r["w"], "h": r["h"], "centers": r["centers"]}, indent=1))
        print(name, r["w"], r["h"])
    b.close()
httpd.shutdown()
