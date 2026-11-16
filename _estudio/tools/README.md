# Herramientas compartidas del estudio

Todo se corre desde la carpeta del estudio (`JUEGOS/`) con el Python de Windows (`py`, que tiene Pillow) y ffmpeg
(`winget install Gyan.FFmpeg`). Las fuentes de la marca están en `_estudio/brand/fuentes/` (OFL).

## clip_tool.py: edición de clips con la marca
Recibe la grabación cruda de cualquier juego y arma los clips según `brand/MARCA.md`: 1080×1920, caja de gancho
(y 150–500), juego en el medio, cierre de 1,5 s con `agus-guino.png` + `@moscode.games` + llamado a la acción,
zonas seguras (nada de texto en los 400 px de abajo ni en los 140 px de la derecha), versión en español (`-es`; inglés solo si se pide con `"idiomas"`)
y `contact.png`.

**Formato vertical por defecto: "blur fill".** Se graba la pantalla entera 16:9 (1920×1080); el juego va completo a
1080×608 en el medio, sobre el mismo video desenfocado y oscurecido, con borde tinta y sombra roja. Opcional por
escena: `"zoom"` (suave desde la vista completa) y `"subtitulo"` abajo del juego. El modo viejo (recortar el juego)
queda con `"modo": "recorte"` o `--modo recorte`. Comparación de los dos: `_estudio/marketing/clips/inflation/_prueba-formato/`.

```
py _estudio/tools/clip_tool.py probar   <tanda.json>   # valida y deja las capas PNG para mirarlas (sin video)
py _estudio/tools/clip_tool.py tanda    <tanda.json>   # arma todos los mp4 + contact.png
py _estudio/tools/clip_tool.py contacto <carpeta>      # rehace la hoja de contacto
```

El formato de `tanda.json` está explicado arriba de todo en `clip_tool.py`. Lo importante:
- `fuente`: la grabación (con `{idioma}` en la ruta, que se cambia por `es`).
- `zoom`: `{"factor": 1.5, "centro": [x, y], "desde": 1.0, "dur": 0.8}` para acercarse a un detalle (`"dur": 0` = fijo).
- `subtitulo`: frase corta abajo del juego (modo blur).
- Solo en modo recorte: `layout` (`vertical`, `cuadrado` 936×936 o `completo`) y `recorte` `[x, y, ancho, alto]`.
- `globos`: Agus en pixel art con un globo de texto (presentación y tráiler; nunca voz ni cara).
- `formato: "horizontal"` arma 1920×1080 (tráiler del canal de YouTube, 30–45 s).
- Si la grabación es más corta que `duracion`, congela el último cuadro (y avisa).

La `tanda.json` de cada tanda queda guardada junto a los clips, así se puede rehacer cambiando un gancho.

### Montaje (clips que atrapan)
Un clip puede llevar `"montaje"` en vez de `"fuente"`: tramos de una sesión larga real (3–10 min del bot), cada uno con
su aceleración (`"vel"`: x2–x8 en lo lento, x1 en los picos), `"golpe"` (flash + refuerzo del sonido del juego al
empezar el tramo), `"zoom"` y `"fuente"` propia (para mezclar sesiones, p. ej. vuelta 1 y vuelta 36). `"contador"`
pone "Minuto N" arriba a la izquierda según el tiempo real de la grabación; `"etiqueta"` lo pisa por tramo
("Vuelta 36 · Hora 2"). La duración del clip es la suma de los tramos. Ejemplo: `_estudio/marketing/clips/inflation/2026-11-16-b/tanda.json`.

### Presentación del estudio
```
py _estudio/tools/clip_tool.py presentacion <presentacion.json>
```
Arma el video del estudio (skill `/presentacion`), vertical y horizontal, en español: Agus con pop + globo, el `>_` que
escribe "moscode.games", cortes de juego con cartelito, "Se vienen más…", dos líneas grandes y el cierre de marca,
con un colchón de sonido de los juegos. La hoja de contacto muestra un cuadro por sección. Formato del JSON en
`cmd_presentacion()`; ejemplo en `_estudio/marketing/presentacion/2026-11-16/presentacion.json`.

## metricas.py: ranking y señales
```
py _estudio/tools/metricas.py pendientes [--juego inflation]   # qué números faltan cargar
py _estudio/tools/metricas.py ranking    [--juego inflation]   # ranking por (compartidos+guardados + comentarios) cada 1.000 vistas,
                                                               # señal de Steam y "sigo / lo dejo" (disenos/validacion.md)
```

## Qué aporta cada juego
Solo la grabación: un script en `tools/clips/` de su repo que hace jugar al juego solo con el Movie Maker de Godot
(`--write-movie`) y deja mp4 crudos (sin carteles propios, con la interfaz en español). Ver el
`tools/clips/` de cada juego.
