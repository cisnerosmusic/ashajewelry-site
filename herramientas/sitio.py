"""Genera publico/ completo desde datos/, estaticos/ e img/originales/, y lo
comprueba (contraste, raya larga, enlaces rotos).

Uso:  python herramientas/sitio.py
Sale con código 1 si algún dato o comprobación falla.
"""
import datetime
import shutil
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from herramientas import comprobar, config, imagenes, paginas  # noqa: E402
from herramientas.datos import ErrorDatos, cargar, provisionales  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent


def _limpiar(publico):
    """Vacía publico/ salvo img/fotos/, que hace de caché de imagenes.py."""
    publico.mkdir(parents=True, exist_ok=True)
    for x in publico.iterdir():
        if x.name == "img" and x.is_dir():
            for y in x.iterdir():
                if y.name != "fotos":
                    shutil.rmtree(y) if y.is_dir() else y.unlink()
            continue
        shutil.rmtree(x) if x.is_dir() else x.unlink()


def _escribir(ruta, texto):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


def generar(raiz=RAIZ, publico=None, hoy=None):
    raiz = Path(raiz)
    publico = Path(publico or raiz / "publico")
    hoy = hoy or datetime.date.today().isoformat()
    d = cargar(raiz / "datos")
    _limpiar(publico)
    shutil.copytree(raiz / "estaticos", publico, dirs_exist_ok=True)
    man = imagenes.procesar(raiz / "img" / "originales", publico / "img" / "fotos")
    pags = paginas.todas(d, man, hoy)
    for nombre, html in pags:
        _escribir(publico / nombre, html)
    _escribir(publico / "robots.txt", paginas.robots())
    _escribir(publico / "llms.txt", paginas.llms(d))
    if config.LANZADO:
        _escribir(publico / "sitemap.xml", paginas.sitemap(d))
        _escribir(publico / "CNAME", config.DOMINIO.split("//")[1].rstrip("/") + "\n")
    return d, pags


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8 por defecto
    try:
        d, pags = generar()
    except ErrorDatos as e:
        print("Datos con problemas:\n" + str(e))
        return 1
    print(f"{len(pags)} páginas generadas en publico/ · LANZADO={config.LANZADO} · {config.url_publica()}")
    n = provisionales(d)
    if n:
        print(f"Aviso: {n} elementos siguen con contenido provisional (ver PENDIENTES.md).")
    problemas = comprobar.todo(RAIZ, RAIZ / "publico")
    if problemas:
        print("Problemas:\n- " + "\n- ".join(problemas))
        return 1
    print("Comprobaciones: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
