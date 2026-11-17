# Investigación de estilos afines a Arité

*Investigación hecha el 2026-11-17 para complementar las referencias que dio el dueño (`Ideas/`, `Ideas/Admitidos/`) y la decisión de usar un estilo propio, isométrico o animado, en lugar de fotos.*

## 1. De dónde viene el lenguaje que usamos

| Corriente | Qué es | Qué tomamos para Arité |
|---|---|---|
| **Axonometría arquitectónica** | Familia de proyecciones paralelas (isométrica, dimétrica, trimétrica) que muestra los tres ejes sin punto de fuga. Auguste Choisy la popularizó en 1873 al combinar planta, corte y alzado en un solo dibujo. Después la usaron Theo van Doesburg (De Stijl), Herbert Bayer (Bauhaus) y la oficina de James Stirling. | Presentar el equipo y la casa como un **objeto de arquitectura**: maqueta sobre un zócalo, muros cortados, despiece. |
| **Poché y rayado (hatching)** | Convención de dibujo arquitectónico. El *poché* rellena de oscuro el material que se cortó; el *rayado* identifica qué material es. La regla es **"rayar solo lo que se corta"**. | El zócalo de la maqueta y los cantos de los muros llevan rayado diagonal. Los bloques de datos usan rayado en lugar de degradados. |
| **Isometría en marcas de tecnología** | Microsoft (Azure, Office 365), Slack, Dropbox y Shopify la adoptaron desde mediados de la década de 2010. IBM la documenta en su *Design Language* como su estilo "más espacial", útil para explicar la relación entre personas y tecnología. | Sus reglas técnicas (ver sección 2). Es **también un riesgo**: es tan común que puede verse como plantilla (ver sección 4). |
| **Estilo Tipográfico Internacional (suizo)** | Retícula estricta, sans pesada, mucho contraste y combinaciones como **rojo sobre crema**. Lo representan Josef Müller-Brockmann y Armin Hofmann. | Paleta roja, tipografía condensada pesada (Antonio), palabras gigantes partidas en dos líneas y datos en las esquinas (cartel "Tu nube en casa"). |
| **Despiece de producto (*exploded view*)** | Recurso de manuales y diseño industrial. Teenage Engineering lo ha usado (despiece del OP-1). Su lenguaje gráfico se inspira en hardware antiguo con límites técnicos (Fairlight, IBM) y en el diseño de Ron Cobb para *Alien*. | El despiece del mini PC con flechas de ensamble apoya el mensaje "nosotros lo armamos". |
| **Animación isométrica en bucle** | La composición isométrica se presta a **bucles** y a movimiento por mosaicos. Se entrega en MP4 o Lottie. | Próxima etapa: el disco que entra a la bahía, las piezas que se ensamblan y la línea punteada que viaja de la laptop al servidor. |

## 2. Reglas técnicas confirmadas, y cómo las cumple Arité

Las reglas vienen de la guía isométrica de IBM y de las convenciones de dibujo arquitectónico.

1. **Ángulos fijos.** Todo se ancla a los ejes isométricos, incluidas las curvas. → En Arité, todas las escenas usan la misma cámara ortográfica (dirección 1, 0.82, 1) en `scenes.html` y `render.html`.
2. **Una sola dirección de luz** en toda la pieza y en toda la serie. → En Arité, el sombreador tiene una luz fija (0.28, 1, 0.62) y tres tonos exactos por cara, sin degradados.
3. **Sombras uniformes.** → En Arité no hay sombras proyectadas. El volumen sale solo de los tres tonos y del contorno de tinta.
4. **Jerarquía de grosor de línea**, como en los planos. → En Arité, el contorno de los objetos es de 2.6 px en el render, las guías y los rótulos de 0.9 a 1.2 px, y las líneas punteadas de 1.4 a 2 px.
5. **Proporciones verdaderas.** En arquitectura, la distorsión se lee como error, no como estilo. → En Arité los equipos se modelan a escala real en mm o cm (mini PC de 112 mm, disco de 3.5" de 147 mm).
6. **Rayar solo lo que se corta.** → En Arité, el rayado va en los cantos del zócalo y de los muros, no en las caras visibles de los objetos.

## 3. Ideas para complementar el sistema

- **Cajetín de plano.** Ya existe en "Plano de tu nube". Se puede repetir en cada lámina con número, título y "dibujó", lo que refuerza la idea de serie técnica.
- **Cotas y escala gráfica** en los isométricos (por ejemplo "112 mm" junto al mini PC) para hablar de tamaño sin fotos.
- **Planta, alzado e isométrico del mismo equipo** en una sola lámina, como hacía Choisy al unir vistas.
- **Figuras de escala.** La arquitectura usa siluetas para dar escala. Nuestras personas hechas de volúmenes y sin rasgos cumplen esa función y evitan la mascota 3D.
- **Contraste de fondo invertido.** Dibujo isométrico claro sobre fondo oscuro (#0D0D0D), como las axonometrías blancas sobre negro. Encaja con la paleta y no la rompe.
- **Animación:** bucles de 4 a 6 s. (1) Ensamble del despiece. (2) Disco que entra a su bahía. (3) Fotos que viajan como tarjetas del celular al servidor. (4) Las barras de "8 min contra 5 h 33 min" que se llenan.

## 4. Riesgos y cómo evitarlos

- **La isometría "SaaS" es un cliché.** Personajes sonrientes, plataformas flotantes, azul y morado, brillos. Eso choca con la lista NO del brief.
  → Para distinguirnos usamos el **lenguaje de arquitectura**: maqueta con zócalo, muros cortados, rayado, rótulos con guías, paleta restringida a 5 colores y nada de degradados.
- **Las paletas limitadas funcionan.** Las guías de isometría señalan que la paleta monocroma o limitada da cohesión y minimalismo, lo que confirma la decisión de quedarnos en 5 colores por paleta.
- **No mostrar marcas** de hardware ni de software de terceros en los dibujos. Las pantallas llevan cuadrículas abstractas de "fotos" y "carpetas".

## Fuentes

- IBM Design Language, estilo isométrico: [uso](https://www.ibm.com/design/language/illustration/isometric-style/usage) · [diseño](https://www.ibm.com/design/language/illustration/isometric-style/design) · [producción](https://ibm.com/design/language/illustration/isometric-style/production)
- [Creative Bloq: Isometric drawing, a designer's guide](https://www.creativebloq.com/features/isometric-drawing)
- [Linearity: Understanding isometric illustration](https://www.linearity.io/blog/isometric-illustration/)
- [Inkbot Design: What is isometric design](https://inkbotdesign.com/?p=272998)
- [Graphic Mama: 60+ ejemplos de ilustración isométrica](https://graphicmama.com/blog/isometric-illustrations/)
- [Adobe: Beginner guide to isometric art](https://www.adobe.com/in/creativecloud/roc/blog/design/beginner-guide-to-isometric-art)
- [Illustrarch: What is an architectural axonometric diagram](https://illustrarch.com/articles/architectural-diagrams/27043-what-is-architectural-axonometric-diagram.html)
- [Columbia GSAPP: Orthographic drawing, plans & sections](https://cdp.arch.columbia.edu/smorgasbord/modules/13-arch-drawing/13-1_orthographic-drawing)
- [Designing Buildings Wiki: Poché](https://designingbuildings.co.uk/wiki/Poche)
- [learnarchitecture.net: Architectural hatch patterns](https://learnarchitecture.net/articles/39298-architectural-hatch-patterns.html)
- [U. Waterloo: The AE Drawing Handbook](https://w.tboake.com/2022/THE%20AE%20DRAWING%20HANDBOOK-Sept2022.pdf)
- [TU Delft repository (Choisy y la axonometría)](https://repository.tudelft.nl/file/File_cd512138-5b4d-4aa1-aed6-18ff760be308?preview=1)
- [Drawing Matter Journal No. 3 (Adam Sharr)](https://drawingmatter.org/wp-content/uploads/2026/08/DMJ_No3_AdamSharr.pdf)
- [Poster House: Swiss Style](https://swissgrid.posterhouse.org/)
- [ManyPixels: The evolution of poster styles](https://www.manypixels.co/blog/print-design/evolution-of-poster-design)
- [zZounds blog (despiece del OP-1)](https://blog.zzounds.com/?p=38883) · [Entrevista Mayku × Teenage Engineering (PDF)](https://cdn.shopify.com/s/files/1/0380/5149/files/MaykuMultiplier_TeenageEngineering_Interview.pdf)
- [GarageFarm: Isometric animation](https://garagefarm.net/blog/isometric-animation-breathing-life-into-stylized-worlds)

*Nota: varias fuentes de búsqueda eran directorios comerciales o páginas de plantillas, y se excluyeron. Las afirmaciones sobre IBM, el poché y Choisy vienen de páginas oficiales o académicas.*
