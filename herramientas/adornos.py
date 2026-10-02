"""Adornos de la marca en SVG, redibujados del logo de ASHA: el diamante, la
estrella de cuatro puntas (0, 90, 180 y 270 grados) y la floritura doble.

Todos pintan con el degradado dorado `url(#oro)`, que `DEFS` define una sola
vez por página (los SVG en línea de un mismo documento comparten ids).
Están pensados para ir sobre fondo oscuro.
"""

# Degradado medido en el logo dorado sobre fondo oscuro: claro arriba,
# más profundo abajo. Todos los tonos pasan 5:1 sobre --oscuro.
ORO_ALTO, ORO_MEDIO, ORO_BAJO = "#F0D07C", "#E2B954", "#C2943A"

DEFS = (
    '<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
    '<linearGradient id="oro" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{ORO_ALTO}"/><stop offset=".45" stop-color="{ORO_MEDIO}"/>'
    f'<stop offset="1" stop-color="{ORO_BAJO}"/></linearGradient></defs></svg>'
)

# Diamante en una caja de 100 x 80: tabla arriba, filetín a 26, punta abajo.
# Lista de trazos (cada uno, una polilínea); marca.py dibuja los mismos.
DIAMANTE_LINEAS = [
    [(22, 3), (78, 3), (97, 26), (50, 77), (3, 26), (22, 3)],  # silueta
    [(3, 26), (97, 26)],                                       # filetín
    [(22, 3), (36, 26), (50, 3), (64, 26), (78, 3)],           # corona en zigzag
    [(50, 3), (50, 77)], [(36, 26), (50, 77)], [(64, 26), (50, 77)],  # pabellón
]
DIAMANTE_TRAZOS = "".join(
    "M" + "L".join(f"{x} {y}" for x, y in linea) for linea in DIAMANTE_LINEAS)

# Estrella de cuatro puntas con lados cóncavos, centrada en (0, 0), radio 10.
ESTRELLA = "M0-10C1-2 2-1 10 0C2 1 1 2 0 10C-1 2-2 1-10 0C-2-1-1-2 0-10Z"

# Floritura: dos ondas cruzadas que forman un lazo doble, en 120 x 14.
FLORITURA = "M2 7C20-1 45-1 62 7S100 15 118 7M2 7C20 15 45 15 62 7S100-1 118 7"


def diamante(clase="diamante", grosor=4):
    return (f'<svg class="{clase}" viewBox="0 0 100 80" aria-hidden="true" focusable="false">'
            f'<path d="{DIAMANTE_TRAZOS}" fill="none" stroke="url(#oro)" stroke-width="{grosor}" '
            'stroke-linejoin="round" stroke-linecap="round"/></svg>')


def estrella(clase="estrella"):
    return (f'<svg class="{clase}" viewBox="-10 -10 20 20" aria-hidden="true" focusable="false">'
            f'<path d="{ESTRELLA}" fill="url(#oro)"/></svg>')


def corona():
    """El conjunto de encima de "ASHA": florituras, estrellas y diamante,
    en la misma disposición que el logo."""
    return (
        '<svg class="corona" viewBox="0 0 300 64" aria-hidden="true" focusable="false">'
        f'<g fill="none" stroke="url(#oro)" stroke-width="1.6" stroke-linecap="round">'
        f'<path transform="translate(8 40)" d="{FLORITURA}"/>'
        f'<path transform="translate(292 40) scale(-1 1)" d="{FLORITURA}"/></g>'
        f'<path transform="translate(112 20) scale(.7)" d="{ESTRELLA}" fill="url(#oro)"/>'
        f'<path transform="translate(188 20) scale(.7)" d="{ESTRELLA}" fill="url(#oro)"/>'
        f'<path transform="translate(126 2) scale(.48)" d="{DIAMANTE_TRAZOS}" fill="none" '
        'stroke="url(#oro)" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>'
        '</svg>'
    )


def separador():
    """Línea, estrella, línea: sustituye a la raya dorada simple."""
    return ('<div class="separador" aria-hidden="true"><span></span>'
            + estrella("estrella estrella-sep") + '<span></span></div>')
