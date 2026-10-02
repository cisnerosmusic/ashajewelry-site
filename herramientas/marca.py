"""Genera los iconos (la "A" dorada sobre círculo aqua, como en sus
historias destacadas de Instagram) y la imagen para redes sociales.

Se ejecuta a mano cuando cambie la marca y la salida se versiona:
    python herramientas/marca.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUA = "#CFF2F6"
ORO = "#BA8621"
ORO_TINTA = "#7A5716"
TINTA = "#1A1408"
RAIZ = Path(__file__).resolve().parent.parent


def _fuente(ruta, tam):
    f = ImageFont.truetype(str(ruta), tam)
    try:
        f.set_variation_by_name("SemiBold")
    except (OSError, ValueError):
        pass
    return f


def icono(tam, fuente):
    """Círculo aqua con borde dorado y una A centrada, con supermuestreo."""
    escala = 4
    t = tam * escala
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    dib = ImageDraw.Draw(im)
    borde = max(escala, round(t * 0.05))
    dib.ellipse((borde // 2, borde // 2, t - borde // 2 - 1, t - borde // 2 - 1),
                fill=AQUA, outline=ORO, width=borde)
    f = _fuente(fuente, round(t * 0.6))
    dib.text((t / 2, t / 2), "A", font=f, fill=ORO_TINTA, anchor="mm")
    return im.resize((tam, tam), Image.LANCZOS)


def og(fuente):
    im = Image.new("RGB", (1200, 630), AQUA)
    circulo = icono(240, fuente)
    im.paste(circulo, (480, 70), circulo)
    dib = ImageDraw.Draw(im)
    dib.text((600, 400), "Asha Jewelry Miami", font=_fuente(fuente, 76), fill=TINTA, anchor="mm")
    dib.line((540, 462, 660, 462), fill=ORO, width=3)
    dib.text((600, 515), "Mercado Fresco y Más · Kiosk 2 · Miami, FL",
             font=_fuente(fuente, 34), fill=ORO_TINTA, anchor="mm")
    return im


def generar(destino, fuente):
    destino = Path(destino)
    (destino / "img").mkdir(parents=True, exist_ok=True)
    salidas = []
    for nombre, tam in (("favicon-32.png", 32), ("apple-touch-icon.png", 180),
                        ("icon-192.png", 192), ("icon-512.png", 512)):
        ruta = destino / nombre
        im = icono(tam, fuente)
        if nombre == "apple-touch-icon.png":
            fondo = Image.new("RGB", im.size, AQUA)
            fondo.paste(im, (0, 0), im)
            im = fondo
        im.save(ruta, optimize=True)
        salidas.append(ruta)
    ruta = destino / "img" / "og.png"
    og(fuente).save(ruta, optimize=True)
    salidas.append(ruta)
    return salidas


if __name__ == "__main__":
    for s in generar(RAIZ / "estaticos", RAIZ / "herramientas" / "fuentes" / "PlayfairDisplay.ttf"):
        print(s.relative_to(RAIZ))
    sys.exit(0)
