"""Third batch (2026-11-17), from the style research (_contexto/investigacion-estilos.md):
  1. fb-lamina   · lámina técnica: planta + alzado + isométrico con cotas y cajetín (paleta neutra)
  2. fb-noche    · axonometría invertida: línea crema sobre negro, acento rojo
  3. fb-ensamble · animación en bucle (GIF) del despiece que se arma solo (paleta roja)
Needs: render_scenes.py unit:neutral eco:night  and  render_anim.py red 30 1100"""
import math, sys, http.server, threading, functools
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from marks import arite, mono
from build_more import scene, overlay, arrow, page_doc, FONTS_RED, FONTS_NEU, TEL

OUT = HERE.parent / "Entregables"
PREV = HERE / "preview"
W, H = 1080, 1350


# ------------------------------------------------------------------ cotas (dimension lines)
def cota(a, b, off, text, color="#0D0D0D", size=15, flip=False):
    """Architectural dimension: extension lines from a,b pushed by vector off, dim line with 45° ticks, centered text."""
    (ax, ay), (bx, by), (ox, oy) = a, b, off
    A, B = (ax + ox, ay + oy), (bx + ox, by + oy)
    L = math.hypot(ox, oy) or 1
    ux, uy = ox / L, oy / L
    ext = lambda p, q: f'<line x1="{p[0] + ux * 4:.1f}" y1="{p[1] + uy * 4:.1f}" x2="{q[0] + ux * 8:.1f}" y2="{q[1] + uy * 8:.1f}" stroke-width="0.8"/>'
    dx, dy = B[0] - A[0], B[1] - A[1]
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90 or ang < -90:
        ang += 180
    tl = math.hypot(dx, dy) or 1
    tx, ty = dx / tl, dy / tl
    tick = lambda p: (f'<line x1="{p[0] - (tx + ux) * 5:.1f}" y1="{p[1] - (ty + uy) * 5:.1f}" '
                      f'x2="{p[0] + (tx + ux) * 5:.1f}" y2="{p[1] + (ty + uy) * 5:.1f}" stroke-width="1.6"/>')
    mx, my = (A[0] + B[0]) / 2 + ux * (13 if not flip else -6), (A[1] + B[1]) / 2 + uy * (13 if not flip else -6)
    return (f'<g stroke="{color}" fill="none">{ext(a, A)}{ext(b, B)}'
            f'<line x1="{A[0]:.1f}" y1="{A[1]:.1f}" x2="{B[0]:.1f}" y2="{B[1]:.1f}" stroke-width="0.9"/>{tick(A)}{tick(B)}</g>'
            f'<text x="{mx:.1f}" y="{my:.1f}" transform="rotate({ang:.2f} {mx:.1f} {my:.1f})" text-anchor="middle" '
            f'dominant-baseline="middle" class="cot" fill="{color}">{text}</text>')


def norm(v, k):
    L = math.hypot(*v) or 1
    return v[0] / L * k, v[1] / L * k


# ================================================================== 1 · Lámina técnica (neutra)
def post_lamina():
    img, pt, sh = scene("unit-neutral", 452, 318, 580, "Isométrico acotado del AriCloud: bahía de dos discos y mini PC")
    P = {k: pt(k) for k in ["pc_fl", "pc_fr", "pc_br", "pc_tr", "enc_fl", "enc_fr", "enc_bl", "enc_tl"]}
    vz = (P["pc_fr"][0] - P["pc_br"][0], P["pc_fr"][1] - P["pc_br"][1])   # screen dir of +z (toward viewer)
    vx = (P["pc_fr"][0] - P["pc_fl"][0], P["pc_fr"][1] - P["pc_fl"][1])   # screen dir of +x
    iso = (cota(P["pc_fl"], P["pc_fr"], norm(vz, 30), "112")
           + cota(P["pc_fr"], P["pc_br"], norm(vx, 30), "112")
           + cota(P["enc_fl"], P["enc_fr"], norm(vz, 30), "110")
           + cota(P["enc_fl"], P["enc_tl"], norm((-vx[0], -vx[1]), 26), "140"))

    # planta y alzado a escala: 1 mm = S px; x de -111 a 141 (252 mm)
    S = 1.25
    X = lambda x: 22 + (x + 111) * S

    def alzado():
        y0 = 30                      # top of the drawing area; ground at y0 + 140*S
        g = y0 + 140 * S
        e = (f'<rect x="{X(-111):.1f}" y="{g - 140 * S:.1f}" width="{110 * S:.1f}" height="{140 * S:.1f}" rx="5" class="f2"/>'
             + "".join(f'<rect x="{X(cx - 18):.1f}" y="{g - 124 * S:.1f}" width="{36 * S:.1f}" height="{116 * S:.1f}" class="f1"/>'
                       f'<rect x="{X(cx - 5):.1f}" y="{g - 92 * S:.1f}" width="{10 * S:.1f}" height="{40 * S:.1f}" class="f3"/>' for cx in (-80, -32))
             + "".join(f'<circle cx="{X(-92 + k * 9):.1f}" cy="{g - 132 * S:.1f}" r="2.4" class="f4"/>' for k in range(3)))
        p = (f'<rect x="{X(29):.1f}" y="{g - 36 * S:.1f}" width="{112 * S:.1f}" height="{34 * S:.1f}" rx="6" class="f2"/>'
             f'<rect x="{X(31):.1f}" y="{g - 38 * S:.1f}" width="{108 * S:.1f}" height="{3 * S:.1f}" class="f1"/>'
             f'<circle cx="{X(47):.1f}" cy="{g - 17 * S:.1f}" r="{4 * S:.1f}" class="f1"/>'
             + "".join(f'<rect x="{X(x):.1f}" y="{g - 19.5 * S:.1f}" width="{w * S:.1f}" height="{h * S:.1f}" class="f3"/>'
                       for x, w, h in ((65, 12, 5), (83, 12, 5), (102, 9, 3.4))))
        ground = f'<line x1="{X(-125):.1f}" y1="{g:.1f}" x2="{X(152):.1f}" y2="{g:.1f}" stroke="#0D0D0D" stroke-width="2.4"/>'
        dims = (cota((X(-111), g), (X(-1), g), (0, 22), "110") + cota((X(29), g), (X(141), g), (0, 22), "112")
                + cota((X(141), g), (X(141), g - 36 * S), (18, 0), "36") + cota((X(-111), g), (X(-111), g - 140 * S), (-16, 0), "140"))
        return f'<svg width="360" height="250" viewBox="0 0 360 250" class="drw">{e}{p}{ground}{dims}</svg>'

    def planta():
        Z = lambda z: 14 + (z + 144) * S * 0.9   # front (z=56) at the bottom
        k = S * 0.9
        e = (f'<rect x="{X(-111):.1f}" y="{Z(-144):.1f}" width="{110 * S:.1f}" height="{200 * k:.1f}" rx="5" class="f2"/>'
             f'<rect x="{X(-108):.1f}" y="{Z(-141):.1f}" width="{104 * S:.1f}" height="{194 * k:.1f}" rx="3" class="f1"/>')
        p = (f'<rect x="{X(29):.1f}" y="{Z(-56):.1f}" width="{112 * S:.1f}" height="{112 * k:.1f}" rx="6" class="f2"/>'
             f'<rect x="{X(31):.1f}" y="{Z(-54):.1f}" width="{108 * S:.1f}" height="{108 * k:.1f}" rx="3" class="f1"/>'
             f'<g transform="translate({X(85) - 26:.1f},{Z(0) - 23:.1f})">' + mono(height=46).replace('<svg ', '<svg width="52" ', 1) + '</g>')
        cable = f'<path d="M{X(-1):.1f} {Z(-30):.1f} H{X(29):.1f}" stroke="#0D0D0D" stroke-width="3" fill="none"/>'
        dims = (cota((X(-111), Z(56)), (X(-111), Z(-144)), (-16, 0), "200")
                + cota((X(141), Z(56)), (X(141), Z(-56)), (18, 0), "112"))
        return f'<svg width="360" height="300" viewBox="0 0 360 300" class="drw">{e}{p}{cable}{dims}</svg>'

    rows = [("Proyecto", "AriCloud · Tu nube en casa"), ("Contenido", "Bahía de 2 discos + mini PC"), ("Cotas", "en milímetros"),
            ("Dibujó", "Leonardo Aguilar"), ("Lámina", "01")]
    caj = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in rows)
    css = f"""
    :root{{--g:#F2F1F0;--ink:#0D0D0D;--ink2:#595959;--tan:#BFAA8F;--grey:#BFBFBF}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--g);color:var(--ink);font-family:'Jost',sans-serif}}
    .logo{{left:64px;top:44px}}
    .kick{{right:64px;top:62px;text-align:right;font-size:16px;line-height:1.45;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--ink2)}}
    .kick b{{color:var(--ink);font-weight:500}}
    .rule{{left:64px;right:64px;top:150px;height:1.2px;background:var(--ink)}}
    .h1{{left:62px;top:172px;font-size:60px;line-height:1.05;font-weight:300;letter-spacing:-.015em}}
    .h1 b{{font-weight:600}}
    .vlabel{{font-size:14px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--ink2);display:flex;gap:10px;align-items:center}}
    .vlabel i{{font-style:normal;display:inline-flex;width:24px;height:24px;border:1.3px solid var(--ink);border-radius:50%;align-items:center;justify-content:center;color:var(--ink);font-size:12px;font-weight:600;letter-spacing:0}}
    .va{{left:44px;top:352px}} .vb{{left:44px;top:654px}} .vc{{left:470px;top:330px}}
    .drw{{display:block;overflow:visible}}
    .da{{left:44px;top:384px}} .db{{left:44px;top:686px}}
    .f1{{fill:#F2F1F0;stroke:#0D0D0D;stroke-width:1.3}} .f2{{fill:#BFBFBF;stroke:#0D0D0D;stroke-width:1.3}}
    .f3{{fill:#595959}} .f4{{fill:#BFAA8F}}
    .cot{{font-family:'Jost',sans-serif;font-size:14px;font-weight:500}}
    .note{{left:64px;top:1018px;width:430px;font-size:21px;line-height:1.38;color:var(--ink)}}
    .note b{{font-weight:500}}
    .caj{{left:560px;top:1000px;width:456px;border:1.2px solid var(--ink);display:flex}}
    .caj .m{{width:110px;border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;font-size:13px;font-weight:500}}
    .caj table{{flex:1;border-collapse:collapse;font-size:13.5px}}
    .caj th{{text-align:left;font-weight:400;color:var(--ink2);padding:5px 10px;border-bottom:1px solid var(--ink);border-right:1px solid var(--ink);width:96px}}
    .caj td{{padding:5px 10px;border-bottom:1px solid var(--ink);font-weight:500}}
    .caj tr:last-child th,.caj tr:last-child td{{border-bottom:0}}
    .cta{{left:0;right:0;top:1206px;bottom:0;background:var(--ink);color:var(--g);padding:0 64px;display:flex;align-items:center;justify-content:space-between}}
    .cta .t{{font-size:20px;line-height:1.4;max-width:430px}}
    .cta .t b{{display:block;color:var(--tan);font-weight:500;font-size:15px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}}
    .cta .tel{{font-size:72px;font-weight:300;letter-spacing:-.01em}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=80)}</div>
  <div class="abs kick">Lámina 01<br><b>AriCloud</b></div>
  <div class="abs rule"></div>
  <h1 class="abs h1">Cabe en un librero.<br>Guarda <b>toda una vida</b> de fotos.</h1>
  <div class="abs vlabel va"><i>A</i>Alzado frontal</div>
  <div class="abs da">{alzado()}</div>
  <div class="abs vlabel vb"><i>B</i>Planta</div>
  <div class="abs db">{planta()}</div>
  <div class="abs vlabel vc"><i>C</i>Isométrico</div>
  {img}
  <svg class="over" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{iso}</svg>
  <p class="abs note">Un mini PC y una bahía de dos discos en espejo. <b>Tus fotos, videos y archivos, en tu casa</b>, sin depender de Apple, Microsoft o Google.</p>
  <div class="abs caj"><div class="m">{mono(height=40)}Arité</div><table>{caj}</table></div>
  <div class="abs cta"><p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p><p class="tel">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Lámina 01", FONTS_NEU, css + ".abs{position:absolute}", body)


# ================================================================== 2 · Axonometría invertida (noche)
def post_noche():
    img, pt, sh = scene("eco-night", 70, 486, 940, "Axonometría en línea clara sobre negro: celular, mini PC, router y bahía de discos")
    flow = arrow(pt("phone", 70, -10), pt("minipc", -70, 10), "#BF0426") + arrow(pt("minipc", 80, -20), pt("enclosure", -70, 10), "#BF0426")
    css = f"""
    :root{{--bg:#0D0D0D;--cream:#F2EFE9;--red:#BF0426;--pink:#DEA6A3}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--bg);color:var(--cream);font-family:'Archivo',sans-serif}}
    .ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}
    .logo{{left:56px;top:44px;color:var(--cream)}}
    .meta{{font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;line-height:1.45}}
    .m-tr{{right:56px;top:56px;text-align:right}}
    .hl{{left:300px;right:300px;top:76px;height:1px;background:var(--cream);opacity:.6}}
    .h1{{left:52px;top:150px;font-size:112px;line-height:.92;letter-spacing:-.005em}}
    .h1 em{{font-style:normal;color:var(--red)}}
    .sub{{left:56px;top:1086px;width:600px;font-size:24px;line-height:1.4}}
    .tagline{{right:56px;top:1090px;width:320px;text-align:right;font-size:17px;line-height:1.4;color:var(--pink)}}
    .tagline b{{display:block;font-family:'Antonio',sans-serif;font-weight:700;font-size:44px;line-height:1;color:var(--cream);text-transform:uppercase;margin-bottom:8px}}
    .foot{{left:56px;right:56px;top:1228px;border-top:1px solid var(--cream);padding-top:20px;display:flex;justify-content:space-between;align-items:flex-end}}
    .foot .meta{{color:var(--pink)}}
    .foot .tel{{font-size:62px;line-height:.9}}
    .lbl{{font-size:14px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;fill:#F2EFE9}}
    """
    px, py = pt("phone", -70, -62)
    sx, sy = pt("enclosure", 10, -196)
    labels = (f'<svg class="over" width="{W}" height="{H}"><text x="{px:.0f}" y="{py:.0f}" class="lbl">Tu celular</text>'
              f'<text x="{sx:.0f}" y="{sy:.0f}" class="lbl">Tu nube, en casa</text></svg>')
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=60)}</div>
  <div class="abs hl"></div>
  <div class="abs meta m-tr">Mini servidores<br>Hogar · Negocio</div>
  <h1 class="abs h1 ant">Tus fotos no deberían<br>vivir en la casa<br>de <em>alguien más.</em></h1>
  {img}
  {overlay(W, H, flow, "#BF0426", "6 6", 2.2)}
  {labels}
  <p class="abs sub">Arité arma tu nube en casa: un mini servidor para tus fotos, videos y archivos, sin depender de Apple, Microsoft o Google.</p>
  <p class="abs tagline"><b>Pagas una vez.</b>Y es tuyo, para siempre.</p>
  <div class="abs foot"><p class="meta">Agenda una presentación<br>de nuestros servicios</p><p class="tel ant">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Noche", FONTS_RED, css + ".abs{position:absolute}", body)


# ================================================================== 3 · Ensamble animado (roja): fondo estático + cuadros
ANIM_BOX = (585, 150, 1020)     # left, top, height of the animation area


def post_ensamble():
    pieces = ["Base", "Chasis con puertos", "Tarjeta madre", "Memoria y SSD", "Disipador", "Ventilador", "Tapa con monograma"]
    pl = "".join(f'<li><span>{i:02d}</span>{p}</li>' for i, p in enumerate(pieces, 1))
    css = f"""
    :root{{--g:#F2EFE9;--ink:#0D0D0D;--red:#BF0426;--pink:#DEA6A3}}
    .post{{position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--g);color:var(--ink);font-family:'Archivo',sans-serif}}
    .ant{{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase}}
    .logo{{left:56px;top:44px}}
    .kick{{left:56px;top:150px;font-size:15px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--red)}}
    .h1{{left:52px;top:184px;font-size:102px;line-height:.9;color:var(--ink)}}
    .h1 em{{font-style:normal;color:var(--red)}}
    .sub{{left:56px;top:520px;width:460px;font-size:22px;line-height:1.42}}
    .list{{left:56px;top:660px;width:440px;list-style:none;border-top:1.2px solid var(--ink)}}
    .list li{{display:flex;gap:16px;font-size:18px;line-height:1;padding:11px 0;border-bottom:1px solid var(--pink)}}
    .list span{{font-family:'Antonio',sans-serif;font-weight:700;color:var(--red);width:26px}}
    .br{{left:552px;top:150px;width:14px;height:1020px;border:2.4px solid var(--red);border-right:0}}
    .cta{{left:0;right:0;top:1206px;bottom:0;background:var(--ink);color:var(--g);padding:0 56px;display:flex;align-items:center;justify-content:space-between}}
    .cta .t{{font-size:20px;line-height:1.4;max-width:440px}}
    .cta .t b{{display:block;color:var(--pink);font-weight:600;font-size:15px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:4px}}
    .cta .tel{{font-size:70px;line-height:1}}
    """
    body = f"""<div class="post">
  <div class="abs logo">{arite(height=72)}</div>
  <p class="abs kick">AriCloud · Ensamble</p>
  <h1 class="abs h1 ant">Lo armamos<br>pieza<br>por <em>pieza.</em></h1>
  <p class="abs sub">Tú eliges las piezas; nosotros ensamblamos tu nube y la probamos antes de llevarla a tu casa.</p>
  <ol class="abs list">{pl}</ol>
  <div class="abs br"></div>
  <div class="abs cta"><p class="t"><b>Contáctanos</b>Agenda una presentación de nuestros servicios</p><p class="tel ant">{TEL}</p></div>
</div>"""
    return page_doc("Arité · Ensamble", FONTS_RED, css + ".abs{position:absolute}", body)


def make_gif(base_png, out_gif, scale=2):
    """Compose the loop: hold exploded, assemble, hold assembled, disassemble. Shared palette (no flicker)."""
    frames = sorted((HERE / "assets" / "anim").glob("ensamble-red-*.png"))
    base = Image.open(base_png).convert("RGB")
    s = base.width / W
    left, top, hh = (int(v * s) for v in ANIM_BOX)
    seq = [0] * 8 + list(range(len(frames))) + [len(frames) - 1] * 30 + list(range(len(frames) - 1, -1, -1))
    cache = {}

    def frame(i):
        if i not in cache:
            im = Image.open(frames[i]).convert("RGBA")
            ww = int(im.width * hh / im.height)
            im = im.resize((ww, hh), Image.LANCZOS)
            c = base.copy()
            c.paste(im, (left + (int(455 * s) - ww) // 2, top), im)
            cache[i] = c
        return cache[i]
    # one palette for all frames, built from the most varied frames
    probe = Image.new("RGB", (base.width, base.height * 2))
    probe.paste(frame(0), (0, 0)); probe.paste(frame(len(frames) // 2), (0, base.height))
    pal = probe.quantize(colors=128, method=Image.MEDIANCUT)
    out = [frame(i).quantize(palette=pal, dither=Image.Dither.NONE) for i in seq]
    out[0].save(out_gif, save_all=True, append_images=out[1:], duration=50, loop=0, optimize=True, disposal=1)
    # static cover (assembled) for platforms that need a still
    frame(len(frames) - 1).save(PREV / "fb-ensamble-final.png")
    return len(seq)


JOBS = {
    "fb-lamina": (post_lamina, "Arite_FB_Lamina-tecnica_Paleta-Neutra.png"),
    "fb-noche": (post_noche, "Arite_FB_Axonometria-noche.png"),
    "fb-ensamble": (post_ensamble, "Arite_FB_Ensamble-animado_Paleta-Roja.gif"),
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
            scale = 1 if key == "fb-ensamble" else 2
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
            pg.goto(f"http://127.0.0.1:{port}/_build/{key}.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            if key == "fb-ensamble":
                base = PREV / "fb-ensamble-base.png"
                pg.query_selector(".post").screenshot(path=str(base))
                n = make_gif(base, OUT / fname)
                print("ok", fname, n, "cuadros")
            else:
                pg.query_selector(".post").screenshot(path=str(OUT / fname))
                print("ok", fname)
            pg.close()
        b.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
