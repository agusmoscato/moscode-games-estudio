# Guía: crear la página de INFLATION en itch.io (demo web)

Archivos de esta carpeta (`_estudio/marketing/itch/inflation/`):
| archivo | para qué |
|---|---|
| `InflationWhatInflation_web_demo.zip` | el juego (11,3 MB, `index.html` en la raíz). No está en git: se regenera (ver abajo) |
| `portada-630x500.png` | Cover image |
| `capturas/01-remarcar.png` … `05-hiperinflacion.png` | Screenshots (1920×1080) |
| `remarcar.gif` | GIF para la descripción (640×360, 7 s, 1,8 MB) |
| `textos.md` | título, frase corta, descripción, etiquetas y clasificación |
| `portada.py` | rehace la portada desde una captura |

## Paso a paso (https://itch.io/game/new)
1. **Title:** `INFLATION? What Inflation? (Demo)` (de `textos.md`).
2. **Project URL:** `inflation-what-inflation-demo` (sin signos de pregunta).
3. **Short description or tagline:** la frase corta de `textos.md`.
4. **Classification:** `Games`.
5. **Kind of project:** `HTML`.
6. **Release status:** `In development`.
7. **Pricing:** `No payments`.
8. **Uploads → Upload files:** subí `InflationWhatInflation_web_demo.zip`. Cuando termine, marcá
   **"This file will be played in the browser"**.
9. **Embed options** (aparecen al marcar lo anterior):
   - **Viewport dimensions:** `1280` × `720` (el juego es 16:9 y escala solo).
   - **"Fullscreen button":** activado (botón para jugar en pantalla completa).
   - **"Click to launch in fullscreen":** desactivado, así se juega directo en la página.
   - **"Mobile friendly":** solo si lo probaste en el celular.
   - **No** marques "SharedArrayBuffer support" (el build es sin threads; no lo necesita).
   - Frame options: dejalo como viene.
10. **Details → Description:** pegá la descripción de `textos.md` (la lista con viñetas y los links). Para el GIF:
    en el editor de la descripción, botón de imagen → subí `remarcar.gif` y ubicalo después del primer párrafo.
11. **Genre:** `Simulation`.
12. **Tags:** las 10 de `textos.md` (escribí cada una y elegí la sugerencia si aparece).
13. **AI generation disclosure:** respondé según cómo hiciste el juego.
14. **App store links / Custom noun:** dejalos vacíos.
15. **Download & install instructions:** vacío (es web).
16. **Community:** `Comments` (sirve para juntar los "¿dónde lo juego?" que cuentan para la señal de Steam).
17. **Visibility & access:** `Draft` mientras lo probás; `Public` cuando esté OK.
18. Columna derecha:
    - **Cover image:** `portada-630x500.png`.
    - **Gameplay video or trailer:** opcional, un link de YouTube (por ejemplo la presentación horizontal o un clip
      cuando estén subidos).
    - **Screenshots:** las 5 de `capturas/`, en orden (01 remarcar primero).
19. **Save & view page.** En la página: probá la demo de punta a punta (clic → sonido: el audio arranca con el primer
    clic, es normal), y mirá la consola (F12) si algo no carga.
20. Opcional, en **Edit theme** (desde la página): fondo tinta `#18191C`, texto papel `#F7F6F2`, links y botones
    amarillo `#FFC21A` (colores de MARCA.md).

## Más campos que ofrece itch.io (en "Metadata" / "More information")
Usá los de `textos.md`: Inputs (Mouse, Keyboard), Languages (Spanish, English), Average session (A few minutes),
Accessibility (Configurable), Platforms (HTML5, lo pone solo).

## Regenerar el zip
Desde `INFLATION-What-Inflation-/`:
```
powershell -File tools/export_all.ps1 -Targets web_demo
```
Exporta con QA (textos, raspadita, sobre y guardado) y deja `export\web_demo\InflationWhatInflation_web_demo.zip`.
Copialo a esta carpeta. Último export: 16/11/2026 16:17, código `fac4687`, QA web OK.
