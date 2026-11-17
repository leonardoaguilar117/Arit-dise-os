"""Brand marks as SVG, rebuilt from the approved logo's measured geometry (stroke 10.6 px on the 960 px master)."""

SW = 11

# Shared "Ari" (from Logo/1. Base negro@2x.png)
ARI = [
    (199, 494.6, 437.5, 352.6),   # A diagonal
    (434.5, 349, 434.5, 630),   # A stem (runs below the baseline)
    (303, 425.5, 439, 425.5),   # A bar
    (475.5, 420, 475.5, 496),  # r stem
    (470, 425.5, 533, 425.5),   # r arm
    (568, 420, 568, 496),  # i
]
ARITE = ARI + [
    (660.5, 327, 660.5, 496),  # t stem
    (604, 425.5, 666, 425.5),      # t bar
    (696, 349, 764, 349),  # macron
    (701.5, 420, 701.5, 496),  # E stem
    (696, 425.5, 764, 425.5),      # E top
    (696, 491, 764, 491),  # E bottom
]


def _c(x):  # open square c, outer-left edge x
    return [(x + 5.3, 420, x + 5.3, 496), (x, 425.5, x + 67, 425.5), (x, 491, x + 67, 491)]


ARICLOUD = ARI + _c(604) + [
    (707.3, 327, 707.3, 496),                                 # l
    (749.3, 420, 749.3, 496), (805.7, 420, 805.7, 496),       # o
    (744, 425.5, 811, 425.5), (744, 491, 811, 491),
    (847.3, 420, 847.3, 496), (903.7, 420, 903.7, 496),       # u
    (842, 491, 909, 491),
] + _c(940) + [(1001.7, 327, 1001.7, 496)]                   # d = c + tall stem

MONO = ARI[:3] + [(470, 349, 537, 349), (475.5, 420, 475.5, 496), (470, 425.5, 537, 425.5), (470, 491, 537, 491)]


def svg(segs, view, height=None, cls="", sw=SW, title=""):
    lines = "".join(f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in segs)
    h = f' height="{height}"' if height else ""
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg class="{cls}" viewBox="{view}"{h} role="img" aria-label="{title}" '
            f'fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="butt">{t}{lines}</svg>')


def arite(height=None, cls="", sw=SW):
    return svg(ARITE, "192 322 578 313", height, cls, sw, "Arité")


def aricloud(height=None, cls="", sw=SW):
    return svg(ARICLOUD, "192 322 820 313", height, cls, sw, "Aricloud")


def mono(height=None, cls="", sw=SW):
    return svg(MONO, "192 322 352 313", height, cls, sw, "AĒ")


# ---- Monoline pictograms in the style of Ideas/ddd.png (48 grid, round caps)
ICON_ATTR = 'viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "confia": """
      <path d="M24 9 C21.3 10.6 19.9 14.4 19.5 19 L18.7 26.4 C18.4 28.8 17 30.7 14.9 32.2 L11.2 35"/>
      <path d="M24 9 C26.7 10.6 28.1 14.4 28.5 19 L29.3 26.4 C29.6 28.8 31 30.7 33.1 32.2 L36.8 35"/>
      <path d="M24 9 V33.5"/>
      <path d="M24 30.5 L21.6 25"/><path d="M24 30.5 L26.4 25"/>
      <path d="M9.2 33 L15 38.8 L11 42.8 L5.2 37 Z"/><path d="M38.8 33 L33 38.8 L37 42.8 L42.8 37 Z"/>
      <path d="M24 33.5 C21 35.2 18 36.6 15 38.8"/><path d="M24 33.5 C27 35.2 30 36.6 33 38.8"/>
      <path d="M24 2.8 V5"/><path d="M17.6 4.6 L18.8 6.4"/><path d="M30.4 4.6 L29.2 6.4"/>""",
    "almacena": """
      <path d="M14.5 35.5 H34.5 C39 35.5 42 32.3 42 28.3 C42 24.4 39.1 21.4 35.3 21.1 C34.4 15.3 29.6 11 23.7 11 C18.6 11 14.3 14.2 12.8 18.9 C8.8 19.6 6 22.9 6 26.9 C6 31.6 9.8 35.5 14.5 35.5 Z"/>
      <path d="M19 28 H29"/><path d="M19 23.5 H29"/>""",
    "sincroniza": """
      <path d="M38.2 19.5 A15 15 0 0 0 11.8 15.6"/><path d="M11 8.8 V16.2 H18.4"/>
      <path d="M9.8 28.5 A15 15 0 0 0 36.2 32.4"/><path d="M37 39.2 V31.8 H29.6"/>""",
    "disfruta": """
      <circle cx="24" cy="24" r="17"/>
      <circle cx="18.2" cy="20.2" r="0.9" fill="currentColor"/><circle cx="29.8" cy="20.2" r="0.9" fill="currentColor"/>
      <path d="M16.5 27.5 C19 33 29 33 31.5 27.5"/>""",
    "persona": """
      <circle cx="24" cy="15" r="5.2"/><path d="M12.5 39 C12.5 30.5 17.6 26.2 24 26.2 C30.4 26.2 35.5 30.5 35.5 39"/>""",
}


def icon(name, size=40, cls="icon"):
    return f'<svg class="{cls}" width="{size}" height="{size}" {ICON_ATTR} aria-hidden="true">{ICONS[name]}</svg>'


# ---- Front elevations (alzados) for the two build options; ground = page ground, ink = currentColor
def alzado_minipc(fill):
    return f"""<svg viewBox="0 0 320 132" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-label="Alzado: mini PC con bahía de dos discos">
  <path d="M132 100 C150 100 150 64 180 64" stroke-dasharray="0" />
  <rect x="20" y="78" width="112" height="40" rx="6" fill="{fill}"/>
  <circle cx="34" cy="98" r="4.2"/><circle cx="48" cy="98" r="1.8"/>
  <rect x="58" y="95" width="12" height="5"/><rect x="76" y="95" width="12" height="5"/><rect x="94" y="96.3" width="9" height="3.4" rx="1.7"/>
  <rect x="180" y="30" width="120" height="88" rx="4" fill="{fill}"/>
  <rect x="192" y="42" width="96" height="28" rx="2"/><rect x="192" y="78" width="96" height="28" rx="2"/>
  <path d="M200 56 H232"/><path d="M200 92 H232"/><circle cx="278" cy="56" r="2.2"/><circle cx="278" cy="92" r="2.2"/>
  <path d="M6 118.8 H314" stroke-width="2.6"/>
</svg>"""


def alzado_nas(fill):
    return f"""<svg viewBox="0 0 320 132" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-label="Alzado: NAS convencional de dos bahías">
  <rect x="96" y="20" width="128" height="98" rx="6" fill="{fill}"/>
  <rect x="108" y="32" width="38" height="74" rx="2"/><rect x="154" y="32" width="38" height="74" rx="2"/>
  <circle cx="127" cy="96" r="3"/><circle cx="173" cy="96" r="3"/>
  <path d="M118 44 H136"/><path d="M164 44 H182"/>
  <circle cx="208" cy="38" r="2.2"/><circle cx="208" cy="50" r="2.2"/><circle cx="208" cy="62" r="2.2"/><circle cx="208" cy="98" r="5"/>
  <path d="M6 118.8 H314" stroke-width="2.6"/>
</svg>"""
