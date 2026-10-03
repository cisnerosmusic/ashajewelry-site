"""Contenido de cada página. `todas()` devuelve [(archivo, html), ...] de las
dos lenguas más la 404."""
from herramientas import adornos, config, schema
from herramientas.datos import ErrorDatos, promo_vigente
from herramientas.plantilla import direccion_corta, enlace_contacto, esc, horario_html, pagina, tx, url_mapa
from herramientas.rutas import SECCIONES, archivo, rel, ruta, ruta_pieza, ruta_servicio

TAM_TARJETA = "(min-width: 48rem) 25vw, 50vw"
TAM_FICHA = "(min-width: 48rem) 50vw, 100vw"


def _alternos(seccion):
    return {x: ruta(seccion, x) for x in config.IDIOMAS}


def precio(d, l, p):
    if p.get("precio") is None:
        return tx(d, "consultar_precio", l)
    valor = float(p["precio"])
    return f"${valor:,.0f}" if valor.is_integer() else f"${valor:,.2f}"


def marco(d, l):
    t = esc(tx(d, "foto_proximamente", l))
    return (f'<div class="marco" role="img" aria-label="{t}">{adornos.diamante("diamante marco-diamante")}'
            f'<span class="marco-t" aria-hidden="true">{t}</span></div>')


def foto(d, l, aqui, item, man, tam, alt, carga="lazy"):
    if not item.get("fotos"):
        return marco(d, l)
    variantes = man[item["fotos"][0]]
    srcset = ", ".join(f"{esc(rel(aqui, p))} {w}w" for w, p in variantes)
    return (f'<img src="{esc(rel(aqui, variantes[-1][1]))}" srcset="{srcset}" sizes="{tam}" '
            f'alt="{esc(alt)}" loading="{carga}" decoding="async">')


def tarjeta(d, l, aqui, p, man):
    return (f'<li class="tarjeta"><a href="{esc(rel(aqui, ruta_pieza(p, l)))}">'
            f'<div class="tarjeta-foto">{foto(d, l, aqui, p, man, TAM_TARJETA, p["nombre"][l])}</div>'
            f'<h3>{esc(p["nombre"][l])}</h3><p class="material">{esc(p["material"][l])}</p>'
            f'<p class="precio">{esc(precio(d, l, p))}</p></a></li>')


def bloque_visita(d, l):
    n = d["negocio"]
    return (f'<dl class="datos">'
            f'<dt>{esc(tx(d, "direccion_t", l))}</dt><dd>{esc(tx(d, "dentro_de", l))}<br>{esc(direccion_corta(d))}</dd>'
            f'<dt>{esc(tx(d, "horario_t", l))}</dt><dd>{horario_html(d, l)}</dd>'
            f'<dt>{esc(tx(d, "telefono_t", l))}</dt><dd><a href="tel:{esc(n["telefono"])}">{esc(n["telefono_visible"])}</a></dd>'
            f'</dl><p><a class="boton boton-borde" href="{esc(url_mapa(d))}" rel="noopener">{esc(tx(d, "abrir_mapa", l))}</a></p>')


def lista_pagos(d, l):
    return "".join(f"<li>{esc(tx(d, x, l))}</li>" for x in ("pago_efectivo", "pago_tarjeta", "layaway"))


def inicio(d, l, man, hoy):
    aqui = ruta("inicio", l)
    href_c, etiqueta_c = enlace_contacto(d, l)
    promo = promo_vigente(d["promos"], hoy)
    bloque_promo = (f'<aside class="promo envoltura"><h2>{esc(tx(d, "promo_t", l))}</h2>'
                    f'<p>{esc(promo["texto"][l])}</p></aside>') if promo else ""
    destacadas = "".join(tarjeta(d, l, aqui, p, man) for p in d["piezas"] if p.get("destacada"))
    servicios_ = "".join(
        f'<li class="servicio"><h3>{esc(s["titulo"][l])}</h3><p>{esc(s["intro"][l])}</p>'
        f'<a href="{esc(rel(aqui, ruta_servicio(s, l)))}">{esc(tx(d, "ver_mas", l))}</a></li>'
        for s in d["servicios"])
    cuerpo = f"""<section class="portada">
<h1 class="logotipo">{adornos.logo("logo-portada", "ASHA Jewelry")}<span class="logo-miami">Miami</span></h1>
{adornos.separador()}
<p class="lema">{esc(tx(d, "lema", l))}</p>
<div class="acciones"><a class="boton boton-principal" href="{esc(href_c)}">{esc(etiqueta_c)}</a> <a class="boton boton-borde" href="{esc(rel(aqui, ruta("como_llegar", l)))}">{esc(tx(d, "cta_como_llegar", l))}</a></div>
</section>
<section class="seccion seccion-negra"><div class="envoltura muestra"><div class="muestra-foto">{foto(d, l, aqui, {"fotos": d["negocio"]["muestra_fotos"]}, man, TAM_FICHA, tx(d, "muestra_alt", l), "eager")}</div><div><h2>{esc(tx(d, "muestra_t", l))}</h2><p>{esc(tx(d, "muestra_p", l))}</p><p><a class="boton boton-principal" href="{esc(rel(aqui, ruta("catalogo", l)))}">{esc(tx(d, "ver_catalogo", l))}</a></p></div></div></section>
{bloque_promo}
<section class="seccion envoltura"><h2>{esc(tx(d, "inicio_destacadas", l))}</h2><ul class="rejilla">{destacadas}</ul>
<p class="mas"><a class="boton boton-borde" href="{esc(rel(aqui, ruta("catalogo", l)))}">{esc(tx(d, "ver_catalogo", l))}</a></p></section>
<section class="seccion seccion-oscura"><div class="envoltura"><h2>{esc(tx(d, "inicio_pagos_t", l))}</h2>
<p>{esc(tx(d, "inicio_pagos_p", l))}</p><ul class="pagos">{lista_pagos(d, l)}</ul>
<p><a href="{esc(rel(aqui, ruta("pagos", l)))}">{esc(tx(d, "ver_mas", l))}</a></p></div></section>
<section class="seccion envoltura"><h2>{esc(tx(d, "inicio_servicios", l))}</h2><ul class="servicios">{servicios_}</ul></section>
<section class="seccion seccion-oscura"><div class="envoltura"><h2>{esc(tx(d, "inicio_visita_t", l))}</h2>
<p>{esc(tx(d, "inicio_visita_p", l))}</p>{bloque_visita(d, l)}</div></section>"""
    return pagina(d, l, aqui, _alternos("inicio"), tx(d, "meta_inicio_t", l), tx(d, "meta_inicio_d", l),
                  cuerpo, [schema.tienda(d, l)], actual="inicio")


def catalogo(d, l, man):
    aqui = ruta("catalogo", l)
    usadas = [c for c in d["categorias"] if any(p["categoria"] == c["id"] for p in d["piezas"])]
    filtros = f'<a href="#" data-filtro="todas">{esc(tx(d, "todas", l))}</a>' + "".join(
        f'<a href="#{esc(c["slug"][l])}" data-filtro="{esc(c["id"])}">{esc(c["nombre"][l])}</a>' for c in usadas)
    secciones = "".join(
        f'<section class="categoria" id="{esc(c["slug"][l])}" data-categoria="{esc(c["id"])}">'
        f'<h2>{esc(c["nombre"][l])}</h2><ul class="rejilla">'
        + "".join(tarjeta(d, l, aqui, p, man) for p in d["piezas"] if p["categoria"] == c["id"])
        + "</ul></section>" for c in usadas)
    cuerpo = (f'<div class="seccion envoltura"><h1>{esc(tx(d, "nav_catalogo", l))}</h1>'
              f'<p class="entradilla">{esc(tx(d, "catalogo_intro", l))}</p>'
              f'<nav class="filtros" aria-label="{esc(tx(d, "nav_catalogo", l))}">{filtros}</nav>{secciones}</div>')
    return pagina(d, l, aqui, _alternos("catalogo"), tx(d, "meta_catalogo_t", l), tx(d, "meta_catalogo_d", l),
                  cuerpo, [schema.tienda(d, l)], actual="catalogo")


def ficha(d, l, p, man):
    aqui = ruta_pieza(p, l)
    cat = next(c for c in d["categorias"] if c["id"] == p["categoria"])
    href_c, _ = enlace_contacto(d, l, tx(d, "msg_pieza", l, nombre=p["nombre"][l], id=p["id"]))
    otras = [x for x in d["piezas"] if x["categoria"] == p["categoria"] and x["id"] != p["id"]][:4]
    relacionadas = (f'<section class="seccion"><h2>{esc(tx(d, "relacionadas", l))}</h2><ul class="rejilla">'
                    + "".join(tarjeta(d, l, aqui, x, man) for x in otras) + "</ul></section>") if otras else ""
    al_catalogo = rel(aqui, ruta("catalogo", l))
    cuerpo = f"""<div class="envoltura">
<p class="miga"><a href="{esc(al_catalogo)}">{esc(tx(d, "nav_catalogo", l))}</a> / <a href="{esc(al_catalogo + "#" + cat["slug"][l])}">{esc(cat["nombre"][l])}</a></p>
<article class="ficha"><div class="ficha-foto">{foto(d, l, aqui, p, man, TAM_FICHA, p["nombre"][l], "eager")}</div>
<div><h1>{esc(p["nombre"][l])}</h1><p class="material">{esc(p["material"][l])}</p><p class="precio">{esc(precio(d, l, p))}</p>
<p>{esc(p["descripcion"][l])}</p>
<p><a class="boton boton-principal" href="{esc(href_c)}">{esc(tx(d, "preguntar_pieza", l))}</a></p></div></article>
{relacionadas}</div>"""
    imagen = man[p["fotos"][0]][-1][1] if p.get("fotos") else None
    return pagina(d, l, aqui, {x: ruta_pieza(p, x) for x in config.IDIOMAS},
                  f'{p["nombre"][l]} · ASHA Jewelry Miami', p["descripcion"][l], cuerpo,
                  [schema.tienda(d, l), schema.producto(d, l, p, imagen)], actual="catalogo")


def servicios(d, l):
    aqui = ruta("servicios", l)
    items = "".join(
        f'<li class="servicio"><h2>{esc(s["titulo"][l])}</h2><p>{esc(s["intro"][l])}</p>'
        f'<a href="{esc(rel(aqui, ruta_servicio(s, l)))}">{esc(tx(d, "ver_mas", l))}</a></li>'
        for s in d["servicios"])
    cuerpo = (f'<div class="seccion envoltura"><h1>{esc(tx(d, "nav_servicios", l))}</h1>'
              f'<p class="entradilla">{esc(tx(d, "servicios_intro", l))}</p><ul class="servicios">{items}</ul></div>')
    return pagina(d, l, aqui, _alternos("servicios"), tx(d, "meta_servicios_t", l), tx(d, "meta_servicios_d", l),
                  cuerpo, [schema.tienda(d, l)] + [schema.servicio(d, l, s) for s in d["servicios"]],
                  actual="servicios")


def servicio(d, l, s, man):
    aqui = ruta_servicio(s, l)
    href_c, etiqueta_c = enlace_contacto(d, l)
    incluye = "".join(f"<li>{esc(x)}</li>" for x in s["incluye"][l])
    cuerpo = f"""<div class="envoltura">
<p class="miga"><a href="{esc(rel(aqui, ruta("servicios", l)))}">{esc(tx(d, "nav_servicios", l))}</a></p>
<article class="ficha"><div class="ficha-foto">{foto(d, l, aqui, s, man, TAM_FICHA, s["titulo"][l], "eager")}</div>
<div><h1>{esc(s["titulo"][l])}</h1><p class="entradilla">{esc(s["intro"][l])}</p><p>{esc(s["descripcion"][l])}</p>
<ul class="lista">{incluye}</ul>
<p><a class="boton boton-principal" href="{esc(href_c)}">{esc(etiqueta_c)}</a></p></div></article></div>"""
    return pagina(d, l, aqui, {x: ruta_servicio(s, x) for x in config.IDIOMAS},
                  f'{s["titulo"][l]} · ASHA Jewelry Miami', s["intro"][l], cuerpo,
                  [schema.tienda(d, l), schema.servicio(d, l, s)], actual="servicios")


def pagos(d, l):
    aqui = ruta("pagos", l)
    href_c, etiqueta_c = enlace_contacto(d, l)
    cuerpo = f"""<div class="seccion envoltura"><h1>{esc(tx(d, "nav_pagos", l))}</h1>
<p class="entradilla">{esc(tx(d, "pagos_intro", l))}</p>
<h2>{esc(tx(d, "pagos_aceptamos_t", l))}</h2><ul class="pagos">{lista_pagos(d, l)}</ul>
<h2>{esc(tx(d, "pagos_layaway_t", l))}</h2><p>{esc(tx(d, "pagos_layaway_p", l))}</p>
<h2>{esc(tx(d, "pagos_plazos_t", l))}</h2><p>{esc(tx(d, "pagos_plazos_p", l))}</p>
<p><a class="boton boton-principal" href="{esc(href_c)}">{esc(etiqueta_c)}</a></p></div>"""
    return pagina(d, l, aqui, _alternos("pagos"), tx(d, "meta_pagos_t", l),
                  tx(d, "meta_pagos_d", l), cuerpo, [schema.tienda(d, l)], actual="pagos")


def como_llegar(d, l, man):
    aqui = ruta("como_llegar", l)
    cuerpo = f"""<div class="seccion envoltura"><h1>{esc(tx(d, "nav_como_llegar", l))}</h1>
<p class="entradilla">{esc(tx(d, "como_llegar_intro", l))}</p>
<div class="ficha"><div class="ficha-foto">{foto(d, l, aqui, d["negocio"], man, TAM_FICHA, tx(d, "dentro_de", l), "eager")}</div>
<div>{bloque_visita(d, l)}</div></div></div>"""
    return pagina(d, l, aqui, _alternos("como_llegar"), tx(d, "meta_como_llegar_t", l),
                  tx(d, "meta_como_llegar_d", l), cuerpo, [schema.tienda(d, l)], actual="como_llegar")


def error404(d):
    base = config.url_publica()
    cuerpo = f"""<div class="seccion envoltura"><h1>{esc(tx(d, "e404_t", "es"))}</h1>
<p lang="en">{esc(tx(d, "e404_t", "en"))}</p>
<p class="acciones" style="justify-content:flex-start"><a class="boton boton-principal" href="{esc(base)}">{esc(tx(d, "volver_inicio", "es"))}</a>
<a class="boton boton-borde" href="{esc(base)}en/" lang="en">{esc(tx(d, "volver_inicio", "en"))}</a></p></div>"""
    return pagina(d, "es", "", _alternos("inicio"), tx(d, "e404_t", "es") + " · ASHA Jewelry Miami",
                  tx(d, "e404_t", "es"), cuerpo, [], indexable=False, absoluto=True)


def _comprobar_fotos(d, man):
    faltan = [f"{x.get('id', 'negocio')}: foto {f} no está en img/originales/"
              for x in d["piezas"] + d["servicios"] + [d["negocio"]]
              for f in x.get("fotos", []) if f not in man]
    faltan += [f"negocio.muestra_fotos: foto {f} no está en img/originales/"
               for f in d["negocio"].get("muestra_fotos", []) if f not in man]
    if faltan:
        raise ErrorDatos("\n".join(faltan))


def todas(d, man, hoy):
    _comprobar_fotos(d, man)
    salida = []
    for l in config.IDIOMAS:
        salida.append((archivo(ruta("inicio", l)), inicio(d, l, man, hoy)))
        salida.append((archivo(ruta("catalogo", l)), catalogo(d, l, man)))
        salida += [(archivo(ruta_pieza(p, l)), ficha(d, l, p, man)) for p in d["piezas"]]
        salida.append((archivo(ruta("servicios", l)), servicios(d, l)))
        salida += [(archivo(ruta_servicio(s, l)), servicio(d, l, s, man)) for s in d["servicios"]]
        salida.append((archivo(ruta("pagos", l)), pagos(d, l)))
        salida.append((archivo(ruta("como_llegar", l)), como_llegar(d, l, man)))
    salida.append(("404.html", error404(d)))
    return salida


def robots():
    if not config.LANZADO:
        return "User-agent: *\nDisallow: /\n"
    return f"User-agent: *\nAllow: /\n\nSitemap: {config.url_publica()}sitemap.xml\n"


def sitemap(d):
    base = config.url_publica()
    grupos = ([_alternos(s) for s in SECCIONES]
              + [{x: ruta_pieza(p, x) for x in config.IDIOMAS} for p in d["piezas"]]
              + [{x: ruta_servicio(s, x) for x in config.IDIOMAS} for s in d["servicios"]])
    urls = []
    for g in grupos:
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{base}{g[x]}"/>' for x in config.IDIOMAS)
        urls += [f"<url><loc>{base}{g[x]}</loc>{alt}</url>" for x in config.IDIOMAS]
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def llms(d):
    n = d["negocio"]
    base = config.url_publica()
    return f"""# {n["nombre"]}

> Joyería en un kiosko dentro de {n["dentro_de"]}, {direccion_corta(d)}. Oro 10K, 14K y 18K, reparación de joyas, ajuste de talla de anillos, grabado y joyas a medida. Efectivo, tarjeta y layaway; sin financiamiento propio. Horario: {tx(d, "horario", "es")}. Teléfono {n["telefono_visible"]}. Abrió en abril de 2026.

> Jewelry kiosk inside {n["dentro_de"]}, {direccion_corta(d)}. 10K, 14K and 18K gold, jewelry repair, ring sizing, engraving and custom jewelry. Cash, card and layaway; no in-house financing. Hours: {tx(d, "horario", "en")}.

Desambiguación / Disambiguation: no es ASHA by Ashley McCormick (Palm Beach) ni Asha Jewelry de Adelaida, Australia (ashajewelry.com). Not affiliated with either.

- [Inicio]({base})
- [Home (English)]({base}en/)
- [Catálogo]({base}{ruta("catalogo", "es")})
- [Servicios]({base}{ruta("servicios", "es")})
- [Cómo llegar]({base}{ruta("como_llegar", "es")})
- [Instagram]({n["instagram"]})
- [TikTok]({n["tiktok"]})
"""
