---
name: arite-respaldo-repo
description: "El proyecto Arité se respalda en GitHub (leonardoaguilar117/Arit-dise-os, rama main); qué hacer cuando el dueño dice \"respalda\""
metadata:
  node_type: memory
  type: reference
  originSessionId: cd2bb6ef-c825-490a-848a-3c900c6a0ba7
  modified: 2026-11-17T18:30:58.421Z
---

La carpeta `Downloads/Arité` es un repo git con remoto `origin` = https://github.com/leonardoaguilar117/Arit-dise-os.git (rama `main`). El primer push se hizo el 2026-11-17.

**Cuando el dueño diga "respalda":**
1. Ejecutar `graphify update .`.
2. Copiar la memoria (`~/.claude/projects/C--Users-leona-Downloads-Arit-/memory/*.md`) a `_contexto/claude-memoria/`.
3. Hacer `git add -A`, luego commit y `git push`.

**Restaurar en otra máquina:** clonar el repo y leer `CLAUDE.md`. Ahí se explica cómo copiar `_contexto/claude-memoria/` de vuelta a la memoria de Claude.

Ver también [[arite-brand-brief]] y [[arite-elementos-admitidos]].
