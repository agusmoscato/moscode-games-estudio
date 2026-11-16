---
name: semana
description: Revisión semanal de los domingos del estudio moscode.games - carga los números de los clips en metricas.csv, ordena qué funcionó, decide qué repetir y qué cortar, mira si hay señal para Steam y escribe el plan de la semana en calendario.md. Usar con /semana o cuando Agus pide revisar métricas o planear la semana.
---

# /semana

Revisión de los domingos. Hablale a Agus en español rioplatense, corto y con números. **No publica nada.**

## 1. Pedir lo que falta
1. `py _estudio/tools/metricas.py pendientes` → lista de filas sin números.
2. Pedile a Agus esos números **en un solo mensaje**, en una tabla fácil de completar: por clip y red, vistas,
   % visto promedio, compartidos+guardados, comentarios, seguidores ganados, y cuántos comentarios piden jugarlo.
   Pedí también: seguidores de itch.io y votos del post de Reddit de la semana (si hubo).
   Aceptá números en formato argentino (12.500, 45,5 %) o capturas de pantalla.
3. Si Agus subió clips que no estaban en el CSV, agregá sus filas.
4. Esperá la respuesta. Si dice que no tiene algún número, dejalo vacío y seguí.

## 2. Cargar
Actualizá las filas de `_estudio/marketing/metricas.csv` (una fila por clip y red; no dupliques). Convenciones de
`notas`: `pide_jugar=N`, `votos=N` (fila `reddit`), `seguidores_itch=N` (fila `itch`, una por semana).
`fecha` = día en que se publicó.

## 3. Analizar
`py _estudio/tools/metricas.py ranking` (y `--juego <slug>` por cada juego con clips). Contale a Agus:
- **Top y fondo**: ranking por compartidos+guardados y comentarios cada 1.000 vistas, con vistas y % visto.
- **Qué repetir**: los ganchos, momentos y formatos de los mejores (variantes concretas para la semana).
- **Qué cortar**: lo que quedó abajo dos semanas seguidas, o con % visto bajo (el gancho no engancha).
- **Señal para Steam** (pagar los USD 100): un clip con 50K+ o 3–4 con 10K+, y comentarios preguntando dónde jugar.
  Decí sí o no con los números. Si es sí, recordá la meta: Next Fest de febrero 2027 con 1.000+ wishlists.
- **Sigo / lo dejo** según `_estudio/disenos/validacion.md`. Si hay veredicto nuevo, sumalo a su tabla de registro.

## 4. Planear la semana (en `_estudio/marketing/calendario.md`)
Filas de lunes a domingo de la semana que viene:
- **1 clip por día** (un solo post), la versión en español, mismo video en TikTok, Shorts y Reels, 19–21 h.
  Solo español: no se planean versiones en inglés. Regla de clips: algo tiene que cambiar o crecer en pantalla
  (MARCA.md); lo que es una acción repetida sin cambio no se sube. Primero los que quedaron sin subir de tandas
  anteriores que se parezcan a los ganadores; si faltan, anotá "nueva tanda con /clips <juego>" y qué momentos grabar.
- **1 post de Reddit** en primera persona: subreddit del género del juego (después r/IndieDev o r/godot, después
  r/indiegames), con título propuesto y el clip que lo acompaña. Escribí el borrador en la misma semana del calendario.
- **Cambios al juego**: lo que piden los comentarios o lo que mostraría mejor el momento fuerte (máx. 3, concretos).
Debajo de la tabla, un bloque "Semana del AAAA-MM-DD" con el resumen del análisis en 5 líneas.

## 5. Cierre
Resumen para Agus: 3 números clave de la semana, qué repetir, qué cortar, Steam sí/no y la semana planeada.
Sin commits ni push.
