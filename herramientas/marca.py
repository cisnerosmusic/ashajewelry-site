"""Genera los iconos (el diamante del logo sobre círculo azul oscuro) y la
imagen para redes sociales (el logo completo de Adys en oro sobre oscuro).

Todo sale del vector original (marca/asha-logo.svg): PyMuPDF lo rasteriza
como máscara y se pinta con el degradado oficial. Se ejecuta a mano cuando
cambie la marca y la salida se versiona:
    python herramientas/marca.py
Necesita PyMuPDF (pip install pymupdf), solo para esta herramienta.
"""
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
if __package__ in (None, ""):
    sys.path.insert(0, str(RAIZ))

from herramientas.adornos import CAJA_DIAMANTE, DIAMANTE, GRADIENTE, LOGO  # noqa: E402

OSCURO = "#102A43"
BLANCO = "#FFFFFF"
LETRA = RAIZ / "estaticos" / "fuentes" / "raleway-latin-600-normal.woff2"
ESCALA = 4  # supermuestreo para bordes limpios


def _rgb(hexa):
    return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def _color(t):
    paradas = [(p, _rgb(c)) for p, c in GRADIENTE]
    for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
        if t <= t1:
            k = (t - t0) / (t1 - t0)
            return tuple(round(a + (b - a) * k) for a, b in zip(c0, c1))
    return paradas[-1][1]


def degradado(ancho, alto):
    """El degradado metálico del logo en diagonal, igual que el SVG de la web
    (x1=0 y1=0 x2=1 y2=1 sobre la caja de la pieza)."""
    tabla = [_color(i / 255) for i in range(256)]
    im = Image.new("RGB", (ancho, alto))
    px = im.load()
    for y in range(alto):
        for x in range(ancho):
            t = (x / max(ancho - 1, 1) + y / max(alto - 1, 1)) / 2
            px[x, y] = tabla[round(t * 255)]
    return im


def mascara(caja, ancho_px, trazo=None):
    """Rasteriza `trazo` (por defecto, el logo completo) dentro de `caja`
    (x, y, ancho, alto, en unidades del viewBox del logo) como máscara L de
    `ancho_px` de anchura."""
    x, y, w, h = caja
    trazo = trazo or LOGO[1]
    regla = LOGO[2]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
           f'width="{w}" height="{h}"><path fill="#000" fill-rule="{regla}" d="{trazo}"/></svg>')
    pagina = fitz.open(stream=svg.encode(), filetype="svg")[0]
    pix = pagina.get_pixmap(matrix=fitz.Matrix(ancho_px / w, ancho_px / w), alpha=True)
    return Image.frombytes("RGBA", (pix.width, pix.height), pix.samples).getchannel("A")


def pegar_oro(im, mascara_, x, y):
    im.paste(degradado(*mascara_.size), (round(x), round(y)), mascara_)


def icono(tam):
    """Círculo azul oscuro con anillo dorado y el diamante del logo."""
    t = tam * ESCALA
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse((0, 0, t - 1, t - 1), fill=OSCURO)
    anillo = Image.new("L", (t, t), 0)
    borde = max(ESCALA, round(t * 0.045))
    ImageDraw.Draw(anillo).ellipse((borde // 2, borde // 2, t - borde // 2 - 1, t - borde // 2 - 1),
                                   outline=255, width=borde)
    pegar_oro(im, anillo, 0, 0)
    m = mascara(CAJA_DIAMANTE, round(t * 0.6), DIAMANTE)
    pegar_oro(im, m, (t - m.width) / 2, (t - m.height) / 2)
    return im.resize((tam, tam), Image.LANCZOS)


def og():
    a, h = 1200 * ESCALA, 630 * ESCALA
    im = Image.new("RGBA", (a, h), OSCURO)
    x, y, w, alto = (float(v) for v in LOGO[0].split())
    m = mascara((x, y, w, alto), 720 * ESCALA)
    pegar_oro(im, m, (a - m.width) / 2, 70 * ESCALA)
    ImageDraw.Draw(im).text((600 * ESCALA, 560 * ESCALA), "MIAMI  ·  MERCADO FRESCO Y MÁS  ·  KIOSK 2",
                            font=ImageFont.truetype(str(LETRA), 26 * ESCALA), fill=BLANCO, anchor="mm")
    return im.resize((1200, 630), Image.LANCZOS).convert("RGB")


def generar(destino):
    destino = Path(destino)
    (destino / "img").mkdir(parents=True, exist_ok=True)
    salidas = []
    for nombre, tam in (("favicon-32.png", 32), ("apple-touch-icon.png", 180),
                        ("icon-192.png", 192), ("icon-512.png", 512)):
        ruta = destino / nombre
        im = icono(tam)
        if nombre == "apple-touch-icon.png":
            fondo = Image.new("RGB", im.size, OSCURO)
            fondo.paste(im, (0, 0), im)
            im = fondo
        im.save(ruta, optimize=True)
        salidas.append(ruta)
    ruta = destino / "img" / "og.png"
    og().save(ruta, optimize=True)
    salidas.append(ruta)
    return salidas


if __name__ == "__main__":
    for s in generar(RAIZ / "estaticos"):
        print(s.relative_to(RAIZ))
    sys.exit(0)
