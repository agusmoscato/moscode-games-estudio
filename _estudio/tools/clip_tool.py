"""Herramienta de clips del estudio moscode.games. Sigue _estudio/brand/MARCA.md al pie de la letra.

Toma la grabación cruda de cualquier juego (un mp4/avi por idioma o uno solo) y arma los clips de marca:
caja de gancho arriba, juego en el medio, cierre con agus-guino + @moscode.games + llamado a la acción,
zonas seguras respetadas, versión en inglés y en español, y una hoja de contacto.

Uso (desde la carpeta del estudio, con el Python de Windows que tiene Pillow):
  py _estudio/tools/clip_tool.py tanda    <tanda.json>   # edita todos los clips de la tanda + contact.png
  py _estudio/tools/clip_tool.py probar   <tanda.json>   # valida la tanda y deja las capas PNG en _capas/ (sin video)
  py _estudio/tools/clip_tool.py contacto <carpeta>      # rehace contact.png con los mp4 de una carpeta
  py _estudio/tools/clip_tool.py presentacion <presentacion.json>   # video del estudio (/presentacion); formato en
                                                                    # el docstring de cmd_presentacion()
  Opción: --modo recorte   usa el modo vertical viejo (recortar el juego) en vez del "blur fill" por defecto.

FORMATO VERTICAL POR DEFECTO: "blur fill" (los juegos son de PC; recortados se ven raros).
Se graba la pantalla del juego ENTERA en 16:9 (1920x1080). En el lienzo 1080x1920:
  - fondo: el mismo video llenando la pantalla, desenfocado fuerte y oscurecido ~38 %;
  - frente: el video completo a 1080x608, centrado (y 656–1264), con borde tinta de 4 px y sombra dura roja;
  - arriba, la caja de gancho; abajo del juego, un "subtitulo" corto opcional (fuera de la zona segura de abajo);
  - "zoom" opcional por escena, suave desde la vista completa: {"factor": 1.5, "centro": [x, y], "desde": 1.0,
    "dur": 0.8} en px de la grabación ("dur": 0 = arranca con zoom). Por defecto, sin zoom.
El modo "recorte" (layout vertical | cuadrado | completo + "recorte") queda con "modo": "recorte" o --modo recorte.

Formato de tanda.json (las rutas relativas son relativas a la carpeta del estudio):
{
  "juego": "inflation",                         # slug (columna "slug" del Mapa en CLAUDE.md)
  "titulo": "INFLATION?",                       # nombre en la caja de gancho (Press Start 2P 22 px)
  "salida": "_estudio/marketing/clips/inflation/2026-11-16",
  "formato": "vertical",                        # "vertical" 1080x1920 (clips) u "horizontal" 1920x1080 (tráiler)
  "modo": "blur",                               # vertical: blur (por defecto) | recorte
  "idiomas": ["es"],                            # por defecto solo español; "en" solo si se pide explícitamente
  "cta": {"es": "Demo gratis en itch.io"},
  "clips": [{
    "n": 1, "nombre": "tijera",
    "fuente": "INFLATION-What-Inflation-/export/clips_crudos/tijera_{idioma}_1920x1080.mp4",   # o {"en": .., "es": ..}
    "inicio": 0.0, "duracion": 16,              # segundos de la fuente; si la fuente es más corta se congela el último cuadro
    "zoom": {"factor": 1.5, "centro": [960, 540], "desde": 1.0, "dur": 0.8},   # opcional
    "subtitulo": {"en": "...", "es": "..."},    # opcional, abajo del juego (solo modo blur)
    "gancho": {"en": "Too many zeros?", "es": "¿Demasiados ceros?"},   # máx. 8 palabras; null = sin caja
    "gancho_hasta": 6,                          # opcional: segundo en que se va la caja (por defecto, hasta el cierre)
    "globos": [{"desde": 0, "hasta": 3, "personaje": "agus-principal",
                "texto": {"en": "...", "es": "..."}}],                   # opcional (Agus en pixel art con globo)
    "cierre": true,                             # últimos 1,5 s con el cierre de marca
    "layout": "vertical", "recorte": [x, y, w, h]   # solo modo recorte: vertical | cuadrado (936x936) | completo
  }]
}
En lugar de "fuente", un clip puede llevar "tramos": cada uno se corta (con "zoom" o "recorte" propio) y se une en
una sola fuente. En modo blur y en horizontal el lienzo es 1920x1080; en modo recorte, "lienzo" (por defecto 1080x1080):
  "tramos": [{"fuente": ".../tijera_{idioma}_1920x1080.mp4", "inicio": 1.6, "dur": 3.4, "zoom": {...}}, ...]
("{idioma}" se reemplaza por en/es; también vale en "fuente").
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Sin shebang a propósito: el lanzador "py" lo respetaría y podría usar otro Python sin Pillow.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Falta Pillow. Usá el Python de Windows: py _estudio/tools/clip_tool.py ...  (o: py -m pip install pillow)")

ESTUDIO = Path(__file__).resolve().parents[1]          # _estudio/
RAIZ = ESTUDIO.parent                                   # carpeta del estudio (JUEGOS)
BRAND = ESTUDIO / "brand"
FUENTE_TITULO = BRAND / "fuentes" / "PressStart2P-Regular.ttf"
FUENTE_TEXTO = BRAND / "fuentes" / "PixelifySans-VF.ttf"

# Colores de MARCA.md
TINTA = (0x18, 0x19, 0x1C)
PAPEL = (0xF7, 0xF6, 0xF2)
AMARILLO = (0xFF, 0xC2, 0x1A)
ROJO = (0xC8, 0x32, 0x1F)

FPS = 30
CIERRE_S = 1.5
MODO_FORZADO: str | None = None   # --modo recorte|blur en la línea de comandos (pisa lo de la tanda)
LAYOUTS_V = {  # modo "recorte": x, y, ancho, alto del juego en el lienzo vertical
    "vertical": (0, 540, 1080, 1380),
    "cuadrado": (72, 560, 936, 936),
}
avisos: list[str] = []


def avisar(msg: str) -> None:
    avisos.append(msg)
    print("  ! " + msg)


# ---------------------------------------------------------------- herramientas externas
def buscar_ffmpeg(nombre: str = "ffmpeg") -> str:
    env = os.environ.get(nombre.upper())
    if env and Path(env).exists():
        return env
    w = shutil.which(nombre)
    if w:
        return w
    local = os.environ.get("LOCALAPPDATA", "")
    for patron in (rf"{local}\Microsoft\WinGet\Links\{nombre}.exe",
                   rf"{local}\Microsoft\WinGet\Packages\Gyan.FFmpeg*\**\bin\{nombre}.exe",
                   rf"{os.environ.get('ProgramData', '')}\chocolatey\bin\{nombre}.exe"):
        hits = glob.glob(patron, recursive=True)
        if hits:
            return hits[0]
    sys.exit(f"No encontré {nombre}. Instalalo con: winget install Gyan.FFmpeg")


FFMPEG = buscar_ffmpeg("ffmpeg")
FFPROBE = buscar_ffmpeg("ffprobe")


def correr(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(f"ffmpeg falló (código {r.returncode})")


def sondear(ruta: Path) -> dict:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "stream=codec_type,width,height:format=duration",
                        "-of", "json", str(ruta)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"No pude leer {ruta}: {r.stderr.strip()}")
    d = json.loads(r.stdout)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    return {"audio": any(s.get("codec_type") == "audio" for s in d.get("streams", [])),
            "w": int(v.get("width", 0)), "h": int(v.get("height", 0)),
            "dur": float(d.get("format", {}).get("duration", 0) or 0)}


# ---------------------------------------------------------------- texto
def fuente_titulo(px: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FUENTE_TITULO), px)


def fuente_texto(px: int, peso: int = 700) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FUENTE_TEXTO), px)
    f.set_variation_by_axes([peso])
    return f


def partir(texto: str, fuente: ImageFont.FreeTypeFont, ancho: int) -> list[str]:
    lineas: list[str] = []
    for parrafo in texto.split("\n"):
        actual = ""
        for palabra in parrafo.split():
            prueba = (actual + " " + palabra).strip()
            if fuente.getlength(prueba) <= ancho or not actual:
                actual = prueba
            else:
                lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def partir_parejo(texto: str, fuente: ImageFont.FreeTypeFont, ancho: int) -> list[str]:
    """Como partir(), pero con las líneas lo más parejas posible (sin una palabra sola abajo)."""
    mejor = partir(texto, fuente, ancho)
    n = len(mejor)
    w = ancho
    while w > ancho // 3:
        w -= 10
        prueba = partir(texto, fuente, w)
        if len(prueba) > n:
            break
        mejor = prueba
    return mejor


def alto_linea(fuente: ImageFont.FreeTypeFont) -> int:
    a, d = fuente.getmetrics()
    return a + d


def caja_marca(d: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, relleno, borde, sombra, sombra_px: int,
               borde_px: int = 6) -> None:
    """Caja sin esquinas redondas, borde liso y sombra dura desplazada (MARCA.md)."""
    d.rectangle([x0 + sombra_px, y0 + sombra_px, x1 + sombra_px, y1 + sombra_px], fill=sombra)
    d.rectangle([x0, y0, x1, y1], fill=borde)
    d.rectangle([x0 + borde_px, y0 + borde_px, x1 - borde_px, y1 - borde_px], fill=relleno)


def texto_centrado(d: ImageDraw.ImageDraw, cx: int, y: int, lineas: list[str], fuente, color, interlineado: int = 4) -> int:
    for ln in lineas:
        w = fuente.getlength(ln)
        d.text((cx - w / 2, y), ln, font=fuente, fill=color)
        y += alto_linea(fuente) + interlineado
    return y


def personaje(nombre: str, lado: int) -> Image.Image:
    ruta = BRAND / "personaje" / f"{nombre}.png"
    if not ruta.exists():
        sys.exit(f"No existe {ruta}")
    return Image.open(ruta).convert("RGBA").resize((lado, lado), Image.NEAREST)   # siempre nearest neighbor


# ---------------------------------------------------------------- capas PNG
def capa_gancho(W: int, H: int, titulo: str, gancho: str) -> Image.Image:
    """Caja amarilla con borde papel de 6 px y sombra roja de 10 px. En vertical ocupa y 150–500 sin tocar
    los 140 px de la derecha."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    vertical = H > W
    ancho = 780 if vertical else 1200
    x0 = (W - ancho) // 2 if vertical else (W - ancho) // 2
    y0 = 150 if vertical else 50
    y_max = 500 if vertical else 360
    pad = 30
    palabras = len(gancho.split())
    if palabras > 8:
        avisar(f"gancho de {palabras} palabras (máx. 8): «{gancho}»")
    ft = fuente_titulo(22)
    for px in range(76, 47, -4):
        fg = fuente_texto(px)
        lineas = partir_parejo(gancho, fg, ancho - 2 * pad - 12)
        alto = pad + alto_linea(ft) + 18 + len(lineas) * (alto_linea(fg) + 2) + pad - 6
        if y0 + alto <= y_max:
            break
        if px == 48:
            avisar(f"el gancho no entra en la caja ni a 48 px: «{gancho}»")
    if px < 76:
        avisar(f"gancho achicado a {px} px para que entre: «{gancho}»")
    y1 = y0 + alto
    caja_marca(d, x0, y0, x0 + ancho, y1, AMARILLO, PAPEL, ROJO, 10)
    cx = x0 + ancho // 2
    y = y0 + pad
    y = texto_centrado(d, cx, y, [titulo], ft, TINTA) + 14
    texto_centrado(d, cx, y, lineas, fg, TINTA, 2)
    return img


def capa_cierre(W: int, H: int, cta: str) -> Image.Image:
    """Últimos 1,5 s: agus-guino, @moscode.games y el llamado a la acción, arriba de la zona tapada por la app."""
    img = Image.new("RGBA", (W, H), TINTA + (232,))
    d = ImageDraw.Draw(img)
    vertical = H > W
    lado = 160
    fh = fuente_titulo(36 if vertical else 44)
    ancho_cta = 780 if vertical else 1400
    parrafos = cta.count("\n") + 1
    for px in range(68 if vertical else 76, 47, -4):        # que cada renglón del llamado entre en una línea
        fc = fuente_texto(px)
        cta_lineas = partir(cta, fc, ancho_cta)
        if len(cta_lineas) <= parrafos:
            break
    else:
        cta_lineas = partir_parejo(cta, fc, ancho_cta)
    alto = lado + 48 + alto_linea(fh) + 30 + len(cta_lineas) * (alto_linea(fc) + 2)
    cx = W // 2
    y = (H - 400 - alto) // 2 + 60 if vertical else (H - alto) // 2
    pj = personaje("agus-guino", lado)
    caja_marca(d, cx - lado // 2 - 6, y - 6, cx + lado // 2 + 5, y + lado + 5, AMARILLO, TINTA, ROJO, 8)
    img.alpha_composite(pj, (cx - lado // 2, y))
    y += lado + 48
    y = texto_centrado(d, cx, y, ["@moscode.games"], fh, PAPEL) + 30
    texto_centrado(d, cx, y, cta_lineas, fc, AMARILLO, 2)
    return img


def capa_globo(W: int, H: int, texto: str, nombre_pj: str) -> Image.Image:
    """Agus (pixel art) con un globo de texto, para la presentación y los tráileres. Queda arriba de la zona segura."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    vertical = H > W
    lado = 240 if vertical else 220
    base = (H - 400) if vertical else (H - 40)          # piso del personaje
    px_, py_ = 60, base - lado
    ft = fuente_texto(54 if vertical else 50)
    ancho_max = (W - 140 - (px_ + lado + 40) - 20) if vertical else 900
    lineas = partir(texto, ft, ancho_max - 56)
    w_txt = max(ft.getlength(l) for l in lineas)
    gw = int(w_txt) + 56
    gh = len(lineas) * (alto_linea(ft) + 2) + 44
    gx0 = px_ + lado + 40
    gy1 = py_ + lado // 2
    gy0 = gy1 - gh
    caja_marca(d, gx0, gy0, gx0 + gw, gy1, PAPEL, TINTA, TINTA, 8)
    # colita del globo hacia Agus
    d.polygon([(gx0 + 6, gy1 - 50), (gx0 + 6, gy1 - 14), (gx0 - 34, gy1 + 10)], fill=TINTA)
    d.polygon([(gx0 + 8, gy1 - 42), (gx0 + 8, gy1 - 22), (gx0 - 18, gy1 + 2)], fill=PAPEL)
    y = gy0 + 22
    for ln in lineas:
        d.text((gx0 + 28, y), ln, font=ft, fill=TINTA)
        y += alto_linea(ft) + 2
    caja_marca(d, px_ - 6, py_ - 6, px_ + lado + 5, py_ + lado + 5, AMARILLO, TINTA, ROJO, 8)
    img.alpha_composite(personaje(nombre_pj, lado), (px_, py_))
    return img


# ---------------------------------------------------------------- video
def corta(p: Path) -> str:
    try:
        return str(p.relative_to(RAIZ))
    except ValueError:
        return str(p)


def por_idioma(valor, idioma: str):
    if isinstance(valor, dict):
        return valor.get(idioma)
    return valor


def ruta_abs(p: str) -> Path:
    q = Path(p)
    return q if q.is_absolute() else (RAIZ / q)


# ---------------------------------------------------------------- formato vertical "blur fill" (por defecto)
# Juegos de PC: se graba la pantalla entera 16:9 y en el vertical va completa (1080x608) en el medio, sobre el mismo
# video desenfocado y oscurecido. Arriba la caja de gancho; abajo, lugar para un subtítulo corto.
FG_W, FG_H = 1080, 608
FG_Y = (1920 - FG_H) // 2                  # 656: el juego ocupa y 656–1264
SUB_Y = FG_Y + FG_H + 40                    # el subtítulo arranca abajo del juego y termina antes de y 1520


def filtro_zoom(z: dict | None, w: int = 1920, h: int = 1080) -> str:
    """Zoom de una escena: {"factor": 1.5, "centro": [x, y], "desde": 1.0, "dur": 0.8} en px de la grabación 16:9.
    Va suave (smoothstep) de la vista completa al zoom; con "dur": 0 arranca ya con zoom. Devuelve "zoompan=...,"."""
    if not z:
        return ""
    f = float(z.get("factor", 1.3))
    cx, cy = z.get("centro", [w / 2, h / 2])
    t0 = float(z.get("desde", 0))
    d = max(float(z.get("dur", 0.8)), 0.001)
    p = f"clip((in/{FPS}-{t0})/{d},0,1)"
    s = f"(({p})*({p})*(3-2*({p})))"
    return (f"zoompan=z='1+{f - 1:.4f}*{s}':"
            f"x='clip({w / 2}+({cx}-{w / 2})*{s}-iw/zoom/2,0,iw-iw/zoom)':"
            f"y='clip({h / 2}+({cy}-{h / 2})*{s}-ih/zoom/2,0,ih-ih/zoom)':d=1:s={w}x{h}:fps={FPS},")


def cadena_blur(entrada: str, dur: float, zoom: dict | None, salida: str, pre: str = "") -> str:
    """Fondo: el mismo video llenando 1080x1920, desenfocado fuerte y oscurecido ~38 %. Frente: el video entero a
    1080x608 centrado (con zoom opcional). El borde y la sombra van en capa_marco()."""
    return (f"{entrada}{pre}scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x18191C,setsar=1,fps={FPS},{filtro_zoom(zoom)}"
            f"tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},setpts=PTS-STARTPTS,split=2[bz][fz];"
            # desenfoque a baja resolución (mismo aspecto, mucho más rápido) y de vuelta a 1080x1920
            f"[bz]scale=270:480:force_original_aspect_ratio=increase,crop=270:480,gblur=sigma=10,"
            f"scale=1080:1920:flags=bicubic,colorchannelmixer=rr=0.62:gg=0.62:bb=0.62[bgz];"
            f"[fz]scale={FG_W}:{FG_H}:flags=lanczos[fgz];"
            f"[bgz][fgz]overlay=0:{FG_Y}{salida}")


def capa_marco(W: int, H: int) -> Image.Image:
    """Borde fino tinta de 4 px y sombra dura roja de 8 px alrededor del juego (el interior queda transparente)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y0, y1 = FG_Y, FG_Y + FG_H - 1
    d.rectangle([8, y1 + 1, W - 1, y1 + 4 + 8], fill=ROJO)                 # sombra (abajo; a la derecha queda afuera)
    d.rectangle([0, y0 - 4, W - 1, y0 - 1], fill=TINTA)
    d.rectangle([0, y1 + 1, W - 1, y1 + 4], fill=TINTA)
    d.rectangle([0, y0 - 4, 3, y1 + 4], fill=TINTA)
    d.rectangle([W - 4, y0 - 4, W - 1, y1 + 4], fill=TINTA)
    return img


def capa_subtitulo(W: int, H: int, texto: str) -> Image.Image:
    """Subtítulo corto abajo del juego (papel con sombra dura tinta), sin entrar en los 400 px de abajo ni en los
    140 px de la derecha."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for px in range(60, 35, -4):
        f = fuente_texto(px)
        lineas = partir_parejo(texto, f, 780)
        if SUB_Y + len(lineas) * (alto_linea(f) + 4) <= H - 400 - 20:
            break
    else:
        avisar(f"el subtítulo no entra abajo del juego: «{texto}»")
    y = SUB_Y
    for ln in lineas:
        x = W // 2 - f.getlength(ln) / 2
        d.text((x + 4, y + 4), ln, font=f, fill=TINTA)
        d.text((x, y), ln, font=f, fill=PAPEL)
        y += alto_linea(f) + 4
    return img


def unir_tramos(clip: dict, idioma: str, destino: Path, lienzo_def=(1080, 1080)) -> Path | None:
    """Corta cada tramo ({fuente, inicio, dur, recorte, zoom}), lo centra en un lienzo tinta del tamaño "lienzo"
    y los une con su sonido. "{idioma}" en la fuente se cambia por en/es. En modo blur el lienzo es 1920x1080
    (pantalla entera) y cada tramo puede tener su "zoom"."""
    lw, lh = clip.get("lienzo", list(lienzo_def))
    cmd = [FFMPEG, "-y", "-v", "error"]
    filtros, pares = [], []
    for i, t in enumerate(clip["tramos"]):
        src = ruta_abs(str(por_idioma(t["fuente"], idioma)).replace("{idioma}", idioma))
        if not src.exists():
            avisar(f"tramo {i + 1}: no existe {src}")
            return None
        d = float(t["dur"])
        cmd += ["-ss", f"{float(t.get('inicio', 0)):.3f}", "-t", f"{d:.3f}", "-i", str(src)]
        crop = ""
        if t.get("recorte"):
            x, y, w, h = t["recorte"]
            crop = f"crop={w}:{h}:{x}:{y},"
        filtros.append(f"[{i}:v]{crop}scale={lw}:{lh}:force_original_aspect_ratio=decrease:flags=lanczos,"
                       f"pad={lw}:{lh}:({lw}-iw)/2:({lh}-ih)/2:color=0x18191C,setsar=1,fps={FPS},"
                       f"{filtro_zoom(t.get('zoom'), lw, lh)}"
                       f"tpad=stop_mode=clone:stop_duration={d:.3f},trim=duration={d:.3f},setpts=PTS-STARTPTS[v{i}]")
        if sondear(src)["audio"]:
            filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration={d:.3f},"
                           f"asetpts=PTS-STARTPTS[a{i}]")
        else:
            filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d:.3f}[a{i}]")
        pares.append(f"[v{i}][a{i}]")
    filtros.append(f"{''.join(pares)}concat=n={len(pares)}:v=1:a=1[v][a]")
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
            "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(destino)]
    correr(cmd)
    return destino


# ---------------------------------------------------------------- montaje (clips "que atrapan", MARCA.md)
# "montaje": {"fuente": ".../sesion_x_{idioma}_1920x1080.mp4",
#             "contador": {"formato": "Minuto {m}", "origen": 0},          # opcional: "Minuto N" en una esquina
#             "tramos": [{"desde": 12.0, "hasta": 40.0, "vel": 8, "golpe": true, "zoom": {...}, "etiqueta": "Vuelta 10"}]}
# Cada tramo se corta de la grabación larga y se acelera "vel" veces (x2–x8 en los tramos lentos, x1 en los picos);
# "golpe" = flash corto + refuerzo del sonido del juego al empezar el tramo; "etiqueta" pisa el contador en ese tramo;
# "cartel" = texto grande abajo del juego durante el tramo (números gigantes traducidos: usar ceros(valor)).
def montaje_duracion(mt: dict) -> float:
    return round(sum((float(t["hasta"]) - float(t["desde"])) / float(t.get("vel", 1)) for t in mt["tramos"]), 3)


def cadena_atempo(vel: float) -> str:
    """atempo acepta 0,5–2 por filtro: se encadena (x8 = 2·2·2). Mantiene el tono del sonido."""
    partes, v = [], vel
    while v > 2.0:
        partes.append("atempo=2.0")
        v /= 2.0
    partes.append(f"atempo={v:.4f}")
    return ",".join(partes)


def capa_contador(W: int, H: int, texto: str) -> Image.Image:
    """Contador chico arriba a la izquierda (fuera de la caja de gancho y de las zonas tapadas por las apps)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = fuente_texto(40)
    w = int(f.getlength(texto))
    x0, y0 = 40, 60
    caja_marca(d, x0, y0, x0 + w + 36, y0 + alto_linea(f) + 18, TINTA, PAPEL, ROJO, 6, 4)
    d.text((x0 + 18, y0 + 8), texto, font=f, fill=AMARILLO)
    return img


def capa_cartel(W: int, H: int, texto: str) -> Image.Image:
    """Cartel grande abajo del juego (MARCA.md, regla 10: traduce los números gigantes, p. ej. "¡UN 6 CON 33 CEROS!").
    Caja amarilla con borde tinta y sombra roja; no entra en los 400 px de abajo ni en los 140 px de la derecha."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for px in range(84, 43, -4):
        f = fuente_texto(px)
        lineas = partir_parejo(texto, f, 740)
        alto = len(lineas) * (alto_linea(f) + 2) + 36
        if len(lineas) <= 2 and SUB_Y + alto <= H - 400 - 20:
            break
    ancho = int(max(f.getlength(l) for l in lineas)) + 60
    x0 = W // 2 - ancho // 2
    caja_marca(d, x0, SUB_Y, x0 + ancho, SUB_Y + alto, AMARILLO, TINTA, ROJO, 10)
    texto_centrado(d, W // 2, SUB_Y + 16, lineas, f, TINTA, 2)
    return img


def ceros(valor: float) -> str:
    """Traduce un monto gigante a ceros: 5.97e33 → "¡UN 6 CON 33 CEROS!" (para los carteles de la regla 10)."""
    import math
    e = int(math.floor(math.log10(valor)))
    m = round(valor / 10 ** e)
    if m >= 10:
        m, e = 1, e + 1
    return f"¡UN {m} CON {e} CEROS!"


def montar(clip: dict, idioma: str, destino: Path) -> Path | None:
    mt = clip["montaje"]
    cmd = [FFMPEG, "-y", "-v", "error"]
    filtros, pares = [], []
    for i, t in enumerate(mt["tramos"]):
        # cada tramo puede venir de otra grabación ("fuente" del tramo); si no, la del montaje
        src = ruta_abs(str(por_idioma(t.get("fuente", mt.get("fuente")), idioma)).replace("{idioma}", idioma))
        if not src.exists():
            avisar(f"montaje: no existe {src}")
            return None
        con_audio = sondear(src)["audio"]
        a, b, v = float(t["desde"]), float(t["hasta"]), float(t.get("vel", 1))
        d_out = (b - a) / v
        cmd += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src)]
        filtros.append(f"[{i}:v]setpts=(PTS-STARTPTS)/{v},fps={FPS},scale=1920:1080:force_original_aspect_ratio=decrease,"
                       f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x18191C,setsar=1,{filtro_zoom(t.get('zoom'))}"
                       f"tpad=stop_mode=clone:stop_duration={d_out:.3f},trim=duration={d_out:.3f},setpts=PTS-STARTPTS[v{i}]")
        if con_audio:
            golpe = ",volume=volume='if(lt(t,0.25),2.0,1)':eval=frame" if t.get("golpe") else ""
            filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,{cadena_atempo(v)}"
                           f"{golpe},apad,atrim=duration={d_out:.3f},asetpts=PTS-STARTPTS[a{i}]")
        else:
            filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d_out:.3f}[a{i}]")
        pares.append(f"[v{i}][a{i}]")
    filtros.append(f"{''.join(pares)}concat=n={len(pares)}:v=1:a=1[v][a]")
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
            "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", str(destino)]
    correr(cmd)
    return destino


def capas_montaje(clip: dict, W: int, H: int, base: str, capas: Path, hasta: float) -> list[tuple[Path, str]]:
    """Contador (cambia con el tiempo real de la grabación) y flashes de los golpes, con su ventana en el clip."""
    mt = clip["montaje"]
    out: list[tuple[Path, str]] = []
    flash = capas / f"{base}-flash.png"
    Image.new("RGBA", (W, H), (255, 246, 210, 120)).save(flash)
    cont = mt.get("contador")
    t_out = 0.0
    hechos: dict[str, Path] = {}
    for i, t in enumerate(mt["tramos"]):
        a, b, v = float(t["desde"]), float(t["hasta"]), float(t.get("vel", 1))
        d_out = (b - a) / v
        if t.get("golpe") and t_out < hasta:
            out.append((flash, f"between(t,{t_out:.3f},{t_out + 0.12:.3f})"))
        if t.get("cartel") and t_out < hasta:
            pc = capas / f"{base}-cartel{i}.png"
            capa_cartel(W, H, str(t["cartel"])).save(pc)
            out.append((pc, f"between(t,{t_out:.3f},{min(t_out + d_out, hasta):.3f})"))
        if cont or t.get("etiqueta"):
            # cortes del tramo donde cambia la etiqueta (cada minuto de la grabación)
            puntos = [a]
            if not t.get("etiqueta"):
                o = float(cont.get("origen", 0))
                k = int((a - o) // 60) + 1
                while o + 60 * k < b:
                    puntos.append(o + 60 * k)
                    k += 1
            puntos.append(b)
            for j in range(len(puntos) - 1):
                s0, s1 = puntos[j], puntos[j + 1]
                if t.get("etiqueta"):
                    txt = t["etiqueta"]
                else:
                    txt = cont.get("formato", "Minuto {m}").format(m=int((s0 - float(cont.get("origen", 0))) // 60) + 1)
                o0, o1 = t_out + (s0 - a) / v, min(t_out + (s1 - a) / v, hasta)
                if o0 >= hasta:
                    continue
                if txt not in hechos:
                    p = capas / f"{base}-cont{len(hechos)}.png"
                    capa_contador(W, H, txt).save(p)
                    hechos[txt] = p
                out.append((hechos[txt], f"between(t,{o0:.3f},{o1:.3f})"))
        t_out += d_out
    return out


def armar_clip(tanda: dict, clip: dict, idioma: str, salida: Path, capas: Path, solo_capas: bool) -> Path | None:
    vertical = tanda.get("formato", "vertical") == "vertical"
    W, H = (1080, 1920) if vertical else (1920, 1080)
    # vertical: "blur" (por defecto, pantalla entera sobre fondo desenfocado) o "recorte" (el modo viejo con layouts)
    modo = (MODO_FORZADO or clip.get("modo") or tanda.get("modo") or "blur") if vertical else "horizontal"
    n = int(clip.get("n", 1))
    base = f"{n:02d}-{clip['nombre']}-{idioma}"
    dur = float(clip.get("duracion", 18))
    if clip.get("montaje"):
        dur = montaje_duracion(clip["montaje"])          # la duración la dan los tramos
    lim = (15, 25) if vertical else (30, 45)
    if not lim[0] <= dur <= lim[1]:
        avisar(f"{base}: dura {dur:g} s (lo pedido es {lim[0]}–{lim[1]} s)")

    # capas
    capas_png: list[tuple[Path, str]] = []
    gancho = por_idioma(clip.get("gancho"), idioma)
    con_cierre = clip.get("cierre", True)
    fin_gancho = dur - CIERRE_S if con_cierre else dur
    if clip.get("gancho_hasta") is not None:          # en horizontal la caja tapa el HUD: puede irse antes
        fin_gancho = min(fin_gancho, float(clip["gancho_hasta"]))
    if modo == "blur":
        p = capas / f"{base}-marco.png"
        capa_marco(W, H).save(p)
        capas_png.append((p, "1"))
        sub = por_idioma(clip.get("subtitulo"), idioma)
        if sub:
            p = capas / f"{base}-subtitulo.png"
            capa_subtitulo(W, H, sub).save(p)
            capas_png.append((p, f"lt(t,{fin_gancho:.3f})"))
    if clip.get("montaje"):
        capas_png += capas_montaje(clip, W, H, base, capas, dur - CIERRE_S if con_cierre else dur)
    if gancho:
        p = capas / f"{base}-gancho.png"
        capa_gancho(W, H, tanda.get("titulo", ""), gancho).save(p)
        capas_png.append((p, f"lt(t,{fin_gancho:.3f})"))
    for i, g in enumerate(clip.get("globos", [])):
        txt = por_idioma(g.get("texto"), idioma)
        if not txt:
            continue
        p = capas / f"{base}-globo{i}.png"
        capa_globo(W, H, txt, g.get("personaje", "agus-principal")).save(p)
        capas_png.append((p, f"between(t,{float(g['desde']):.3f},{float(g['hasta']):.3f})"))
    if con_cierre:
        p = capas / f"{base}-cierre.png"
        capa_cierre(W, H, por_idioma(tanda.get("cta"), idioma) or "").save(p)
        capas_png.append((p, f"gte(t,{dur - CIERRE_S:.3f})"))
    if solo_capas:
        return None

    # fuente: una grabación, un montaje de una sesión larga, o varios tramos que se unen en una sola
    if clip.get("montaje"):
        src = montar(clip, idioma, capas / f"{base}-montaje.mp4")
        if src is None:
            return None
        clip = {k: v for k, v in clip.items() if k not in ("recorte", "inicio", "zoom")}
    elif clip.get("tramos"):
        src = unir_tramos(clip, idioma, capas / f"{base}-fuente.mp4",
                          (1920, 1080) if modo in ("blur", "horizontal") else (1080, 1080))
        if src is None:
            return None
        clip = {k: v for k, v in clip.items() if k not in ("recorte", "inicio", "zoom")}
    else:
        src_txt = por_idioma(clip["fuente"], idioma) or por_idioma(clip["fuente"], "es")
        src = ruta_abs(src_txt.replace("{idioma}", idioma))
    if not src.exists():
        avisar(f"{base}: no existe la grabación {src}")
        return None
    info = sondear(src)
    inicio = float(clip.get("inicio", 0))
    if info["dur"] and info["dur"] - inicio < dur - 0.05:
        avisar(f"{base}: la grabación tiene {info['dur'] - inicio:.1f} s desde el inicio; congelo el último cuadro hasta {dur:g} s")

    if modo == "blur":
        if clip.get("recorte"):
            avisar(f"{base}: en modo blur no se usa \"recorte\" (se muestra la pantalla entera); usá \"zoom\"")
        if info["w"] and info["w"] < info["h"]:
            avisar(f"{base}: la grabación es vertical; el modo blur espera la pantalla entera 16:9 (1920x1080)")
        filtros = [cadena_blur("[0:v]", dur, clip.get("zoom"), "[v0]")]
    else:
        cad = "[0:v]"
        if clip.get("recorte"):
            x, y, w, h = clip["recorte"]
            cad += f"crop={w}:{h}:{x}:{y},"
        layout = clip.get("layout", "vertical")
        area = clip.get("area") or (LAYOUTS_V.get(layout) if vertical and layout != "completo" else None)
        if layout == "completo" or area is None:
            cad += f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
        else:
            ax, ay, aw, ah = area
            cad += (f"scale={aw}:{ah}:force_original_aspect_ratio=decrease:flags=lanczos,"
                    f"pad={W}:{H}:{ax}+({aw}-iw)/2:{ay}+({ah}-ih)/2:color=0x18191C,")
        cad += (f"setsar=1,fps={FPS},{filtro_zoom(clip.get('zoom'), W, H) if not vertical else ''}"
                f"tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},setpts=PTS-STARTPTS[v0]")
        filtros = [cad]
    ultimo = "v0"
    for i, (_, cuando) in enumerate(capas_png):
        filtros.append(f"[{ultimo}][{i + 1}:v]overlay=0:0:enable='{cuando}'[v{i + 1}]")
        ultimo = f"v{i + 1}"
    filtros.append(f"[{ultimo}]format=yuv420p[vout]")

    cmd = [FFMPEG, "-y", "-v", "error", "-ss", f"{inicio:.3f}", "-t", f"{dur:.3f}", "-i", str(src)]
    for p, _ in capas_png:
        cmd += ["-i", str(p)]
    idx_audio = len(capas_png) + 1
    if info["audio"]:
        filtros.append(f"[0:a]apad,atrim=duration={dur:.3f},asetpts=PTS-STARTPTS,"
                       f"afade=t=out:st={max(0.0, dur - 0.8):.3f}:d=0.8[aout]")
    else:
        avisar(f"{base}: la grabación no tiene sonido; va con silencio")
        cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        filtros.append(f"[{idx_audio}:a]anull[aout]")
    destino = salida / f"{base}.mp4"
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", "-t", f"{dur:.3f}", str(destino)]
    correr(cmd)
    mb = destino.stat().st_size / 1e6
    if mb > 50:
        avisar(f"{base}: pesa {mb:.0f} MB (TikTok acepta más, pero conviene < 50 MB)")
    print(f"  ✔ {corta(destino)}  ({dur:g} s, {mb:.1f} MB)")
    return destino


# ---------------------------------------------------------------- hoja de contacto
def cuadro(video: Path, t: float, ancho: int, tmp: Path) -> Image.Image:
    out = tmp / f"f{abs(hash((str(video), t)))}.png"
    correr([FFMPEG, "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(video), "-frames:v", "1",
            "-vf", f"scale={ancho}:-2", str(out)])
    return Image.open(out).convert("RGB")


def hoja_contacto(carpeta: Path, por_seccion: dict[str, list[float]] | None = None) -> Path | None:
    """Clips: 4 cuadros de cada video en español (0,4 s, 35 %, 70 %, cierre).
    por_seccion = {"vertical": [t, ...], "horizontal": [...]}: una fila por video, un cuadro por sección."""
    if por_seccion:
        videos = sorted(carpeta.glob("*-es.mp4")) or sorted(carpeta.glob("*.mp4"))
    else:
        # solo español: los -es.mp4 (los -en.mp4 viejos que queden en la carpeta no se usan)
        videos = sorted(carpeta.glob("*-es.mp4")) or sorted(carpeta.glob("*.mp4"))
    if not videos:
        print("  (no hay mp4 para la hoja de contacto)")
        return None
    filas = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for v in videos:
            info = sondear(v)
            vertical = info["h"] > info["w"]
            if por_seccion:
                tiempos = por_seccion["vertical" if vertical else "horizontal"]
                ancho = 160 if vertical else 288
                cuadros = [cuadro(v, t, ancho, tmp) for t in tiempos]
                filas.append((v, info, cuadros, "un cuadro por sección"))
                continue
            ancho = 216 if vertical else 384
            # 6 cuadros por clip, para ver el ritmo y la escalada (MARCA.md)
            dd = info["dur"]
            tiempos = [0.3, dd * 0.2, dd * 0.4, dd * 0.6, dd * 0.8, dd - 0.6]
            cuadros = [cuadro(v, t, ancho, tmp) for t in tiempos]
            filas.append((v, info, cuadros, "0 / 20 / 40 / 60 / 80 % / cierre"))
        fl = fuente_texto(28)
        sep, cab = 16, 44
        ancho_total = sep + max(sum(c.width + sep for c in cs) for _, _, cs, _ in filas)
        alto_total = sep + sum(cab + max(c.height for c in cs) + sep for _, _, cs, _ in filas)
        hoja = Image.new("RGB", (ancho_total, alto_total), PAPEL)
        d = ImageDraw.Draw(hoja)
        y = sep
        for v, info, cs, nota in filas:
            etiqueta = f"{v.stem}   ·   {info['dur']:.1f} s   ·   {nota}"
            d.text((sep, y + 6), etiqueta, font=fl, fill=TINTA)
            y += cab
            x = sep
            for c in cs:
                d.rectangle([x - 3, y - 3, x + c.width + 2, y + c.height + 2], fill=TINTA)
                hoja.paste(c, (x, y))
                x += c.width + sep
            y += max(c.height for c in cs) + sep
    destino = carpeta / "contact.png"
    hoja.save(destino)
    print(f"  ✔ {corta(destino)}")
    return destino


# ---------------------------------------------------------------- presentación del estudio
# Segmentos animados dibujados cuadro a cuadro con Pillow y pasados a ffmpeg por tubería.

def codificar_cuadros(cuadros, W: int, H: int, destino: Path) -> None:
    p = subprocess.Popen([FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest",
                          "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS),
                          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(destino)], stdin=subprocess.PIPE)
    for c in cuadros:
        p.stdin.write(c.convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit(f"ffmpeg falló codificando {destino.name}")


def n_cuadros(dur: float) -> int:
    return int(round(dur * FPS))


def escala_pop(t: float, t0: float = 0.0) -> float:
    """0 → 1,15 → 1 en 0,25 s (el "pop")."""
    x = t - t0
    if x <= 0:
        return 0.0
    if x < 0.12:
        return 1.15 * x / 0.12
    if x < 0.25:
        return 1.15 - 0.15 * (x - 0.12) / 0.13
    return 1.0


def globo_centrado(d: ImageDraw.ImageDraw, cx: int, y_abajo: int, lineas: list[str], fuente, cola_x: int) -> None:
    """Globo de texto (papel, borde tinta, sombra tinta) con la colita hacia abajo, apuntando a cola_x."""
    gw = int(max(fuente.getlength(l) for l in lineas)) + 64
    gh = len(lineas) * (alto_linea(fuente) + 4) + 44
    x0, y0 = cx - gw // 2, y_abajo - gh
    caja_marca(d, x0, y0, x0 + gw, y_abajo, PAPEL, TINTA, TINTA, 8)
    cx_cola = max(x0 + 40, min(x0 + gw - 40, cola_x))
    d.polygon([(cx_cola - 22, y_abajo - 6), (cx_cola + 22, y_abajo - 6), (cx_cola - 6, y_abajo + 40)], fill=TINTA)
    d.polygon([(cx_cola - 13, y_abajo - 8), (cx_cola + 13, y_abajo - 8), (cx_cola - 4, y_abajo + 24)], fill=PAPEL)
    y = y0 + 22
    for ln in lineas:
        d.text((cx - fuente.getlength(ln) / 2, y), ln, font=fuente, fill=TINTA)
        y += alto_linea(fuente) + 4


def seg_pop(W: int, H: int, dur: float, texto: str):
    vertical = H > W
    base = Image.open(BRAND / "personaje" / "agus-principal.png").convert("RGBA")
    lado = 460 if vertical else 420
    cx, cy = (540, 1060) if vertical else (W // 2, 660)
    ft = fuente_texto(64 if vertical else 66)
    lineas = partir_parejo(texto, ft, 720 if vertical else 1300)
    for i in range(n_cuadros(dur)):
        t = i / FPS
        img = Image.new("RGBA", (W, H), TINTA + (255,))
        d = ImageDraw.Draw(img)
        s = escala_pop(t, 0.05)
        if s > 0:
            l = max(2, int(lado * s))
            x0, y0 = cx - l // 2, cy - l // 2
            sh = max(2, int(10 * s))
            d.rectangle([x0 - 6 + sh, y0 - 6 + sh, x0 + l + 5 + sh, y0 + l + 5 + sh], fill=ROJO)
            d.rectangle([x0 - 6, y0 - 6, x0 + l + 5, y0 + l + 5], fill=TINTA)
            img.alpha_composite(base.resize((l, l), Image.NEAREST), (x0, y0))
        if t >= 0.45:
            globo_centrado(d, cx, cy - lado // 2 - 70, lineas, ft, cx + 40)
        yield img


def seg_logo(W: int, H: int, dur: float, con_texto: str | None = None):
    """El símbolo >_ (brand/logo, nearest neighbor en múltiplos de 16 px) aparece con un pop y abajo se "escribe"
    moscode.games como en una terminal, con el cursor rojo titilando. Con con_texto: el >_ titilando y un texto abajo
    (cartel "More coming soon…")."""
    vertical = H > W
    palabra = "moscode.games"
    logo = Image.open(BRAND / "logo" / "logo-512.png").convert("RGB")
    lado = (384 if vertical else 320) if con_texto is None else (448 if vertical else 384)
    logo = logo.resize((lado, lado), Image.NEAREST)
    # el cursor del logo-512 ocupa x 288–416, y 320–384: para que titile se lo tapa con tinta
    k = lado / 512
    cursor = (int(288 * k), int(320 * k), int(416 * k), int(384 * k))
    px = 56 if vertical else 96
    f = fuente_titulo(px)
    ft = fuente_texto(76 if vertical else 84)
    lineas = partir_parejo(con_texto, ft, 780 if vertical else 1400) if con_texto else []
    alto = lado + 60 + (px if not con_texto else len(lineas) * (alto_linea(ft) + 4))
    y_logo = (int(H * 0.40) if vertical else H // 2) - alto // 2
    escribir = dur * 0.55
    for i in range(n_cuadros(dur)):
        t = i / FPS
        img = Image.new("RGB", (W, H), TINTA)
        d = ImageDraw.Draw(img)
        s = escala_pop(t, 0.0) if not con_texto else 1.0
        if s > 0:
            l = max(16, int(lado * s) // 16 * 16)
            lg = logo if l == lado else logo.resize((l, l), Image.NEAREST)
            img.paste(lg, (W // 2 - l // 2, y_logo + (lado - l) // 2))
        titila = int(t / 0.3) % 2 == 1
        y_txt = y_logo + lado + 60
        if con_texto:
            if titila:
                x0 = W // 2 - lado // 2
                d.rectangle([x0 + cursor[0], y_logo + cursor[1], x0 + cursor[2], y_logo + cursor[3]], fill=TINTA)
            texto_centrado(d, W // 2, y_txt, lineas, ft, PAPEL)
        else:
            n = min(len(palabra), int(len(palabra) * max(0.0, t - 0.25) / escribir))
            x = (W - (len(palabra) + 1) * px) // 2
            for j, ch in enumerate(palabra[:n]):
                d.text((x, y_txt), ch, font=f, fill=PAPEL if j < len("moscode") else AMARILLO)
                x += px
            if n < len(palabra) or not titila:
                d.rectangle([x, y_txt + int(px * 0.78), x + px - 1, y_txt + px - 1], fill=ROJO)
        yield img


def seg_lineas(W: int, H: int, dur: float, l1: str, l2: str):
    vertical = H > W
    ft = fuente_texto(112 if vertical else 120)
    a = partir_parejo(l1, ft, 800 if vertical else 1600)
    b = partir_parejo(l2, ft, 800 if vertical else 1600)
    alto = (len(a) + len(b)) * (alto_linea(ft) + 6) + 40
    y0 = (int(H * 0.42) if vertical else H // 2) - alto // 2
    t2 = dur * 0.38
    for i in range(n_cuadros(dur)):
        t = i / FPS
        img = Image.new("RGB", (W, H), TINTA)
        d = ImageDraw.Draw(img)
        y = texto_centrado(d, W // 2, y0 - int(30 * max(0.0, 1 - t / 0.2)), a, ft, PAPEL, 6) + 40
        if t >= t2:
            texto_centrado(d, W // 2, y - int(30 * max(0.0, 1 - (t - t2) / 0.2)), b, ft, AMARILLO, 6)
        yield img


def seg_cierre(W: int, H: int, dur: float, cta: str):
    img = Image.new("RGBA", (W, H), TINTA + (255,))
    img.alpha_composite(capa_cierre(W, H, cta))
    for _ in range(n_cuadros(dur)):
        yield img


def cartelito(W: int, H: int, nombre: str, x: int, y: int) -> Image.Image:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = fuente_titulo(28 if H > W else 34)
    w = int(f.getlength(nombre))
    pad = 22
    caja_marca(d, x, y, x + w + 2 * pad, y + f.size + 2 * pad, AMARILLO, TINTA, ROJO, 8)
    d.text((x + pad, y + pad), nombre, font=f, fill=TINTA)
    return img


def seg_corte(W: int, H: int, dur: float, m: dict, idioma: str, destino: Path, capas: Path,
              modo: str = "blur") -> None:
    """Un corte de juego con el cartelito del nombre. Vertical en modo blur: pantalla entera 16:9 sobre el fondo
    desenfocado, con "zoom" opcional. Vertical en modo recorte u horizontal: "recorte" opcional."""
    vertical = H > W
    blur = vertical and modo == "blur"
    src = ruta_abs(str(por_idioma(m["fuente"], idioma)).replace("{idioma}", idioma))
    if not src.exists():
        sys.exit(f"No existe la grabación {src}")
    png = capas / f"cartel-{abs(hash((m['juego'], W, modo)))}.png"
    if not png.exists():
        if blur:
            capa = capa_marco(W, H)
            capa.alpha_composite(cartelito(W, H, m["juego"], 72, FG_Y - 100))
        else:
            capa = cartelito(W, H, m["juego"], 72 if vertical else 60, 430 if vertical else 50)
        capa.save(png)
    info = sondear(src)
    if blur:
        filtros = [cadena_blur("[0:v]", dur, m.get("zoom"), "[g]") + ";[g][1:v]overlay=0:0,format=yuv420p[v]"]
    else:
        ax, ay, aw, ah = (0, 560, 1080, 960) if vertical else (0, 0, W, H)
        crop = ""
        if m.get("recorte"):
            x, y, w, h = m["recorte"]
            crop = f"crop={w}:{h}:{x}:{y},"
        filtros = [f"[0:v]{crop}scale={aw}:{ah}:force_original_aspect_ratio=decrease:flags=lanczos,"
                   f"pad={W}:{H}:{ax}+({aw}-iw)/2:{ay}+({ah}-ih)/2:color=0x18191C,setsar=1,fps={FPS},"
                   f"{filtro_zoom(m.get('zoom'), W, H) if not vertical else ''}"
                   f"tpad=stop_mode=clone:stop_duration={dur:.3f},trim=duration={dur:.3f},setpts=PTS-STARTPTS[g];"
                   f"[g][1:v]overlay=0:0,format=yuv420p[v]"]
    cmd = [FFMPEG, "-y", "-v", "error", "-ss", f"{float(m.get('inicio', 0)):.3f}", "-t", f"{dur:.3f}", "-i", str(src),
           "-i", str(png)]
    if info["audio"]:
        filtros.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=duration={dur:.3f},"
                       f"asetpts=PTS-STARTPTS[a]")
    else:
        cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo"]
        filtros.append("[2:a]anull[a]")
    cmd += ["-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "fast",
            "-crf", "16", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{dur:.3f}",
            str(destino)]
    correr(cmd)


def cmd_presentacion(ruta: Path) -> None:
    """Video de presentación del estudio (skill /presentacion). Formato del JSON:
    {
      "salida": "_estudio/marketing/presentacion/2026-11-16",
      "idiomas": ["es"], "formatos": ["vertical", "horizontal"],      # por defecto solo español
      "textos": {"globo": {...}, "linea1": {...}, "linea2": {...}, "pronto": {...}, "cta": {...}},
      "itch": "moscode-games.itch.io",                 # va abajo del llamado a la acción en la horizontal
      "musica": {"fuente": ".../arbol_{idioma}_1920x1080.mp4", "inicio": 0, "volumen": 0.3},   # colchón de sonido
      "pronto": true,                                  # cartel "More coming soon…" (si hay menos de 3 juegos)
      "tiempos": {"vertical": {"pop": 2, "logo": 2, "corte": 2, "pronto": 2, "lineas": 4, "cierre": 2},
                  "horizontal": {"pop": 3, "logo": 3, "corte": 4, "pronto": 3, "lineas": 5, "cierre": 4}},
      "momentos": [{"juego": "NOMBRE", "formatos": ["vertical"], "fuente": "..._{idioma}_1920x1080.mp4",
                    "inicio": 5.2, "recorte": [x, y, w, h]}]
    }"""
    spec = json.loads(ruta.read_text(encoding="utf-8"))
    salida = ruta_abs(spec["salida"])
    salida.mkdir(parents=True, exist_ok=True)
    capas = salida / "_capas"
    capas.mkdir(exist_ok=True)
    tx = spec["textos"]
    secciones: dict[str, list[float]] = {}
    for formato in spec.get("formatos", ["vertical", "horizontal"]):
        vertical = formato == "vertical"
        W, H = (1080, 1920) if vertical else (1920, 1080)
        tm = spec["tiempos"][formato]
        momentos = [m for m in spec["momentos"] if formato in m.get("formatos", ["vertical", "horizontal"])]
        # para la hoja de contacto: un cuadro por sección (el globo ya visible, el logo escrito, cada corte, etc.)
        t, ts = 0.0, []
        partes = [("pop", 0.85), ("logo", 0.9)] + [("corte", 0.5)] * len(momentos) + \
            ([("pronto", 0.5)] if spec.get("pronto") else []) + [("lineas", 0.9), ("cierre", 0.5)]
        for nombre, frac in partes:
            ts.append(round(t + tm[nombre] * frac, 2))
            t += tm[nombre]
        secciones[formato] = ts
        for idioma in spec.get("idiomas", ["es"]):
            T = lambda k: por_idioma(tx[k], idioma)
            segs: list[Path] = []
            def nuevo(nombre: str) -> Path:
                p = capas / f"{formato}-{idioma}-{len(segs):02d}-{nombre}.mp4"
                segs.append(p)
                return p
            codificar_cuadros(seg_pop(W, H, tm["pop"], T("globo")), W, H, nuevo("pop"))
            codificar_cuadros(seg_logo(W, H, tm["logo"]), W, H, nuevo("logo"))
            for m in momentos:
                seg_corte(W, H, tm["corte"], m, idioma, nuevo("corte"), capas,
                          MODO_FORZADO or m.get("modo") or spec.get("modo") or "blur")
            if spec.get("pronto"):
                codificar_cuadros(seg_logo(W, H, tm["pronto"], T("pronto")), W, H, nuevo("pronto"))
            codificar_cuadros(seg_lineas(W, H, tm["lineas"], T("linea1"), T("linea2")), W, H, nuevo("lineas"))
            cta = T("cta") + ("" if vertical or not spec.get("itch") else "\n" + spec["itch"])
            codificar_cuadros(seg_cierre(W, H, tm["cierre"], cta), W, H, nuevo("cierre"))

            total = tm["pop"] + tm["logo"] + tm["corte"] * len(momentos) + tm["lineas"] + tm["cierre"] + \
                (tm["pronto"] if spec.get("pronto") else 0)
            lim = (15, 20) if vertical else (30, 45)
            if not lim[0] <= total <= lim[1]:
                avisar(f"{formato}-{idioma}: dura {total:g} s (lo pedido es {lim[0]}–{lim[1]} s)")
            lista = capas / f"{formato}-{idioma}.txt"
            lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
            destino = salida / f"presentacion-{formato}-{idioma}.mp4"
            cmd = [FFMPEG, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista)]
            mus = spec.get("musica")
            fa = f"afade=t=out:st={total - 0.8:.3f}:d=0.8"
            if mus:
                src = ruta_abs(str(por_idioma(mus["fuente"], idioma)).replace("{idioma}", idioma))
                cmd += ["-stream_loop", "-1", "-ss", f"{float(mus.get('inicio', 0)):.3f}", "-i", str(src)]
                vol = float(mus.get("volumen", 0.3))
                filtro = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={vol},atrim=duration={total:.3f},"
                          f"asetpts=PTS-STARTPTS,afade=t=in:d=0.4[b];"
                          f"[0:a][b]amix=inputs=2:duration=first:normalize=0,{fa}[a]")
            else:
                filtro = f"[0:a]{fa}[a]"
            cmd += ["-filter_complex", filtro, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-movflags", "+faststart", "-t", f"{total:.3f}", str(destino)]
            correr(cmd)
            mb = destino.stat().st_size / 1e6
            print(f"  ✔ {corta(destino)}  ({total:g} s, {mb:.1f} MB)")
    hoja_contacto(salida, secciones)
    shutil.rmtree(capas, ignore_errors=True)
    print(f"Listo, {len(avisos)} aviso(s)." if avisos else "Listo, sin avisos.")
    for a in avisos:
        print("  - " + a)


# ---------------------------------------------------------------- main
def cmd_tanda(ruta: Path, solo_capas: bool) -> None:
    tanda = json.loads(ruta.read_text(encoding="utf-8"))
    salida = ruta_abs(tanda["salida"])
    salida.mkdir(parents=True, exist_ok=True)
    capas = salida / "_capas"
    capas.mkdir(exist_ok=True)
    idiomas = tanda.get("idiomas", ["es"])
    print(f"Tanda {tanda.get('juego', '?')} → {salida}")
    for clip in tanda["clips"]:
        for idioma in idiomas:
            armar_clip(tanda, clip, idioma, salida, capas, solo_capas)
    if not solo_capas:
        hoja_contacto(salida)
        shutil.rmtree(capas, ignore_errors=True)
    else:
        print(f"  capas en {capas}")
    print(f"Listo, {len(avisos)} aviso(s)." if avisos else "Listo, sin avisos.")
    for a in avisos:
        print("  - " + a)


def main() -> None:
    global MODO_FORZADO
    if "--modo" in sys.argv:
        i = sys.argv.index("--modo")
        MODO_FORZADO = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
        if MODO_FORZADO not in ("blur", "recorte"):
            sys.exit("--modo tiene que ser blur o recorte")
        del sys.argv[i:i + 2]
    if len(sys.argv) < 3 or sys.argv[1] not in ("tanda", "probar", "contacto", "presentacion"):
        print(__doc__)
        sys.exit(1)
    for f in (FUENTE_TITULO, FUENTE_TEXTO):
        if not f.exists():
            sys.exit(f"Falta la fuente {f}")
    sub, arg = sys.argv[1], Path(sys.argv[2])
    if sub == "contacto":
        hoja_contacto(arg if arg.is_absolute() else ruta_abs(str(arg)))
    elif sub == "presentacion":
        cmd_presentacion(arg if arg.is_absolute() else Path.cwd() / arg)
    else:
        cmd_tanda(arg if arg.is_absolute() else Path.cwd() / arg, solo_capas=(sub == "probar"))


if __name__ == "__main__":
    main()
