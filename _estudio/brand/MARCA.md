# moscode.games — Kit de marca y clips

Este archivo es para Claude Code. Todo lo visual y todos los clips de este juego siguen estas reglas.
Identidad completa (diseño): https://claude.ai/artifact/Dr2GBS8A7vcdaEPV22A9uo

## Estudio
- Nombre: **moscode.games** (siempre en minúscula).
- Estudio indie de Argentina. Juegos cortos, con una idea rara y humor, que dan gusto jugar. No se encasilla en un género: puede ser incremental, simulador, arcade, puzzle, roguelike o lo que pida la idea. Lema: "Small, weird games that feel great to play." / "Juegos chicos que dan gusto tocar."
- Cuentas:
  - TikTok: @moscode.games
  - Instagram: @moscode.games
  - YouTube: @moscode.games
  - itch.io: moscode-games.itch.io
  - Reddit: u/moscodegames
  - Mail del estudio: (completar)

## Colores
| Nombre | Hex | Uso |
|---|---|---|
| Tinta | #18191C | bordes, texto, fondos oscuros |
| Papel | #F7F6F2 | fondo claro, texto sobre tinta |
| Amarillo moneda | #FFC21A | rellenos y cajas de texto; encima siempre texto tinta |
| Rojo remarcado | #C8321F | acentos, ".games", sombras duras; texto rojo solo grande (≥24 px) |

Sin degradados ni esquinas redondas. Bordes de 4–6 px en tinta y sombra dura desplazada (6–10 px) en tinta o rojo.

## Tipografías (Google Fonts, licencia OFL)
- **Press Start 2P**: logo y títulos cortos (máx. 4–5 palabras).
- **Pixelify Sans** (400 y 700): titulares de clips, números y textos.

## Logo
- `logo/`: el símbolo `>_` en píxeles (`>` amarillo, cursor rojo, fondo tinta). Escalar SIEMPRE con nearest neighbor y en múltiplos de 16 px.
- `logo/avatar-800.png`: foto de perfil para todas las redes.
- Wordmark: "moscode" + ".games" (".games" en rojo sobre claro, en amarillo sobre tinta), en Press Start 2P.

## Personaje
- `personaje/`: Agus en pixel art con un mate. Fondo amarillo incluido.
  - `agus-principal.png`: uso general (de frente, sonriendo).
  - `agus-guino.png`: cierre de los clips.
  - `agus-anteojos.png`: para anuncios, récords y momentos de "flex".
  - `agus-sonrisa.png`: tres cuartos, para devlogs.
- Escalar con nearest neighbor. No redibujar ni cambiar colores.

## Especificación de clips (TikTok, YouTube Shorts, Instagram Reels)
- **Solo español** (desde el 16/11/2026): clips, presentación, captions, guiones y textos van solo en español (voseo). No se hacen versiones en inglés.
- **Algo tiene que cambiar**: Cada clip tiene que tener algo que CAMBIE o CREZCA en pantalla (antes/después, consecuencia, escalada o remate). Una acción repetida sin cambio no es un clip.
- **Solo texto + sonido del juego**: sin voz en off y sin cara a cámara, en todos los clips, la presentación y los tráileres. Agus aparece solo en pixel art (`personaje/`), con globos de texto o en el cierre.
- **Presentación**: la presentación es del estudio moscode.games, no de un juego, y no menciona la inflación ni temas de los juegos. Se regenera con cada juego nuevo (`/presentacion`).
- Formato: MP4 H.264, 1080×1920, 30 o 60 fps, 15–25 s, sonido del juego.
- **Segundo 0**: el momento más impactante del juego ya en pantalla. Nada de intros ni logos al principio.
- **Gancho arriba** (y 150–500 px): caja amarilla con borde papel de 6 px y sombra roja de 10 px; adentro el nombre del juego en Press Start 2P 22 px y el gancho en Pixelify Sans 700 de 76 px, máximo 8 palabras.
- **Formato vertical "blur fill"** (por defecto en todos los videos verticales: clips y presentación). Los juegos son de PC y recortados se ven raros:
  - Se graba siempre la pantalla del juego **entera en 16:9 (1920×1080)**, sin recortar la interfaz.
  - **Fondo**: el mismo video llenando 1080×1920, recortado al centro, con desenfoque fuerte y oscurecido un 30–40 % para que el texto se lea.
  - **Frente**: el video completo a 1080 de ancho (1080×608), centrado verticalmente (y 656–1264), con borde fino tinta de 4 px y sombra dura roja.
  - **Arriba del juego**: la caja de gancho. **Abajo del juego**: espacio para un subtítulo corto opcional (Pixelify Sans 700, papel con sombra tinta).
  - **Zoom por escena** (opcional, por defecto sin zoom): si un detalle se ve chico, el frente puede ser un recorte 16:9 de una zona del juego (1,3×–1,5×), yendo suave de la vista completa al zoom. También se usa para dejar afuera montos o textos que no van (por ejemplo, en la presentación del estudio).
  - El modo viejo de recorte vertical (juego recortado en un área de 936×936 o vertical, fondo tinta) queda como opción (`--modo recorte`), no por defecto.
- **Cierre (últimos 1,5 s)**: `personaje/agus-guino.png` a 96–160 px, "@moscode.games" en Press Start 2P y el llamado a la acción en Pixelify Sans 700 amarillo ("Demo gratis en itch.io" / "Agregalo a tu lista en Steam" cuando haya página).
- **Zonas seguras**: nada de texto en los 400 px de abajo ni en los 140 px de la derecha (la interfaz de las apps los tapa).
- Fondo de cierres y carteles: tinta #18191C.
- Salida: `clips/AAAA-MM-DD/NN-nombre-es.mp4`, más una hoja de contacto (`contact.png`) para revisar de un vistazo.

## Reglas de un clip que atrapa (todas las tandas)
1. **Segundo 0 en el pico**: arranca en el medio de la acción, con la pantalla ya llena (números volando, partículas, algo moviéndose). Nunca una pantalla quieta o casi vacía.
2. **Algo nuevo cada 1,5–3 s ("beat")**: un negocio nuevo, un número que salta, un evento, una explosión, un cartel del juego. Más de 3 s sin un cambio visible → se corta.
3. **Escalada**: empieza chico y termina ENORME. Los números crecen x100 o x1000 en el clip (de $500 a $50 millones, de 1 negocio a 10, de 1 billete a una lluvia). El final siempre es lo más grande del video.
4. **Tensión**: en algún momento casi pierde (la inflación lo está comiendo, el pizarrón en rojo, la plata no alcanza) y se salva justo con una buena jugada.
5. **Montaje, no tiempo real**: se graban sesiones largas (3–10 min de juego real con el bot) y se comprimen en ~23 s con cortes rápidos y aceleraciones (x2–x8 en los tramos lentos). Contador chico en una esquina ("Día 1 → Día 90", "Minuto 1 → Minuto 30") para que se entienda que pasó tiempo.
6. **Remate o loop**: el último segundo es el pico (el número más grande, la dorada, la tijera) o empalma con el principio para que se vea dos veces.
7. **El gancho promete la escalada o la tensión**, no la acción repetida ("De vender empanadas a imprimir billetes", "Casi me funde la inflación", "¿Cuánto podés juntar antes de que te coma la inflación?").
8. **Preguntas**: al menos 3 clips por tanda terminan (gancho o caption) con una pregunta que invite a comentar ("¿Qué hubieras comprado vos?", "¿Hasta dónde llegás?").
9. **Juice al máximo**: al grabar, las opciones más altas del juego (partículas, sacudón, calidad, volumen de efectos).

**Formatos** (al menos 5 distintos por tanda): progresión comprimida (una partida entera en 23 s) · casi pierdo (se dispara, pizarrón rojo, remontada) · decisión con consecuencia (elige y se ve el resultado grande) · antes / después (minuto 1 vs. minuto 30, o antes y después de la tijera) · lluvia (abundancia exagerada que termina en algo enorme) · error que da bronca (una jugada medio mala a propósito que se paga, para que comenten "yo lo hacía mejor") · suspenso con remate (sobres o raspaditas acelerados: solo la tensión y el premio).

**Revisión**: cada clip se puntúa del 1 al 10 con estas reglas; menos de 7 se rehace o se descarta. La hoja de contacto muestra 6 cuadros por clip para ver el ritmo.

## Textos de publicación (`clips/AAAA-MM-DD/captions.md`)
Para cada clip:
- TikTok / Reels: 1 línea con gancho + pregunta para que comenten + 3–5 hashtags (#indiegame #gamedev #godot + los del género de ESTE juego + el del juego).
- YouTube Shorts: título ≤ 60 caracteres + misma descripción.
- Solo en español.

## Reglas de voz
- Humor argentino que se entienda afuera. Voseo en español.
- Números grandes y concretos ("x10.000", "$1.250.000").
- Nunca política partidaria.
