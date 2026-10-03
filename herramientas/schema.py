"""JSON-LD de schema.org: la tienda (dentro de Fresco y Más), productos y
servicios. Lo que no está verificado (horas, geo, mapa) no se emite."""
from herramientas import config
from herramientas.rutas import ruta, ruta_pieza, ruta_servicio

DIAS = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday",
        "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"}


def id_tienda():
    return config.url_publica() + "#tienda"


def _direccion(a, con_unidad):
    calle = f"{a['calle']}, {a['unidad']}" if con_unidad and a.get("unidad") else a["calle"]
    return {"@type": "PostalAddress", "streetAddress": calle, "addressLocality": a["ciudad"],
            "addressRegion": a["estado"], "postalCode": a["cp"], "addressCountry": a["pais"]}


def tienda(d, l):
    n = d["negocio"]
    base = config.url_publica()
    t = {
        "@type": "JewelryStore",
        "@id": id_tienda(),
        "name": n["nombre"],
        "alternateName": n.get("marca"),
        "url": base + ruta("inicio", l),
        "telephone": n["telefono"],
        "image": base + "img/og.png",
        "logo": base + "img/insignia.jpg",
        "address": _direccion(n["direccion"], True),
        "containedInPlace": {"@type": "GroceryStore", "name": n["dentro_de"],
                             "address": _direccion(n["direccion"], False)},
        "paymentAccepted": ", ".join(n["pagos"] + ["Layaway"]),
        "sameAs": [n["instagram"], n["tiktok"]],
    }
    if n.get("apertura"):
        t["foundingDate"] = n["apertura"]
    if n.get("geo"):
        t["geo"] = {"@type": "GeoCoordinates", "latitude": n["geo"]["lat"],
                    "longitude": n["geo"]["lon"]}
    if n.get("mapa"):
        t["hasMap"] = n["mapa"]
    if n.get("horas"):
        t["openingHoursSpecification"] = [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [f"https://schema.org/{DIAS[x]}" for x in h["dias"]],
            "opens": h["abre"],
            "closes": h["cierra"],
        } for h in n["horas"]]
    return t


def producto(d, l, pieza, imagen=None):
    base = config.url_publica()
    o = {
        "@type": "Product",
        "name": pieza["nombre"][l],
        "description": pieza["descripcion"][l],
        "url": base + ruta_pieza(pieza, l),
        "brand": {"@type": "Brand", "name": d["negocio"].get("marca") or d["negocio"]["nombre"]},
        "material": pieza["material"][l],
    }
    if imagen:
        o["image"] = base + imagen
    if pieza.get("precio") is not None:
        disponible = pieza.get("disponible", True)
        o["offers"] = {
            "@type": "Offer",
            "price": f"{pieza['precio']:.2f}",
            "priceCurrency": "USD",
            "availability": "https://schema.org/" + ("InStock" if disponible else "OutOfStock"),
            "seller": {"@id": id_tienda()},
        }
    return o


def servicio(d, l, s):
    return {
        "@type": "Service",
        "name": s["titulo"][l],
        "description": s["intro"][l],
        "url": config.url_publica() + ruta_servicio(s, l),
        "provider": {"@id": id_tienda()},
        "areaServed": "Miami, FL",
    }
