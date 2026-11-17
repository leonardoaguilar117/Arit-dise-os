"""Fourth batch (2026-11-17): same brand, no isometrics. Three 2D directions:
  A · fb-corte       · corte arquitectónico (sección) de una casa con poché, paleta roja
  B · fb-numeros     · cartel suizo: retícula y cifras, paleta neutra
  C · fb-pictogramas · sistema de pictogramas de trazo recto y remate cuadrado (la regla del logo), fondo rojo"""
import sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from marks import arite, mono
from build_more import page_doc, FONTS_RED, FONTS_NEU, TEL

OUT = HERE.parent / "Entregables"
W, H = 1080, 1350


def hatch_def(id_, color, op=0.6, gap=8, w=1.2):
    return (f'<pattern id="{id_}" width="{gap}" height="{gap}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<line x1="0" y1="0" x2="0" y2="{gap}" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}"/></pattern>')


# ================================================================== A · Corte arquitectónico
def section_svg():
    INK, RED, PINK, CREAM = "#0D0D0D", "#BF0426", "#DEA6A3", "#F2EFE9"
    o = [f'<defs>{hatch_def("earth", INK, .55, 9)}{hatch_def("wall", INK, .0, 9)}'
         f'<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10" fill="none" stroke="{RED}" stroke-width="1.6"/></marker></defs>']
    # terreno (rayado) y línea de suelo
    o.append(f'<rect x="0" y="566" width="960" height="70" fill="url(#earth)"/>')
    o.append(f'<line x1="0" y1="566" x2="960" y2="566" stroke="{INK}" stroke-width="2.4"/>')
    # poché: muros, losas y techo cortados (relleno sólido)
    P = [  # (x, y, w, h)
        (86, 214, 18, 352), (856, 214, 18, 352),      # muros exteriores
        (86, 214, 788, 14),                            # losa de azotea (plafón)
        (86, 380, 788, 16), (86, 550, 788, 16),        # losa entrepiso y firme
        (470, 396, 14, 154),                           # muro interior planta baja
        (470, 214, 14, 166),                           # muro interior planta alta
    ]
    # vanos de ventana en muros exteriores (huecos)
    holes = [(86, 254, 18, 70), (856, 254, 18, 70), (86, 430, 18, 70), (856, 430, 18, 70)]
    for x, y, w, h in P:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{INK}"/>')
    for x, y, w, h in holes:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{CREAM}"/>'
                 f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="{INK}" stroke-width="1"/>'
                 f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{INK}" stroke-width="1"/><line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" stroke="{INK}" stroke-width="1"/>')
    # puerta interior planta alta (hueco) y planta baja
    o.append(f'<rect x="470" y="300" width="14" height="80" fill="{CREAM}"/><rect x="470" y="470" width="14" height="80" fill="{CREAM}"/>')
    # techo a dos aguas cortado
    o.append(f'<polygon points="62,222 480,40 898,222 898,240 480,60 62,240" fill="{INK}"/>')
    # --- mobiliario en alzado (línea fina)
    L = f'fill="none" stroke="{INK}" stroke-width="1.6"'
    # planta alta izq.: recámara (cama, buró con celular)
    o.append(f'<rect x="130" y="326" width="230" height="40" {L}/><rect x="130" y="300" width="14" height="80" fill="{INK}"/>'
             f'<rect x="150" y="314" width="56" height="12" {L}/><line x1="130" y1="366" x2="360" y2="366" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<rect x="384" y="336" width="54" height="44" {L}/><rect x="402" y="324" width="16" height="12" fill="{RED}"/>')  # buró + celular
    # planta alta der.: cuarto con tablet en escritorio pequeño
    o.append(f'<line x1="560" y1="330" x2="700" y2="330" stroke="{INK}" stroke-width="3"/><line x1="572" y1="330" x2="572" y2="380" stroke="{INK}" stroke-width="1.6"/>'
             f'<line x1="688" y1="330" x2="688" y2="380" stroke="{INK}" stroke-width="1.6"/><rect x="610" y="306" width="34" height="24" fill="{RED}"/>')
    o.append(f'<rect x="740" y="270" width="80" height="50" {L}/><line x1="746" y1="296" x2="814" y2="296" stroke="{INK}" stroke-width="1"/>')  # cuadro
    # planta baja izq.: sala (sillón + TV)
    o.append(f'<path d="M130 550 V500 H150 V520 H300 V500 H320 V550" {L}/><line x1="150" y1="520" x2="300" y2="520" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<rect x="372" y="456" width="80" height="48" fill="{RED}"/><line x1="412" y1="504" x2="412" y2="520" stroke="{INK}" stroke-width="1.6"/>'
             f'<rect x="366" y="520" width="92" height="30" {L}/>')
    # planta baja der.: estudio (escritorio + laptop + librero con servidor)
    o.append(f'<line x1="530" y1="482" x2="690" y2="482" stroke="{INK}" stroke-width="3"/><line x1="542" y1="482" x2="542" y2="550" stroke="{INK}" stroke-width="1.6"/>'
             f'<line x1="678" y1="482" x2="678" y2="550" stroke="{INK}" stroke-width="1.6"/><path d="M576 482 L590 456 H628" fill="none" stroke="{RED}" stroke-width="3"/>')
    o.append(f'<rect x="740" y="410" width="96" height="140" {L}/><line x1="740" y1="456" x2="836" y2="456" stroke="{INK}" stroke-width="1.6"/>'
             f'<line x1="740" y1="502" x2="836" y2="502" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<rect x="750" y="468" width="34" height="34" fill="{RED}"/><rect x="790" y="480" width="38" height="22" fill="{PINK}" stroke="{INK}" stroke-width="1.2"/>'
             f'<rect x="752" y="420" width="8" height="36" fill="{INK}"/><rect x="764" y="426" width="8" height="30" fill="{PINK}"/><rect x="776" y="418" width="8" height="38" fill="{INK}"/>')
    # --- flujos de datos hacia el servidor
    srv = (767, 470)
    for x, y in [(410, 324), (627, 306), (412, 470), (610, 456)]:
        o.append(f'<line x1="{x}" y1="{y}" x2="{srv[0] - 6 if x < srv[0] else srv[0]}" y2="{srv[1] - 4}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 5" marker-end="url(#ar)"/>')
    # --- nube de alguien más, fuera y tachada
    o.append(f'<g transform="translate(820,40)"><path d="M14 46 H86 C98 46 106 38 106 28 C106 18 98 11 88 11 C84 3 76 -2 66 -2 C54 -2 46 6 44 15 C34 14 24 20 22 30 C14 30 6 36 6 40 C6 44 10 46 14 46 Z" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 4"/>'
             f'<line x1="10" y1="58" x2="104" y2="-8" stroke="{RED}" stroke-width="3"/></g>')
    # --- rótulos con número (círculo) y línea de corte A–A'
    tags = [(1, 410, 300, "Celular"), (2, 627, 286, "Tablet"), (3, 412, 438, "Tele"), (4, 594, 436, "Laptop"), (5, 767, 392, "AriCloud")]
    for n, x, y, t in tags:
        o.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{CREAM}" stroke="{RED}" stroke-width="1.6"/>'
                 f'<text x="{x}" y="{y + 4.5}" text-anchor="middle" class="tg">{n}</text>')
    o.append(f'<text x="924" y="128" text-anchor="end" class="lb">La nube de alguien más</text>')
    for x in (20, 940):
        o.append(f'<line x1="{x}" y1="150" x2="{x}" y2="610" stroke="{INK}" stroke-width="1" stroke-dasharray="14 4 2 4"/>'
                 f'<circle cx="{x}" cy="136" r="13" fill="none" stroke="{INK}" stroke-width="1.4"/><text x="{x}" y="141" text-anchor="middle" class="tg k">A</text>')
    return f'<svg width="960" height="640" viewBox="0 0 960 640" aria-label="Corte arquitectónico de una casa: celular, tablet, tele y laptop guardan sus fotos en el AriCloud del estudio">{"".join(o)}</svg>'


def post_corte():
    leg = [("1", "Celular"), ("2", "Tablet"), ("3", "Tele"), ("4", "Laptop"), ("5", "AriCloud")]
    lg = "".join(f'<li><span>{n}</span>{t}</li>' for n, t in leg)
    css = f"""
    :root{{--g:#F2EFE9;--ink:#0D0D0D;--red:#BF0426;--pink:#DEA6A3}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--g);color:var(--ink);font-family:'Archivo',sans-serif}}
    .ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}
    .abs{{position:absolute}}
    .logo{{left:56px;top:44px}}
    .meta{{right:56px;top:58px;text-align:right;font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;line-height:1.45}}
    .meta b{{color:var(--red);font-weight:600}}
    .rule{{left:56px;right:56px;top:144px;height:1.2px;background:var(--ink)}}
    .h1{{left:52px;top:164px;font-size:96px;line-height:.92}}
    .h1 em{{font-style:normal;color:var(--red)}}
    .drw{{left:60px;top:378px}}
    .tg{{font-family:'Antonio',sans-serif;font-weight:700;font-size:13px;fill:#BF0426}}
    .tg.k{{fill:#0D0D0D;font-size:14px}}
    .lb{{font-family:'Archivo',sans-serif;font-size:13px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;fill:#0D0D0D}}
    .cap{{left:56px;top:1036px;font-size:14px;font-weight:600;letter-spacing:.14em;text-transform:uppercase}}
    .legend{{left:56px;top:1064px;list-style:none;display:flex;gap:26px;font-size:18px}}
    .legend span{{display:inline-flex;width:24px;height:24px;border:1.6px solid var(--red);border-radius:50%;align-items:center;justify-content:center;
                 font-family:'Antonio',sans-serif;font-weight:700;font-size:13px;color:var(--red);margin-right:8px;vertical-align:-3px}}
    .sub{{left:56px;top:1112px;width:960px;font-size:21px;line-height:1.4}}
    .cta{{left:0;right:0;top:1206px;bottom:0;background:var(--red);color:var(--g);padding:0 56px;display:flex;align-items:center;justify-content:space-between}}
    .cta .t{{font-size:20px;line-height:1.4;max-width:440px}}
    .cta .t b{{display:block;font-weight:600;font-size:15px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px;color:var(--ink)}}
    .cta .tel{{font-size:70px;line-height:1}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=72)}</div>
  <div class="abs meta">Corte A–A'<br><b>Tu casa con AriCloud</b></div>
  <div class="abs rule"></div>
  <h1 class="abs h1 ant">Todo lo que ves en tu casa,<br>se <em>guarda</em> en tu casa.</h1>
  <div class="abs drw">{section_svg()}</div>
  <p class="abs cap">Corte A–A' · Sin escala</p>
  <ul class="abs legend">{lg}</ul>
  <p class="abs sub">Celulares, tablet, tele y laptop respaldan sus fotos en un mini servidor en tu estudio. Nada sube a la nube de Apple, Microsoft o Google.</p>
  <div class="abs cta"><p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p><p class="tel ant">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Corte", FONTS_RED, css, body)


# ================================================================== B · Cartel suizo de cifras (neutra)
def post_numeros():
    rows = [("0", "mensualidades", "Pagas una vez el equipo y la instalación. No hay renta mensual."),
            ("2", "discos en espejo", "Cada foto se guarda dos veces. Si un disco falla, el otro tiene todo."),
            ("1–6", "personas por equipo", "Una cuenta para cada quien en casa, con su espacio y sus fotos.")]
    rw = ""
    for i, (n, t, d) in enumerate(rows):
        rw += (f'<div class="row r{i}"><p class="idx">0{i + 1}</p><p class="n">{n}</p>'
               f'<div class="tx"><h3>{t}</h3><p>{d}</p></div></div>')
    cols = "".join(f'<i style="left:{64 + k * 159.2:.1f}px"></i>' for k in range(7))
    css = f"""
    :root{{--g:#F2F1F0;--ink:#0D0D0D;--ink2:#595959;--tan:#BFAA8F;--grey:#BFBFBF}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--g);color:var(--ink);font-family:'Jost',sans-serif}}
    .abs{{position:absolute}}
    .grid i{{position:absolute;top:0;bottom:0;width:1px;background:var(--grey);opacity:.55}}
    .logo{{left:64px;top:46px}}
    .meta{{right:64px;top:60px;text-align:right;font-size:15px;line-height:1.45;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}}
    .meta b{{color:var(--ink);font-weight:500}}
    .h1{{left:64px;top:164px;font-size:40px;line-height:1.12;font-weight:300;letter-spacing:-.01em;width:960px}}
    .h1 b{{font-weight:600}}
    .row{{position:absolute;left:64px;right:64px;height:286px;border-top:1.4px solid var(--ink)}}
    .r0{{top:300px}} .r1{{top:586px}} .r2{{top:872px}}
    .idx{{position:absolute;left:0;top:12px;font-size:15px;font-weight:500;letter-spacing:.14em;color:var(--ink2)}}
    .n{{position:absolute;left:-10px;top:4px;font-size:300px;line-height:1;font-weight:200;letter-spacing:-.05em}}
    .r1 .n{{color:var(--tan);font-weight:300}}
    .r2 .n{{font-size:230px;top:30px}}
    .tx{{position:absolute;left:541px;top:40px;width:410px}}
    .tx h3{{font-size:34px;font-weight:500;line-height:1.05}}
    .tx p{{font-size:20px;line-height:1.4;margin-top:12px;color:var(--ink2)}}
    .cta{{left:0;right:0;top:1170px;bottom:0;background:var(--ink);color:var(--g);padding:0 64px;display:flex;align-items:center;justify-content:space-between}}
    .cta .t{{font-size:20px;line-height:1.4;max-width:420px}}
    .cta .t b{{display:block;color:var(--tan);font-weight:500;font-size:15px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}}
    .cta .tel{{font-size:76px;font-weight:300;letter-spacing:-.01em}}
    """
    body = f"""<div class="post">
  <div class="abs grid" style="left:0;top:0;width:{W}px;height:1170px">{cols}</div>
  <div class="abs logo">{arite(height=80)}</div>
  <div class="abs meta">AriCloud<br><b>en tres cifras</b></div>
  <h1 class="abs h1">Tu nube, en tu casa.<br><b>Sin depender</b> de Apple, Microsoft o Google.</h1>
  {rw}
  <div class="abs cta"><p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p><p class="tel">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Cifras", FONTS_NEU, css, body)


# ================================================================== C · Pictogramas (regla del logo: solo trazos rectos, remate cuadrado)
PICTOS = [
    ("Tus fotos", '<rect x="10" y="14" width="44" height="36"/><polyline points="14,46 26,32 34,40 40,34 50,46"/><rect x="40" y="20" width="6" height="6"/>'),
    ("En tu casa", '<polyline points="8,30 32,10 56,30"/><polyline points="16,24 16,52 48,52 48,24"/><polyline points="28,52 28,40 36,40 36,52"/>'),
    ("Sin mensualidad", '<rect x="12" y="18" width="40" height="34"/><line x1="12" y1="28" x2="52" y2="28"/><line x1="22" y1="12" x2="22" y2="22"/><line x1="42" y1="12" x2="42" y2="22"/><line x1="8" y1="56" x2="56" y2="8" class="x"/>'),
    ("Dos discos en espejo", '<rect x="8" y="12" width="18" height="40"/><rect x="38" y="12" width="18" height="40"/><line x1="13" y1="44" x2="21" y2="44"/><line x1="43" y1="44" x2="51" y2="44"/><polyline points="29,26 35,26"/><polyline points="32,22 36,26 32,30"/><polyline points="35,38 29,38"/><polyline points="32,34 28,38 32,42"/>'),
    ("Desde tu celular", '<rect x="20" y="6" width="24" height="52"/><line x1="28" y1="52" x2="36" y2="52"/><rect x="25" y="13" width="6" height="6"/><rect x="33" y="13" width="6" height="6"/><rect x="25" y="21" width="6" height="6"/><rect x="33" y="21" width="6" height="6"/>'),
    ("Seguro fuera de casa", '<rect x="16" y="30" width="32" height="24"/><polyline points="22,30 22,16 42,16 42,30"/><line x1="32" y1="38" x2="32" y2="46"/>'),
    ("Tú decides quién entra", '<rect x="26" y="8" width="12" height="12"/><polyline points="18,44 18,26 46,26 46,44"/><polyline points="36,50 42,56 56,40" class="x"/>'),
    ("Lo armamos", '<rect x="14" y="40" width="36" height="12"/><rect x="18" y="24" width="28" height="8"/><rect x="22" y="8" width="20" height="8"/><line x1="32" y1="16" x2="32" y2="22"/><line x1="32" y1="32" x2="32" y2="38"/>'),
    ("Te enseñamos", '<rect x="8" y="10" width="48" height="30"/><line x1="32" y1="40" x2="32" y2="50"/><polyline points="22,58 32,50 42,58"/><line x1="16" y1="20" x2="34" y2="20"/><line x1="16" y1="28" x2="28" y2="28"/>'),
]


def post_pictos():
    cells = "".join(
        f'<div class="cell"><svg viewBox="0 0 64 64" width="112" height="112" fill="none" stroke="currentColor" stroke-width="3.2" '
        f'stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true">{svg}</svg><p><span>{i:02d}</span>{t}</p></div>'
        for i, (t, svg) in enumerate(PICTOS, 1))
    css = f"""
    :root{{--red:#BF0426;--cream:#F2EFE9;--pink:#DEA6A3;--ink:#0D0D0D}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--red);color:var(--cream);font-family:'Archivo',sans-serif}}
    .ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}
    .abs{{position:absolute}}
    .logo{{left:56px;top:44px;color:var(--cream)}}
    .meta{{right:56px;top:58px;text-align:right;font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;line-height:1.45}}
    .h1{{left:52px;top:150px;font-size:100px;line-height:.92}}
    .h1 em{{font-style:normal;color:var(--ink)}}
    .grid{{left:56px;top:388px;width:968px;display:grid;grid-template-columns:repeat(3,1fr);border-top:1.2px solid var(--cream);border-left:1.2px solid var(--cream)}}
    .cell{{height:236px;border-right:1.2px solid var(--cream);border-bottom:1.2px solid var(--cream);padding:30px 28px;display:flex;flex-direction:column;justify-content:space-between}}
    .cell svg .x{{stroke:var(--ink)}}
    .cell p{{font-size:20px;font-weight:600;line-height:1.2}}
    .cell p span{{display:block;font-family:'Antonio',sans-serif;font-size:14px;letter-spacing:.12em;color:var(--pink);margin-bottom:4px}}
    .note{{left:56px;top:1118px;width:968px;font-size:17px;line-height:1.4;color:var(--pink)}}
    .note b{{color:var(--cream);font-weight:600}}
    .foot{{left:56px;right:56px;top:1214px;border-top:1.2px solid var(--cream);padding-top:20px;display:flex;justify-content:space-between;align-items:flex-end}}
    .foot .m{{font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;line-height:1.45}}
    .foot .tel{{font-size:66px;line-height:.9}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=64)}</div>
  <div class="abs meta">AriCloud<br>en 9 señales</div>
  <h1 class="abs h1 ant">Tu nube en casa,<br><em>sin letras chiquitas.</em></h1>
  <div class="abs grid">{cells}</div>
  <p class="abs note"><b>Dibujados con la regla del logo Arité:</b> solo trazos rectos, del mismo grosor y con remate cuadrado.</p>
  <div class="abs foot"><p class="m">Agenda una presentación<br>de nuestros servicios</p><p class="tel ant">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Señales", FONTS_RED, css, body)


JOBS = {
    "fb-corte": (post_corte, "Arite_FB_Corte-casa_Paleta-Roja.png"),
    "fb-numeros": (post_numeros, "Arite_FB_Cifras_Paleta-Neutra.png"),
    "fb-pictogramas": (post_pictos, "Arite_FB_Pictogramas_Paleta-Roja.png"),
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
            (HERE / f"{key}.html").write_text(fn(), encoding="utf-8")
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
            pg.goto(f"http://127.0.0.1:{port}/_build/{key}.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            pg.query_selector(".post").screenshot(path=str(OUT / fname))
            pg.close()
            print("ok", fname)
        b.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
