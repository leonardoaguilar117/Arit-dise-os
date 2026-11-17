# Graph Report - .  (2026-11-10)

## Corpus Check
- 19 files · ~119,679 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 148 nodes · 263 edges · 6 communities
- Extraction: 59% EXTRACTED · 41% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.84)
- Token cost: 259,938 input · 0 output

## Community Hubs (Navigation)
- NAS y topologia de red
- Lenguaje editorial arquitectonico
- Mini PC y puertos
- Logo Arite y paleta roja
- Paleta neutra y principios de color
- Anti-referencias (No realizar)

## God Nodes (most connected - your core abstractions)
1. `Anti-reference: generic commercial tech design` - 14 edges
2. `Arité wordmark (approved logo, base version)` - 13 edges
3. `NAS Unit (2-bay, dark grey, centre of diagram)` - 13 edges
4. `Anti-reference screenshot 165625: Canva-style grid of generic AI/tech templates` - 13 edges
5. `AĒ monogram (first and last letters of the wordmark, E tucked against the A stem)` - 11 edges
6. `Candidate palette 1: neutral warm (beige + grays + near-black)` - 10 edges
7. `Candidate palette 2: red + cream + pink + near-black` - 10 edges
8. `Conjunto Residencial Architectural Project Sheet (reference image)` - 10 edges
9. `Mini PC (black square chassis, rounded corners)` - 10 edges
10. `Hairline wordmark variant (same geometry, very thin strokes)` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Two candidate color palettes for Arité (choice pending)` --conceptually_related_to--> `Arité (brand: home-server integral solutions + software development for SMEs)`  [INFERRED]
  Colores/1.png → Logo/1. Base negro@2x.png
- `Candidate palette 1: neutral warm (beige + grays + near-black)` --conceptually_related_to--> `Arité (brand: home-server integral solutions + software development for SMEs)`  [INFERRED]
  Colores/1.png → Logo/1. Base negro@2x.png
- `Candidate palette 2: red + cream + pink + near-black` --conceptually_related_to--> `Arité (brand: home-server integral solutions + software development for SMEs)`  [INFERRED]
  Colores/2.png → Logo/1. Base negro@2x.png
- `Base variant: near-black strokes on white ground` --conceptually_related_to--> `#0D0D0D near-black (primary text / dark ground, palette 1)`  [INFERRED]
  Logo/1. Base negro@2x.png → Colores/1.png
- `Design principle: near-black anchor + light neutral ground + one accent color` --conceptually_related_to--> `Design principle: geometric, technical minimalism (lines, right angles, generous whitespace)`  [INFERRED]
  Colores/1.png → Logo/1. Base negro@2x.png

## Hyperedges (group relationships)
- **Arité logo system: base wordmark, hairline variant and AĒ monogram** — logo_1_base_negro_2x_base_black_on_white_variant, logo_10_hairline_2x_hairline_variant, logo_11_monograma_a_1x_ae_monogram, logo_1_base_negro_2x_arite_wordmark [INFERRED 0.95]
- **Construction traits shared by every Arité logo variant** — logo_1_base_negro_2x_monoline_straight_strokes, logo_1_base_negro_2x_diagonal_a_extended_stem, logo_1_base_negro_2x_macron_over_e, logo_1_base_negro_2x_open_letterforms [INFERRED 0.85]
- **Shared palette skeleton: near-black + off-white/cream grounds across both candidate palettes** — colores_1_0d0d0d, colores_2_0d0d0d, colores_1_f2f1f0, colores_2_f2efe9, colores_2_eeebe2 [INFERRED 0.85]
- **Reference images forming the neutral monochrome/gray infographic style** — ideas_captura_de_pantalla_2026_11_10_165248, ideas_captura_de_pantalla_2026_11_10_165337, ideas_captura_de_pantalla_2026_11_10_165438, ideas_captura_de_pantalla_2026_11_10_165248_neutral_monochrome_style [INFERRED 0.85]
- **Traits and images forming the bold red/cream infographic style** — ideas_captura_de_pantalla_2026_11_10_165819, ideas_captura_de_pantalla_2026_11_10_165844, ideas_captura_de_pantalla_2026_11_10_165819_heavy_condensed_grotesque, ideas_captura_de_pantalla_2026_11_10_165819_red_cream_palette, ideas_captura_de_pantalla_2026_11_10_165819_process_timeline, ideas_captura_de_pantalla_2026_11_10_165248_black_and_white_architecture_photography [INFERRED 0.85]
- **Shared thin-line visual language (drawings, logo, icons, type)** — ideas_captura_de_pantalla_2026_11_10_165248_floor_plans, ideas_captura_de_pantalla_2026_11_10_165248_main_elevation, ideas_captura_de_pantalla_2026_11_10_165337_line_art_house_logo, ideas_captura_de_pantalla_2026_11_10_170307_monoline_icon_style, ideas_captura_de_pantalla_2026_11_10_165337_thin_geometric_sans [INFERRED 0.75]
- **NAS Depicted in Four Visual Styles (flat outline, white line, filled glyph, isometric)** — ideas_1761322267033_nas, ideas_5_9_nas_storage_system, ideas_nas_server_icon_vector_filled_260nw_1541091866_nas_glyph, ideas_nas_nas_unit [INFERRED 0.95]
- **NAS-Centred Office Network (cloud, laptop, desktop, users around one file server)** — ideas_1761322267033_nas, ideas_1761322267033_cloud, ideas_1761322267033_laptop, ideas_1761322267033_desktop, ideas_1761322267033_user_with_folder, ideas_1761322267033_user_with_document, ideas_1761322267033_file_server [EXTRACTED 1.00]
- **Compact Mini PC as Home-Server Hardware (palm-sized, full port set)** — ideas_61ewnxrjyil_mini_pc, ideas_61ewnxrjyil_fits_in_a_hand, ideas_sddefault_mini_pc, ideas_sddefault_rear_ports, ideas_sddefault_fingers_for_scale [INFERRED 0.85]
- **Rejected visual tropes that together form the generic commercial tech look Arité must avoid** — anti_reference_generic_commercial_tech_design, avoid_neon_blue_purple_gradient, avoid_glowing_circuit_board_lines, avoid_3d_robot_mascots, avoid_ai_brain_and_cyborg_head_imagery, avoid_hexagon_grid_patterns, avoid_particle_network_backgrounds, avoid_teal_flat_tech_icon_clutter, avoid_futuristic_display_fonts, avoid_neon_glow_sign_effects, avoid_dense_tech_infographic_layouts, avoid_halftone_pastel_gradient_blobs, avoid_canva_stock_template_look [INFERRED 0.85]

## Communities (6 total, 0 thin omitted)

### Community 0 - "NAS y topologia de red"
Cohesion: 0.09
Nodes (37): NAS File Server Hub-and-Spoke Diagram (flat line illustration), Cloud (dashed link above NAS), Desktop Client with Folder, Two Front Drive Bays, File Server (role label under NAS), Flat Outline Illustration Style (grey + light blue, thick strokes), Hub-and-Spoke Topology (NAS as central hub), Laptop Client with Folder (+29 more)

### Community 1 - "Lenguaje editorial arquitectonico"
Cohesion: 0.10
Nodes (35): Conjunto Residencial Architectural Project Sheet (reference image), Black and White Architecture Photography, Bold Uppercase Sans Heading with Small Uppercase Section Labels, Floor Plans (Plantas) in black line work, Isometric Cutaway View (Vista Isometrica), gray render, Circular Location Map Callout (Ubicacion), Main Elevation Line Drawing (Fachada Principal), Circular Material Swatches (Madera, Concreto, Acero, Piedra) (+27 more)

### Community 2 - "Mini PC y puertos"
Cohesion: 0.12
Nodes (22): Palm-Sized Mini PC Product Photo (held in hand), Red '3 Year Warranty' Shield Badge, Audio Jack (front), Silver Angular Chevron Logo Mark on Lid, Compactness / 'Fits in a Hand' Idea, Front I/O Panel (power button, audio jack, 2x USB-A, USB Type-C), Open Hand Holding the Device, Mini PC (black square chassis, rounded corners) (+14 more)

### Community 3 - "Logo Arite y paleta roja"
Cohesion: 0.19
Nodes (20): #0D0D0D near-black (primary text / dark ground, palette 1), #0D0D0D near-black (primary text / dark ground, palette 2), Logo file: 10. Hairline@2x.png (thin-stroke wordmark on off-white), Hairline stroke weight (approx. 3px on a 960px canvas, about a quarter of base), Hairline wordmark variant (same geometry, very thin strokes), Logo file: 11. Monograma AĒ@1x.png (AĒ monogram reversed on near-black), AĒ monogram (first and last letters of the wordmark, E tucked against the A stem), Design principle: use the monogram where the full wordmark does not fit (+12 more)

### Community 4 - "Paleta neutra y principios de color"
Cohesion: 0.16
Nodes (19): Palette file: Colores/1.png (neutral warm palette screenshot with hex codes), #595959 dark gray (secondary text), #BFAA8F warm beige / sand (accent of palette 1), #BFBFBF light-mid gray (borders, dividers, muted elements), Two candidate color palettes for Arité (choice pending), #F2F1F0 off-white (light background of palette 1), Design principle: near-black anchor + light neutral ground + one accent color, Candidate palette 1: neutral warm (beige + grays + near-black) (+11 more)

### Community 5 - "Anti-referencias (No realizar)"
Cohesion: 0.33
Nodes (15): Anti-reference: generic commercial tech design, AVOID: 3D cartoon robot mascots, AVOID: glowing AI brains, cyborg heads and robotic hands, AVOID: Canva stock-template look (placeholder copy, interchangeable 'AI / Future Technology' headlines), AVOID: dense tall tech infographic layouts (numbered boxes + icons), AVOID: futuristic / sci-fi display fonts, AVOID: glowing circuit-board trace lines, AVOID: pastel halftone-dot gradient blobs (+7 more)

## Knowledge Gaps
- **30 isolated node(s):** `Logo file: 10. Hairline@2x.png (thin-stroke wordmark on off-white)`, `Logo file: 11. Monograma AĒ@1x.png (AĒ monogram reversed on near-black)`, `Palette file: Colores/1.png (neutral warm palette screenshot with hex codes)`, `#595959 dark gray (secondary text)`, `Palette file: Colores/2.png (red / cream / pink palette screenshot with hex codes)` (+25 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mini PC (black square chassis, rounded corners)` connect `Mini PC y puertos` to `NAS y topologia de red`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Anti-reference: generic commercial tech design` (e.g. with `AVOID: 3D cartoon robot mascots` and `AVOID: glowing AI brains, cyborg heads and robotic hands`) actually correct?**
  _`Anti-reference: generic commercial tech design` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Arité wordmark (approved logo, base version)` (e.g. with `AĒ monogram (first and last letters of the wordmark, E tucked against the A stem)` and `Design principle: approved logo must be respected (no redrawing, no alteration)`) actually correct?**
  _`Arité wordmark (approved logo, base version)` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `NAS Unit (2-bay, dark grey, centre of diagram)` (e.g. with `Hub-and-Spoke Topology (NAS as central hub)` and `NAS Storage System (3-bay icon)`) actually correct?**
  _`NAS Unit (2-bay, dark grey, centre of diagram)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `AĒ monogram (first and last letters of the wordmark, E tucked against the A stem)` (e.g. with `Hairline wordmark variant (same geometry, very thin strokes)` and `Arité wordmark (approved logo, base version)`) actually correct?**
  _`AĒ monogram (first and last letters of the wordmark, E tucked against the A stem)` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Logo file: 10. Hairline@2x.png (thin-stroke wordmark on off-white)`, `Logo file: 11. Monograma AĒ@1x.png (AĒ monogram reversed on near-black)`, `Palette file: Colores/1.png (neutral warm palette screenshot with hex codes)` to the rest of the system?**
  _30 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `NAS y topologia de red` be split into smaller, more focused modules?**
  _Cohesion score 0.09309309309309309 - nodes in this community are weakly interconnected._