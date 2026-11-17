# Guía: página de INFLATION en itch.io (demo web)

Archivos de esta carpeta (`_estudio/marketing/itch/inflation/`):
| archivo | para qué |
|---|---|
| `InflationWhatInflation_web_demo.zip` | el juego (11,3 MB, `index.html` en la raíz). Export del 16/11 21:56 con el código actual, QA web OK |
| `portada-630x500.png` | Cover image (igual al artboard "Itch" del canvas de identidad). `portada.py` la rehace |
| `capturas/01-hiperinflacion.png` … `05-sobre-dorado.png` | Screenshots (1920×1080, sacadas de las sesiones de clips) |
| `casi-me-funde.gif` | GIF para la descripción (640×360, 7 s, 1,6 MB): la corrida cambiaria → hiperinflación |
| `textos.md` | título, frase corta, descripción, etiquetas, género, clasificación y opciones del embed |
| `prompt-chrome.md` | prompt para que Claude in Chrome complete la página de edición (sin imágenes, sin precio, sin publicar) |

## Orden
1. **Crear el proyecto** (itch.io → Upload new project): título `INFLATION? What Inflation?`, Project URL `inflation`,
   Kind of project `HTML`. Guardar como borrador (Draft). Sin esto, butler no puede subir ("invalid game").
2. **Subir el build con butler** (desde `JUEGOS/`):
   `"%LOCALAPPDATA%\butler\butler.exe" push _estudio/marketing/itch/inflation/InflationWhatInflation_web_demo.zip moscode-games/inflation:html5`
   (butler ya está instalado y logueado en esta PC).
3. **Completar la página** con `prompt-chrome.md` en Claude in Chrome (o a mano con `textos.md`). Embed: 1280 × 720,
   botón de pantalla completa sí, "Click to launch in fullscreen" no, SharedArrayBuffer NO (el build es sin hilos).
4. **Subir las imágenes** a mano: Cover image = `portada-630x500.png`; Screenshots = las 5 de `capturas/` en orden;
   el GIF en la descripción, después del primer párrafo (botón de imagen del editor).
5. **Probar** la página en borrador (el audio arranca con el primer clic: es normal) y recién ahí pasar a Public.

## Regenerar el zip
Desde `INFLATION-What-Inflation-/`: `powershell -File tools/export_all.ps1 -Targets web_demo` (exporta con QA) y copiar
`export\web_demo\InflationWhatInflation_web_demo.zip` a esta carpeta.
