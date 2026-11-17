# Arité — contexto del proyecto

Marca de servidores caseros (AriCloud) y desarrollo de software para pymes.

## Antes de diseñar
- Lee `_contexto/claude-memoria/` (brief de marca, elementos admitidos). Si la memoria local de Claude se perdió, copia esos archivos a
  `~/.claude/projects/<carpeta-del-proyecto>/memory/`.
- Lee `_contexto/investigacion-estilos.md` (linaje axonométrico, reglas isométricas, poché, riesgos de cliché).
- El logo no se toca; solo se usan las dos paletas (neutra y roja); el estilo propio es isométrico o animado, nunca fotos copiadas.

## Estructura
- `Logo/`, `Colores/`, `Ideas/`, `No realizar/`: brief original del dueño. `Ideas/Admitidos/`: referencias del 2026-11-17.
- `Entregables/`: PDFs y publicaciones finales.
- `_build/`: generadores (Python + Playwright + Chrome).
  - `render3d.py` + `render.html`: despiece del mini PC → `assets/despiece-*.png`
  - `render_scenes.py` + `scenes.html`: escenas isométricas (ecosistema, oficina) → `assets/scene-*.png`
  - `build_pdf.py`: PDFs AriCloud (neutra, roja, plano). `build_fb.py`: primera publicación FB.
  - `build_more.py`: publicaciones FB 2 y 3, PDF Negocios (neutra/roja), PDF "Así se arma tu nube".

## graphify
Este proyecto tiene un grafo de conocimiento en `graphify-out/`.
- Para preguntas sobre el proyecto, primero `graphify query "<pregunta>"`; `graphify path "<A>" "<B>"` y `graphify explain "<concepto>"`.
- Tras modificar código, `graphify update .`.
