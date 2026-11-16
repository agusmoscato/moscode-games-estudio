# Presentación — INFLATION? What Inflation? (16/11/2026)

Regla de marca: **solo texto + sonido del juego**. Sin voz en off ni cara. Agus aparece solo en pixel art
(`agus-principal.png`) con globos de texto. Primero el juego: nunca un "hola, soy Agus".

> **Estado: BORRADOR.** Lo hice con los momentos que el juego muestra hoy. Falta el momento más importante,
> "los precios se disparan", porque el v2 no lo muestra (ver abajo). Cuando exista, reemplaza los 3,4 s del principio
> y el video queda como está escrito en la columna "Ideal".

## Lo que falta: "los precios se disparan"
- El guion `precio_empanada` del grabador ya no muestra eso: en la grabación de hoy el carrito pasa de **$22,8 a $21**
  (baja) y el juego dice "Inflation held back… Prices x0.92". `hiperinflacion` tampoco: la plata va de $80,01K a $80,3K.
- La causa es el diseño v2, no un bug del director: el freno (`economy_logic.gd`, `brake_s: 12`) no deja que el
  negocio más barato cueste más de 12 s de tu producción, y si el director adelanta la inflación, el juego la corrige
  con deflación. Los guiones de `clip_director.gd` son del diseño anterior.
- Para decidir (Agus): ¿cuál es el momento "inflación" del v2 que tiene que salir en los clips? Opciones:
  (a) un guion nuevo con mucha producción para que el freno deje subir los precios nominales (se ven ceros que crecen,
  pero el chiste de "no me alcanza" no está); (b) mostrar la pared: el cartel "Inflation held back (was heading to X %
  a month)" con una X enorme y la empanada transpirando; (c) apoyarse en la tijera de los ceros, que ya funciona y es
  bien de inflación.

## Vertical, 21,5 s (borrador hecho: `01-presentacion-en.mp4` / `-es.mp4`)
Caja de gancho todo el video. EN: **"Argentina's inflation was so bad I made this"** · ES: **"La inflación argentina me hizo hacer esto"**.

| seg | qué se ve (borrador) | Ideal | globo de Agus EN | globo de Agus ES | sonido |
|---|---|---|---|---|---|
| 0–3,4 | Reforma: el billete viejo "$100,000,000,000" y la tijera corta los ceros | precios disparándose (ver arriba) y después la tijera | — | — | tijera + golpe de la reforma |
| 3,4–8,4 | Pantalla principal: la empanada, la plata, los negocios | igual | "Solo dev from Argentina" | "Dev solo, desde Argentina" | clics, caja registradora |
| 8,4–15,4 | Sobre de figuritas: sale una DORADA | igual | "There's even a sticker album" | "Hay hasta álbum de figuritas" | apertura del sobre, brillo de la dorada |
| 15,4–20 | Zoom a la plata: "$1 T" | precio de un carrito con muchos ceros | "How much is an empanada where you live?" | "¿Cuánto sale una empanada en tu país?" | murmullo de pizarrón |
| 20–21,5 | Cierre de marca: agus-guino, @moscode.games, "Free demo on itch.io" / "Demo gratis en itch.io" | igual | — | — | fade out |

(El globo va sin emoji: la fuente pixel no tiene banderas.)

## Tráiler horizontal (canal de YouTube), 36 s (borrador hecho: `02-trailer-en.mp4` / `-es.mp4`)
Caja de gancho arriba. EN: **"A clicker about Argentine inflation"** · ES: **"Un clicker sobre la inflación argentina"**.

| seg | qué se ve | globo EN | globo ES |
|---|---|---|---|
| 0–4 | La tijera corta los ceros del billete viejo | — | — |
| 4–10 | Pantalla principal, la empanada y los negocios | "I'm a solo dev from Argentina" | "Soy dev solo, de Argentina" |
| 10–16 | El billete volador y el frenesí | "Catch the flying bills" | "Atrapá los billetes que vuelan" |
| 16–23 | Sobre de figuritas con dorada | "Collect 60 stickers" | "Llená el álbum de 60 figuritas" |
| 23–30 | El árbol de 115 nodos | "115 upgrades to beat inflation" | "115 mejoras para ganarle a la inflación" |
| 30–34,5 | La plata en $1 T | "Free demo out now" | "Demo gratis ya disponible" |
| 34,5–36 | Cierre de marca | — | — |

Números verificados en `data/`: 60 figuritas (`stickers.json`) y 114 nodos + el final en `tree.json` (115, como en el README).

## Cuándo usarlo
Fijarlo en el perfil alrededor del día 5 de clips. El tráiler va como tráiler del canal de YouTube (para no suscriptos).
