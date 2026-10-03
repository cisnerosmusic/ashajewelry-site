"""Rutas de cada página en cada idioma y enlaces relativos entre ellas.

Una ruta es la carpeta de la página relativa a la raíz del sitio, con barra
final ("catalogo/"), o "" para la portada en español. Los enlaces internos
son siempre relativos: así el sitio funciona igual en la vista previa
(/ashajewelry-site/) que en el dominio.
"""
import posixpath

SECCIONES = {
    "inicio": {"es": "", "en": "en/"},
    "catalogo": {"es": "catalogo/", "en": "en/catalog/"},
    "servicios": {"es": "servicios/", "en": "en/services/"},
    "pagos": {"es": "formas-de-pago/", "en": "en/payment-options/"},
    "como_llegar": {"es": "como-llegar/", "en": "en/visit/"},
}


def ruta(seccion, l):
    return SECCIONES[seccion][l]


def ruta_pieza(pieza, l):
    return SECCIONES["catalogo"][l] + pieza["slug"][l] + "/"


def ruta_servicio(servicio, l):
    return SECCIONES["servicios"][l] + servicio["slug"][l] + "/"


def rel(desde, destino):
    """Enlace relativo desde la carpeta `desde` hasta `destino`.

    `destino` es una carpeta (termina en "/" o es "") o un archivo
    ("css/sitio.css"). Las carpetas devuelven siempre barra final.
    """
    base = desde.rstrip("/") or "."
    es_carpeta = destino == "" or destino.endswith("/")
    r = posixpath.relpath(destino.rstrip("/") or ".", base)
    if es_carpeta:
        return "./" if r == "." else r + "/"
    return r


def archivo(ruta_pagina):
    """Ruta del index.html de una página dentro de publico/."""
    return ruta_pagina + "index.html"
