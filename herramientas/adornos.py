"""Logo de ASHA y sus piezas, a partir del vector original de Adys
(marca/asha-logo.svg y marca/asha-solo-letras.svg, extraídos del PDF del kit).

El diamante y la estrella no se redibujan: son los subtrazados del propio
logo que caen dentro de su silueta. Todo pinta con el degradado dorado
`url(#oro)`; `DEFS` define degradado y trazados una sola vez por página y
cada uso es un <use>. Pensado para fondo oscuro.
"""
import re
from pathlib import Path

MARCA = Path(__file__).resolve().parent.parent / "marca"

# Colores oficiales de la ficha gráfica: oro #D5A332 y oro claro #FDCF55.
ORO, ORO_CLARO = "#D5A332", "#FDCF55"
# Degradado "metálico" de la versión dorada del logo de Adys, medido a lo largo
# de su diagonal: bronce, oro, el reflejo claro que cruza la S y la H, oro y
# bronce profundo. Es para el logo (gráfico); los botones usan ORO/ORO_CLARO.
GRADIENTE = [
    (0.0, "#A66706"), (0.18, "#B07F12"), (0.3, "#D6A635"), (0.42, "#F0C14A"),
    (0.52, "#FDCF55"), (0.62, "#F2C44B"), (0.72, "#D8A635"), (0.84, "#B7841A"),
    (1.0, "#9C6300"),
]

# Cajas medidas sobre el trazado del logo (unidades de su viewBox).
CAJA_DIAMANTE = (86.0, 0.0, 39.0, 29.4)
CAJA_ESTRELLA = (69.6, 4.7, 13.3, 13.3)
# Silueta del diamante (tabla, filetín y punta) con medio punto de margen.
DIAMANTE_SILUETA = [(91.3, -0.3), (119.7, -0.3), (125.4, 8.4), (105.45, 30.0), (85.5, 8.4)]


def _leer(nombre):
    texto = (MARCA / nombre).read_text(encoding="utf-8")
    caja = re.search(r'viewBox="([^"]+)"', texto).group(1)
    trazo = re.search(r' d="([^"]+)"', texto).group(1)
    regla = re.search(r'fill-rule="([^"]+)"', texto).group(1)
    return caja, trazo, regla


def _dentro(punto, poligono):
    x, y = punto
    dentro = False
    for (x1, y1), (x2, y2) in zip(poligono, poligono[1:] + poligono[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            dentro = not dentro
    return dentro


def subtrazos(trazo, poligono):
    """Los subtrazados (cada "M...") con todos sus puntos dentro del polígono."""
    elegidos = []
    for sub in ("M" + s for s in trazo.split("M") if s):
        n = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", sub)]
        if all(_dentro(p, poligono) for p in zip(n[0::2], n[1::2])):
            elegidos.append(sub)
    return "".join(elegidos)


def _rect(caja):
    x, y, w, h = caja
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


LOGO = _leer("asha-logo.svg")
LETRAS = _leer("asha-solo-letras.svg")
DIAMANTE = subtrazos(LOGO[1], DIAMANTE_SILUETA)
ESTRELLA = subtrazos(LOGO[1], _rect(CAJA_ESTRELLA))

DEFS = (
    '<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
    '<linearGradient id="oro" x1="0" y1="0" x2="1" y2="1">'
    + "".join(f'<stop offset="{t}" stop-color="{c}"/>' for t, c in GRADIENTE)
    + '</linearGradient>'
    f'<path id="asha-logo" fill-rule="{LOGO[2]}" d="{LOGO[1]}"/>'
    f'<path id="asha-letras" fill-rule="{LETRAS[2]}" d="{LETRAS[1]}"/>'
    f'<path id="asha-diamante" fill-rule="{LOGO[2]}" d="{DIAMANTE}"/>'
    f'<path id="asha-estrella" fill-rule="{LOGO[2]}" d="{ESTRELLA}"/>'
    '</defs></svg>'
)


def _svg(id_trazo, caja, clase, etiqueta=None):
    if not isinstance(caja, str):
        caja = " ".join(map(str, caja))
    accesible = (f'role="img" aria-label="{etiqueta}"' if etiqueta
                 else 'aria-hidden="true" focusable="false"')
    return (f'<svg class="{clase}" viewBox="{caja}" {accesible}>'
            f'<use href="#{id_trazo}" fill="url(#oro)"/></svg>')


def logo(clase="logo", etiqueta=None):
    """Logo completo: corona, ASHA y JEWELRY."""
    return _svg("asha-logo", LOGO[0], clase, etiqueta)


def letras(clase="letras", etiqueta=None):
    """Solo ASHA y JEWELRY, sin la corona."""
    return _svg("asha-letras", LETRAS[0], clase, etiqueta)


def diamante(clase="diamante"):
    return _svg("asha-diamante", CAJA_DIAMANTE, clase)


def estrella(clase="estrella"):
    return _svg("asha-estrella", CAJA_ESTRELLA, clase)


def separador():
    """Línea, estrella, línea."""
    return ('<div class="separador" aria-hidden="true"><span></span>'
            + estrella("estrella estrella-sep") + '<span></span></div>')
