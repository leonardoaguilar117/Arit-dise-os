"""Second batch (2026-11-17): two Facebook posts + two 2-page Letter PDFs, built on the isometric scenes
(scenes.html -> assets/scene-*.png). Run render_scenes.py first if the scenes change."""
import json, sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from marks import arite, aricloud
from build_pdf import hatch

OUT = HERE.parent / "Entregables"
PREV = HERE / "preview"
TEL = "55 7196 2228"


def scene(name, left, top, width, alt):
    """Place a rendered scene; returns (html, pt) where pt(key) gives page coords of a named center."""
    meta = json.loads((HERE / "assets" / f"scene-{name}.json").read_text())
    h = width * meta["h"] / meta["w"]
    html = (f'<img class="render" src="../_build/assets/scene-{name}.png" '
            f'style="left:{left}px;top:{top}px;width:{width}px;height:{h:.1f}px" alt="{alt}">')

    def pt(key, dx=0.0, dy=0.0):
        if isinstance(key, tuple):
            fx, fy = key
        else:
            c = meta["centers"][key]
            fx, fy = c["x"], c["y"]
        return left + fx * width + dx, top + fy * h + dy
    return html, pt, h


def overlay(W, H, body, color, dash="5 5", width=1.6):
    return (f'<svg class="over" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-dasharray="{dash}"><defs><marker id="ah{color[1:]}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10" fill="none" stroke="{color}" '
            f'stroke-width="1.6" stroke-dasharray="none"/></marker></defs>{body}</svg>')


def arrow(a, b, color):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" marker-end="url(#ah{color[1:]})"/>'


def line(a, b):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'


def tag(label, x, y, cls="tag"):
    return f'<span class="{cls}" style="left:{x:.1f}px;top:{y:.1f}px">{label}</span>'


COMMON = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-kerning:normal}
.abs{position:absolute}
.render{position:absolute;display:block}
.over{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}
.hatch{position:absolute;inset:0;width:100%;height:100%}
.field{position:absolute;overflow:hidden}
.field>*:not(.hatch){position:relative}
"""

FONTS_RED = '<link href="https://fonts.googleapis.com/css2?family=Antonio:wght@500;700&family=Archivo:wght@400;500;600&display=block" rel="stylesheet">'
FONTS_NEU = '<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=block" rel="stylesheet">'


def page_doc(title, fonts, css, body, size=None):
    pg = f"@page{{size:{size};margin:0}}" if size else ""
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{title}</title>{fonts}'
            f'<style>{pg}{COMMON}{css}</style></head><body>{body}</body></html>')


# =================================================================== POST 2 · negocio · paleta neutra
def post_negocio():
    W, H = 1080, 1350
    img, pt, sh = scene("office-neutral", 300, 452, 740, "Oficina isométrica: una persona trabaja en su laptop y el servidor Arité guarda todo desde el librero")
    lap, srv, rt, per = pt("screen"), pt("server"), pt((0.300, 0.197)), pt("person", 0, -40)
    lines = line(lap, srv) + line(srv, rt)
    marks = "".join(tag(l, x - 17, y - 17, "tag t-on") for l, (x, y) in
                    (("A", pt("screen", 58, -26)), ("B", pt("server", -6, -64)), ("C", pt((0.300, 0.197), 50, -8))))
    pts = [("A", "Tu equipo trabaja", "Laptops y celulares guardan en carpetas compartidas."),
           ("B", "Tu servidor Arité", "Guarda y respalda todo cada noche, en discos en espejo."),
           ("C", "Tu red privada", "Entras desde fuera de la oficina por tu VPN.")]
    col = "".join(f'<div class="pt"><span class="tag">{l}</span><h3>{t}</h3><p>{d}</p></div>' for l, t, d in pts)
    css = f"""
    :root{{--g:#F2F1F0;--ink:#0D0D0D;--ink2:#595959;--tan:#BFAA8F;--grey:#BFBFBF}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--g);color:var(--ink);font-family:'Jost',sans-serif}}
    .logo{{left:64px;top:46px}}
    .kick{{right:64px;top:66px;text-align:right;font-size:17px;line-height:1.4;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}}
    .kick b{{color:var(--ink);font-weight:500}}
    .rule{{left:64px;right:64px;top:160px;height:1.2px;background:var(--ink)}}
    .h1{{left:62px;top:186px;font-size:78px;line-height:1.02;font-weight:300;letter-spacing:-.015em}}
    .h1 b{{font-weight:600}}
    .sub{{left:64px;top:372px;width:820px;font-size:26px;line-height:1.38;color:var(--ink2)}}
    .col{{left:64px;top:520px;width:250px}}
    .pt{{position:relative;margin-bottom:34px}}
    .pt h3{{font-size:25px;font-weight:500;margin-top:12px;line-height:1.1}}
    .pt p{{font-size:18px;line-height:1.38;margin-top:6px;color:var(--ink2)}}
    .tag{{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border:1.6px solid var(--ink);border-radius:50%;font-size:17px;font-weight:600;line-height:1;background:var(--g)}}
    .t-on{{position:absolute;background:var(--ink);color:var(--g)}}
    .cta{{left:0;right:0;top:1188px;bottom:0;background:var(--ink);color:var(--g);padding:0 64px;display:flex;align-items:center;justify-content:space-between}}
    .cta .t{{font-size:21px;line-height:1.4;max-width:430px}}
    .cta .t b{{display:block;color:var(--tan);font-weight:500;font-size:16px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:6px}}
    .cta .tel{{font-size:78px;font-weight:300;letter-spacing:-.01em}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=86)}</div>
  <div class="abs kick">Mini servidores<br><b>para tu negocio</b></div>
  <div class="abs rule"></div>
  <h1 class="abs h1">Los archivos de tu negocio,<br>en <b>tu</b> negocio.</h1>
  <p class="abs sub">Sin depender de un tercero como Apple, Microsoft o Google. Un mini servidor en tu oficina guarda, comparte y respalda el trabajo de todo tu equipo.</p>
  {img}
  {overlay(W, H, lines, "#0D0D0D", "4 5", 1.8)}
  {marks}
  <div class="abs col">{col}</div>
  <div class="abs cta"><p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p><p class="tel">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Negocio", FONTS_NEU, css, body), (W, H)


# =================================================================== POST 3 · cartel rojo "Tu nube en casa"
def post_cartel():
    W, H = 1080, 1350
    img, pt, sh = scene("eco-red", 40, 300, 1000, "Isométrico del ecosistema Aricloud: mini PC, bahía de discos con un disco afuera, router y celular")
    arr = arrow(pt("drive2", 30, -40), pt("bay2", 18, 30), "#F2EFE9")
    css = f"""
    :root{{--red:#BF0426;--cream:#F2EFE9;--pink:#DEA6A3;--ink:#0D0D0D}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--red);color:var(--cream);font-family:'Archivo',sans-serif}}
    .ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}
    .logo{{left:56px;top:44px;color:var(--cream)}}
    .meta{{font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;line-height:1.45}}
    .m-tr{{right:56px;top:58px;text-align:right}}
    .hl{{left:300px;right:300px;top:78px;height:1.2px;background:var(--cream);opacity:.85}}
    .w1{{left:48px;top:96px;font-size:268px;line-height:.86;letter-spacing:-.01em}}
    .w2{{right:46px;top:786px;font-size:268px;line-height:.86;letter-spacing:-.01em;z-index:3}}
    .sub{{left:56px;top:1076px;width:620px;font-size:25px;line-height:1.38;font-weight:500}}
    .sub b{{font-weight:600}}
    .pay{{right:56px;top:1062px;width:300px;text-align:right}}
    .pay .n{{font-size:66px;line-height:.9}}
    .pay p{{font-size:17px;line-height:1.35;margin-top:8px}}
    .foot{{left:56px;right:56px;top:1234px;border-top:1.2px solid var(--cream);padding-top:22px;display:flex;justify-content:space-between;align-items:flex-end}}
    .foot .tel{{font-size:62px;line-height:.9}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=60)}</div>
  <div class="abs hl"></div>
  <div class="abs meta m-tr">Mini servidores<br>Hogar · Negocio</div>
  <p class="abs w1 ant">Tu nube</p>
  {img}
  {overlay(W, H, arr, "#F2EFE9", "5 5", 2)}
  <p class="abs w2 ant">en casa.</p>
  <p class="abs sub">¿Te falta espacio en iCloud? Armamos un mini servidor para tus fotos y archivos. <b>Sin depender de Apple, Microsoft o Google.</b></p>
  <div class="abs pay"><p class="n ant">0</p><p>mensualidades.<br>Pagas una vez y es tuyo.</p></div>
  <div class="abs foot"><p class="meta">Agenda una presentación<br>de nuestros servicios</p><p class="tel ant">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Tu nube en casa", FONTS_RED, css, body), (W, H)


# =================================================================== PDF · Arité para negocios (neutra)
def pdf_negocio(pal="neutral"):
    red = pal == "red"
    lc = "#BF0426" if red else "#0D0D0D"
    img, pt, sh = scene(f"office-{pal}", 262, 344, 520, "Oficina isométrica con una persona en su laptop y el servidor Arité en el librero")
    marks_at = {"A": pt("screen", 40, -22), "B": pt("server", -4, -46), "C": pt((0.300, 0.197), 36, -6), "D": pt("person", 34, -10)}
    lines = line(pt("screen"), pt("server")) + line(pt("server"), pt((0.300, 0.197)))
    marks = "".join(tag(k, x - 12, y - 12, "tag t-on") for k, (x, y) in marks_at.items())
    pts = [("A", "Comparte", "Las carpetas del equipo en un solo lugar, con permisos por persona."),
           ("B", "Respalda", "Copias automáticas cada noche, en dos discos en espejo."),
           ("C", "Accede", "Desde fuera de la oficina, por tu VPN privada."),
           ("D", "Controla", "Tú decides quién entra, qué ve y cuánto tiempo se guarda.")]
    col = "".join(f'<div class="pt"><span class="tag">{l}</span><h3>{t}</h3><p>{d}</p></div>' for l, t, d in pts)

    eimg, ept, esh = scene(f"eco-{pal}", 262, 432, 514, "Isométrico del equipo: router, mini PC, bahía de discos con un disco afuera y un celular")
    callouts = [("Tu celular y tu laptop", "phone", (0, 0)), ("Router y VPN", "router", (-12, 10)), ("Mini PC: el servidor", "minipc", (0, 0)),
                ("Bahía de discos", "enclosure", (0, -40)), ("Discos en espejo", "drive2", (-10, 0))]
    pts2 = sorted(((t, ept(k, *d)) for t, k, d in callouts), key=lambda p: p[1][1])
    ys, lead, labels = [], "", ""
    for t, (ax, ay) in pts2:
        y = ay if not ys else max(ay, ys[-1] + 30)
        ys.append(y)
        lead += f'<polyline points="236,{y:.1f} 250,{y:.1f} {ax:.1f},{ay:.1f}"/><circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.6" fill="{lc}" stroke="none"/>'
        labels += f'<div class="abs callout" style="right:{816 - 228}px;top:{y - 9:.1f}px">{t}</div>'
    steps = [("01", "Diagnóstico", "Visitamos tu negocio y vemos cuánta información manejan y quién la usa."),
             ("02", "Diseño", "Elegimos las piezas a tu medida: discos, capacidad y cuentas por persona."),
             ("03", "Armado", "Ensamblamos y probamos el servidor en nuestro taller antes de entregarlo."),
             ("04", "Instalación", "Lo conectamos en tu oficina y capacitamos a tu equipo en una sesión.")]
    st = "".join(f'<div class="step"><p class="n">{n}</p><h3>{t}</h3><p>{d}</p></div>' for n, t, d in steps)
    head = f'<header class="abs lockup">{arite()}<span class="div"></span><span class="lk">Negocios</span></header><div class="abs rule"></div>'
    css = """
    @page{size:8.5in 11in;margin:0}
    :root{--g:#F2F1F0;--ink:#0D0D0D;--ink2:#595959;--tan:#BFAA8F;--grey:#BFBFBF}
    body{font-family:'Jost',sans-serif;color:var(--ink);font-size:12px;line-height:1.45}
    .page{position:relative;width:816px;height:1056px;overflow:hidden;background:var(--g);break-after:page}
    .page:last-child{break-after:auto}
    .lockup{left:40px;top:34px;display:flex;align-items:center;gap:22px}
    .lockup svg{height:78px;width:auto}
    .lockup .div{width:1.2px;height:52px;background:var(--ink);margin-bottom:12px}
    .lk{font-size:40px;font-weight:300;letter-spacing:-.01em;margin-bottom:14px}
    .rule{left:40px;right:40px;top:132px;height:1px;background:var(--ink)}
    .h1{left:40px;top:156px;font-size:44px;line-height:1.08;font-weight:300;letter-spacing:-.015em}
    .h1 b{font-weight:600}
    .lede{left:40px;top:270px;width:600px;font-size:16px;line-height:1.5;color:var(--ink)}
    .col{left:40px;top:356px;width:200px}
    .pt{margin-bottom:22px}
    .pt h3{font-size:18px;font-weight:500;margin-top:8px;line-height:1.1}
    .pt p{font-size:11.5px;line-height:1.42;margin-top:4px}
    .tag{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border:1.2px solid var(--ink);border-radius:50%;font-size:11.5px;font-weight:600;line-height:1;background:var(--g)}
    .t-on{position:absolute;background:var(--ink);color:var(--g)}
    .phil{left:40px;top:846px;width:420px;padding-left:30px}
    .phil .br{position:absolute;left:0;top:4px;bottom:4px;width:12px;border:2px solid var(--ink);border-right:0}
    .phil h4{font-size:13px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2)}
    .phil p{font-size:34px;line-height:1.12;font-weight:300;margin-top:6px}
    .phil p b{font-weight:600}
    .ideal{left:500px;top:846px;width:276px;border-top:1px solid var(--ink);padding-top:10px}
    .ideal h4{font-size:13px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2)}
    .ideal li{list-style:none;font-size:14px;line-height:1.3;padding:7px 0;border-bottom:1px solid var(--grey)}
    .by{right:40px;bottom:26px;font-size:10.5px;color:var(--ink2)}
    .h2{left:40px;top:156px;font-size:40px;line-height:1.08;font-weight:300;letter-spacing:-.015em}
    .steps{left:40px;top:226px;width:736px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
    .step{border-top:1.2px solid var(--ink);padding-top:10px}
    .step .n{font-size:44px;font-weight:300;line-height:1;letter-spacing:-.02em}
    .step h3{font-size:17px;font-weight:500;margin-top:8px}
    .step p{font-size:11.5px;line-height:1.42;margin-top:4px}
    .eqh{left:40px;top:410px;width:200px}
    .eqh h3{font-size:22px;font-weight:300;line-height:1.15}
    .callout{font-size:11.5px;line-height:18px;white-space:nowrap;text-align:right}
    .f1{left:40px;top:780px;width:450px;height:150px;background:var(--tan);padding:18px 20px}
    .f2{left:506px;top:780px;width:270px;height:150px;background:var(--grey);padding:18px 20px}
    .f1 h3{font-size:22px;font-weight:500}
    .f1 p{font-size:13px;line-height:1.45;margin-top:8px;max-width:400px}
    .f2 .n{font-size:64px;font-weight:300;line-height:.9;letter-spacing:-.03em}
    .f2 p{font-size:12px;line-height:1.4;margin-top:8px}
    .cta{left:40px;right:40px;top:956px;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid var(--ink);padding-top:12px}
    .cta p{font-size:15px;line-height:1.35}
    .cta .tel{font-size:34px;font-weight:300;letter-spacing:-.01em;line-height:1}
    """
    if red:   # 2026-11-17: mismo diseño, paleta roja (#EEEBE2 #BF0426 #F2EFE9 #DEA6A3 #0D0D0D)
        css += """
    :root{--g:#F2EFE9;--ink:#0D0D0D;--ink2:#0D0D0D;--tan:#BF0426;--grey:#DEA6A3;--red:#BF0426}
    .h1 b,.phil p b,.step .n,.h2,.eqh h3{color:var(--red)}
    .phil h4,.ideal h4{color:var(--red)}
    .phil .br{border-color:var(--red)}
    .ideal{border-top-color:var(--red)}
    .ideal li{border-bottom-color:var(--grey)}
    .step{border-top-color:var(--red)}
    .tag{border-color:var(--red);color:var(--red)}
    .t-on{background:var(--red);border-color:var(--red);color:var(--g)}
    .f1{color:var(--g)}
    .cta{border-top-color:var(--red)}
    .cta .tel{color:var(--red);font-weight:400}
    .by{color:var(--ink)}
    """
    body = f"""<section class="page">
  {head}
  <h1 class="abs h1">Los archivos de tu negocio,<br>en <b>tu</b> negocio.</h1>
  <p class="abs lede">Arité diseña, arma e instala un servidor privado para tu oficina. Tu equipo guarda, comparte y respalda su trabajo sin depender de servicios como Google Drive, OneDrive o Dropbox.</p>
  <div class="abs col">{col}</div>
  {img}
  {overlay(816, 1056, lines, lc, "3 4", 1.4 if red else 1.2)}
  {marks}
  <div class="abs phil"><span class="br"></span><h4>Nuestra filosofía</h4><p>Si lo pagas,<br>debe ser <b>tuyo</b>.</p></div>
  <div class="abs ideal"><h4>Ideal para</h4><ul><li>Despachos contables y legales</li><li>Consultorios y clínicas</li><li>Estudios de diseño y arquitectura</li><li>Tiendas, talleres y oficinas pequeñas</li></ul></div>
  <p class="abs by">By: Leonardo Aguilar</p>
</section>
<section class="page">
  {head}
  <h2 class="abs h2">Así trabajamos</h2>
  <div class="abs steps">{st}</div>
  <div class="abs eqh"><h3>Lo que llega a tu oficina</h3></div>
  {eimg}
  {overlay(816, 1056, lead, lc, "none", 0.9)}
  {labels}
  <div class="field f1">{hatch("n1", "#0D0D0D", .28 if red else .18, 7)}<h3>Software a la medida</h3><p>También desarrollamos sistemas para tu negocio, como inventarios, citas, cotizaciones o punto de venta, que viven en tu propio servidor y no en la nube de alguien más.</p></div>
  <div class="field f2">{hatch("n2", "#BF0426" if red else "#0D0D0D", .35 if red else .16, 7)}<p class="n">0</p><p>mensualidades de nube. Pagas una vez el equipo y la instalación.</p></div>
  <div class="abs cta"><p>Agenda una presentación de nuestros servicios</p><p class="tel">{TEL}</p></div>
  <p class="abs by">By: Leonardo Aguilar</p>
</section>"""
    return page_doc("Arité Negocios", FONTS_NEU, css, body), None


# =================================================================== PDF · Así se arma tu Aricloud (roja)
GB = 50_000            # MB de fotos (≈ 12,000 fotos de celular)
LAN, UP = 110, 2.5     # MB/s: cable de red gigabit / subida de internet de 20 Mbps


def hms(sec):
    h, m = int(sec // 3600), round(sec % 3600 / 60)
    return f"{h} h {m} min" if h else f"{m} min"


def pdf_aricloud():
    img, pt, sh = scene("eco-red", 40, 290, 736, "Isométrico del ecosistema Aricloud: mini PC, bahía de discos con un disco afuera, router y celular")
    nums = {"1": pt("minipc", -60, -20), "2": pt("enclosure", 60, -60), "3": pt("drive2", -60, -50), "4": pt("router", 50, -40), "5": pt("phone", -30, -50)}
    marks = "".join(tag(k, x - 13, y - 13, "tag t-on") for k, (x, y) in nums.items())
    arr = arrow(pt("drive2", 26, -30), pt("bay2", 14, 24), "#BF0426")
    legend = [("1", "Mini PC", "El cerebro: corre el sistema y la app de fotos."),
              ("2", "Bahía de discos", "Donde viven tus fotos, videos y archivos."),
              ("3", "Discos en espejo", "Si uno falla, el otro tiene la copia."),
              ("4", "Router", "Conecta tu nube a la casa y a tu VPN."),
              ("5", "Tu celular", "Respalda cada foto nueva, solo.")]
    lg = "".join(f'<div class="lg"><span class="tag">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n, t, d in legend)

    tl, tc = GB / LAN, GB / UP
    X0, X1 = 0, 736
    wl = max(6, (X1 - X0) * tl / tc)
    bars = f"""<svg width="736" height="150" viewBox="0 0 736 150" aria-label="Tiempo para copiar 50 GB: {hms(tl)} por cable a Aricloud contra {hms(tc)} subiendo a internet">
      <defs><pattern id="bh" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#0D0D0D" stroke-width="1" stroke-opacity=".35"/></pattern></defs>
      <text x="0" y="14" class="bl">Aricloud, por cable de red en tu casa</text>
      <rect x="0" y="24" width="{wl:.1f}" height="34" fill="#BF0426"/>
      <text x="{wl + 12:.1f}" y="50" class="bv red">{hms(tl)}</text>
      <text x="0" y="92" class="bl">Nube por internet, con una subida de 20 Mbps</text>
      <rect x="0" y="102" width="736" height="34" fill="#DEA6A3"/><rect x="0" y="102" width="736" height="34" fill="url(#bh)"/>
      <text x="726" y="128" text-anchor="end" class="bv">{hms(tc)}</text>
    </svg>"""
    faq = [("¿Qué pasa si un disco se descompone?", "Tus discos trabajan en espejo: el otro tiene una copia idéntica. Cambiamos el disco y la información se vuelve a copiar sola."),
           ("¿Puedo ver mis fotos fuera de casa?", "Sí. Desde tu celular o tu computadora, por tu VPN personal, como si estuvieras en casa."),
           ("¿Necesito saber de computadoras?", "No. Lo armamos, lo instalamos y te enseñamos a usarlo en una sesión."),
           ("¿Puedo crecer después?", "Sí. Agregas o cambias discos por unos más grandes, sin pagar mensualidades.")]
    fq = "".join(f'<div class="fq"><h3>{q}</h3><p>{a}</p></div>' for q, a in faq)
    # espejo: dos discos en alzado con la misma cuadrícula de fotos
    tiles = ["#BF0426", "#DEA6A3", "#0D0D0D", "#DEA6A3", "#BF0426", "#DEA6A3", "#0D0D0D", "#BF0426", "#DEA6A3"]

    def disk(x):
        t = "".join(f'<rect x="{x + 18 + (i % 3) * 24}" y="{30 + (i // 3) * 24}" width="20" height="20" fill="{c}"/>' for i, c in enumerate(tiles))
        return (f'<rect x="{x}" y="10" width="108" height="118" fill="#F2EFE9" stroke="#0D0D0D" stroke-width="1.4"/>{t}'
                f'<line x1="{x + 18}" y1="112" x2="{x + 90}" y2="112" stroke="#0D0D0D" stroke-width="1.4"/>')
    mirror = (f'<svg width="300" height="140" viewBox="0 0 300 140" aria-label="Dos discos con las mismas fotos: espejo">{disk(0)}{disk(192)}'
              f'<line x1="118" y1="58" x2="182" y2="58" stroke="#BF0426" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#mh)"/>'
              f'<line x1="182" y1="80" x2="118" y2="80" stroke="#BF0426" stroke-width="1.6" stroke-dasharray="4 4" marker-end="url(#mh)"/>'
              f'<defs><marker id="mh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10" fill="none" stroke="#BF0426" stroke-width="1.6"/></marker></defs></svg>')
    head = f'<header class="abs lockup">{arite()}<span class="div"></span>{aricloud()}</header><div class="abs rule"></div>'
    css = """
    @page{size:8.5in 11in;margin:0}
    :root{--g:#F2EFE9;--ink:#0D0D0D;--red:#BF0426;--pink:#DEA6A3;--cream:#EEEBE2}
    body{font-family:'Archivo',sans-serif;color:var(--ink);font-size:12px;line-height:1.45}
    .ant,.lg h3,.fq h3{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}
    .page{position:relative;width:816px;height:1056px;overflow:hidden;background:var(--g);break-after:page}
    .page:last-child{break-after:auto}
    .lockup{left:40px;top:34px;display:flex;align-items:center;gap:22px}
    .lockup svg{height:66px;width:auto}
    .lockup .div{width:1.2px;height:48px;background:var(--ink);margin-bottom:14px}
    .rule{left:40px;right:40px;top:132px;height:1.2px;background:var(--ink)}
    .h1{left:40px;top:150px;font-size:64px;line-height:.98;color:var(--red)}
    .lede{left:40px;top:224px;width:560px;font-size:15px;line-height:1.5;font-weight:500}
    .tag{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border:1.4px solid var(--ink);border-radius:50%;font-size:12px;font-weight:600;line-height:1;background:var(--g)}
    .t-on{position:absolute;background:var(--red);border-color:var(--red);color:var(--g)}
    .legend{left:40px;top:770px;width:736px;display:grid;grid-template-columns:repeat(5,1fr);gap:16px;border-top:1.2px solid var(--ink);padding-top:14px}
    .lg h3{font-size:19px;margin-top:8px;line-height:1.05}
    .lg p{font-size:11.5px;line-height:1.4;margin-top:4px}
    .lg .tag{background:var(--red);border-color:var(--red);color:var(--g)}
    .band{left:40px;top:924px;width:736px;height:86px;background:var(--red);color:var(--g);display:flex;align-items:center;justify-content:space-between;padding:0 24px}
    .band .q{font-size:36px;line-height:1;white-space:nowrap}
    .band p.r{font-size:13px;line-height:1.4;max-width:270px;text-align:right}
    .by{right:40px;bottom:22px;font-size:10.5px}
    .h2{left:40px;top:150px;font-size:58px;line-height:.98;color:var(--red)}
    .lede2{left:40px;top:278px;width:600px;font-size:14.5px;line-height:1.5}
    .bars{left:40px;top:340px}
    .bl{font-family:'Archivo',sans-serif;font-size:13px;font-weight:500;fill:#0D0D0D}
    .bv{font-family:'Antonio',sans-serif;font-weight:700;font-size:24px;fill:#0D0D0D;text-transform:uppercase}
    .bv.red{fill:#BF0426}
    .stat{left:40px;top:502px;width:736px;height:86px;border-bottom:1.2px solid var(--ink)}
    .stat .n{position:absolute;left:0;top:4px;font-size:70px;line-height:.9;color:var(--red);white-space:nowrap}
    .stat .c{position:absolute;right:0;bottom:16px;font-size:13px;line-height:1.4;width:290px}
    .mir{left:40px;top:618px;width:736px;display:flex;gap:28px;align-items:center}
    .mir h3{font-size:30px;line-height:1;color:var(--red)}
    .mir p{font-size:13.5px;line-height:1.5;margin-top:8px;max-width:380px}
    .faq{left:40px;top:792px;width:736px;display:grid;grid-template-columns:1fr 1fr;gap:12px 28px}
    .fq{border-top:1px solid var(--pink);padding-top:8px}
    .fq h3{font-size:17px;line-height:1.1}
    .fq p{font-size:11.5px;line-height:1.42;margin-top:4px}
    .cta{left:0;right:0;top:972px;bottom:0;background:var(--ink);color:var(--g);padding:0 40px;display:flex;align-items:center;justify-content:space-between}
    .cta p{font-size:14px;line-height:1.35}
    .cta .tel{font-size:44px;line-height:1}
    .cta .tel small{font-family:'Archivo',sans-serif;font-size:12px;font-weight:500;text-transform:none;display:block;color:var(--pink);letter-spacing:.12em;margin-bottom:6px;text-align:right}
    """
    body = f"""<section class="page">
  {head}
  <h1 class="abs h1 ant">Así se arma tu nube.</h1>
  <p class="abs lede">Tu Aricloud no es una caja cerrada: son piezas elegidas para ti, armadas y probadas por nosotros antes de llegar a tu casa.</p>
  {img}
  {overlay(816, 1056, arr, "#BF0426", "4 4", 1.6)}
  {marks}
  <div class="abs legend">{lg}</div>
  <div class="abs band"><p class="q ant">Si lo pagas, debe ser tuyo.</p><p class="r">Tú defines tu producto como quieras: capacidad, discos y cuentas por persona.</p></div>
  <p class="abs by">By: Leonardo Aguilar</p>
</section>
<section class="page">
  {head}
  <h2 class="abs h2 ant">Rápido, porque<br>está en tu casa.</h2>
  <p class="abs lede2">Lo que tarda copiar 50 GB de fotos, unas 12,000 de celular, a tu Aricloud por cable de red, contra subirlas a una nube por internet.</p>
  <div class="abs bars">{bars}</div>
  <div class="abs stat"><p class="n ant">{tc / tl:.0f}× más rápido</p><p class="c">Tus fotos no viajan por internet para guardarse: van directo de tu celular o tu computadora al equipo de tu casa.</p></div>
  <div class="abs mir">{mirror}<div><h3 class="ant">Cada foto, guardada dos veces</h3><p>Tu Aricloud escribe todo en dos discos distintos al mismo tiempo. Si uno falla, el otro sigue con todo y lo reponemos sin que pierdas nada.</p></div></div>
  <div class="abs faq">{fq}</div>
  <div class="abs cta"><p>Agenda una presentación de nuestros servicios.<br>Pago único desde $15,890.</p><p class="tel ant"><small>Para más información</small>{TEL}</p></div>
</section>"""
    return page_doc("Aricloud · Así se arma tu nube", FONTS_RED, css, body), None


JOBS = {
    "fb-negocio": (post_negocio, "Arite_FB_Negocio_Paleta-Neutra.png"),
    "fb-cartel": (post_cartel, "Arite_FB_Tu-nube-en-casa_Paleta-Roja.png"),
    "pdf-negocio": (pdf_negocio, "Arite_Negocios_Paleta-Neutra.pdf"),
    "pdf-negocio-roja": (lambda: pdf_negocio("red"), "Arite_Negocios_Paleta-Roja.pdf"),
    "pdf-arma": (pdf_aricloud, "Aricloud_Asi-se-arma-tu-nube_Paleta-Roja.pdf"),
}


def main():
    only = sys.argv[1:] or list(JOBS)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE.parent))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        for key in only:
            fn, fname = JOBS[key]
            html, size = fn()
            (HERE / f"{key}.html").write_text(html, encoding="utf-8")
            if size:
                pg = b.new_page(viewport={"width": size[0], "height": size[1]}, device_scale_factor=2)
            else:
                pg = b.new_page(viewport={"width": 816, "height": 1056})
            pg.goto(f"http://127.0.0.1:{port}/_build/{key}.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            if size:
                pg.query_selector(".post").screenshot(path=str(OUT / fname))
            else:
                for i, el in enumerate(pg.query_selector_all(".page")):
                    el.screenshot(path=str(PREV / f"{key}-p{i + 1}.png"))
                pg.pdf(path=str(OUT / fname), prefer_css_page_size=True, print_background=True)
            pg.close()
            print("ok", fname)
        b.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
