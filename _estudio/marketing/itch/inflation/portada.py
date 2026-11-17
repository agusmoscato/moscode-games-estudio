"""Portada de itch.io (630x500) de INFLATION, igual al artboard "Itch" del canvas de identidad (Design):
fondo amarillo, borde tinta, título rojo con sombra, "DEMO GRATIS" y la etiqueta de precio tachado girada.
Uso (desde JUEGOS/): py _estudio/marketing/itch/inflation/portada.py"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "_estudio" / "tools"))
sys.argv = [sys.argv[0]]
import clip_tool as ct  # fuentes y colores de la marca

K = 3                               # se dibuja a 3x y se reduce: bordes nítidos
W, H = 630, 500
GRIS = (0x5F, 0x63, 0x6A)
s = lambda v: int(round(v * K))

img = Image.new("RGB", (s(W), s(H)), ct.AMARILLO)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, s(W) - 1, s(H) - 1], outline=ct.TINTA, width=s(8))

x, y = 44, 44                       # borde 8 + padding 36
GAP = 18
f_pre = ct.fuente_titulo(s(12))
d.text((s(x), s(y)), "MOSCODE.GAMES PRESENTA", font=f_pre, fill=ct.TINTA)
y += 12 * 1.6 + GAP
f_tit = ct.fuente_titulo(s(44))
d.text((s(x) + s(4), s(y) + s(4)), "INFLATION?", font=f_tit, fill=ct.TINTA)      # sombra dura
d.text((s(x), s(y)), "INFLATION?", font=f_tit, fill=ct.ROJO)
y += 44 * 1.25 + GAP
f_sub = ct.fuente_titulo(s(24))
d.text((s(x), s(y)), "What Inflation?", font=f_sub, fill=ct.TINTA)
y += 24 * 1.3 + GAP
f_txt = ct.fuente_texto(s(22), 400)
for ln in ct.partir("Un kiosco, precios que suben solos y vos remarcando para no fundirte.", f_txt, s(340)):
    d.text((s(x), s(y)), ln, font=f_txt, fill=ct.TINTA)
    y += 22 * 1.35

# botón DEMO GRATIS abajo a la izquierda (margin-top: auto)
f_btn = ct.fuente_titulo(s(14))
bw, bh = f_btn.getlength("DEMO GRATIS") + s(32), s(14) + s(28)
by1 = s(H - 44)
by0 = by1 - bh
d.rectangle([s(x) + s(5), by0 + s(5), s(x) + bw + s(5), by1 + s(5)], fill=ct.ROJO)
d.rectangle([s(x), by0, s(x) + bw, by1], fill=ct.TINTA)
d.text((s(x) + s(16), by0 + s(14)), "DEMO GRATIS", font=f_btn, fill=ct.AMARILLO)

# etiqueta de precio: papel, borde tinta 4, sombra tinta 6, girada -8° (antihorario), abajo a la derecha
f_viejo = ct.fuente_texto(s(18), 400)
f_nuevo = ct.fuente_texto(s(40), 700)
tw = max(f_viejo.getlength("$ 100"), f_nuevo.getlength("$ 1.250"))
ew, eh = int(tw) + s(36) + s(8), s(18 * 1.2) + s(40 * 1.15) + s(28) + s(8)
tag = Image.new("RGBA", (ew + s(6), eh + s(6)), (0, 0, 0, 0))
td = ImageDraw.Draw(tag)
td.rectangle([s(6), s(6), ew - 1 + s(6), eh - 1 + s(6)], fill=ct.TINTA)
td.rectangle([0, 0, ew - 1, eh - 1], fill=ct.TINTA)
td.rectangle([s(4), s(4), ew - 1 - s(4), eh - 1 - s(4)], fill=ct.PAPEL)
tx, ty = s(4) + s(18), s(4) + s(14)
td.text((tx, ty), "$ 100", font=f_viejo, fill=GRIS)
vw = f_viejo.getlength("$ 100")
ly = ty + s(18) * 0.62
td.line([tx, ly, tx + vw, ly], fill=GRIS, width=s(2))                           # tachado
td.text((tx, ty + s(18 * 1.2)), "$ 1.250", font=f_nuevo, fill=ct.ROJO)
rot = tag.rotate(8, resample=Image.BICUBIC, expand=True)                       # PIL: positivo = antihorario
cx, cy = s(W - 30) - ew // 2, s(H - 30) - eh // 2                               # centro de la caja sin rotar
img.paste(rot, (cx - rot.width // 2, cy - rot.height // 2), rot)

out = Path(__file__).with_name("portada-630x500.png")
img.resize((W, H), Image.LANCZOS).save(out)
print("ok", out)
