"""Render the exploded mini PC for each palette with headless Chrome; save PNG + label anchors."""
import base64, json, sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "assets"
OUT.mkdir(exist_ok=True)
palettes = sys.argv[1:] or ["neutral", "red", "plano"]

handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE))
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
port = httpd.server_address[1]

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                          args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page()
    pg.on("console", lambda m: print("console:", m.text))
    pg.on("pageerror", lambda e: print("pageerror:", e))
    for spec in palettes:
        # spec: palette[:dy:dz:suffix]
        parts = spec.split(":")
        pal = parts[0]
        qs = f"palette={pal}"
        name = pal
        if len(parts) >= 3:
            qs += f"&dy={parts[1]}&dz={parts[2]}"
            name += "-" + (parts[3] if len(parts) > 3 else "c")
            if len(parts) > 4:
                qs += f"&dx={parts[4]}"
            if len(parts) > 5 and parts[5]:
                qs += f"&st={parts[5]}"
            if len(parts) > 6:
                qs += "&lay=" + __import__("urllib.parse").parse.quote(parts[6])
        pg.goto(f"http://127.0.0.1:{port}/render.html?{qs}")
        pg.wait_for_function("window.__result", timeout=60000)
        r = pg.evaluate("window.__result")
        (OUT / f"despiece-{name}.png").write_bytes(base64.b64decode(r["png"].split(",", 1)[1]))
        (OUT / f"despiece-{name}.json").write_text(json.dumps({"w": r["w"], "h": r["h"], "labels": r["labels"], "centers": r.get("centers")}, indent=1))
        print(name, r["w"], r["h"])
    b.close()
httpd.shutdown()
