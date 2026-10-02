"""Carga y valida datos/. Si algo no cuadra, lanza ErrorDatos con todos los
problemas juntos, para arreglarlos de una vez."""
import json
from pathlib import Path

from herramientas.config import IDIOMAS

NOMBRES = ("negocio", "textos", "servicios", "categorias", "piezas", "promos")
NEGOCIO_OBLIGATORIO = ("nombre", "direccion", "dentro_de", "telefono",
                       "telefono_visible", "dias", "instagram", "tiktok", "pagos")


class ErrorDatos(Exception):
    pass


def cargar(carpeta):
    carpeta = Path(carpeta)
    d = {n: json.loads((carpeta / f"{n}.json").read_text(encoding="utf-8")) for n in NOMBRES}
    validar(d)
    return d


def _bilingue(valor, donde, problemas):
    if not isinstance(valor, dict) or any(not valor.get(l) for l in IDIOMAS):
        problemas.append(f"{donde}: falta texto en algún idioma ({', '.join(IDIOMAS)})")


def _unicos(elementos, tipo, problemas):
    ids = set()
    slugs = {l: set() for l in IDIOMAS}
    for e in elementos:
        if e.get("id") in ids:
            problemas.append(f"{tipo}.{e.get('id')}: id repetido")
        ids.add(e.get("id"))
        for l in IDIOMAS:
            s = (e.get("slug") or {}).get(l)
            if s in slugs[l]:
                problemas.append(f"{tipo}.{e.get('id')}: slug repetido en {l} ({s})")
            slugs[l].add(s)
    return ids


def validar(d):
    p = []
    for campo in NEGOCIO_OBLIGATORIO:
        if not d["negocio"].get(campo):
            p.append(f"negocio.{campo}: falta")
    for clave, valor in d["textos"].items():
        _bilingue(valor, f"textos.{clave}", p)
    ids_cat = _unicos(d["categorias"], "categorias", p)
    for c in d["categorias"]:
        for campo in ("slug", "nombre"):
            _bilingue(c.get(campo), f"categorias.{c.get('id')}.{campo}", p)
    _unicos(d["piezas"], "piezas", p)
    for pz in d["piezas"]:
        donde = f"piezas.{pz.get('id')}"
        if pz.get("categoria") not in ids_cat:
            p.append(f"{donde}: categoría inexistente ({pz.get('categoria')})")
        for campo in ("slug", "nombre", "descripcion", "material"):
            _bilingue(pz.get(campo), f"{donde}.{campo}", p)
        precio = pz.get("precio")
        if precio is not None and (isinstance(precio, bool) or not isinstance(precio, (int, float)) or precio <= 0):
            p.append(f"{donde}: precio debe ser null o un número mayor que 0")
    _unicos(d["servicios"], "servicios", p)
    for s in d["servicios"]:
        for campo in ("slug", "titulo", "intro", "descripcion", "incluye"):
            _bilingue(s.get(campo), f"servicios.{s.get('id')}.{campo}", p)
    for pr in d["promos"]:
        _bilingue(pr.get("texto"), f"promos.{pr.get('id')}.texto", p)
        if not pr.get("desde") or not pr.get("hasta") or pr["desde"] > pr["hasta"]:
            p.append(f"promos.{pr.get('id')}: fechas desde/hasta inválidas")
    if p:
        raise ErrorDatos("\n".join(p))


def promo_vigente(promos, hoy):
    """La primera promo cuyo rango [desde, hasta] incluye `hoy` (AAAA-MM-DD)."""
    for pr in promos:
        if pr["desde"] <= hoy <= pr["hasta"]:
            return pr
    return None


def provisionales(d):
    """Cuántos elementos siguen con contenido provisional."""
    n = sum(1 for x in d["piezas"] + d["servicios"] if x.get("provisional"))
    return n + (1 if d["negocio"].get("provisional") else 0)
