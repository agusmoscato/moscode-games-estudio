# Validación de ideas: ¿sigo o lo dejo?

Criterios decididos en MEMORIA.md (análisis de mercado, noviembre 2026). Se aplican a cada juego y a cada idea
de juego nuevo, mirando los clips publicados. Los números salen de `_estudio/marketing/metricas.csv`;
`py _estudio/tools/metricas.py ranking --juego <slug>` los marca solos.

## SIGO si se cumplen 3 de 5
| # | Criterio | De dónde sale |
|---|---|---|
| 1 | Un clip con **100K+ vistas** (sumando TikTok + Shorts + Reels) | columna `vistas` |
| 2 | **Compartidos y guardados ≥ 1,5 %** de las vistas | `compartidos_guardados` / `vistas` |
| 3 | **50+ comentarios que piden jugarlo** ("¿dónde lo juego?", "¿cuándo sale?", "link") | `notas`: `pide_jugar=N` |
| 4 | **itch.io con 300+ seguidores** | fila con red `itch`, `notas`: `seguidores_itch=N` |
| 5 | **Reddit con 200+ votos** en un post | fila con red `reddit`, `notas`: `votos=N` |

## LO DEJO si
- **Ningún clip pasa las 20K vistas después de 10 clips** publicados de esa idea.

Cuando no se cumple ninguna de las dos cosas: seguir publicando y no decidir todavía.

## Señal para pagar Steam (USD 100)
Aparte de lo anterior: un clip con **50K+** vistas, o **3–4 clips con 10K+**, y comentarios que pregunten dónde
jugarlo. Meta: Steam Next Fest de febrero 2027 con más de 1.000 wishlists.

## Ideas en espera (juego 3, se elige por los números de sus clips)
| Idea | Gancho en 3 s | Estado |
|---|---|---|
| Destapador | destapar cañerías y que salgan cosas absurdas | sin clips |
| Empujapesos / Peso Pusher | coin pusher con devaluación y reformas que quitan ceros | sin clips |
| Aduana / Bottomless Baggage | valija sin fondo, 2D cenital | sin clips |
| El Asado / Too Many Choripanes | incremental de 4 a 10.000 choripanes | sin clips |

## Registro de veredictos
| fecha | juego / idea | clips | criterios cumplidos | veredicto | nota |
|---|---|---|---|---|---|
