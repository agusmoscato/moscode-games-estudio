# moscode.games — Estudio

Esta carpeta es el estudio. Cada subcarpeta es el repo de un juego, salvo `_estudio/`, que tiene todo lo compartido.

Soy Agus, dev solo de Argentina. Hago juegos cortos con ideas raras y humor, en Godot 4 (GDScript). No me encasillo en un género. Hablame en español rioplatense.

## Mapa
| Carpeta | slug | Qué es | Estado (16/11/2026) |
|---|---|---|---|
| `_estudio/` | — | Marca, memoria, marketing, herramientas de clips compartidas | activo |
| `INFLATION-What-Inflation-/` | `inflation` | Juego 1: "INFLATION? What Inflation?", clicker casual con renacimientos sobre la inflación argentina (Godot 4.4.1, 2D) | terminando: rediseño v2 en `main` con cambios sin commitear; builds de Windows y demo web exportados; falta playtest humano, subir la demo a itch.io y clips diarios. Clips: `tools/clips/grabar.ps1` |
| `Plastiquito/` (no existe todavía) | `plastiquito` | Juego 2: clicker de reventar plástico de burbujas | por empezar: se crea con `/nuevo-juego Plastiquito` cuando termine lo urgente de INFLATION (no antes) |
| `FiestaFatal/` | `aguafiestas` | AGUAFIESTAS (carpeta FiestaFatal) — en pausa. Party game 3D de deducción social con un traidor oculto (Godot 4.7.2, Jolt) | en pausa desde el 16/11/2026 (Etapa 2 terminada): no se trabaja ni se hacen clips hasta que Agus lo diga. Fuera de la prioridad |

El `slug` es el nombre corto que usan los comandos, `metricas.csv` y `_estudio/marketing/clips/<slug>/`.
Cuando aparezca un juego nuevo, sumalo a esta tabla (usá /nuevo-juego).

## Reglas del estudio
- Todo lo visual y todos los clips siguen `_estudio/brand/MARCA.md`. Leelo antes de hacer cualquier pieza.
- Cada juego tiene su propio `CLAUDE.md` con sus reglas técnicas. Si un juego lo contradice en algo técnico, gana el del juego. En marca, gana MARCA.md.
- Herramientas compartidas (post-proceso de clips con ffmpeg, hojas de contacto, textos) viven en `_estudio/tools/`. Cada juego solo aporta su grabación (Godot `--write-movie` con un bot que juega solo) en `tools/clips/` de su repo.
- Herramientas: `_estudio/tools/clip_tool.py` (edición de marca, EN/ES, `contact.png`) y `_estudio/tools/metricas.py` (ranking y señales). Se corren con `py` (Python de Windows con Pillow) desde esta carpeta. Ver `_estudio/tools/README.md`.
- Salidas de marketing: `_estudio/marketing/clips/<slug>/AAAA-MM-DD/` (videos, `tanda.json`, `captions.md`, `contact.png`). Presentación del estudio: `_estudio/marketing/presentacion/AAAA-MM-DD/`.
- Métricas: `_estudio/marketing/metricas.csv`. Calendario: `_estudio/marketing/calendario.md`. Criterios de "sigo / lo dejo": `_estudio/disenos/validacion.md`.
- No subas nada a redes ni hagas commits o push sin que te lo pida.
- Prioridad actual: 1) INFLATION a itch.io y clips diarios, 2) Steam cuando haya señal, 3) Plastiquito.

## Comandos del estudio
- `/clips <juego>`: graba, edita y escribe los textos de una tanda de clips.
- `/presentacion`: video de presentación del estudio moscode.games (quién es y qué juegos hace), para fijar en los perfiles. Se regenera con cada juego nuevo.
- `/semana`: revisión de los domingos con las métricas y el plan de la semana que viene.
- `/nuevo-juego <nombre>`: prepara un repo nuevo con la marca y lo suma al mapa.
