# Arité · Diseños

Identidad visual y piezas de comunicación de **Arité**, que hace soluciones integrales de servidores caseros y desarrollo de software para pymes. Su producto principal es **AriCloud**, un mini servidor armado a la medida para guardar en casa las fotos y los archivos del cliente, sin depender de Google, Apple o Microsoft.

> Lo que se vende es el **servicio y el ensamblaje del ecosistema**, no el aparato. Nunca se nombran marcas de hardware.
> Filosofía: ***"Si lo pagas, debe ser tuyo."***

---

## Identidad en una página

| | |
|---|---|
| **Logo** | Wordmark "Arité" hecho solo de trazos rectos monolínea con remate cuadrado, más el monograma **AĒ**. **No se modifica.** Archivos en `Logo/`. Se reconstruye en vector en `_build/marks.py`. |
| **Paleta neutra** | `#BFAA8F` `#F2F1F0` `#BFBFBF` `#595959` `#0D0D0D`: lámina técnica, tipografía Jost |
| **Paleta roja** | `#EEEBE2` `#BF0426` `#F2EFE9` `#DEA6A3` `#0D0D0D`: editorial, tipografía Antonio (condensada) + Archivo |
| **Idea rectora** | Lenguaje de **arquitectura aplicado a servidores**: plantas, alzados, isométricos, despieces, rayado (poché) y corchetes |
| **Estilo de imagen** | **Isométrico propio** o animación. Sin fotos copiadas. Personas hechas de volúmenes, sin rasgos |
| **NO hacer** | Tecnología genérica tipo plantilla: neón azul o morado, degradados, circuitos brillantes, robots o mascotas 3D, cerebros IA, hexágonos, partículas |

Detalle completo: [`_contexto/claude-memoria/arite-brand-brief.md`](_contexto/claude-memoria/arite-brand-brief.md) · Investigación de estilos afines: [`_contexto/investigacion-estilos.md`](_contexto/investigacion-estilos.md)

---

## Entregables (`Entregables/`)

| Archivo | Formato | Contenido |
|---|---|---|
| `Aricloud_Paleta-Roja.pdf` | Carta, 3 h. | AriCloud: puntos Confía, Almacena, Sincroniza, Disfruta; despiece del mini PC; opciones, precios y comparativa con la nube de renta |
| `Aricloud_Asi-se-arma-tu-nube_Paleta-Roja.pdf` | Carta, 2 h. | Ecosistema isométrico numerado (mini PC, bahía, discos en espejo, router, celular); velocidad local contra nube (8 min contra 5 h 33 min); discos en espejo; preguntas frecuentes |
| `Arite_Negocios_Paleta-Roja.pdf` | Carta, 2 h. | Oficina isométrica con marcadores A–D (Comparte, Respalda, Accede, Controla); "Ideal para"; "Así trabajamos" en 4 pasos; equipo con rótulos; software a la medida |
| `Arite_Negocios_Paleta-Neutra.pdf` | Carta, 2 h. | El mismo documento en la paleta neutra |
| `Arite_FB_Paleta-Roja.png` | 1080×1350 | "¿Te falta espacio en iCloud para tus fotos?" con el despiece y "Arité lo soluciona" |
| `Arite_FB_Negocio_Paleta-Neutra.png` | 1080×1350 | "Los archivos de tu negocio, en tu negocio": oficina isométrica A–B–C |
| `Arite_FB_Tu-nube-en-casa_Paleta-Roja.png` | 1080×1350 | Cartel "TU NUBE / EN CASA." con el ecosistema isométrico |
| `Arite_FB_Lamina-tecnica_Paleta-Neutra.png` | 1080×1350 | Lámina técnica: alzado, planta e isométrico del AriCloud con cotas en mm y cajetín. "Cabe en un librero." |
| `Arite_FB_Axonometria-noche.png` | 1080×1350 | Axonometría invertida (línea crema sobre negro): "Tus fotos no deberían vivir en la casa de alguien más." |
| `Arite_FB_Ensamble-animado_Paleta-Roja.gif` | 1080×1350, GIF en bucle | El despiece del mini PC se arma pieza por pieza y se vuelve a abrir (unos 5 s) |
| `Arite_FB_Corte-casa_Paleta-Roja.png` | 1080×1350 | **Sin isométrico.** Corte arquitectónico A–A' de una casa con poché: celular, tablet, tele y laptop guardan en el AriCloud del estudio; la nube de alguien más, tachada |
| `Arite_FB_Cifras_Paleta-Neutra.png` | 1080×1350 | **Sin isométrico.** Cartel suizo de retícula: 0 mensualidades · 2 discos en espejo · 1–6 personas |
| `Arite_FB_Pictogramas_Paleta-Roja.png` | 1080×1350 | **Sin isométrico.** 9 pictogramas dibujados con la regla del logo (solo trazos rectos, remate cuadrado): "Tu nube en casa, sin letras chiquitas" |

Contacto que aparece en las piezas: **55 7196 2228**.

---

## Estructura del repositorio

```
Logo/              Logo original (base negro, hairline, monograma AĒ). Intocable.
Colores/           Las dos paletas.
Ideas/             Referencias del brief (lámina técnica, editorial rojo-crema).
  Admitidos/       Referencias del 2026-11-17: se usan como tema y composición, no como técnica.
No realizar/       Ejemplos de lo que la marca NO debe parecer.
Entregables/       Piezas finales (PDF y PNG).
Calculadora imagenes/  Calculadora web (calculadora.html).
_build/            Generadores: todo se produce desde código.
_contexto/         Memoria de la marca e investigación, para recuperar el contexto.
graphify-out/      Grafo de conocimiento del proyecto (graphify).
CLAUDE.md          Instrucciones para Claude Code en este proyecto.
```

### Generadores (`_build/`)

| Script | Qué produce |
|---|---|
| `marks.py` | Logo, AriCloud y monograma en SVG, a partir de la geometría medida del logo; también iconos monolínea y alzados |
| `render.html` + `render3d.py` | Despiece isométrico del mini PC (three.js) → `assets/despiece-*.png` |
| `scenes.html` + `render_scenes.py` | Escenas isométricas: **ecosistema**, **oficina** y **unidad** (equipo solo, con puntos para cotas). Paletas `red`, `neutral` y `night` (línea crema sobre negro) → `assets/scene-*.png` |
| `build_pdf.py` | PDFs de AriCloud (neutra, roja, plano) |
| `build_fb.py` | Primera publicación de Facebook |
| `build_more.py` | Publicaciones 2 y 3, PDF Negocios (neutra y roja) y PDF "Así se arma tu nube" |
| `render_anim.py` | Cuadros de la animación de ensamble (modo `t=` y cámara fija de `render.html`) → `assets/anim/` |
| `build_tanda3.py` | Lámina técnica, axonometría noche y GIF de ensamble (ideas de la investigación de estilos) |
| `build_tanda4.py` | Tres direcciones 2D sin isométrico: corte arquitectónico, cartel suizo de cifras y pictogramas |

**Requisitos:** Python 3.13, `pip install playwright` y Google Chrome instalado en `C:\Program Files\Google\Chrome\Application\chrome.exe`. Las fuentes (Jost, Antonio, Archivo) y three.js se cargan desde internet al generar.

```bash
cd _build
python render_scenes.py            # (opcional) volver a generar las escenas isométricas
python build_more.py               # todas las piezas de la segunda tanda
python build_more.py pdf-negocio-roja   # solo una: fb-negocio | fb-cartel | pdf-negocio | pdf-negocio-roja | pdf-arma
python build_pdf.py red            # PDFs AriCloud: neutral | red | plano
python render_scenes.py unit:neutral eco:night && python render_anim.py red 30 1100
python build_tanda3.py             # fb-lamina | fb-noche | fb-ensamble
python build_tanda4.py             # fb-corte | fb-numeros | fb-pictogramas
```

---

## Recuperar el contexto en otra computadora

1. `git clone https://github.com/leonardoaguilar117/Arit-dise-os.git`
2. Copia `_contexto/claude-memoria/*.md` a `~/.claude/projects/<carpeta-del-proyecto>/memory/` para que Claude recuerde el brief, las paletas y las reglas.
3. Instala graphify y consulta el grafo: `graphify query "<pregunta>"`. Después de cambiar código: `graphify update .`
4. Abre Claude Code en la carpeta. `CLAUDE.md` le da el contexto.

**Respaldo:** al terminar una sesión, dile a Claude **"respalda"**. Actualiza el grafo, copia la memoria, hace commit y push.

---

*Diseño: Leonardo Aguilar · Generado con Claude Code*
