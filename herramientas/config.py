"""Ajustes del sitio que cambian al conectar el dominio."""

# False mientras el sitio vive en la vista previa de GitHub Pages: todas las
# páginas salen con noindex y robots.txt bloquea a todos. Al conectar
# ashajewelryusa.com se pone a True y se regenera.
LANZADO = False
DOMINIO = "https://ashajewelryusa.com/"
VISTA_PREVIA = "https://cisnerosmusic.github.io/ashajewelry-site/"
VERSION = "2"  # súbela cada vez que cambien estaticos/css o estaticos/js
IDIOMAS = ("es", "en")


def url_publica():
    """Raíz absoluta del sitio, con barra final."""
    return DOMINIO if LANZADO else VISTA_PREVIA
