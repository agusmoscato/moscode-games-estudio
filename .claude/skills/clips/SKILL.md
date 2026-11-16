---
name: clips
description: Graba, edita y escribe los textos de una tanda de clips de marketing (TikTok, Shorts, Reels) de un juego del estudio moscode.games. Usar cuando Agus escribe /clips <juego> o pide clips, videos cortos o una tanda para redes de un juego.
---

# /clips <juego>

Arma una tanda de clips de un juego: 10 ideas, grabación con el bot del juego, edición de marca en inglés y español,
textos de publicación, filas en métricas y los 3 que conviene subir primero. **Nunca publica nada.**
Hablale a Agus en español rioplatense.

## 0. Qué juego
- El argumento es el slug o el nombre del juego. Buscalo en la tabla "Mapa" de `CLAUDE.md` (columna `slug`).
  Si no hay argumento, usá el primero de la prioridad actual del `CLAUDE.md` del estudio.
- Si el juego figura **en pausa** en el Mapa (hoy: AGUAFIESTAS), no hagas clips: decíselo a Agus y pará.
- Los clips son **solo texto + sonido del juego**: nada de voz en off ni cara (MARCA.md).
- Si el juego no tiene `tools/clips/` con un grabador, no inventes uno a ciegas: decíselo a Agus y ofrecé armarlo
  (siguiendo el `CLAUDE.md` del juego) antes de seguir.

## 1. Leer antes de proponer
1. `_estudio/brand/MARCA.md` (reglas de clips, voz y textos; manda sobre todo lo visual).
2. El `CLAUDE.md` y el `README` del juego, y `tools/clips/README.md` del juego (qué guiones hay, cuánto dura cada uno,
   qué recorte conviene, en qué idiomas graba).
3. Métricas: `py _estudio/tools/metricas.py ranking --juego <slug>`. Lo que mejor anduvo (compartidos+guardados y
   comentarios cada 1.000 vistas) se repite con variantes; lo que no anduvo, no.
4. Tandas anteriores en `_estudio/marketing/clips/<slug>/*/captions.md`, para no repetir ganchos.

## 2. Proponer 10 ideas
Una tabla con: nº, momento fuerte (lo más impactante en pantalla en el segundo 0), guion del grabador que lo muestra
(existente o nuevo), gancho EN y gancho ES (máx. 8 palabras cada uno; ES con voseo; números grandes y concretos),
y por qué puede funcionar (con el dato de métricas si lo hay). Fórmula: se entiende en 3 segundos, da gusto mirarlo,
multiplica un elemento. Nada de política partidaria.

Después de mostrar la tabla, seguí con la grabación sin esperar, salvo que Agus haya pedido revisar antes.
- Las ideas que usan guiones existentes se graban directo (pueden variar tramo, recorte o gancho).
- Si una idea necesita un guion nuevo en el juego, eso es código del juego: agregalo solo si es chico y sigue el
  `CLAUDE.md` del juego, y si el archivo no tiene cambios sin commitear de Agus (`git status`). Si no, reemplazá la
  idea por una variante de un guion existente y anotalo como pendiente.

## 3. Grabar
Grabá **siempre la pantalla entera en 16:9 (1920×1080)**: el formato vertical es "blur fill" (MARCA.md) y no se
recorta la interfaz. Corré el grabador del juego (`tools/clips/` de su repo), por ejemplo en INFLATION:
`powershell -NoProfile -ExecutionPolicy Bypass -File INFLATION-What-Inflation-/tools/clips/grabar.ps1 -Clips tijera,billete -Size 1920x1080`
Deja los crudos en `export/clips_crudos/<guion>_<idioma>_1920x1080.mp4` del repo. Abre una ventana de Godot mientras
graba (avisale a Agus que no la tape). Si un guion falla 8 veces, seguí con el resto y anotalo.

## 4. Editar con la herramienta compartida
1. Carpeta de salida: `_estudio/marketing/clips/<slug>/AAAA-MM-DD/` (fecha de hoy; si ya existe, sumá `-b`).
2. Escribí ahí `tanda.json` (formato en el encabezado de `_estudio/tools/clip_tool.py`): `titulo` = nombre del juego
   corto en mayúsculas, `cta` = "Free demo on itch.io" / "Demo gratis en itch.io" (o "Wishlist on Steam" /
   "Agregalo a tu lista en Steam" cuando haya página), duración 15–25 s. Formato vertical **"blur fill"** (por
   defecto, no hace falta ponerlo): pantalla entera 1080×608 en el medio sobre el mismo video desenfocado.
   - Si un detalle se ve chico, usá `"zoom"` en esa escena (1,3×–1,5×, suave desde la vista completa:
     `{"factor": 1.5, "centro": [x, y], "desde": 1.0, "dur": 0.8}` en px de la grabación). Por defecto, sin zoom.
   - `"subtitulo"` opcional abajo del juego (una frase corta EN/ES que sume, no que repita el gancho).
   - El modo viejo de recorte vertical solo si Agus lo pide (`"modo": "recorte"` o `--modo recorte`).
   Nombres de archivo: `NN-nombre` en minúscula con guiones (el `NN` es el nº de la idea).
3. `py _estudio/tools/clip_tool.py probar <tanda.json>` y mirá con Read 2 o 3 PNG de `_capas/` (gancho y cierre):
   que el texto entre, que no tape lo importante, que respete las zonas seguras. Corregí ganchos largos.
4. `py _estudio/tools/clip_tool.py tanda <tanda.json>`. Revisá los avisos (duración, ganchos achicados, sin sonido).
5. Mirá `contact.png` con Read. Si algo se ve mal (pantalla vacía, momento fuerte que no está en el segundo 0,
   detalle ilegible), ajustá `inicio`/`zoom`/`subtitulo` y volvé a correr solo ese clip.

## 5. Textos: `captions.md`
En la misma carpeta, para cada clip y según MARCA.md:
- **TikTok / Reels**: 1 línea con el gancho + una pregunta que invite a comentar + 3–5 hashtags
  (#indiegame #gamedev #godot + los del género del juego + el del juego).
- **YouTube Shorts**: título de 60 caracteres o menos + la misma descripción.
- En inglés y en español (ES con voseo).
Arriba de todo, una tabla con nº, archivo EN, archivo ES, gancho y duración.

## 6. Métricas y calendario
- Sumá a `_estudio/marketing/metricas.csv` una fila por clip en inglés y por red (`tiktok`, `shorts`, `reels`):
  `fecha` = día planeado de publicación, `juego` = slug, `clip` = `AAAA-MM-DD/NN-nombre-en`, números vacíos,
  `notas` = `pendiente de subir`. No toques las filas que ya están.
- Recomendá **cuáles 3 subir primero** y por qué (gancho más claro en 3 s, momento más fuerte, lo que dicen las
  métricas). Sumalos a `_estudio/marketing/calendario.md` en los próximos 3 días libres, a las 19–21 h.

## 7. Cierre
Mostrale a Agus: la carpeta, la tabla de clips, los 3 recomendados con el orden, los avisos de la herramienta, y
cualquier guion nuevo o cambio que hayas hecho en el juego. Recordale que él sube a mano. Sin commits ni push.
