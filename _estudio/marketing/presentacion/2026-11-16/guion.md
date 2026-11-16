# Presentación de moscode.games (16/11/2026)

Video del **estudio**, no de un juego. Se fija arriba en el perfil de TikTok, Instagram y YouTube (en YouTube, el
horizontal como tráiler del canal). Solo texto + sonido de los juegos: sin voz ni cara. Sin temas políticos ni
económicos. Se regenera con `/presentacion` cuando haya un juego nuevo.

Juegos incluidos: INFLATION? What Inflation? (AGUAFIESTAS está en pausa; Plastiquito todavía no existe).
Como hay menos de 3 juegos, van 4 momentos distintos de INFLATION + el cartel "More coming soon…".
Momentos elegidos para que se disfruten sin contexto: la figurita dorada, el billete volador, el árbol comprándose
y la empanada.

Formato vertical **"blur fill"** (MARCA.md): la pantalla del juego entera (1080×608) en el medio, sobre el mismo video
desenfocado y oscurecido, con borde tinta y sombra roja; el cartelito "INFLATION? What Inflation?" justo arriba.
Como en INFLATION la barra de arriba muestra la plata y la inflación del mes, cada corte usa **zoom fijo a la zona de
la acción** (arranca ya con zoom, así nunca se leen): figuritas 1,4×, billete 1,5×, árbol 1,15× (saca la línea "…the
economy"), empanada 1,8× (saca también "Reform: once you earn…"). En la horizontal, recortes 16:9 con el mismo criterio.

## Portada (al fijarlo)
El primer cuadro es casi todo tinta (Agus recién entra con el pop), así que hay que elegir la portada a mano:
- **TikTok e Instagram (vertical): el segundo 3,8** → el `>_` grande con "moscode.games" ya escrito. Es lo que mejor
  dice "estudio" en la grilla del perfil. Alternativa: el **segundo 1,7** (Agus con el globo "I make small, weird
  games." / "Hago juegos chicos y raros."), más cálida.
- **YouTube (horizontal, tráiler del canal)**: no lleva portada propia (se reproduce solo); si la pide, el **segundo 5,7**
  (logo con el nombre escrito).

Sonido: el de cada corte de juego + de fondo, el sonido del árbol de INFLATION al 35 % (fade in y fade out).

## Vertical — 1080×1920, 20 s (`presentacion-vertical-en.mp4` / `-es.mp4`)
| seg | qué se ve | texto EN | texto ES |
|---|---|---|---|
| 0–2 | Agus en pixel art (`agus-principal.png`) aparece con un pop sobre tinta; a los 0,45 s, un globo arriba | I make small, weird games. | Hago juegos chicos y raros. |
| 2–4 | el símbolo `>_` entra con un pop y abajo se escribe letra por letra "moscode.games" (Press Start 2P; "moscode" papel, ".games" amarillo), cursor rojo titilando | moscode.games | moscode.games |
| 4–6 | blur fill: sobre de figuritas, salen las últimas y la **dorada** (cartelito "INFLATION? What Inflation?") | — | — |
| 6–8 | blur fill: el billete volador cruza la lista de negocios | — | — |
| 8–10 | blur fill: el árbol de mejoras, se compran nodos | — | — |
| 10–12 | blur fill: la empanada y la columna de mejoras | — | — |
| 12–14 | cartel sobre tinta con el `>_` grande, el cursor titilando | More coming soon… | Se vienen más… |
| 14–18 | texto grande; la segunda línea aparece a los 1,5 s | 1 dev. 1 mate. → Lots of weird ideas. | 1 dev. 1 mate. → Muchas ideas raras. |
| 18–20 | cierre de MARCA.md: `agus-guino.png`, "@moscode.games" | Follow for the next one | Seguime para el próximo |

## Horizontal — 1920×1080, 34 s (`presentacion-horizontal-en.mp4` / `-es.mp4`)
| seg | qué se ve | texto EN | texto ES |
|---|---|---|---|
| 0–3 | Agus con pop + globo | I make small, weird games. | Hago juegos chicos y raros. |
| 3–6 | `>_` con pop + "moscode.games" que se escribe, cursor rojo | moscode.games | moscode.games |
| 6–10 | sobre de figuritas: se abre y salen las figuritas hasta la dorada | — | — |
| 10–14 | el billete volador y el FRENZY | — | — |
| 14–18 | el árbol de mejoras comprándose | — | — |
| 18–22 | la pantalla principal con la empanada | — | — |
| 22–25 | `>_` titilando | More coming soon… | Se vienen más… |
| 25–30 | dos líneas que aparecen de a una | 1 dev. 1 mate. → Lots of weird ideas. | 1 dev. 1 mate. → Muchas ideas raras. |
| 30–34 | cierre: `agus-guino.png`, "@moscode.games", llamado y link | Follow for the next one · moscode-games.itch.io | Seguime para el próximo · moscode-games.itch.io |

## Para rehacerlo
`py _estudio/tools/clip_tool.py presentacion _estudio/marketing/presentacion/2026-11-16/presentacion.json`
(los momentos, recortes, textos y tiempos están en `presentacion.json`).
