# moscode.games — estudio

Estudio indie de Argentina (Agus, dev solo): juegos cortos, con una idea rara y humor, en Godot 4.
Este repo es **lo compartido del estudio**: marca, memoria, herramientas de clips, marketing y los comandos de
Claude Code. Cada juego tiene su propio repo, que se clona al lado.

## Estructura
```
JUEGOS/                         ← este repo (raíz)
├── CLAUDE.md                   instrucciones del estudio para Claude Code (mapa de juegos, reglas, prioridades)
├── .claude/skills/             comandos /clips, /presentacion, /semana, /nuevo-juego
├── _estudio/
│   ├── MEMORIA.md              decisiones del estudio (fórmula, roadmap, marketing)
│   ├── brand/                  MARCA.md, logo, personaje (pixel art), fuentes (OFL)
│   ├── disenos/validacion.md   criterios de "sigo / lo dejo" y señal para Steam
│   ├── tools/                  clip_tool.py (edición de clips y presentación), metricas.py
│   └── marketing/              calendario.md, metricas.csv, clips/<juego>/<fecha>/, presentacion/<fecha>/
├── INFLATION-What-Inflation-/  (repo propio, no entra acá)
└── FiestaFatal/                (repo propio, no entra acá)
```
Los videos (`*.mp4`) no se versionan: se regeneran con `_estudio/tools/clip_tool.py` a partir de `tanda.json` /
`presentacion.json` y las grabaciones de cada juego. Sí se versionan los textos (`captions.md`, `guion.md`), las
tandas y las hojas de contacto (`contact.png`).

## Clonar todo en una PC nueva
```
git clone https://github.com/agusmoscato/moscode-games-estudio.git JUEGOS
cd JUEGOS
git clone https://github.com/agusmoscato/INFLATION-What-Inflation-.git
# FiestaFatal (AGUAFIESTAS, en pausa) y los juegos que vengan, también al lado, cada uno con su repo.
```
Herramientas: Godot (cada juego dice qué versión; INFLATION se arma con `powershell -File tools/setup.ps1`),
ffmpeg (`winget install Gyan.FFmpeg`) y el Python de Windows con Pillow (`py -m pip install pillow`).

## Comandos (en Claude Code, abierto en esta carpeta)
- `/clips <juego>`: propone 10 ideas, graba con el bot del juego, edita los clips con la marca (EN y ES, formato
  vertical "blur fill"), escribe los textos, suma filas a métricas y recomienda los 3 primeros. No publica nada.
- `/presentacion`: video de presentación del estudio (vertical y horizontal, EN y ES) para fijar en los perfiles.
  Se regenera con cada juego nuevo.
- `/semana`: revisión de los domingos: carga métricas, ranking, qué repetir y qué cortar, señal para Steam y el
  plan de la semana en `calendario.md`.
- `/nuevo-juego <nombre>`: prepara la carpeta de un juego nuevo con la marca, lo suma al mapa y propone 5 clips
  para validar la idea.
