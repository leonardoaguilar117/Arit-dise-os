"""Build the three Aricloud promo PDFs (Letter, 2 pages each) and PNG previews."""
import json, sys, http.server, threading, functools
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from marks import arite, aricloud, mono, icon, alzado_minipc, alzado_nas, SW

OUT = HERE.parent / "Entregables"
OUT.mkdir(exist_ok=True)
PREV = HERE / "preview"
PREV.mkdir(exist_ok=True)

PARTS = [("lid", "Tapa"), ("fan", "Ventilador"), ("sink", "Disipador"), ("ssd", "SSD del sistema"),
         ("ram", "Memoria RAM"), ("board", "Tarjeta madre y procesador"), ("shell", "Chasis con puertos"), ("base", "Base")]


def leaders(render, left, top, height, label_right, min_gap=22, color="currentColor"):
    """Exploded-view callouts: label text right-aligned at label_right, leader to each part's anchor."""
    meta = json.loads((HERE / "assets" / f"despiece-{render}.json").read_text())
    w = height * meta["w"] / meta["h"]
    pts = []
    for key, text in PARTS:
        a = meta["labels"][key]
        pts.append([text, left + a["x"] * w, top + a["y"] * height])
    pts.sort(key=lambda p: p[2])
    ys = []
    for _, _, ay in pts:
        y = ay if not ys else max(ay, ys[-1] + min_gap)
        ys.append(y)
    svg, html = [], []
    for (text, ax, ay), ly in zip(pts, ys):
        x0 = label_right + 8
        svg.append(f'<polyline points="{x0},{ly:.1f} {x0 + 14},{ly:.1f} {ax:.1f},{ay:.1f}" />'
                   f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.6" fill="{color}" stroke="none"/>')
        html.append(f'<div class="callout" style="right:{816 - label_right}px;top:{ly - 8:.1f}px">{text}</div>')
    img = f'<img class="render" src="../_build/assets/despiece-{render}.png" style="left:{left}px;top:{top}px;height:{height}px;width:{w:.1f}px" alt="Despiece isométrico de un mini PC: base, chasis, tarjeta madre, memoria, SSD, disipador, ventilador y tapa">'
    over = (f'<svg class="leaders" width="816" height="1056" viewBox="0 0 816 1056" fill="none" '
            f'stroke="{color}" stroke-width="0.9">{"".join(svg)}</svg>')
    return img + over + "".join(html), w


def hatch(id_, color, opacity, gap=7):
    return (f'<svg class="hatch" aria-hidden="true"><defs><pattern id="{id_}" width="{gap}" height="{gap}" '
            f'patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="{gap}" '
            f'stroke="{color}" stroke-width="1" stroke-opacity="{opacity}"/></pattern></defs>'
            f'<rect width="100%" height="100%" fill="url(#{id_})"/></svg>')


COPY = {
    "box2": "Aricloud es un servidor en casa que da solución a la problemática de almacenamiento en nube por suscripción. Te permite guardar fotos, videos y archivos sin depender de suscripciones a servicios como Google Fotos, iCloud, Dropbox o OneDrive. Podrás tener tu información lista para consultar en cualquier parte desde tus dispositivos, todo desde tu red VPN personal.",
    "box4": "Ten la seguridad y la confianza de que tu información está verdaderamente en tus manos y no en el servidor de una corporación.",
    "box3": "Tú diseñas y eliges, nosotros armamos el Aricloud según tus necesidades.",
    "points": [
        ("A", "confia", "Confía", "Tus fotos viven en un equipo que es tuyo, dentro de tu casa."),
        ("B", "almacena", "Almacena", "Fotos, videos y archivos de toda la familia en un solo lugar."),
        ("C", "sincroniza", "Sincroniza", "Tu celular y tu computadora respaldan solos cada foto nueva."),
        ("D", "disfruta", "Disfruta", "Mira tus recuerdos cuando quieras, ordenados por fecha y lugar."),
    ],
}

TIERS = [
    ("Personal", "1", "1 TB", "2 × 1 TB", "150,000", "$15,890", "78 h"),
    ("Familiar", "2 a 6", "2 TB", "2 × 2 TB", "529,000", "$22,900", "156 h"),
    ("Personalizado", "–", "–", "–", "–", "A convenir", "–"),
]


def pricing_table():
    head = "".join(f"<th scope='col'>{t[0]}</th>" for t in TIERS)
    rows = [
        ("Personas", 1), ("Espacio para tus archivos", 2), ("Discos en espejo", 3), ("Fotos de celular, hasta", 4), ("Video en 4K, hasta", 6),
    ]
    body = "".join(f"<tr><th scope='row'>{r}</th>" + "".join(f"<td>{t[i]}</td>" for t in TIERS) + "</tr>" for r, i in rows)
    body += "<tr class='price'><th scope='row'>Pago único</th>" + "".join(f"<td>{t[5]}</td>" for t in TIERS) + "</tr>"
    return f"<table class='prices'><thead><tr><td></td>{head}</tr></thead><tbody>{body}</tbody></table>"


OPTIONS = [
    ("6", "A la medida", "Para más de 1 persona", "Un mini PC de bajo consumo conectado a una bahía para dos o cuatro discos duros. Compacto, silencioso y fácil de crecer.",
     ["Mini PC con procesador de bajo consumo", "Memoria RAM y SSD para el sistema", "Bahía externa de 2 o 4 discos", "Discos duros de 2 a 8 TB"], "minipc"),
    ("7", "NAS Clásico", "Para 1 persona", "Un gabinete NAS de dos o cuatro bahías, elegido según tu presupuesto y configurado por nosotros.",
     ["Gabinete NAS de 2 o 4 bahías", "Discos duros de 2 a 8 TB", "El mismo sistema y apps de fotos", "Armado y probado antes de entregarse"], "nas"),
]
INCLUDES = "Ambas incluyen instalación en tu casa, respaldo automático de celulares, una cuenta por persona y una sesión para enseñarte a usarlo."



# ------------------------------------------------------------------ hoja comparativa (solo paleta roja)
COMP_COLS = ["Aricloud", "Google One", "iCloud+", "Dropbox / OneDrive"]
COMP_MONTH = ["$0", "$199", "$179", "Plan de pago"]
# 2 = lo cubre, 1 = a medias, 0 = no lo cubre   (Aricloud, Google One, iCloud+, Dropbox / OneDrive)
COMP_ROWS = [
    ("Pagas una vez y se acabó", [2, 0, 0, 0]),
    ("Tus archivos viven en tu casa", [2, 0, 0, 0]),
    ("Tú decides quién entra y qué se guarda", [2, 1, 1, 1]),
    ("Sin alzas de precio ni cambios de plan", [2, 0, 0, 0]),
    ("Creces agregando discos, no pagando más", [2, 1, 1, 1]),
    ("Tus archivos siguen contigo aunque dejes de pagar", [2, 0, 0, 0]),
    ("Instalación y asesoría en tu casa", [2, 0, 0, 0]),
    ("Acceso desde cualquier lugar y dispositivo", [2, 2, 2, 2]),
]


def mark(v, cls=""):
    c = f' class="{cls}"' if cls else ""
    if v == 2:
        return f'<svg{c} width="20" height="20" viewBox="0 0 20 20" aria-label="Sí"><circle cx="10" cy="10" r="8" fill="currentColor"/></svg>'
    if v == 1:
        return (f'<svg{c} width="20" height="20" viewBox="0 0 20 20" aria-label="A medias"><circle cx="10" cy="10" r="7.2" fill="none" stroke="currentColor" stroke-width="1.5"/>'
                f'<path d="M10 2.8 A7.2 7.2 0 0 0 10 17.2 Z" fill="currentColor"/></svg>')
    return f'<svg{c} width="20" height="20" viewBox="0 0 20 20" aria-label="No"><circle cx="10" cy="10" r="7.2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'


def compare_page_table():
    head = "".join(f'<th scope="col" class="{"hl" if i == 0 else ""}">{n}</th>' for i, n in enumerate(COMP_COLS))
    rows = '<tr class="month"><th scope="row"><span class="num">00</span>Lo que pagas cada mes</th>' + "".join(
        f'<td class="{"hl" if i == 0 else ""}"><b>{v}</b></td>' for i, v in enumerate(COMP_MONTH)) + "</tr>"
    for n, (label, vals) in enumerate(COMP_ROWS, 1):
        rows += f'<tr><th scope="row"><span class="num">{n:02d}</span>{label}</th>' + "".join(
            f'<td class="{"hl" if i == 0 else ""}">{mark(v)}</td>' for i, v in enumerate(vals)) + "</tr>"
    scores = [sum(v[i] for _, v in COMP_ROWS) for i in range(4)]
    mx = 16
    bars = ""
    for name, sc in zip(COMP_COLS, scores):
        segs = "".join(f'<i class="{"on" if k < sc else ""}"></i>' for k in range(mx))
        bars += f'<div class="bar {"me" if name == "Aricloud" else ""}"><span class="bn">{name}</span><span class="bs">{segs}</span><span class="bv">{sc // 2 if sc % 2 == 0 else sc / 2:g}<small>/8</small></span></div>'
    return f"""<section class="page pc">
  <header class="abs p2-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <div class="abs p2-rule"></div>
  <h2 class="abs h-sec cp-title display">Aricloud contra la nube de renta</h2>
  <p class="abs cp-lede">Las nubes por suscripción son cómodas, pero tu información vive en su casa y la pagas cada mes. Así se ve lo que ganas con la tuya.</p>
  <div class="abs cp-table"><table><colgroup><col class="c0"></colgroup><thead><tr><td></td>{head}</tr></thead><tbody>{rows}</tbody></table></div>
  <div class="abs cp-bars"><h3 class="h-sec">Beneficios que cubre cada una</h3>{bars}</div>
  <div class="abs cp-claim"><p class="display">La única que <em>no se renta.</em></p></div>
  <p class="abs cp-foot">{mark(2)}lo cubre{mark(1)}a medias{mark(0)}no lo cubre. Precios de referencia en pesos mexicanos de los planes de 2 TB (Google One, iCloud+); pueden variar. Aricloud: pago único, sin mensualidades; en la opción Personal, 1 TB en espejo.</p>
</section>
"""


GOOGLE, ICLOUD = 199 * 12, 179 * 12      # MXN por año, planes de 2 TB
PERSONAL, FAMILIAR = 15890, 22900
YEARS = 12


def money(n):
    return f"${n:,.0f}"


def time_chart():
    X0, X1, YB, YT = 56, 585, 380, 20
    sx = lambda t: X0 + t * (X1 - X0) / YEARS
    sy = lambda v: YB - v * (YB - YT) / 30000
    o = []
    o.append('<defs><pattern id="sv" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             '<line x1="0" y1="0" x2="0" y2="7" stroke="#BF0426" stroke-width="1" stroke-opacity="0.55"/></pattern></defs>')
    for v in range(0, 30001, 5000):
        y = sy(v)
        o.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#DEA6A3" stroke-width="1"/>')
        o.append(f'<text x="{X0 - 8}" y="{y + 3.5:.1f}" text-anchor="end" class="ax">{money(v)}</text>')
    for t in range(0, YEARS + 1):
        x = sx(t)
        o.append(f'<line x1="{x:.1f}" y1="{YB}" x2="{x:.1f}" y2="{YB + 5}" stroke="#0D0D0D" stroke-width="1.2"/>')
        o.append(f'<text x="{x:.1f}" y="{YB + 19}" text-anchor="middle" class="ax">{t}</text>')
    o.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="#0D0D0D" stroke-width="1.4"/>')
    o.append(f'<text x="{X1 + 8}" y="{YB + 19}" class="ax">años</text>')
    # zona de ahorro: entre Aricloud Personal y Google One, después del cruce
    t1 = PERSONAL / GOOGLE
    o.append(f'<polygon points="{sx(t1):.1f},{sy(PERSONAL):.1f} {sx(YEARS):.1f},{sy(PERSONAL):.1f} {sx(YEARS):.1f},{sy(GOOGLE * YEARS):.1f}" fill="url(#sv)"/>')
    # suscripciones
    o.append(f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(YEARS):.1f}" y2="{sy(GOOGLE * YEARS):.1f}" stroke="#0D0D0D" stroke-width="2.2"/>')
    o.append(f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(YEARS):.1f}" y2="{sy(ICLOUD * YEARS):.1f}" stroke="#0D0D0D" stroke-width="2.2" stroke-dasharray="6 4"/>')
    # Aricloud: pago único (sube una vez y se queda plano)
    for val, w in ((PERSONAL, 3.6), (FAMILIAR, 3.6)):
        o.append(f'<path d="M{sx(0)} {sy(0)} V{sy(val):.1f} H{sx(YEARS):.1f}" fill="none" stroke="#BF0426" stroke-width="{w}" stroke-linejoin="miter"/>')
    # cruces
    for val, name in ((PERSONAL, "p"), (FAMILIAR, "f")):
        t = val / GOOGLE
        x, y = sx(t), sy(val)
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{YB}" stroke="#BF0426" stroke-width="1.2" stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#EEEBE2" stroke="#BF0426" stroke-width="2.2"/>')
        o.append(f'<rect x="{x - 28:.1f}" y="{YB - 24}" width="56" height="18" fill="#EEEBE2"/>')
        o.append(f'<text x="{x:.1f}" y="{YB - 11}" text-anchor="middle" class="al red">año {t:.1f}</text>')
    # etiquetas al final de cada línea
    def end(v, name, sub, red=False):
        y = sy(v)
        c = "red" if red else ""
        return (f'<text x="{X1 + 10}" y="{y - 2:.1f}" class="en {c}">{name}</text>'
                f'<text x="{X1 + 10}" y="{y + 15:.1f}" class="al big {c}">{sub}</text>')
    o.append(end(GOOGLE * YEARS, "Google One · 2 TB", money(GOOGLE * YEARS)))
    o.append(end(ICLOUD * YEARS, "iCloud+ · 2 TB", money(ICLOUD * YEARS)))
    o.append(end(FAMILIAR, "Aricloud Familiar · 2 TB", money(FAMILIAR), True))
    o.append(end(PERSONAL, "Aricloud Personal · 1 TB", money(PERSONAL), True))
    ex, ey = sx(10.35), sy(19300)
    o.append(f'<rect x="{ex - 46:.1f}" y="{ey - 12:.1f}" width="92" height="18" fill="#EEEBE2"/><text x="{ex:.1f}" y="{ey + 1:.1f}" text-anchor="middle" class="al red">lo que te ahorras</text>')
    return (f'<svg viewBox="0 0 736 410" width="736" height="410" aria-label="Gráfica de dinero acumulado contra tiempo: las suscripciones suben cada mes y Aricloud se paga una sola vez">'
            + "".join(o) + '</svg>')


BENEFITS = ["Pagas una vez, sin mensualidades", "Tus archivos viven en tu casa", "Tú decides quién entra y qué se guarda",
            "Creces agregando discos, no pagando más", "Instalación y asesoría en tu casa", "Acceso desde cualquier lugar, por tu VPN personal"]


def compare_page():
    save = GOOGLE * YEARS - PERSONAL
    bl = "".join(f'<li><span class="num">{i:02d}</span>{b}</li>' for i, b in enumerate(BENEFITS, 1))
    return f"""<section class="page pc">
  <header class="abs p2-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <div class="abs p2-rule"></div>
  <h2 class="abs h-sec cp-title display">Ellas cobran cada mes.<br>Aricloud, una sola vez.</h2>
  <p class="abs cp-lede">Dinero acumulado en 12 años. Una suscripción de 2 TB sube todos los meses; tu Aricloud se paga una vez y la línea se queda plana.</p>
  <div class="abs cp-chart">{time_chart()}</div>
  <div class="abs cp-stat"><p class="display big">{money(save)}</p><p class="cap">que te ahorras en 12 años con Aricloud Personal frente a Google One de 2 TB. Después del año 7, tu nube es gratis.</p></div>
  <div class="abs cp-ben"><h3 class="h-sec">Y lo que el dinero no mide</h3><ul>{bl}</ul></div>
  <p class="abs cp-foot">Precios de referencia en pesos mexicanos: Google One 2 TB $199/mes, iCloud+ 2 TB $179/mes; pueden variar y aquí no se suman alzas futuras. Aricloud: pago único, armado e instalación incluidos; Personal con 1 TB en espejo y Familiar con 2 TB en espejo.</p>
</section>
"""


# ---- versión 2: familia con un plan por persona (más corto el tiempo de retorno)
SUB = 179                                   # MXN/mes, plan de 2 TB por persona (el más económico de la comparación)
HOUSES = [(6, "6 personas"), (4, "4 personas"), (2, "2 personas")]
YEARS2 = 6


def time_chart():
    X0, X1, YB, YT = 56, 585, 322, 16
    VMAX = 80000
    sx = lambda t: X0 + t * (X1 - X0) / YEARS2
    sy = lambda v: YB - v * (YB - YT) / VMAX
    o = ['<defs><pattern id="sv" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<line x1="0" y1="0" x2="0" y2="7" stroke="#BF0426" stroke-width="1" stroke-opacity="0.55"/></pattern></defs>']
    for v in range(0, VMAX + 1, 20000):
        y = sy(v)
        o.append(f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" stroke="#DEA6A3" stroke-width="1"/>')
        o.append(f'<text x="{X0 - 8}" y="{y + 3.5:.1f}" text-anchor="end" class="ax">{money(v)}</text>')
    for t in range(0, YEARS2 + 1):
        x = sx(t)
        o.append(f'<line x1="{x:.1f}" y1="{YB}" x2="{x:.1f}" y2="{YB + 5}" stroke="#0D0D0D" stroke-width="1.2"/>')
        o.append(f'<text x="{x:.1f}" y="{YB + 19}" text-anchor="middle" class="ax">{t}</text>')
    o.append(f'<line x1="{X0}" y1="{YB}" x2="{X1}" y2="{YB}" stroke="#0D0D0D" stroke-width="1.4"/>')
    o.append(f'<text x="{X1 + 8}" y="{YB + 19}" class="ax">años</text>')
    m4 = FAMILIAR / (SUB * 4)
    t4 = m4 / 12
    o.append(f'<polygon points="{sx(t4):.1f},{sy(FAMILIAR):.1f} {sx(YEARS2):.1f},{sy(FAMILIAR):.1f} {sx(YEARS2):.1f},{sy(SUB * 4 * 12 * YEARS2):.1f}" fill="url(#sv)"/>')
    styles = {6: ("2.6", ""), 4: ("2.6", ""), 2: ("2.2", "6 4")}
    for n, _ in HOUSES:
        w, d = styles[n]
        da = f' stroke-dasharray="{d}"' if d else ""
        o.append(f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(YEARS2):.1f}" y2="{sy(SUB * n * 12 * YEARS2):.1f}" stroke="#0D0D0D" stroke-width="{w}"{da}/>')
    o.append(f'<path d="M{sx(0)} {sy(0)} V{sy(FAMILIAR):.1f} H{sx(YEARS2):.1f}" fill="none" stroke="#BF0426" stroke-width="3.8"/>')
    for n, _ in HOUSES:
        meses = FAMILIAR / (SUB * n)
        x, y = sx(meses / 12), sy(FAMILIAR)
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{YB}" stroke="#BF0426" stroke-width="1.2" stroke-dasharray="3 3"/>')
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#EEEBE2" stroke="#BF0426" stroke-width="2.2"/>')
        o.append(f'<rect x="{x - 30:.1f}" y="{YB - 24}" width="60" height="18" fill="#EEEBE2"/>')
        o.append(f'<text x="{x:.1f}" y="{YB - 11}" text-anchor="middle" class="al red">{meses:.0f} meses</text>')

    def end(ynm, name, val, red=False):
        c = "red" if red else ""
        return (f'<text x="{X1 + 10}" y="{ynm}" class="en {c}">{name}</text>'
                f'<text x="{X1 + 10}" y="{ynm + 17}" class="al big {c}">{val}</text>')
    o.append(end(sy(SUB * 6 * 12 * YEARS2) + 4, "Familia de 6 · un plan c/u", money(SUB * 6 * 12 * YEARS2)))
    o.append(end(sy(SUB * 4 * 12 * YEARS2) + 4, "Familia de 4 · un plan c/u", money(SUB * 4 * 12 * YEARS2)))
    o.append(end(sy(SUB * 2 * 12 * YEARS2) - 20, "Familia de 2 · un plan c/u", money(SUB * 2 * 12 * YEARS2)))
    o.append(end(sy(FAMILIAR) + 16, "Aricloud Familiar · 2 TB", money(FAMILIAR), True))
    ex, ey = sx(5.0), sy(31000)
    o.append(f'<rect x="{ex - 48:.1f}" y="{ey - 12:.1f}" width="96" height="18" fill="#EEEBE2"/><text x="{ex:.1f}" y="{ey + 1:.1f}" text-anchor="middle" class="al red">lo que te ahorras</text>')
    return (f'<svg viewBox="0 0 736 354" width="736" height="354" aria-label="Gráfica de dinero acumulado contra tiempo en una familia con un plan de nube por persona: Aricloud se paga solo en 21, 32 o 64 meses">'
            + "".join(o) + '</svg>')


def compare_page():
    save4 = SUB * 4 * 12 * YEARS2 - FAMILIAR
    stats = "".join(
        f'<div class="st"><p class="display big">{FAMILIAR / (SUB * n):.0f} meses</p><p class="cap">y se paga sola en una familia de {n}</p></div>'
        for n, _ in HOUSES)
    bl = "".join(f'<li><span class="num">{i:02d}</span>{b}</li>' for i, b in enumerate(BENEFITS, 1))
    return f"""<section class="page pc">
  <header class="abs p2-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <div class="abs p2-rule"></div>
  <h2 class="abs h-sec cp-title display">Tu familia ya paga nube.<br>Aricloud se paga sola.</h2>
  <p class="abs cp-lede">Dinero acumulado en 6 años si cada persona de casa tiene su propio plan de 2 TB. Mientras más son en casa, más rápido se recupera la inversión.</p>
  <div class="abs cp-chart">{time_chart()}</div>
  <div class="abs cp-stats">{stats}</div>
  <div class="abs cp-risk"><svg class="hatch" aria-hidden="true"><defs><pattern id="h9" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#0D0D0D" stroke-width="1" stroke-opacity="0.22"/></pattern></defs><rect width="100%" height="100%" fill="url(#h9)"/></svg>
    <p class="display rk">Si dejas de pagar,<br>te pueden borrar todo.</p>
    <p class="rt">Con una nube por suscripción, tus recuerdos existen mientras pagues. Con Aricloud viven en tu casa: nadie puede cobrarlos, bloquearlos ni borrarlos.</p></div>
  <div class="abs cp-ben"><ul>{bl}</ul></div>
  <p class="abs cp-foot">Referencia: plan de 2 TB a {money(SUB)}/mes por persona (iCloud+, el más económico; Google One 2 TB está en $199). El cálculo supone una cuenta de pago por persona; los planes familiares compartidos lo cambian. En una familia de 4, ahorras {money(save4)} en 6 años. Aricloud Familiar: {money(FAMILIAR)} pago único, 2 TB en espejo, armado e instalación incluidos. Los precios pueden variar.</p>
</section>
"""

# ------------------------------------------------------------------ PDF 1 and 2 (same structure, two palettes)
THEMES = {
    "neutral": dict(
        file="Aricloud_Paleta-Neutra.pdf", render="neutral",
        fonts="family=Jost:wght@300;400;500;600",
        css="""
        :root{--ground:#F2F1F0;--ink:#0D0D0D;--ink2:#595959;--rule:#BFBFBF;--accent:#BFAA8F;--field:#BFAA8F;--field-ink:#0D0D0D;
              --field2:#BFBFBF;--field2-ink:#0D0D0D;--p2-ground:#F2F1F0;--p2-ink:#0D0D0D;--p2-ink2:#595959;--p2-rule:#BFBFBF;--hi:#0D0D0D;}
        body{font-family:'Jost',sans-serif}
        .display{font-family:'Jost',sans-serif;font-weight:300;letter-spacing:-0.01em}
        .h-sec{font-weight:400;letter-spacing:-0.01em}
        .vtext{font-weight:300}
        .vtext em{font-weight:600}
        .price td{font-weight:500}
        """,
        hatch=("#0D0D0D", 0.22), hatch2=("#0D0D0D", 0.18), frame=True,
    ),
    "red": dict(
        file="Aricloud_Paleta-Roja.pdf", render="red",
        fonts="family=Antonio:wght@500;700&family=Archivo:wght@400;500;600",
        css="""
        :root{--ground:#F2EFE9;--ink:#0D0D0D;--ink2:#0D0D0D;--rule:#DEA6A3;--accent:#BF0426;--field:#BF0426;--field-ink:#F2EFE9;
              --field2:#DEA6A3;--field2-ink:#0D0D0D;--p2-ground:#BF0426;--p2-ink:#F2EFE9;--p2-ink2:#F2EFE9;--p2-rule:#DEA6A3;--hi:#BF0426;}
        body{font-family:'Archivo',sans-serif}
        .display,.h-sec,.vtext,.big-n,.price td,.opt h3,.point h3,.prices thead th{font-family:'Antonio',sans-serif;text-transform:uppercase}
        .display{font-weight:700;letter-spacing:-0.005em;line-height:1.02}
        .h-sec{font-weight:700;color:var(--accent)}
        .p2 .h-sec{color:var(--p2-ink)}
        .vtext{font-weight:700;color:var(--ink)}
        .vtext em{color:var(--accent)}
        .point h3{font-weight:700;font-size:21px;letter-spacing:0.01em}
        .opt h3{font-weight:700;font-size:28px}
        .prices thead th{font-weight:700;font-size:19px}
        .price td{font-weight:700;font-size:30px}
        .box2 p{font-weight:500}
        """,
        hatch=("#0D0D0D", 0.28), hatch2=("#BF0426", 0.35), frame=False,
        # revisión 2026-11-11 (anotaciones del dueño): despiece abierto sin rótulos, sin letras A–D, Aricloud centrado
        despiece="red-k3", arrow_at={"base": 0.42, "ram": 0.38, "board": 0.42, "lid": 0.5}, tags=False, cloud_center=True, compare=True,
    ),
}

BASE_CSS = """
@page{size:8.5in 11in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact;color:var(--ink);font-size:12px;line-height:1.45;font-kerning:normal}
.page{position:relative;width:816px;height:1056px;overflow:hidden;background:var(--ground);page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto;break-after:auto}
.abs{position:absolute}
.lockup{display:flex;align-items:center;gap:22px;color:var(--ink)}
.lockup .div{width:1.2px;align-self:stretch;background:var(--ink);opacity:.9;margin:6px 0 22px}
.hatch{position:absolute;inset:0;width:100%;height:100%}
.field{position:absolute;overflow:hidden}
.field>*:not(.hatch){position:relative}
.render{position:absolute;display:block}
.leaders{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}
.callout{position:absolute;font-size:10.5px;line-height:16px;white-space:nowrap;text-align:right}
.frame{position:absolute;border:1px solid var(--rule)}
.tag{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border:1.2px solid currentColor;border-radius:50%;font-size:11px;font-weight:600;line-height:1}
"""


def doc_a(theme_key):
    t = THEMES[theme_key]
    hc, ho = t["hatch"]; hc2, ho2 = t["hatch2"]
    pts = "".join(
        f"""<div class="point"><div class="pt-head">{icon(ic, 40)}{f'<span class="tag" aria-hidden="true">{k}</span>' if t.get("tags", True) else ""}</div>
            <h3>{title}</h3><p>{txt}</p></div>""" for k, ic, title, txt in COPY["points"])
    people = "".join(icon("persona", 30) for _ in range(6))
    if t.get("despiece"):
        # despiece sin rótulos, abierto en diagonal para llenar el blanco bajo las cajas 4 y 3
        meta = json.loads((HERE / "assets" / f"despiece-{t['despiece']}.json").read_text())
        # despiece en constelación (boceto del dueño, 2026-11-11): chasis al centro, piezas alrededor
        dh = 394; dw = dh * meta["w"] / meta["h"]; dl = 782 - dw; dt = 622
        callouts = (f'<img class="render" src="../_build/assets/despiece-{t["despiece"]}.png" '
                    f'style="left:{dl:.1f}px;top:{dt:.1f}px;height:{dh:.1f}px;width:{dw:.1f}px" '
                    f'alt="Despiece isométrico de un mini PC: base, chasis, tarjeta madre, memoria, SSD, disipador, ventilador y tapa">')
        # flechas de ensamble: cada pieza apunta hacia el chasis, donde se monta
        c = {k: (dl + v["x"] * dw, dt + v["y"] * dh) for k, v in meta["centers"].items()}
        hub = c["shell"]
        AL = t.get("arrow_len", 26)
        arrows = ""
        for k in ["lid", "ram", "ssd", "board", "fan", "sink", "base"]:
            px, py = c[k]
            ux, uy = hub[0] - px, hub[1] - py
            L = (ux * ux + uy * uy) ** 0.5; ux, uy = ux / L, uy / L
            f = t.get("arrow_at", {}).get(k, 0.5)
            mx, my = px + (hub[0] - px) * f, py + (hub[1] - py) * f
            sx, sy = mx - ux * AL / 2, my - uy * AL / 2
            ex, ey = mx + ux * AL / 2, my + uy * AL / 2
            arrows += f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" marker-end="url(#ah)"/>'
        callouts += (f'<svg class="leaders" width="816" height="1056" viewBox="0 0 816 1056" fill="none" '
                     f'stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="3 3">'
                     f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                     f'<path d="M0 0 L10 5 L0 10" fill="none" stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="none"/></marker></defs>'
                     f'{arrows}</svg>')
    else:
        callouts, rw = leaders(t["render"], left=0, top=630, height=400, label_right=0)  # placeholder to get width
        rleft = 776 - rw
        callouts, _ = leaders(t["render"], left=rleft, top=630, height=400, label_right=rleft - 6)
    if t.get("cloud_center"):
        head1 = (f'<header class="abs p1-head lockup">{arite()}<span class="div"></span></header>'
                 f'<div class="abs p1-head p1-cloud">{aricloud()}</div>')
    else:
        head1 = f'<header class="abs p1-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>'
    bracket = f'<svg class="bracket" viewBox="0 0 150 30" width="150" height="30" fill="none" stroke="currentColor" stroke-width="{SW * 0.32:.2f}" stroke-linecap="butt" aria-hidden="true"><path d="M1.8 30 V1.8 H148.2 V30"/></svg>'
    frames = ""
    if t["frame"]:
        frames = """<div class="frame" style="left:240px;top:312px;width:352px;height:302px"></div>
                    <div class="frame" style="left:606px;top:312px;width:170px;height:302px"></div>"""
    opts = ""
    for num, title, kicker, desc, comps, kind in OPTIONS:
        draw = alzado_minipc("var(--p2-ground)") if kind == "minipc" else alzado_nas("var(--p2-ground)")
        lis = "".join(f"<li>{c}</li>" for c in comps)
        opts += f"""<article class="opt"><div class="draw">{draw}</div><h3>{title}</h3><p class="kicker">{kicker}</p>
                    <p class="desc">{desc}</p><ul>{lis}</ul></article>"""

    css = BASE_CSS + t["css"] + """
    .p1-head{left:40px;top:34px;height:84px}
    .p1-head svg{height:84px;width:auto}
    .p1-cloud{left:508px;transform:translateX(-50%);color:var(--ink)}
    .p1-cloud svg{display:block}
    .p1-rule{left:40px;right:40px;top:132px;height:1.2px;background:var(--ink)}
    .points{left:40px;top:150px;width:176px;display:flex;flex-direction:column;gap:15px}
    .point .pt-head{display:flex;align-items:flex-start;justify-content:space-between;color:var(--ink)}
    .point h3{font-size:18px;line-height:1.1;margin-top:8px;font-weight:500}
    .point p{font-size:11.5px;line-height:1.42;margin-top:4px;color:var(--ink)}
    .box2{left:240px;top:156px;width:536px}
    .box2 p{text-align:justify;text-justify:inter-word;hyphens:auto;font-size:16.5px;line-height:1.42;letter-spacing:-0.005em}
    .box4{left:240px;top:312px;width:352px;height:302px}
    .box4 .stmt{position:absolute;left:18px;top:16px;right:18px;font-size:22.5px;line-height:1.25}
    .box4 .field{left:0;right:0;bottom:0;height:128px;background:var(--field);color:var(--field-ink)}
    .box4 .field .row{display:flex;align-items:flex-end;gap:14px;padding:14px 18px 0}
    .big-n{font-size:64px;line-height:.82;font-weight:500;letter-spacing:-0.03em}
    .box4 .field .lbl{font-size:13px;line-height:1.25;padding-bottom:2px}
    .people{display:flex;gap:4px;padding:12px 14px 0}
    .box3{left:606px;top:312px;width:170px;height:302px}
    .box3 .txt{position:absolute;left:14px;right:14px;top:16px;font-size:15px;line-height:1.36}
    .box3 .field{left:0;right:0;bottom:0;height:128px;background:var(--field2);color:var(--field2-ink);padding:14px}
    .box3 .field .lbl{font-size:12px;line-height:1.3;margin-top:8px}
    .philo{left:40px;top:664px;width:250px}
    .philo h2{font-size:24px;line-height:1.05}
    .philo .bracket{display:block;margin-top:26px;margin-left:2px;color:var(--ink)}
    .vtext{writing-mode:vertical-rl;font-size:41px;line-height:1.06;height:290px;margin-left:24px;margin-top:6px;letter-spacing:0.005em}
    .vtext em{font-style:normal;text-decoration:underline;text-decoration-thickness:3.5px;text-underline-offset:7px;text-decoration-color:var(--hi)}
    .sign{right:40px;bottom:26px;font-size:10.5px;color:var(--ink2)}
    .callout{color:var(--ink)}

    /* hoja comparativa */
    .pc{background:#EEEBE2}
    .pc .p2-head{color:var(--ink)} .pc .lockup .div{background:var(--ink)}
    .pc .p2-rule{background:var(--ink)}
    .cp-title{left:40px;top:112px;width:736px;font-size:46px;line-height:1;color:var(--accent)}
    .cp-lede{left:40px;top:172px;width:560px;font-size:13.5px;line-height:1.45}
    .cp-table{left:40px;top:232px;width:736px}
    .cp-table table{width:100%;border-collapse:collapse;table-layout:fixed}
    .cp-table col.c0{width:292px}
    .cp-table th,.cp-table td{text-align:center;vertical-align:middle;height:45px;border-top:1px solid var(--rule);font-size:12.5px;padding:0 6px}
    .cp-table thead th,.cp-table thead td{border-top:none;height:44px;font-family:'Antonio',sans-serif;text-transform:uppercase;font-weight:700;font-size:15px;line-height:1.05;vertical-align:bottom;padding-bottom:8px}
    .cp-table tbody th{text-align:left;font-weight:400;position:relative;padding-left:32px;line-height:1.25}
    .cp-table .num{position:absolute;left:0;top:50%;transform:translateY(-50%);font-family:'Antonio',sans-serif;font-weight:700;font-size:13px;color:var(--accent)}
    .cp-table .hl{background:var(--accent);color:var(--field-ink);border-top-color:rgba(242,239,233,.35)}
    .cp-table thead th.hl{font-size:19px;padding-top:12px}
    .cp-table td svg{display:block;margin:0 auto}
    .cp-table tr.month td{font-family:'Antonio',sans-serif;font-weight:700;font-size:19px}
    .cp-table tr.month td b{font-weight:700}
    .cp-table tr.month td:not(.hl){color:var(--ink)}
    .cp-bars{left:40px;top:742px;width:420px}
    .cp-bars h3{font-size:22px;line-height:1;margin-bottom:14px}
    .bar{display:grid;grid-template-columns:140px 1fr 44px;align-items:center;height:30px;border-top:1px solid var(--rule)}
    .bar .bn{font-size:12px}
    .bar .bs{display:flex;gap:2px}
    .bar .bs i{flex:1;height:12px;background:transparent;box-shadow:inset 0 0 0 1px var(--rule)}
    .bar .bs i.on{background:var(--ink)}
    .bar.me .bs i.on{background:var(--accent)}
    .bar .bv{text-align:right;font-family:'Antonio',sans-serif;font-weight:700;font-size:18px}
    .bar .bv small{font-size:11px;opacity:.7}
    .bar.me .bn{font-weight:600}
    .cp-claim{left:500px;top:742px;width:276px}
    .cp-claim p{font-size:50px;line-height:.98}
    .cp-claim em{font-style:normal;color:var(--accent)}
    .cp-foot{left:40px;top:966px;width:736px;font-size:10px;line-height:1.5}
    .cp-foot svg{display:inline-block;vertical-align:-4px;width:14px;height:14px;margin:0 3px 0 10px}
    .cp-foot svg:first-child{margin-left:0}

    .cp-title{line-height:.98}
    .cp-lede{top:222px}
    .cp-chart{left:40px;top:262px;width:736px;height:410px}
    .cp-chart text{font-family:'Archivo',sans-serif}
    .cp-chart .ax{font-size:10.5px;fill:#0D0D0D}
    .cp-chart .al{font-family:'Antonio',sans-serif;font-weight:700;text-transform:uppercase;font-size:12px;fill:#0D0D0D;letter-spacing:.02em}
    .cp-chart .al.big{font-size:17px}
    .cp-chart .en{font-size:10px;fill:#0D0D0D}
    .cp-chart .red{fill:#BF0426}
    .cp-stat{left:40px;top:690px;width:736px;display:flex;align-items:center;gap:22px;border-top:1.2px solid var(--ink);padding-top:14px}
    .cp-stat .big{font-size:64px;line-height:.9;color:var(--accent);flex:none}
    .cp-stat .cap{font-size:13.5px;line-height:1.4;max-width:380px}
    .cp-ben{left:40px;top:790px;width:736px}
    .cp-ben h3{font-size:22px;line-height:1;margin-bottom:10px}
    .cp-ben ul{list-style:none;display:grid;grid-template-columns:1fr 1fr;column-gap:28px;grid-auto-flow:column;grid-template-rows:repeat(3,auto)}
    .cp-ben li{font-size:12.5px;line-height:1.3;padding:8px 0 8px 34px;border-top:1px solid var(--rule);position:relative}
    .cp-ben .num{position:absolute;left:0;top:8px;font-family:'Antonio',sans-serif;font-weight:700;font-size:13px;color:var(--accent)}

    .cp-chart{top:268px;height:354px}
    .cp-stats{left:40px;top:632px;width:736px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px;border-top:1.2px solid var(--ink);padding-top:10px}
    .cp-stats .big{font-size:46px;line-height:.95;color:var(--accent)}
    .cp-stats .cap{font-size:11.5px;line-height:1.3;margin-top:4px}
    .cp-risk{left:40px;top:722px;width:736px;height:112px;background:var(--field);color:var(--field-ink);display:flex;align-items:center;gap:28px;padding:0 22px;overflow:hidden}
    .cp-risk>*:not(.hatch){position:relative}
    .cp-risk .rk{font-size:34px;line-height:1;flex:none}
    .cp-risk .rt{font-size:14px;line-height:1.45}
    .cp-risk .rt b{font-weight:600}
    .cp-ben{top:852px}
    .cp-foot{top:968px}
    /* page 2 */
    .p2{background:var(--p2-ground);color:var(--p2-ink)}
    .p2 .lockup{color:var(--p2-ink)} .p2 .lockup .div{background:var(--p2-ink)}
    .p2-head{left:40px;top:34px;height:42px}
    .p2-head svg{height:42px;width:auto}
    .p2-rule{left:40px;right:40px;top:92px;height:1.2px;background:var(--p2-ink)}
    .opts{left:40px;top:116px;width:736px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
    .opt{border:1px solid var(--p2-rule);padding:14px 18px 12px}
    .opt .draw{color:var(--p2-ink);height:96px}
    .opt .draw svg{width:100%;height:96px}
    .opt h3{font-size:22px;line-height:1.1;margin-top:12px;font-weight:500}
    .opt .kicker{font-size:11.5px;color:var(--p2-ink2);margin-top:2px}
    .opt .desc{font-size:12.5px;line-height:1.42;margin-top:8px}
    .opt ul{list-style:none;margin-top:10px}
    .opt li{font-size:11.5px;line-height:1.3;padding:4px 0;border-top:1px solid var(--p2-rule)}
    .includes{left:40px;top:484px;width:736px;font-size:12.5px}
    .p2 .h-sec.big{left:40px;top:526px;font-size:46px;line-height:1}
    .prices-wrap{left:40px;top:588px;width:610px}
    table.prices{width:100%;border-collapse:collapse;color:var(--p2-ink)}
    .prices th,.prices td{text-align:left;padding:7px 10px 7px 0;border-top:1px solid var(--p2-rule);font-size:13px;vertical-align:baseline}
    .prices thead td,.prices thead th{border-top:none}
    .prices thead th{font-size:16px;font-weight:500;padding-bottom:8px}
    .prices tbody th{font-weight:400;color:var(--p2-ink2);width:30%}
    .prices tr.price td{font-size:26px;letter-spacing:-0.01em;padding-top:12px}
    .prices tr.price th{padding-top:16px}
    .note{left:40px;top:872px;width:640px;font-size:10.5px;line-height:1.45;color:var(--p2-ink2)}
    .p2 .vtext{position:absolute;left:auto;right:28px;top:530px;height:380px;font-size:27px;line-height:1.32;letter-spacing:0.14em;margin:0;white-space:nowrap;color:var(--p2-ink)}
    .cta{left:40px;top:930px;width:736px;border-top:1.2px solid var(--p2-ink);padding-top:16px;display:flex;justify-content:space-between;align-items:flex-end}
    .cta p{font-size:15px;line-height:1.3}
    .cta .tel{display:block;font-size:34px;line-height:1.1;margin-top:2px}
    """
    tel = '<a class="display tel" href="tel:+525571962228" style="color:inherit;text-decoration:none">55 7196 2228</a>'
    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Aricloud</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{t['fonts']}&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<section class="page p1">
  {head1}
  <div class="abs p1-rule"></div>
  <div class="abs box2"><p>{COPY['box2']}</p></div>
  <div class="abs points">{pts}</div>
  {frames}
  <div class="abs box4"><p class="stmt display">{COPY['box4']}</p>
    <div class="field">{hatch('h1', hc, ho)}<div class="row"><span class="big-n">1–6</span><span class="lbl">Funciona para<br>1 a 6 personas</span></div><div class="people">{people}</div></div></div>
  <div class="abs box3"><p class="txt">{COPY['box3']}</p>
    <div class="field">{hatch('h2', hc2, ho2)}<span class="big-n">0</span><p class="lbl">suscripciones mensuales. Pagas una vez.</p></div></div>
  <div class="abs philo"><h2 class="h-sec">Nuestra filosofía</h2>{bracket}
    <p class="vtext">Si lo pagas,<br>debe ser<br><em>tuyo</em></p></div>
  {callouts}
  <p class="abs sign">By: Leonardo Aguilar</p>
</section>
{compare_page() if t.get("compare") else ""}<section class="page p2">
  <header class="abs p2-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <div class="abs p2-rule"></div>
  <div class="abs opts">{opts}</div>
  <p class="abs includes">{INCLUDES}</p>
  <h2 class="abs h-sec big display">Precios</h2>
  <div class="abs prices-wrap">{pricing_table()}</div>
  <p class="abs note">Precios en pesos mexicanos (MXN): armado, instalación y configuración incluidos, sin mensualidades. En espejo, cada archivo se guarda en dos discos: si uno falla, sigue en el otro.</p>
  <p class="vtext">“En la era de las<br>suscripciones,<br>somos la resistencia”</p>
  <div class="abs cta"><p>Para más información, agenda con nosotros al{tel}</p>{mono(54)}</div>
</section>
</body></html>"""
    return html


# ------------------------------------------------------------------ PDF 3: "Plano de tu nube"
def floor_plan():
    """Planta arquitectónica de una casa. Every device line stays inside the walls."""
    W = 3.2  # wall stroke
    rooms = """
    <rect x="20" y="20" width="560" height="380" fill="var(--paper)" stroke="var(--ink)" stroke-width="7"/>
    <g stroke="var(--ink)" stroke-width="3.2">
      <path d="M260 20 V150"/><path d="M260 190 V250"/><path d="M20 250 H120"/><path d="M160 250 H330"/>
      <path d="M330 250 V400"/><path d="M420 20 V120"/><path d="M420 160 V250"/><path d="M370 250 H580"/>
      <path d="M460 250 V280"/><path d="M460 320 V400"/>
    </g>
    <g stroke="var(--ink)" stroke-width="1" fill="none">
      <path d="M260 150 A40 40 0 0 1 300 190"/><path d="M260 190 H300" stroke-dasharray="2 3"/>
      <path d="M120 250 A40 40 0 0 0 160 210"/><path d="M160 250 V210" stroke-dasharray="2 3"/>
      <path d="M420 120 A40 40 0 0 1 380 160"/><path d="M420 160 H380" stroke-dasharray="2 3"/>
      <path d="M330 250 A40 40 0 0 1 370 290"/><path d="M370 250 V290" stroke-dasharray="2 3"/>
      <path d="M460 280 A40 40 0 0 1 500 320"/><path d="M460 320 H500" stroke-dasharray="2 3"/>
    </g>
    <g stroke="var(--paper)" stroke-width="9"><path d="M70 20 H190"/><path d="M470 20 H550"/><path d="M20 300 V360"/><path d="M380 400 H440"/><path d="M580 60 V130"/></g>
    <g stroke="var(--ink)" stroke-width="1"><path d="M70 17 H190 M70 23 H190"/><path d="M470 17 H550 M470 23 H550"/><path d="M17 300 V360 M23 300 V360"/><path d="M380 397 H440 M380 403 H440"/><path d="M577 60 V130 M583 60 V130"/></g>
    <g fill="none" stroke="var(--ink)" stroke-width="1.1">
      <rect x="44" y="60" width="150" height="62" rx="6"/><rect x="44" y="60" width="150" height="16" rx="4"/>
      <rect x="92" y="150" width="70" height="44" rx="2"/>
      <rect x="290" y="40" width="110" height="78" rx="4"/><path d="M290 66 H400"/>
      <rect x="440" y="40" width="120" height="96" rx="4"/><rect x="452" y="44" width="44" height="22" rx="3"/><rect x="504" y="44" width="44" height="22" rx="3"/>
      <rect x="40" y="290" width="160" height="22" rx="2"/>
      <rect x="350" y="300" width="96" height="46" rx="2"/>
      <rect x="480" y="340" width="86" height="40" rx="2"/>
    </g>"""
    return rooms


def doc_plano():
    labels = [(140, 238, "Sala"), (340, 238, "Cocina"), (500, 238, "Recámara 1"), (110, 390, "Recámara 2"),
              (395, 390, "Estudio"), (520, 390, "Baño")]
    room_txt = "".join(f'<text x="{x}" y="{y}" text-anchor="middle">{t}</text>' for x, y, t in labels)
    hub = (398, 322)
    devices = [(118, 92, "tele"), (124, 172, "laptop"), (346, 80, "cel"), (498, 92, "cel"), (120, 300, "cel"), (520, 196, "laptop")]
    lines = "".join(f'<path d="M{hub[0]} {hub[1]} L{x} {y}" />' for x, y, _ in devices)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.2"/>'
                   f'<text class="dn" x="{x}" y="{y + 3.6}" text-anchor="middle">{i + 1}</text>' for i, (x, y, _) in enumerate(devices))
    plan = f"""<svg viewBox="0 0 600 420" width="736" aria-label="Planta de una casa: el Aricloud está en el estudio y seis dispositivos se conectan a él sin salir de la casa">
      {floor_plan()}
      <g stroke="var(--accent)" stroke-width="1.6" stroke-dasharray="5 4" fill="none">{lines}</g>
      {dots}
      <rect x="{hub[0] - 22}" y="{hub[1] - 13}" width="44" height="26" rx="3" fill="var(--accent)"/>
      <text class="hubt" x="{hub[0]}" y="{hub[1] + 4}" text-anchor="middle">Aricloud</text>
      <g class="rooms">{room_txt}</g>
    </svg>"""

    def cajetin(sheet, title):
        return f"""<div class="caj"><div class="c1">{mono(30)}<span>Aricloud</span></div>
          <dl><div><dt>Proyecto</dt><dd>{title}</dd></div><div><dt>Cliente</dt><dd>Tu familia</dd></div>
          <div><dt>Capacidad</dt><dd>1 a 6 personas</dd></div><div><dt>Dibujó</dt><dd>Leonardo Aguilar</dd></div>
          <div><dt>Lámina</dt><dd>{sheet} de 2</dd></div></dl></div>"""

    callouts, rw = leaders("plano", left=0, top=0, height=520, label_right=0)
    rleft = 776 - rw
    callouts, _ = leaders("plano", left=rleft, top=104, height=520, label_right=rleft - 8)
    pts = "".join(f"""<div class="pt">{icon(ic, 34)}<h3>{title}</h3><p>{txt}</p></div>""" for k, ic, title, txt in COPY["points"])
    rows = "".join(f"<tr><td>{t[0]}</td><td>{t[1]}</td><td>{t[2]}</td><td>{t[4]}</td><td class='pr'>{t[5]}</td></tr>" for t in TIERS)
    css = BASE_CSS + """
    :root{--ground:#EEEBE2;--paper:#F2EFE9;--ink:#0D0D0D;--ink2:#0D0D0D;--rule:#0D0D0D;--accent:#BF0426;--sand:#BFAA8F}
    body{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 100}
    .wide{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 118;font-weight:700;letter-spacing:-0.015em}
    .p1-head{left:40px;top:34px;height:52px;color:var(--ink)} .p1-head svg{height:52px;width:auto}
    .hl{left:40px;top:116px;width:736px;font-size:45px;line-height:1}
    .hl em{font-style:normal;color:var(--accent)}
    .lede{left:40px;top:236px;width:520px;font-size:16px;line-height:1.45}
    .plan{left:40px;top:330px;width:736px}
    .plan svg .rooms text{font-size:10.5px;fill:var(--ink);letter-spacing:.01em}
    .plan svg .dn{font-size:9px;font-weight:600;fill:var(--ink)}
    .plan svg .hubt{font-size:8.5px;font-weight:600;fill:var(--paper)}
    .legend{left:40px;top:858px;width:400px;font-size:11.5px;line-height:1.45}
    .legend b{font-weight:600}
    .caj{position:absolute;right:40px;bottom:36px;width:300px;border:1.4px solid var(--ink);font-size:10px;display:grid;grid-template-columns:96px 1fr}
    .caj .c1{border-right:1px solid var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;padding:8px;font-weight:600;font-size:11px}
    .caj dl div{display:grid;grid-template-columns:62px 1fr;border-top:1px solid var(--ink);padding:3px 8px}
    .caj dl div:first-child{border-top:none}
    .caj dt{color:var(--ink)} .caj dd{font-weight:600}
    .sheet2 .p1-head{height:40px} .sheet2 .p1-head svg{height:40px}
    .h2{left:40px;top:104px;width:330px;font-size:40px;line-height:1}
    .h2 em{font-style:normal;color:var(--accent)}
    .s2-lede{left:40px;top:238px;width:300px;font-size:14px;line-height:1.45}
    .pts{left:40px;top:340px;width:300px;display:grid;grid-template-columns:1fr 1fr;gap:18px 20px}
    .pt h3{font-size:16px;margin-top:6px;font-weight:600}
    .pt p{font-size:11px;line-height:1.4;margin-top:2px}
    .callout{font-size:10px;color:var(--ink)}
    .sched{left:40px;top:640px;width:736px}
    .sched h3{font-size:24px;line-height:1}
    .sched table{width:100%;border-collapse:collapse;margin-top:12px}
    .sched th,.sched td{text-align:left;font-size:12.5px;padding:7px 8px 7px 0;border-top:1px solid var(--ink)}
    .sched thead th{font-weight:600;border-top:1.4px solid var(--ink);font-size:11px}
    .sched td.pr{font-weight:700;font-size:18px;font-variation-settings:'wdth' 118}
    .sched .fine{font-size:10px;line-height:1.45;margin-top:8px;max-width:620px}
    .philo3{left:40px;top:904px;width:390px}
    .philo3 p{font-size:30px;line-height:1.02}
    .philo3 em{font-style:normal;color:var(--accent)}
    .tel3{left:40px;top:986px;font-size:13px}
    .tel3 a{color:var(--ink);text-decoration:none;font-weight:700;font-size:17px;font-variation-settings:'wdth' 118}
    """
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Aricloud · Plano de tu nube</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<section class="page">
  <header class="abs p1-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <h1 class="abs hl wide">Tu nube cabe en tu casa.<br>Y <em>no sale de ella.</em></h1>
  <p class="abs lede">{COPY['box2']}</p>
  <div class="abs plan">{plan}</div>
  <p class="abs legend"><b>Planta de una casa con Aricloud.</b> El equipo vive en el estudio; los celulares, la computadora y la tele de hasta seis personas se respaldan y ven sus fotos por la red de la casa. {COPY['box4']}</p>
  {cajetin(1, 'Tu nube en casa')}
</section>
<section class="page sheet2">
  <header class="abs p1-head lockup">{arite()}<span class="div"></span>{aricloud()}</header>
  <h2 class="abs h2 wide">Por dentro,<br>pieza por <em>pieza.</em></h2>
  <p class="abs s2-lede">{COPY['box3']} Un mini PC de bajo consumo con discos en espejo: compacto, silencioso y tuyo.</p>
  <div class="abs pts">{pts}</div>
  {callouts}
  <div class="abs sched"><h3 class="wide">Cuadro de precios</h3>
    <table><thead><tr><th>Plan</th><th>Personas</th><th>Espacio</th><th>Fotos de celular, aprox.</th><th>Pago único</th></tr></thead><tbody>{rows}</tbody></table>
    <p class="fine">Pesos mexicanos, opción a la medida (mini PC y bahía de discos) con armado, instalación y configuración incluidos, sin mensualidades. Dos discos en espejo: si uno falla, tus fotos siguen en el otro. También armamos con NAS convencional; el precio depende del gabinete. Tú defines tu producto como quieras.</p></div>
  <div class="abs philo3"><p class="wide">Si lo pagas, debe ser <em>tuyo.</em></p></div>
  <p class="abs tel3">Agenda con nosotros: <a href="tel:+525571962228">55 7196 2228</a></p>
  {cajetin(2, 'Despiece y precios')}
</section>
</body></html>"""


def main():
    docs = {
        "neutral": (doc_a("neutral"), THEMES["neutral"]["file"]),
        "red": (doc_a("red"), THEMES["red"]["file"]),
        "plano": (doc_plano(), "Aricloud_Plano-de-tu-nube.pdf"),
    }
    only = sys.argv[1:] or list(docs)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE.parent))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    port = httpd.server_address[1]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        pg = b.new_page(viewport={"width": 816, "height": 1056})
        pg.on("console", lambda m: print("console:", m.text) if m.type == "error" else None)
        for key in only:
            html, fname = docs[key]
            src = HERE / f"doc-{key}.html"
            src.write_text(html, encoding="utf-8")
            pg.goto(f"http://127.0.0.1:{port}/_build/doc-{key}.html", wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            for i, el in enumerate(pg.query_selector_all(".page")):
                el.screenshot(path=str(PREV / f"{key}-p{i + 1}.png"))
            pg.pdf(path=str(OUT / fname), prefer_css_page_size=True, print_background=True)
            print("ok", fname)
        b.close()
    httpd.shutdown()


if __name__ == "__main__":
    main()
