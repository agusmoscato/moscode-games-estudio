---
name: presentacion
description: Genera el video de presentación del ESTUDIO moscode.games (quién es y qué tipo de juegos hace), vertical y horizontal, EN y ES, para fijar arriba en el perfil de TikTok, Instagram y YouTube. Se regenera cada vez que el estudio tiene un juego nuevo. Usar con /presentacion o cuando Agus pide el video de presentación del estudio o el tráiler del canal.
---

# /presentacion

## Objetivo
Un video que diga **quién es moscode.games y qué tipo de juegos hace**, para fijarlo arriba en el perfil de TikTok,
Instagram y YouTube. Es del estudio, no de un juego. Se regenera cada vez que el estudio tiene un juego nuevo.
Hablale a Agus en español rioplatense. **No publica nada**, sin commits ni push.

## Reglas
- Solo texto + música/sonidos de los juegos. Sin voz ni cara (como todo lo demás).
- Respetar `_estudio/brand/MARCA.md` (colores, tipografías, zonas seguras, cierre).
- Inglés como versión principal + versión en español (voseo).
- **Ningún tema político ni económico**: no se menciona la inflación ni el tema de ningún juego. En los cortes de
  juego, elegí momentos que se disfruten sin contexto (algo que explota, que brilla, que se abre, que vuela) y evitá
  los que son "sobre el tema" (en INFLATION: nada de la tijera de ceros, la reforma, carteles de inflación ni montos).

## Formato de los cortes de juego
Vertical en **"blur fill"** (MARCA.md, por defecto en la herramienta): la pantalla del juego **entera** en 16:9,
1080×608 en el medio, sobre el mismo video desenfocado y oscurecido, con borde tinta y sombra roja; el cartelito con
el nombre del juego va justo arriba. No se recorta la barra de arriba del juego **salvo** que se vean montos o textos
del tema (inflación, plata, economía): en ese caso, `"zoom"` a la zona de la acción (con `"dur": 0` para que arranque
ya con zoom y nunca se lean). Horizontal: pantalla entera, o `"recorte"` 16:9 por el mismo motivo.

## Estructura vertical (1080×1920, 15–20 s)
| seg | qué pasa | texto EN | texto ES |
|---|---|---|---|
| 0–2 | `brand/personaje/agus-principal.png` aparece con un "pop" + globo de texto | I make small, weird games. | Hago juegos chicos y raros. |
| 2–4 | el logo `>_` se "escribe" como en una terminal hasta formar "moscode.games" (Press Start 2P), cursor rojo titilando | moscode.games | moscode.games |
| 4–14 | cortes rápidos (1,5–2 s c/u) del mejor momento de cada juego del estudio que NO esté en pausa, con el nombre del juego en un cartelito | (nombre del juego) | (nombre del juego) |
| | si hay menos de 3 juegos: momentos distintos del mismo juego y al final un cartel sobre tinta con el `>_` titilando | More coming soon… | Se vienen más… |
| 14–18 | texto grande en dos líneas que aparecen de a una | 1 dev. 1 mate. → Lots of weird ideas. | 1 dev. 1 mate. → Muchas ideas raras. |
| últimos 2 | cierre de MARCA.md: `agus-guino.png`, "@moscode.games" | Follow for the next one | Seguime para el próximo |

## Versión horizontal (1920×1080, 30–45 s)
Tráiler del canal de YouTube: misma estructura, con más tiempo para los juegos (3–4 s cada uno) y al final el link de
itch.io (`moscode-games.itch.io`).

## Cómo se hace
1. **Juegos**: tabla "Mapa" del `CLAUDE.md` del estudio; solo los que no están en pausa ni "por empezar" sin
   carpeta. Para cada uno, su `tools/clips/README.md` (grabador, recortes que funcionan) y las métricas
   (`py _estudio/tools/metricas.py ranking --juego <slug>`: si un momento anduvo bien en clips, va primero).
2. **Grabar** lo que falte con el grabador de cada juego, siempre la pantalla entera en 16:9 (1920×1080; sirve para
   las dos versiones). Mirá cuadros con ffmpeg + Read antes de elegir `inicio` y `zoom`/`recorte`: el momento tiene
   que verse en el primer medio segundo del corte, y no se tiene que leer ningún monto ni texto del tema.
3. **Salida**: `_estudio/marketing/presentacion/AAAA-MM-DD/`. Escribí ahí `presentacion.json` (formato en el
   encabezado de `_estudio/tools/clip_tool.py`, subcomando `presentacion`) y corré:
   `py _estudio/tools/clip_tool.py presentacion _estudio/marketing/presentacion/AAAA-MM-DD/presentacion.json`
   Genera `presentacion-vertical-en.mp4`, `-es.mp4`, `presentacion-horizontal-en.mp4`, `-es.mp4` y `contact.png`.
   Si a la herramienta le falta algo, agregalo en `clip_tool.py` (no hagas videos a mano).
4. Mirá `contact.png` con Read y corregí lo que se vea mal (texto en zonas seguras, corte vacío, momento que no se
   entiende sin contexto).
5. **`guion.md`**: segundo a segundo, lo que se ve y el texto en los dos idiomas, para las dos versiones, y **qué
   segundo elegir como portada** al fijarlo (el primer cuadro es casi todo tinta por el pop).
6. Las presentaciones viejas quedan en su carpeta con fecha; si una ya no sirve, movela a
   `_estudio/marketing/presentacion/_descartado/`.

## Cierre
Mostrale a Agus `contact.png`, los archivos y el guion. Recordale fijarlo arriba en los tres perfiles (en YouTube,
el horizontal como tráiler del canal) y regenerarlo con `/presentacion` cuando salga un juego nuevo.
