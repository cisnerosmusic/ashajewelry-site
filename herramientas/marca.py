"""Genera los iconos (el diamante dorado del logo sobre círculo azul oscuro) y
la imagen para redes sociales (corona, ASHA y JEWELRY en oro sobre oscuro).

La geometría del diamante, la estrella y la floritura sale de adornos.py, la
misma que usa la web. Se ejecuta a mano cuando cambie la marca y la salida se
versiona:
    python herramientas/marca.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
if __package__ in (None, ""):
    sys.path.insert(0, str(RAIZ))

from herramientas.adornos import DIAMANTE_LINEAS, ORO_ALTO, ORO_BAJO, ORO_MEDIO  # noqa: E402

OSCURO = "#102A43"
ORO = "#BA8621"
BLANCO = "#FFFFFF"
MONTSERRAT = RAIZ / "estaticos" / "fuentes" / "montserrat-latin-600-normal.woff2"
ESCALA = 4  # supermuestreo para bordes limpios


def _fuente(ruta, tam, variacion="SemiBold"):
    f = ImageFont.truetype(str(ruta), tam)
    try:
        f.set_variation_by_name(variacion)
    except (OSError, ValueError):
        pass
    return f


def _rgb(hexa):
    return tuple(int(hexa[i:i + 2], 16) for i in (1, 3, 5))


def degradado(ancho, alto):
    """Oro de arriba (claro) a abajo (profundo), como en el logo."""
    paradas = [(0.0, _rgb(ORO_ALTO)), (0.45, _rgb(ORO_MEDIO)), (1.0, _rgb(ORO_BAJO))]
    columna = Image.new("RGB", (1, alto))
    for y in range(alto):
        t = y / max(alto - 1, 1)
        for (t0, c0), (t1, c1) in zip(paradas, paradas[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                columna.putpixel((0, y), tuple(round(a + (b - a) * k) for a, b in zip(c0, c1)))
                break
    return columna.resize((ancho, alto))


def pintar_oro(im, mascara):
    """Rellena con el degradado dorado lo que la máscara (L) marca, dentro de
    la caja que ocupa, para que cada pieza tenga su propio claro-oscuro."""
    caja = mascara.getbbox()
    if not caja:
        return
    x0, y0, x1, y1 = caja
    im.paste(degradado(x1 - x0, y1 - y0), (x0, y0), mascara.crop(caja))


def trazar_diamante(dib, x, y, ancho, grosor):
    """Dibuja el diamante en una máscara con su esquina superior izquierda en
    (x, y) y `ancho` de anchura (la caja original mide 100 x 80)."""
    k = ancho / 100
    for linea in DIAMANTE_LINEAS:
        puntos = [(x + px * k, y + py * k) for px, py in linea]
        dib.line(puntos, fill=255, width=grosor, joint="curve")
        for p in (puntos[0], puntos[-1]):
            r = grosor / 2
            dib.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=255)


def icono(tam):
    """Círculo azul oscuro con borde dorado y el diamante dentro."""
    t = tam * ESCALA
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    dib = ImageDraw.Draw(im)
    dib.ellipse((0, 0, t - 1, t - 1), fill=OSCURO)
    mascara = Image.new("L", (t, t), 0)
    md = ImageDraw.Draw(mascara)
    borde = max(ESCALA, round(t * 0.045))
    md.ellipse((borde // 2, borde // 2, t - borde // 2 - 1, t - borde // 2 - 1), outline=255, width=borde)
    ancho = t * 0.62
    # Grosor mayor en tamaños pequeños para que el diamante se lea a 32 px.
    grosor = max(ESCALA * 2, round(t * (0.05 if tam <= 64 else 0.026)))
    trazar_diamante(md, (t - ancho) / 2, (t - ancho * 0.8) / 2 + t * 0.02, ancho, grosor)
    pintar_oro(im, mascara)
    return im.resize((tam, tam), Image.LANCZOS)


def _bezier(p0, p1, p2, p3, pasos=24):
    return [tuple((1 - s) ** 3 * a + 3 * (1 - s) ** 2 * s * b + 3 * (1 - s) * s ** 2 * c + s ** 3 * e
                  for a, b, c, e in zip(p0, p1, p2, p3)) for s in (i / pasos for i in range(pasos + 1))]


def estrella(md, cx, cy, r):
    """Estrella de cuatro puntas con lados cóncavos (la de adornos.ESTRELLA)."""
    puntas = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    contorno = []
    for (ax, ay), (bx, by) in zip(puntas, puntas[1:] + puntas[:1]):
        # Mismos controles que el SVG: muy cerca del centro, lados hundidos.
        c1 = (ax * 0.2 + bx * 0.1, ay * 0.2 + by * 0.1)
        c2 = (ax * 0.1 + bx * 0.2, ay * 0.1 + by * 0.2)
        contorno += _bezier((ax, ay), c1, c2, (bx, by))
    md.polygon([(cx + x * r, cy + y * r) for x, y in contorno], fill=255)


def floritura(md, x, y, ancho, grosor, espejo=False):
    """Dos ondas cruzadas (la de adornos.FLORITURA), en una caja de 120 x 14."""
    k = ancho / 120

    def p(px, py):
        return (x + (120 - px if espejo else px) * k, y + py * k)

    for signo in (1, -1):
        a = _bezier((2, 7), (20, 7 - 8 * signo), (45, 7 - 8 * signo), (62, 7))
        b = _bezier((62, 7), (79, 7 + 8 * signo), (100, 7 + 8 * signo), (118, 7))
        md.line([p(*q) for q in a + b], fill=255, width=grosor, joint="curve")


def og():
    a, h = 1200 * ESCALA, 630 * ESCALA
    im = Image.new("RGBA", (a, h), OSCURO)
    E = ESCALA
    # Cada pieza dorada en su propia máscara, para que el degradado se ajuste a ella.
    piezas = []

    def nueva():
        m = Image.new("L", (a, h), 0)
        piezas.append(m)
        return ImageDraw.Draw(m)

    md = nueva()
    floritura(md, 318 * E, 118 * E, 240 * E, 3 * E)
    floritura(md, 642 * E, 118 * E, 240 * E, 3 * E, espejo=True)
    md = nueva()
    estrella(md, 522 * E, 92 * E, 14 * E)
    estrella(md, 678 * E, 92 * E, 14 * E)
    md = nueva()
    trazar_diamante(md, 550 * E, 52 * E, 100 * E, 4 * E)
    md = nueva()
    md.text((600 * E, 300 * E), "ASHA", font=_fuente(RAIZ / "herramientas" / "fuentes" / "PlayfairDisplay.ttf", 210 * E),
            fill=255, anchor="mm")
    md = nueva()
    md.text((612 * E, 440 * E), "J E W E L R Y", font=_fuente(MONTSERRAT, 40 * E), fill=255, anchor="mm")
    for m in piezas:
        pintar_oro(im, m)
    dib = ImageDraw.Draw(im)
    dib.text((600 * E, 540 * E), "MIAMI  ·  MERCADO FRESCO Y MÁS  ·  KIOSK 2",
             font=_fuente(MONTSERRAT, 26 * E), fill=BLANCO, anchor="mm")
    return im.resize((1200, 630), Image.LANCZOS).convert("RGB")


def generar(destino, fuente=None):
    """Escribe iconos e imagen OG en `destino`. `fuente` se mantiene por
    compatibilidad; la tipografía sale de estaticos/ y herramientas/fuentes/."""
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
