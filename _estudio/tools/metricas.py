"""Métricas del estudio moscode.games: lee _estudio/marketing/metricas.csv y saca el ranking y las señales.

Uso (desde la carpeta del estudio):
  py _estudio/tools/metricas.py pendientes [--juego inflation]   # filas sin números (lo que hay que pedirle a Agus)
  py _estudio/tools/metricas.py ranking    [--juego inflation]   # clips ordenados + señal de Steam + sigo / lo dejo

Convenciones de metricas.csv (una fila por clip y por red; /semana actualiza la fila, no agrega otra):
  fecha        día de publicación (AAAA-MM-DD)
  clip         <AAAA-MM-DD de la tanda>/<NN-nombre>-<idioma>, p. ej. 2026-11-16/01-tijera-en
  red          tiktok | shorts | reels | reddit | itch
  pct_visto    porcentaje promedio visto (0–100)
  notas        texto libre + claves opcionales: pide_jugar=N (comentarios que piden jugarlo), votos=N (Reddit),
               seguidores_itch=N (fila de red itch)
Criterios: _estudio/disenos/validacion.md
"""
from __future__ import annotations

import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

CSV = Path(__file__).resolve().parents[1] / "marketing" / "metricas.csv"
REDES_VIDEO = {"tiktok", "shorts", "reels"}


def num(v: str) -> float | None:
    v = (v or "").strip().replace("%", "").replace(" ", "")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", v):          # 12.500 → 12500 (separador de miles argentino)
        v = v.replace(".", "")
    v = v.replace(",", ".")                             # 45,5 → 45.5
    try:
        return float(v)
    except ValueError:
        return None


def clave(notas: str, k: str) -> int:
    m = re.search(rf"{k}\s*=\s*(\d+)", notas or "")
    return int(m.group(1)) if m else 0


def leer(juego: str | None) -> list[dict]:
    with CSV.open(encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f))
    return [r for r in filas if not juego or r["juego"] == juego]


def pendientes(filas: list[dict]) -> None:
    def falta(r: dict) -> bool:
        if r["red"] == "reddit":
            return num(r["vistas"]) is None and not clave(r.get("notas", ""), "votos")
        if r["red"] == "itch":
            return not clave(r.get("notas", ""), "seguidores_itch")
        return num(r["vistas"]) is None
    faltan = [r for r in filas if falta(r)]
    if not faltan:
        print("No falta ningún número.")
        return
    print(f"Faltan números de {len(faltan)} fila(s):")
    for r in faltan:
        print(f"  {r['fecha'] or '(sin fecha)':10}  {r['juego']:12} {r['clip']:34} {r['red']}")


def ranking(filas: list[dict]) -> None:
    clips: dict[tuple, dict] = defaultdict(lambda: {"vistas": 0.0, "cg": 0.0, "com": 0.0, "seg": 0.0, "pide": 0,
                                                    "visto": [], "redes": {}})
    reddit_votos = 0
    itch_seg = 0
    for r in filas:
        notas = r.get("notas", "")
        reddit_votos = max(reddit_votos, clave(notas, "votos")) if r["red"] == "reddit" else reddit_votos
        itch_seg = max(itch_seg, clave(notas, "seguidores_itch"))
        if r["red"] not in REDES_VIDEO:
            continue
        v = num(r["vistas"])
        if v is None:
            continue
        c = clips[(r["juego"], r["clip"])]
        c["vistas"] += v
        c["cg"] += num(r["compartidos_guardados"]) or 0
        c["com"] += num(r["comentarios"]) or 0
        c["seg"] += num(r["seguidores_ganados"]) or 0
        c["pide"] += clave(notas, "pide_jugar")
        if num(r["pct_visto"]) is not None:
            c["visto"].append(num(r["pct_visto"]))
        c["redes"][r["red"]] = v
    if not clips:
        print("Todavía no hay clips con vistas cargadas.")
        return
    lista = []
    for (juego, clip), c in clips.items():
        k = max(c["vistas"], 1) / 1000
        lista.append({"juego": juego, "clip": clip, **c, "cg_k": c["cg"] / k, "com_k": c["com"] / k,
                      "visto_prom": sum(c["visto"]) / len(c["visto"]) if c["visto"] else None})
    lista.sort(key=lambda x: (x["cg_k"] + x["com_k"], x["vistas"]), reverse=True)

    print(f"{'#':>2}  {'clip':34} {'vistas':>9} {'CG/1k':>6} {'com/1k':>6} {'%visto':>6} {'seg':>5}  redes")
    for i, x in enumerate(lista, 1):
        redes = " ".join(f"{k}:{int(v)}" for k, v in sorted(x["redes"].items()))
        vp = f"{x['visto_prom']:.0f}" if x["visto_prom"] is not None else "-"
        print(f"{i:>2}  {x['clip'][:34]:34} {int(x['vistas']):>9} {x['cg_k']:>6.1f} {x['com_k']:>6.1f} {vp:>6} {int(x['seg']):>5}  {redes}")

    for juego in sorted({x["juego"] for x in lista}):
        js = [x for x in lista if x["juego"] == juego]
        mejor = max(x["vistas"] for x in js)
        c10k = sum(1 for x in js if x["vistas"] >= 10_000)
        tot_v = sum(x["vistas"] for x in js)
        tot_cg = sum(x["cg"] for x in js)
        pide = sum(x["pide"] for x in js)
        print(f"\n== {juego} ({len(js)} clips con números, {int(tot_v)} vistas) ==")
        steam = mejor >= 50_000 or c10k >= 3
        print(f"Señal de Steam: {'SÍ' if steam else 'todavía no'} (mejor clip {int(mejor)}; clips con 10K+: {c10k}; "
              f"comentarios que piden jugar: {pide}) — además tiene que haber comentarios preguntando dónde jugar.")
        criterios = [
            ("un clip con 100K+ vistas", mejor >= 100_000),
            ("compartidos+guardados ≥ 1,5 % de las vistas", tot_v > 0 and tot_cg / tot_v >= 0.015),
            ("50+ comentarios que piden jugarlo", pide >= 50),
            ("itch.io con 300+ seguidores", itch_seg >= 300),
            ("Reddit con 200+ votos", reddit_votos >= 200),
        ]
        ok = sum(1 for _, b in criterios if b)
        for txt, b in criterios:
            print(f"  [{'x' if b else ' '}] {txt}")
        if ok >= 3:
            print(f"  → SIGO ({ok}/5)")
        elif len(js) >= 10 and mejor < 20_000:
            print(f"  → LO DEJO: {len(js)} clips y ninguno pasó los 20K")
        else:
            print(f"  → todavía sin veredicto ({ok}/5; LO DEJO solo si 10 clips no pasan los 20K)")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] not in ("pendientes", "ranking"):
        print(__doc__)
        sys.exit(1)
    juego = args[args.index("--juego") + 1] if "--juego" in args else None
    filas = leer(juego)
    pendientes(filas) if args[0] == "pendientes" else ranking(filas)


if __name__ == "__main__":
    main()
