---
name: nuevo-juego
description: Prepara la carpeta de un juego nuevo del estudio moscode.games (CLAUDE.md del juego, tools/clips/, carpeta de clips de marketing), lo suma al Mapa del estudio y propone 5 clips para validar la idea. Usar con /nuevo-juego <nombre> o cuando Agus arranca un juego o una idea nueva.
---

# /nuevo-juego <nombre>

Hablale a Agus en español rioplatense. No hagas `git init`, commits ni push, ni crees el proyecto de Godot, salvo
que Agus lo pida (al final ofrecelo).

## 1. Nombres
- **Carpeta**: el nombre del juego como lo escribe Agus, sin espacios (p. ej. `Plastiquito`).
- **Slug**: minúsculas, sin espacios ni signos (p. ej. `plastiquito`). Se usa en métricas, clips y comandos.
- Si la carpeta ya existe, no pises nada: solo agregá lo que falte y decí qué ya estaba.
- Si es una de las ideas de `_estudio/MEMORIA.md` (Plastiquito, Destapador, Empujapesos, Aduana, El Asado), usá lo
  que ya está decidido ahí. Si falta lo esencial (de qué se trata, el gancho de 3 s), preguntale a Agus con una sola
  pregunta antes de escribir.

## 2. Crear
1. `<Carpeta>/CLAUDE.md` del juego, corto, con:
   - Qué es (1 línea), el gancho que se entiende en 3 s, el elemento que se multiplica, precio y duración meta
     (fórmula de MEMORIA.md: USD 3–10, 5–15 h, 3–5 meses).
   - Stack: Godot 4 (versión estable más nueva instalada), GDScript, tipado estático, comentarios en español.
   - Reglas técnicas iniciales (datos de balance en archivos de datos, tests headless, cómo verificar).
   - Esta línea, textual: "Este juego es parte del estudio moscode.games: para todo lo visual y los clips, seguir
     ../_estudio/brand/MARCA.md."
   - Una sección "Clips para validar" con las 5 ideas del paso 3.
2. `<Carpeta>/tools/clips/README.md`: cómo va a grabar este juego (bot que juega solo + Godot `--write-movie`,
   mp4 crudos en `export/clips_crudos/<guion>_<idioma>.mp4`, sin carteles propios, EN y ES) y que la edición la hace
   `_estudio/tools/clip_tool.py`. Si hay proyecto Godot, tomá de modelo `INFLATION-What-Inflation-/tools/clips/`.
3. `_estudio/marketing/clips/<slug>/`.
4. Sumá la fila al Mapa de `CLAUDE.md` del estudio (carpeta, slug, qué es, estado "por empezar") sin tocar las demás.
5. En `_estudio/disenos/validacion.md`, si la idea estaba en "Ideas en espera", actualizá su estado.

## 3. Cinco clips para validar la idea
Antes de programar mucho: 5 clips que se puedan hacer con un prototipo de una semana (o con un mockup), cada uno con
el momento fuerte del segundo 0, gancho EN y ES (máx. 8 palabras), qué hay que prototipar para grabarlo, y qué
número diría "sigo" (criterios de `_estudio/disenos/validacion.md`: 3 de 5 para seguir; ningún clip arriba de 20K
después de 10 clips = lo dejo).

## 4. Cierre
Mostrá el árbol de lo creado, la fila nueva del Mapa y los 5 clips. Ofrecé: crear el proyecto de Godot, `git init`
y armar el primer guion del grabador.
