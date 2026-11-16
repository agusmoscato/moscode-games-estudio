"""Portada de itch.io (630x500) para INFLATION, con la marca de _estudio/brand/MARCA.md.
Uso (desde JUEGOS/): py _estudio/marketing/itch/inflation/portada.py <captura_1920x1080.png> _estudio/marketing/itch/inflation/portada-630x500.png
La captura de base sale de: INFLATION-What-Inflation-/export/clips_crudos/precio_empanada_es_1920x1080.mp4 (segundo 1)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

RAIZ = Path(r"d:/Usuarios/Agustin/Documents/JUEGOS")
sys.path.insert(0, str(RAIZ / "_estudio" / "tools"))
sys.argv, args = [sys.argv[0]], sys.argv[1:]
import clip_tool as ct  # fuentes, colores y cajas de marca

src, out = Path(args[0]), Path(args[1])
W, H = 630, 500
# trabajo a 2x y bajo al final para bordes nítidos
K = 2
img = Image.new("RGB", (W * K, H * K), ct.TINTA)
juego = Image.open(src).convert("RGB")

# fondo: la pantalla del juego desenfocada y oscura (mismo criterio que el blur fill)
fondo = juego.resize((int(1920 * H * K / 1080), H * K), Image.LANCZOS)
x0 = (fondo.width - W * K) // 2
fondo = fondo.crop((x0, 0, x0 + W * K, H * K)).filter(ImageFilter.GaussianBlur(18))
fondo = ImageEnhance.Brightness(fondo).enhance(0.45)
img.paste(fondo, (0, 0))
d = ImageDraw.Draw(img)

# la empanada del juego (recorte de la captura, zona de la empanada) con marco tinta y sombra roja
emp = juego.crop((110, 210, 530, 495))            # solo la empanada (sin el contador de plata ni textos)
ew = 300 * K
emp = emp.resize((ew, int(ew * emp.height / emp.width)), Image.LANCZOS)
ex, ey = (W * K - ew) // 2, 186 * K
ct.caja_marca(d, ex - 6, ey - 6, ex + ew + 5, ey + emp.height + 5, ct.TINTA, ct.TINTA, ct.ROJO, 10 * K // 2)
img.paste(emp, (ex, ey))

# caja de título (amarilla, borde papel, sombra roja)
ft = ct.fuente_titulo(28 * K)
fs = ct.fuente_texto(30 * K)
t1, t2 = "INFLATION?", "What Inflation?"
bw = int(max(ft.getlength(t1), fs.getlength(t2))) + 60 * K
bx0 = (W * K - bw) // 2
by0, by1 = 34 * K, 34 * K + 120 * K
ct.caja_marca(d, bx0, by0, bx0 + bw, by1, ct.AMARILLO, ct.PAPEL, ct.ROJO, 8 * K, 4 * K)
ct.texto_centrado(d, W * K // 2, by0 + 26 * K, [t1], ft, ct.TINTA)
ct.texto_centrado(d, W * K // 2, by0 + 68 * K, [t2], fs, ct.TINTA)

# franja de abajo: >_ + @moscode.games y "Demo gratis"
logo = Image.open(RAIZ / "_estudio" / "brand" / "logo" / "logo-256.png").convert("RGB").resize((64 * K, 64 * K), Image.NEAREST)
img.paste(logo, (24 * K, H * K - 88 * K))
fm = ct.fuente_titulo(16 * K)
d.text((100 * K, H * K - 70 * K), "moscode", font=fm, fill=ct.PAPEL)
d.text((100 * K + fm.getlength("moscode"), H * K - 70 * K), ".games", font=fm, fill=ct.AMARILLO)
fd = ct.fuente_texto(26 * K)
txt = "Demo gratis"
tw = fd.getlength(txt)
d.text((W * K - 28 * K - tw, H * K - 76 * K), txt, font=fd, fill=ct.AMARILLO)

img.resize((W, H), Image.LANCZOS).save(out)
print("ok", out)
