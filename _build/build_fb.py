"""Facebook sales-group post (1080x1350, 4:5) in the red palette. Output: Entregables/Arite_FB_*.png"""
import json, sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from marks import arite, alzado_minipc, alzado_nas
from build_pdf import hatch

OUT = HERE.parent / "Entregables"
PREV = HERE / "preview"
W, H = 1080, 1350


def despiece(left, top, height):
    """Constellation render with dashed assembly arrows converging on the chassis."""
    meta = json.loads((HERE / "assets" / "despiece-red-k1.json").read_text())
    w = height * meta["w"] / meta["h"]
    c = {k: (left + v["x"] * w, top + v["y"] * height) for k, v in meta["centers"].items()}
    hub = c["shell"]
    at = {"lid": 0.5, "ram": 0.45, "ssd": 0.5, "board": 0.42, "fan": 0.5, "sink": 0.5, "base": 0.45}
    AL = 36
    arrows = ""
    for k in ["lid", "ram", "board", "fan", "sink", "base"]:
        px, py = c[k]
        ux, uy = hub[0] - px, hub[1] - py
        L = (ux * ux + uy * uy) ** 0.5
        ux, uy = ux / L, uy / L
        mx, my = px + (hub[0] - px) * at[k], py + (hub[1] - py) * at[k]
        arrows += (f'<line x1="{mx - ux * AL / 2:.1f}" y1="{my - uy * AL / 2:.1f}" '
                   f'x2="{mx + ux * AL / 2:.1f}" y2="{my + uy * AL / 2:.1f}" marker-end="url(#ah)"/>')
    img = (f'<img class="render" src="../_build/assets/despiece-red-k1.png" '
           f'style="left:{left}px;top:{top}px;height:{height}px;width:{w:.1f}px" alt="">')
    svg = (f'<svg class="over" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" '
           f'stroke="var(--red)" stroke-width="1.6" stroke-dasharray="4 4">'
           f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0 0 L10 5 L0 10" fill="none" stroke="var(--red)" stroke-width="1.6"/></marker></defs>'
           f'{arrows}</svg>')
    return img + svg


def post():
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Arité · Facebook</title>
<link href="https://fonts.googleapis.com/css2?family=Antonio:wght@500;700&family=Archivo:wght@400;500;600&display=block" rel="stylesheet">
<style>
:root{{--ground:#EEEBE2;--paper:#F2EFE9;--ink:#0D0D0D;--red:#BF0426;--pink:#DEA6A3}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--ground)}}
.post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--ground);color:var(--ink);
       font-family:'Archivo',sans-serif;font-kerning:normal}}
.abs{{position:absolute}}
.render{{position:absolute;display:block}}
.over{{position:absolute;left:0;top:0;pointer-events:none}}
.hatch{{position:absolute;inset:0;width:100%;height:100%}}
.field{{position:absolute;overflow:hidden}}
.field>*:not(.hatch){{position:relative}}
.ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}

.logo{{left:64px;top:52px;color:var(--ink)}}
.kicker{{right:64px;top:70px;text-align:right;font-size:17px;line-height:1.35;font-weight:600;letter-spacing:.14em;text-transform:uppercase}}
.kicker b{{color:var(--red);font-weight:600}}
.rule{{left:64px;right:64px;height:1.5px;background:var(--ink)}}

.h1{{left:60px;top:198px;font-size:100px;line-height:.93;letter-spacing:-.005em}}
.h1 em{{font-style:normal;color:var(--red)}}

.q2{{left:64px;top:700px;width:600px;padding-left:44px;font-size:29px;line-height:1.32;font-weight:500;letter-spacing:-.005em}}
.q2 .br{{position:absolute;left:0;top:6px;bottom:6px;width:16px;border:3px solid var(--ink);border-right:0}}
.q2 b{{font-weight:600;color:var(--red)}}

.solve{{left:64px;top:856px;width:620px;height:288px;background:var(--red);color:var(--paper);padding:30px 34px}}
.solve .lbl{{font-size:16px;font-weight:600;letter-spacing:.14em;text-transform:uppercase}}
.solve .big{{font-size:94px;line-height:.92;margin-top:16px}}

.mini{{left:700px;top:856px;width:316px;height:288px;background:var(--pink);padding:26px 26px}}
.mini svg{{display:block;width:250px;height:auto;color:var(--ink)}}
.mini svg{{margin-top:22px}}
.mini p{{font-size:23px;line-height:1.26;font-weight:600;margin-top:22px}}

.cta{{left:0;right:0;top:1176px;bottom:0;background:var(--ink);color:var(--paper);padding:0 64px;
      display:flex;align-items:center;justify-content:space-between}}
.cta .t{{font-size:21px;line-height:1.35;font-weight:500;max-width:420px}}
.cta .t b{{display:block;color:var(--pink);font-weight:600;font-size:16px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:6px}}
.cta .tel{{font-size:92px;line-height:1;letter-spacing:.005em;color:var(--paper)}}
</style></head><body>
<div class="post">
  <div class="abs logo">{arite(height=92)}</div>
  <div class="abs kicker">Mini servidores<br><b>Hogar · Negocio</b></div>
  <div class="abs rule" style="top:168px"></div>

  <h1 class="abs h1 ant">¿Te falta<br><em>espacio</em><br>en iCloud<br>para tus<br>fotos?</h1>
  {despiece(left=496, top=190, height=500)}

  <div class="abs q2"><span class="br"></span>¿O buscas mantener tu información <b>en privado</b>, sin depender de un tercero como Apple, Microsoft o Google?</div>

  <div class="field solve">{hatch("hr", "#0D0D0D", .14, 9)}
    <div class="lbl">La respuesta</div>
    <div class="big ant">Arité lo<br>soluciona.</div>
  </div>
  <div class="field mini">{hatch("hp", "#0D0D0D", .16, 9)}
    {alzado_minipc("#F2EFE9")}
    <p>Mini servidores para tu hogar o negocio.</p>
  </div>

  <div class="abs cta">
    <p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p>
    <p class="tel ant">55 7196 2228</p>
  </div>
</div>
</body></html>"""


def main():
    src = HERE / "fb-post.html"
    src.write_text(post(), encoding="utf-8")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE.parent))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.goto(f"http://127.0.0.1:{port}/_build/fb-post.html", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        pg.query_selector(".post").screenshot(path=str(OUT / "Arite_FB_Paleta-Roja.png"))
        pg.set_viewport_size({"width": W, "height": H})
        b.close()
    httpd.shutdown()
    print("ok")


if __name__ == "__main__":
    main()
