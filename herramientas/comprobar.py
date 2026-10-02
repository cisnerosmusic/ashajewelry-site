"""Comprobaciones antes de publicar: contraste de la paleta, raya larga en
textos y enlaces internos rotos en publico/."""
import html
import re
from pathlib import Path

RAYA = "\u2014"
MINIMO_AA = 4.5
# (texto, fondo): cada par que el CSS usa para texto debe cumplir AA.
PARES_TEXTO = [
    ("tinta", "claro"), ("gris", "claro"),
    ("blanco", "oscuro"), ("oro-claro", "oscuro"), ("tinta", "oro"),
    ("blanco", "tinta"), ("oro-claro", "tinta"),
]
ESQUEMA = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
ATRIBUTO = re.compile(r'\s(?:href|src)="([^"]*)"')
SRCSET = re.compile(r'\ssrcset="([^"]*)"')


def _luminancia(hexa):
    canales = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contraste(a, b):
    la, lb = _luminancia(a), _luminancia(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def tokens_css(texto):
    return {m.group(1): m.group(2).upper()
            for m in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})", texto)}


def comprobar_contraste(css_texto):
    t = tokens_css(css_texto)
    problemas = []
    for texto, fondo in PARES_TEXTO:
        if texto not in t or fondo not in t:
            problemas.append(f"contraste: falta el color --{texto} o --{fondo} en el CSS")
            continue
        c = contraste(t[texto], t[fondo])
        if c < MINIMO_AA:
            problemas.append(f"contraste: --{texto} sobre --{fondo} = {c:.2f} (< {MINIMO_AA})")
    return problemas


def comprobar_rayas(archivos):
    return [f"raya larga en {a}" for a in archivos
            if RAYA in Path(a).read_text(encoding="utf-8")]


def _destinos(texto):
    for m in ATRIBUTO.finditer(texto):
        yield m.group(1)
    for m in SRCSET.finditer(texto):
        for parte in m.group(1).split(","):
            if parte.strip():
                yield parte.strip().split()[0]


def comprobar_enlaces(publico):
    publico = Path(publico).resolve()
    problemas = []
    for pagina in sorted(publico.rglob("*.html")):
        for crudo in _destinos(pagina.read_text(encoding="utf-8")):
            url = html.unescape(crudo)
            if not url or url.startswith(("#", "//")) or ESQUEMA.match(url):
                continue
            camino = url.split("#")[0].split("?")[0]
            if not camino:
                continue
            destino = (pagina.parent / camino).resolve()
            if camino.endswith("/") or destino.is_dir():
                destino = destino / "index.html"
            if publico not in destino.parents or not destino.is_file():
                problemas.append(f"enlace roto en {pagina.relative_to(publico)}: {crudo}")
    return problemas


def todo(raiz, publico):
    raiz, publico = Path(raiz), Path(publico)
    css = (raiz / "estaticos" / "css" / "sitio.css").read_text(encoding="utf-8")
    textos = sorted((raiz / "datos").glob("*.json")) + sorted(publico.rglob("*.html")) \
        + sorted(publico.glob("*.txt"))
    return comprobar_contraste(css) + comprobar_rayas(textos) + comprobar_enlaces(publico)
