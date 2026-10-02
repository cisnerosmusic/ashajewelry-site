"""Esqueleto común de todas las páginas: <head>, cabecera, pie y botón fijo."""
import html
import json
import urllib.parse

from herramientas import config
from herramientas.rutas import rel, ruta

MENU = ("catalogo", "servicios", "financiamiento", "como_llegar")


def esc(s):
    return html.escape(str(s), quote=True)


def tx(d, clave, l, **campos):
    """Texto `clave` de textos.json en el idioma `l`, con {campos} rellenos."""
    s = d["textos"][clave][l]
    return s.format(**campos) if campos else s


def enlace_contacto(d, l, mensaje=None):
    """(href, etiqueta) del contacto principal: WhatsApp si hay número
    confirmado en negocio.json; si no, una llamada."""
    n = d["negocio"]
    if n.get("whatsapp"):
        texto = mensaje or tx(d, "msg_general", l)
        numero = n["whatsapp"].lstrip("+")
        return (f"https://wa.me/{numero}?text={urllib.parse.quote(texto)}",
                tx(d, "cta_whatsapp", l))
    return f"tel:{n['telefono']}", tx(d, "cta_llamar", l)


def direccion_corta(d):
    a = d["negocio"]["direccion"]
    return f"{a['calle']}, {a['ciudad']}, {a['estado']} {a['cp']}"


def url_mapa(d):
    consulta = f"{d['negocio']['dentro_de']}, {direccion_corta(d)}"
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(consulta)


def jsonld(objetos):
    if not objetos:
        return ""
    s = json.dumps({"@context": "https://schema.org", "@graph": objetos}, ensure_ascii=False)
    return '<script type="application/ld+json">' + s.replace("</", "<\\/") + "</script>\n"


def pagina(d, l, aqui, alternos, titulo, descripcion, cuerpo, schema,
           actual=None, indexable=True, absoluto=False):
    """HTML completo de una página.

    `aqui`: ruta de la página ("catalogo/"). `alternos`: {idioma: ruta} de la
    misma página en cada idioma. `actual`: sección del menú resaltada.
    `indexable=False` (404): noindex siempre y sin canónica. `absoluto=True`
    (404): enlaces absolutos, porque Pages la sirve en cualquier profundidad.
    """
    base = config.url_publica()

    def r(destino):
        return esc(base + destino if absoluto else rel(aqui, destino))

    otro = "en" if l == "es" else "es"
    cabeza = []
    if not (config.LANZADO and indexable):
        cabeza.append('<meta name="robots" content="noindex, nofollow">')
    if indexable:
        cabeza.append(f'<link rel="canonical" href="{base}{aqui}">')
        cabeza += [f'<link rel="alternate" hreflang="{x}" href="{base}{alternos[x]}">'
                   for x in config.IDIOMAS]
        cabeza.append(f'<link rel="alternate" hreflang="x-default" href="{base}{alternos["es"]}">')
    cabeza = "\n".join(cabeza)
    marcado = ' aria-current="page"'
    nav = "".join(
        f'<li><a href="{r(ruta(s, l))}"{marcado if s == actual else ""}>{esc(tx(d, "nav_" + s, l))}</a></li>'
        for s in MENU)
    href_c, etiqueta_c = enlace_contacto(d, l)
    n = d["negocio"]
    v = config.VERSION
    locale = "es_US" if l == "es" else "en_US"
    return f"""<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)}</title>
<meta name="description" content="{esc(descripcion)}">
{cabeza}
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(descripcion)}">
<meta property="og:url" content="{base}{aqui}">
<meta property="og:image" content="{base}img/og.png">
<meta property="og:locale" content="{locale}">
<meta name="theme-color" content="#CFF2F6">
<link rel="icon" href="{r('favicon.svg')}" type="image/svg+xml">
<link rel="icon" href="{r('favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r('apple-touch-icon.png')}">
<link rel="preload" href="{r('fuentes/playfair-display-latin-600-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r('fuentes/montserrat-latin-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r('css/sitio.css')}?v={v}">
{jsonld(schema)}</head>
<body>
<a class="saltar" href="#contenido">{esc(tx(d, "saltar", l))}</a>
<header class="cabecera">
<a class="marca" href="{r(ruta("inicio", l))}"><img src="{r('img/insignia.jpg')}" width="56" height="56" alt=""><span>Asha Jewelry<small>Miami</small></span></a>
<button class="menu-boton" type="button" aria-expanded="false" aria-controls="menu" hidden>{esc(tx(d, "menu", l))}</button>
<nav id="menu" aria-label="{esc(tx(d, "menu", l))}"><ul>{nav}<li><a class="idioma" href="{r(alternos[otro])}" hreflang="{otro}" lang="{otro}">{esc(tx(d, "otro_idioma", l))}</a></li></ul></nav>
</header>
<main id="contenido">
{cuerpo}
</main>
<footer class="pie">
<div class="pie-fila">
<p><strong>{esc(n["nombre"])}</strong><br>{esc(tx(d, "dentro_de", l))}<br>{esc(direccion_corta(d))}</p>
<p>{esc(tx(d, "horario", l))}<br><a href="tel:{esc(n["telefono"])}">{esc(n["telefono_visible"])}</a><br><a href="{esc(n["instagram"])}" rel="noopener">Instagram @ashajewelryshop</a></p>
</div>
<p class="pie-legal">© 2026 {esc(n["nombre"])} · {esc(tx(d, "credito", l))} <a href="https://index01.net">Index01</a></p>
</footer>
<a class="contacto-fijo" href="{esc(href_c)}">{esc(etiqueta_c)}</a>
<script src="{r('js/sitio.js')}?v={v}" defer></script>
</body>
</html>
"""
