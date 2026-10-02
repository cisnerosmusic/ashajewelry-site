# Asha Jewelry Miami · plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sitio estático bilingüe (ES raíz, EN en `/en/`) de Asha Jewelry Miami, generado desde `datos/` a `publico/` y publicado en GitHub Pages con `noindex` hasta conectar `ashajewelryusa.com`.

**Architecture:** Generador en Python con la librería estándar (Pillow solo para imágenes): `herramientas/` lee `datos/*.json`, copia `estaticos/` y escribe `publico/`, que es lo único que se sirve, vía GitHub Actions. Todos los enlaces internos son relativos, así que el mismo `publico/` funciona en `/ashajewelry-site/` y en el dominio. Canónicas, hreflang, sitemap y Open Graph usan `config.url_publica()`.

**Tech Stack:** Python 3.12, Pillow 12, unittest, HTML/CSS/JS sin frameworks, GitHub Actions (`actions/deploy-pages`).

Spec: `docs/superpowers/specs/2026-10-02-ashajewelry-site-design.md`.

## Global Constraints

- El HTML nunca se edita a mano: se regenera con `python herramientas/sitio.py`.
- Solo `publico/` se publica. `README.md`, `CLAUDE.md`, `PENDIENTES.md`, `docs/`, `datos/` y `herramientas/` nunca llegan a Pages.
- `LANZADO = False`: todas las páginas llevan `<meta name="robots" content="noindex, nofollow">` y `robots.txt` lleva `Disallow: /`.
- No se publica ningún dato sin fuente. Lo no verificado (horas, WhatsApp, geo) queda en `null` y no se muestra.
- Sin raya larga (U+2014) en `datos/` ni en `publico/`.
- Español en la raíz y espejo completo en inglés en `/en/`.
- Paleta: `--aqua #CFF2F6`, `--oro-claro #DEAC3B`, `--oro #BA8621`, `--oro-tinta #7A5716`, `--tinta #1A1408`, `--blanco #FFFFFF`. Los dorados de texto sobre fondo claro solo pueden ser `--oro-tinta`. Todo texto debe cumplir AA (4.5:1).
- Tipografía: Playfair Display 600 para títulos y Montserrat 400/600 para texto, autoalojadas en WOFF2.
- Sin fotos de stock ni generadas con IA. Las fotos que faltan se sustituyen por el marco "Foto próximamente / Photo coming soon".
- Commits con identidad `Ernesto Cisneros <ernestocisnerosmusic@gmail.com>` (ya configurada en el repo) y la línea `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Comando de pruebas, desde la raíz del repo: `python -m unittest discover -s tests -t . -v`.

## Estructura de archivos

```
.gitattributes                 # LF en todo
.gitignore                     # __pycache__
.github/workflows/pages.yml    # sube publico/ a Pages
README.md · CLAUDE.md · PENDIENTES.md
datos/negocio.json textos.json servicios.json categorias.json piezas.json promos.json
estaticos/                     # se copia tal cual a publico/
  css/sitio.css  js/sitio.js
  fuentes/*.woff2 + OFL.txt
  img/insignia.jpg (avatar de TikTok, 480 px)  img/og.png
  favicon.svg favicon-32.png apple-touch-icon.png icon-192.png icon-512.png
img/originales/.gitkeep        # fotos tal como llegan
herramientas/__init__.py
  config.py     # LANZADO, dominios, VERSION, IDIOMAS
  rutas.py      # rutas por idioma y enlaces relativos
  datos.py      # carga y valida datos/
  comprobar.py  # contraste, rayas, enlaces rotos
  schema.py     # JSON-LD
  plantilla.py  # <head>, cabecera, pie, contacto
  paginas.py    # cuerpo de cada página, sitemap, robots, llms
  imagenes.py   # originales a WebP
  marca.py      # favicons y og.png (se ejecuta a mano y se versiona la salida)
  sitio.py      # orquesta: genera publico/ y comprueba
  fuentes/PlayfairDisplay.ttf  # solo para marca.py, no se publica
tests/__init__.py test_rutas.py test_datos.py test_comprobar.py test_schema.py
      test_plantilla.py test_imagenes.py test_marca.py test_sitio.py
publico/                       # generado y versionado
```

---

### Task 1: Esqueleto, configuración y rutas

**Files:**
- Create: `.gitattributes`, `.gitignore`, `herramientas/__init__.py`, `herramientas/config.py`, `herramientas/rutas.py`, `tests/__init__.py`, `tests/test_rutas.py`
- Modify: `docs/superpowers/specs/2026-10-02-ashajewelry-site-design.md` (sección 5, viñeta `BASE`)

**Interfaces:**
- Produces: `config.LANZADO: bool`, `config.DOMINIO: str`, `config.VISTA_PREVIA: str`, `config.VERSION: str`, `config.IDIOMAS = ("es", "en")`, `config.url_publica() -> str` (con barra final). `rutas.SECCIONES: dict[str, dict[str, str]]`, `rutas.ruta(seccion, l) -> str`, `rutas.ruta_pieza(pieza, l) -> str`, `rutas.ruta_servicio(servicio, l) -> str`, `rutas.rel(desde, destino) -> str`, `rutas.archivo(ruta) -> str`.

- [ ] **Step 1: Archivos base**

`.gitattributes`:
```
* text=auto eol=lf
*.png binary
*.jpg binary
*.webp binary
*.woff2 binary
*.ttf binary
```

`.gitignore`:
```
__pycache__/
*.pyc
```

`herramientas/__init__.py` y `tests/__init__.py`: vacíos.

`herramientas/config.py`:
```python
"""Ajustes del sitio que cambian al conectar el dominio."""

# False mientras el sitio vive en la vista previa de GitHub Pages: todas las
# páginas salen con noindex y robots.txt bloquea a todos. Al conectar
# ashajewelryusa.com se pone a True y se regenera.
LANZADO = False
DOMINIO = "https://ashajewelryusa.com/"
VISTA_PREVIA = "https://cisnerosmusic.github.io/ashajewelry-site/"
VERSION = "1"  # súbela cada vez que cambien estaticos/css o estaticos/js
IDIOMAS = ("es", "en")


def url_publica():
    """Raíz absoluta del sitio, con barra final."""
    return DOMINIO if LANZADO else VISTA_PREVIA
```

- [ ] **Step 2: Prueba que falla**

`tests/test_rutas.py`:
```python
import unittest

from herramientas import rutas


class TestRutas(unittest.TestCase):
    def test_portada_espanol_es_raiz(self):
        self.assertEqual(rutas.ruta("inicio", "es"), "")
        self.assertEqual(rutas.ruta("inicio", "en"), "en/")

    def test_secciones_en_ingles(self):
        self.assertEqual(rutas.ruta("como_llegar", "en"), "en/visit/")
        self.assertEqual(rutas.ruta("financiamiento", "es"), "financiamiento/")

    def test_ruta_pieza_y_servicio(self):
        pieza = {"slug": {"es": "anillo-de-oro", "en": "gold-ring"}}
        self.assertEqual(rutas.ruta_pieza(pieza, "en"), "en/catalog/gold-ring/")
        servicio = {"slug": {"es": "grabado", "en": "engraving"}}
        self.assertEqual(rutas.ruta_servicio(servicio, "es"), "servicios/grabado/")

    def test_rel_desde_raiz(self):
        self.assertEqual(rutas.rel("", "en/"), "en/")
        self.assertEqual(rutas.rel("", ""), "./")

    def test_rel_misma_carpeta(self):
        self.assertEqual(rutas.rel("en/", "en/"), "./")

    def test_rel_ficha_a_raiz(self):
        self.assertEqual(rutas.rel("catalogo/anillo-de-oro/", ""), "../../")

    def test_rel_a_archivo(self):
        self.assertEqual(rutas.rel("en/catalog/gold-ring/", "css/sitio.css"), "../../../css/sitio.css")

    def test_archivo(self):
        self.assertEqual(rutas.archivo(""), "index.html")
        self.assertEqual(rutas.archivo("en/visit/"), "en/visit/index.html")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Verificar que falla**

Run: `python -m unittest discover -s tests -t . -v`
Expected: ERROR `ImportError: cannot import name 'rutas'`

- [ ] **Step 4: Implementación**

`herramientas/rutas.py`:
```python
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
    "financiamiento": {"es": "financiamiento/", "en": "en/financing/"},
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
```

- [ ] **Step 5: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 8 tests OK

- [ ] **Step 6: Actualizar la spec**

En la sección 5 de la spec, sustituye la viñeta que empieza por `- **\`BASE\`**` por:
```
- **Enlaces relativos**: todos los enlaces internos son relativos (`rutas.rel`), así que el mismo `publico/` funciona en `/ashajewelry-site/` y en el dominio. Solo canónicas, hreflang, sitemap y Open Graph usan URL absoluta, con `config.url_publica()`: la vista previa mientras `LANZADO = False` y `https://ashajewelryusa.com/` después.
```
Y en la sección 9, en "Conexión del dominio", cambia `` `BASE = "/"`, `LANZADO = True` `` por `` `LANZADO = True` ``.

- [ ] **Step 7: Commit**

```bash
git add .gitattributes .gitignore herramientas tests docs/superpowers/specs
git commit -m "Esqueleto: configuración, rutas por idioma y enlaces relativos

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Datos y validación

**Files:**
- Create: `datos/negocio.json`, `datos/textos.json`, `datos/servicios.json`, `datos/categorias.json`, `datos/piezas.json`, `datos/promos.json`, `herramientas/datos.py`, `tests/test_datos.py`

**Interfaces:**
- Consumes: `config.IDIOMAS`.
- Produces: `datos.NOMBRES` (tupla de nombres de archivo sin `.json`), `datos.ErrorDatos(Exception)`, `datos.cargar(carpeta) -> dict` (claves = NOMBRES), `datos.validar(d) -> None` (lanza `ErrorDatos` con todos los problemas separados por `\n`), `datos.promo_vigente(promos, hoy_iso) -> dict | None`, `datos.provisionales(d) -> int`.
- Forma de los datos: los campos bilingües son `{"es": str, "en": str}`. `incluye` es `{"es": [str], "en": [str]}`. `precio` es `null` o un número mayor que 0. `fotos` es una lista de nombres base de archivo de `img/originales/` sin extensión.

- [ ] **Step 1: Datos**

`datos/negocio.json`:
```json
{
  "nombre": "Asha Jewelry Miami",
  "marca": "ASHA Jewelry",
  "apertura": "2026-04-14",
  "direccion": {
    "calle": "12107 SW 152nd St",
    "unidad": "Kiosk 2",
    "ciudad": "Miami",
    "estado": "FL",
    "cp": "33177",
    "pais": "US"
  },
  "dentro_de": "Mercado Fresco y Más",
  "geo": null,
  "telefono": "+17869781981",
  "telefono_visible": "786-978-1981",
  "whatsapp": null,
  "dias": ["Tu", "We", "Th", "Fr", "Sa", "Su"],
  "horas": null,
  "instagram": "https://www.instagram.com/ashajewelryshop/",
  "pagos": ["Affirm", "Afterpay", "Klarna", "Zip", "Shop Pay"],
  "fotos": [],
  "provisional": true
}
```

`datos/textos.json`:
```json
{
  "lema": {"es": "Oro auténtico 10K, 14K y 18K, con financiamiento, dentro de Fresco y Más", "en": "Authentic 10K, 14K and 18K gold, with financing, inside Fresco y Más"},
  "nav_catalogo": {"es": "Catálogo", "en": "Catalog"},
  "nav_servicios": {"es": "Servicios", "en": "Services"},
  "nav_financiamiento": {"es": "Financiamiento", "en": "Financing"},
  "nav_como_llegar": {"es": "Cómo llegar", "en": "Visit us"},
  "menu": {"es": "Menú", "en": "Menu"},
  "saltar": {"es": "Saltar al contenido", "en": "Skip to content"},
  "otro_idioma": {"es": "English", "en": "Español"},
  "cta_whatsapp": {"es": "Escríbenos por WhatsApp", "en": "Message us on WhatsApp"},
  "cta_llamar": {"es": "Llámanos", "en": "Call us"},
  "cta_como_llegar": {"es": "Cómo llegar", "en": "Get directions"},
  "dentro_de": {"es": "Dentro de Mercado Fresco y Más, kiosko 2", "en": "Inside Mercado Fresco y Más, kiosk 2"},
  "horario": {"es": "Martes a domingo · Lunes cerrado", "en": "Tuesday to Sunday · Closed on Mondays"},
  "credito": {"es": "Sitio por", "en": "Website by"},
  "foto_proximamente": {"es": "Foto próximamente", "en": "Photo coming soon"},
  "consultar_precio": {"es": "Consultar precio", "en": "Ask for price"},
  "preguntar_pieza": {"es": "Pregunta por esta pieza", "en": "Ask about this piece"},
  "msg_pieza": {"es": "Hola, me interesa esta pieza de su web: {nombre} ({id})", "en": "Hi, I'm interested in this piece from your website: {nombre} ({id})"},
  "msg_general": {"es": "Hola, vi su web y tengo una pregunta", "en": "Hi, I saw your website and have a question"},
  "ver_catalogo": {"es": "Ver el catálogo", "en": "See the catalog"},
  "ver_mas": {"es": "Más información", "en": "Learn more"},
  "todas": {"es": "Todas", "en": "All"},
  "relacionadas": {"es": "También te puede gustar", "en": "You may also like"},
  "inicio_destacadas": {"es": "Piezas destacadas", "en": "Featured pieces"},
  "inicio_servicios": {"es": "Reparamos, ajustamos y creamos", "en": "We repair, resize and create"},
  "inicio_financiamiento_t": {"es": "Llévatela hoy, págala a tu ritmo", "en": "Take it home today, pay at your pace"},
  "inicio_financiamiento_p": {"es": "Aceptamos Affirm, Afterpay, Klarna, Zip y Shop Pay, y tenemos layaway.", "en": "We accept Affirm, Afterpay, Klarna, Zip and Shop Pay, and we offer layaway."},
  "inicio_visita_t": {"es": "Te esperamos en el kiosko 2", "en": "Come see us at kiosk 2"},
  "inicio_visita_p": {"es": "Estamos dentro de Mercado Fresco y Más. Si pasas por aquí, no te vas con las manos vacías.", "en": "We're inside Mercado Fresco y Más. Stop by and you won't leave empty-handed."},
  "promo_t": {"es": "Promoción del mes", "en": "This month's offer"},
  "layaway": {"es": "Layaway", "en": "Layaway"},
  "catalogo_intro": {"es": "Una muestra de lo que tenemos en la vitrina. Las piezas cambian a menudo: si buscas algo concreto, escríbenos.", "en": "A sample of what's in our display case. Pieces change often, so if you're looking for something specific, get in touch."},
  "servicios_intro": {"es": "Arreglamos la joya que ya tienes y hacemos la que imaginas.", "en": "We fix the jewelry you already own and make the piece you have in mind."},
  "financiamiento_intro": {"es": "Elige cómo pagar. Las condiciones dependen de cada plataforma y de su aprobación; te las explicamos en el kiosko.", "en": "Choose how to pay. Terms depend on each platform and on approval; we'll walk you through them at the kiosk."},
  "financiamiento_plataformas_t": {"es": "Plataformas que aceptamos", "en": "Platforms we accept"},
  "financiamiento_layaway_t": {"es": "Layaway (apartado)", "en": "Layaway"},
  "financiamiento_layaway_p": {"es": "Aparta tu pieza y págala poco a poco. Pregúntanos las condiciones.", "en": "Reserve your piece and pay it off little by little. Ask us for the details."},
  "como_llegar_intro": {"es": "Estamos dentro de Mercado Fresco y Más, en el kiosko 2.", "en": "We're inside Mercado Fresco y Más, at kiosk 2."},
  "direccion_t": {"es": "Dirección", "en": "Address"},
  "horario_t": {"es": "Horario", "en": "Hours"},
  "telefono_t": {"es": "Teléfono", "en": "Phone"},
  "abrir_mapa": {"es": "Abrir en Google Maps", "en": "Open in Google Maps"},
  "e404_t": {"es": "Esta página no existe", "en": "This page doesn't exist"},
  "volver_inicio": {"es": "Volver al inicio", "en": "Back to home"},
  "meta_inicio_t": {"es": "Asha Jewelry Miami · Joyería dentro de Fresco y Más (33177)", "en": "Asha Jewelry Miami · Jewelry store inside Fresco y Más (33177)"},
  "meta_inicio_d": {"es": "Oro auténtico 10K, 14K y 18K, reparación de joyas, ajuste de anillos y grabado. Financiamiento y layaway. Kiosko 2 dentro de Mercado Fresco y Más, Miami.", "en": "Authentic 10K, 14K and 18K gold, jewelry repair, ring sizing and engraving. Financing and layaway. Kiosk 2 inside Mercado Fresco y Más, Miami."},
  "meta_catalogo_t": {"es": "Catálogo de joyas de oro · Asha Jewelry Miami", "en": "Gold jewelry catalog · Asha Jewelry Miami"},
  "meta_catalogo_d": {"es": "Anillos, pulseras, cadenas, dijes y aretes de oro en nuestro kiosko de Fresco y Más, Miami.", "en": "Gold rings, bracelets, chains, pendants and earrings at our kiosk inside Fresco y Más, Miami."},
  "meta_servicios_t": {"es": "Reparación de joyas y más · Asha Jewelry Miami", "en": "Jewelry repair and more · Asha Jewelry Miami"},
  "meta_servicios_d": {"es": "Reparación de joyas, ajuste de talla de anillos, grabado y joyas a medida en Miami (33177).", "en": "Jewelry repair, ring sizing, engraving and custom jewelry in Miami (33177)."},
  "meta_financiamiento_t": {"es": "Financiamiento y layaway · Asha Jewelry Miami", "en": "Financing and layaway · Asha Jewelry Miami"},
  "meta_financiamiento_d": {"es": "Paga con Affirm, Afterpay, Klarna, Zip o Shop Pay, o aparta tu joya con layaway.", "en": "Pay with Affirm, Afterpay, Klarna, Zip or Shop Pay, or reserve your piece with layaway."},
  "meta_como_llegar_t": {"es": "Cómo llegar · Asha Jewelry Miami", "en": "Visit us · Asha Jewelry Miami"},
  "meta_como_llegar_d": {"es": "Kiosko 2 dentro de Mercado Fresco y Más, 12107 SW 152nd St, Miami, FL 33177. Martes a domingo.", "en": "Kiosk 2 inside Mercado Fresco y Más, 12107 SW 152nd St, Miami, FL 33177. Tuesday to Sunday."}
}
```

`datos/categorias.json`:
```json
[
  {"id": "anillos", "slug": {"es": "anillos", "en": "rings"}, "nombre": {"es": "Anillos", "en": "Rings"}},
  {"id": "pulseras", "slug": {"es": "pulseras", "en": "bracelets"}, "nombre": {"es": "Pulseras", "en": "Bracelets"}},
  {"id": "cadenas", "slug": {"es": "cadenas", "en": "chains"}, "nombre": {"es": "Cadenas", "en": "Chains"}},
  {"id": "dijes", "slug": {"es": "dijes", "en": "pendants"}, "nombre": {"es": "Dijes", "en": "Pendants"}},
  {"id": "aretes", "slug": {"es": "aretes", "en": "earrings"}, "nombre": {"es": "Aretes", "en": "Earrings"}}
]
```

`datos/piezas.json`:
```json
[
  {"id": "dije-nombre", "categoria": "dijes", "slug": {"es": "dije-con-nombre", "en": "name-pendant"}, "nombre": {"es": "Dije con tu nombre", "en": "Custom name pendant"}, "descripcion": {"es": "Tu nombre, o el de quien quieres, convertido en joya. Lo hacemos a la medida.", "en": "Your name, or someone you love, turned into jewelry. Made to order."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": true, "disponible": true, "provisional": true},
  {"id": "dije-inicial", "categoria": "dijes", "slug": {"es": "dije-de-inicial", "en": "initial-pendant"}, "nombre": {"es": "Dije de inicial", "en": "Initial pendant"}, "descripcion": {"es": "La inicial que tú elijas, para llevar todos los días o para regalar.", "en": "The initial of your choice, to wear every day or to give as a gift."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": true, "disponible": true, "provisional": true},
  {"id": "aretes-boton", "categoria": "aretes", "slug": {"es": "aretes-de-boton", "en": "stud-earrings"}, "nombre": {"es": "Aretes de botón 4, 5 y 6 mm", "en": "Stud earrings 4, 5 and 6 mm"}, "descripcion": {"es": "Ligeros y cómodos para el día a día.", "en": "Lightweight and comfortable for everyday wear."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": true, "disponible": true, "provisional": true},
  {"id": "argollas-pequenas", "categoria": "aretes", "slug": {"es": "argollas-pequenas", "en": "huggie-hoops"}, "nombre": {"es": "Argollas pequeñas 10, 12 y 14 mm", "en": "Huggie hoops 10, 12 and 14 mm"}, "descripcion": {"es": "Argollas que abrazan el lóbulo, ligeras y cómodas.", "en": "Small hoops that hug the earlobe, lightweight and comfortable."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": true, "disponible": true, "provisional": true},
  {"id": "set-regalo", "categoria": "cadenas", "slug": {"es": "set-de-regalo", "en": "gift-set"}, "nombre": {"es": "Set de regalo", "en": "Gift set"}, "descripcion": {"es": "Un conjunto pensado para regalar: para mamá, para ti o para esa persona especial.", "en": "A set made for gifting: for mom, for you or for someone special."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": false, "disponible": true, "provisional": true},
  {"id": "cadena-oro", "categoria": "cadenas", "slug": {"es": "cadena-de-oro", "en": "gold-chain"}, "nombre": {"es": "Cadena de oro", "en": "Gold chain"}, "descripcion": {"es": "Cadenas en distintos largos y grosores. Pregúntanos por las que hay en vitrina.", "en": "Chains in different lengths and widths. Ask us what's in the display case."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": false, "disponible": true, "provisional": true},
  {"id": "anillo-oro", "categoria": "anillos", "slug": {"es": "anillo-de-oro", "en": "gold-ring"}, "nombre": {"es": "Anillo de oro", "en": "Gold ring"}, "descripcion": {"es": "Anillos de oro, y si no es tu talla, te lo ajustamos.", "en": "Gold rings, and if it's not your size, we'll resize it."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": false, "disponible": true, "provisional": true},
  {"id": "pulsera-oro", "categoria": "pulseras", "slug": {"es": "pulsera-de-oro", "en": "gold-bracelet"}, "nombre": {"es": "Pulsera de oro", "en": "Gold bracelet"}, "descripcion": {"es": "Pulseras de oro para todos los días o para una ocasión especial.", "en": "Gold bracelets for every day or for a special occasion."}, "material": {"es": "Oro", "en": "Gold"}, "precio": null, "fotos": [], "destacada": false, "disponible": true, "provisional": true}
]
```

`datos/servicios.json`:
```json
[
  {"id": "reparacion", "slug": {"es": "reparacion-de-joyas", "en": "jewelry-repair"}, "titulo": {"es": "Reparación de joyas", "en": "Jewelry repair"}, "intro": {"es": "¿Se rompió la cadena o se soltó el broche? Tráela y le buscamos solución.", "en": "Broken chain or loose clasp? Bring it in and we'll find a fix."}, "descripcion": {"es": "Revisamos tu pieza en el kiosko y te decimos qué necesita antes de empezar.", "en": "We look at your piece at the kiosk and tell you what it needs before we start."}, "incluye": {"es": ["Cadenas y pulseras rotas", "Broches y cierres", "Piezas de oro y plata"], "en": ["Broken chains and bracelets", "Clasps and closures", "Gold and silver pieces"]}, "fotos": [], "provisional": true},
  {"id": "ajuste", "slug": {"es": "ajuste-de-anillos", "en": "ring-sizing"}, "titulo": {"es": "Ajuste de talla de anillos", "en": "Ring sizing"}, "intro": {"es": "¿El anillo te queda grande o pequeño? Lo ajustamos a tu medida.", "en": "Ring too big or too small? We'll size it to fit you."}, "descripcion": {"es": "Medimos tu dedo en el kiosko y te explicamos cómo queda el ajuste.", "en": "We measure your finger at the kiosk and explain how the resizing works."}, "incluye": {"es": ["Agrandar o achicar anillos", "Medición de talla"], "en": ["Sizing rings up or down", "Ring size measuring"]}, "fotos": [], "provisional": true},
  {"id": "grabado", "slug": {"es": "grabado", "en": "engraving"}, "titulo": {"es": "Grabado", "en": "Engraving"}, "intro": {"es": "Un nombre, una fecha, unas palabras: lo grabamos en tu joya.", "en": "A name, a date, a few words: we engrave it on your jewelry."}, "descripcion": {"es": "Tráenos la pieza o elige una en el kiosko y te enseñamos las opciones.", "en": "Bring your piece or choose one at the kiosk and we'll show you the options."}, "incluye": {"es": ["Nombres y fechas", "Mensajes cortos"], "en": ["Names and dates", "Short messages"]}, "fotos": [], "provisional": true},
  {"id": "a-medida", "slug": {"es": "joyas-a-medida", "en": "custom-jewelry"}, "titulo": {"es": "Joyas a medida y personalizadas", "en": "Custom and personalized jewelry"}, "intro": {"es": "Dijes con nombre, iniciales y piezas hechas para ti.", "en": "Name pendants, initials and pieces made just for you."}, "descripcion": {"es": "Cuéntanos qué tienes en mente y lo hacemos realidad en oro.", "en": "Tell us what you have in mind and we'll make it real in gold."}, "incluye": {"es": ["Dijes con nombre", "Iniciales", "Fabricación de piezas"], "en": ["Name pendants", "Initials", "Custom-made pieces"]}, "fotos": [], "provisional": true}
]
```

`datos/promos.json`:
```json
[]
```

- [ ] **Step 2: Prueba que falla**

`tests/test_datos.py`:
```python
import copy
import json
import unittest
from pathlib import Path

from herramientas import datos
from herramientas.datos import ErrorDatos

RAIZ = Path(__file__).resolve().parent.parent


def reales():
    return {n: json.loads((RAIZ / "datos" / f"{n}.json").read_text(encoding="utf-8"))
            for n in datos.NOMBRES}


class TestDatos(unittest.TestCase):
    def test_datos_reales_validan(self):
        d = datos.cargar(RAIZ / "datos")
        self.assertEqual(set(d), set(datos.NOMBRES))

    def test_falta_ingles(self):
        d = reales()
        d["textos"]["lema"]["en"] = ""
        with self.assertRaisesRegex(ErrorDatos, "textos.lema"):
            datos.validar(d)

    def test_categoria_inexistente(self):
        d = reales()
        d["piezas"][0]["categoria"] = "relojes"
        with self.assertRaisesRegex(ErrorDatos, "relojes"):
            datos.validar(d)

    def test_precio_invalido(self):
        d = reales()
        d["piezas"][0]["precio"] = -5
        with self.assertRaisesRegex(ErrorDatos, "precio"):
            datos.validar(d)

    def test_slug_repetido(self):
        d = reales()
        d["piezas"][1]["slug"] = copy.deepcopy(d["piezas"][0]["slug"])
        with self.assertRaisesRegex(ErrorDatos, "slug repetido"):
            datos.validar(d)

    def test_id_repetido(self):
        d = reales()
        d["piezas"][1]["id"] = d["piezas"][0]["id"]
        with self.assertRaisesRegex(ErrorDatos, "id repetido"):
            datos.validar(d)

    def test_junta_todos_los_problemas(self):
        d = reales()
        d["textos"]["lema"]["en"] = ""
        d["piezas"][0]["categoria"] = "relojes"
        with self.assertRaises(ErrorDatos) as e:
            datos.validar(d)
        self.assertIn("textos.lema", str(e.exception))
        self.assertIn("relojes", str(e.exception))

    def test_promo_vigente(self):
        promos = [{"id": "oct", "texto": {"es": "a", "en": "b"}, "desde": "2026-10-01", "hasta": "2026-10-31"}]
        self.assertEqual(datos.promo_vigente(promos, "2026-10-15")["id"], "oct")
        self.assertIsNone(datos.promo_vigente(promos, "2026-11-01"))

    def test_provisionales_cuenta_todo(self):
        d = reales()
        esperado = (sum(1 for x in d["piezas"] + d["servicios"] if x.get("provisional"))
                    + (1 if d["negocio"].get("provisional") else 0))
        self.assertEqual(datos.provisionales(d), esperado)
        self.assertGreater(esperado, 0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Verificar que falla**

Run: `python -m unittest tests.test_datos -v`
Expected: ERROR `ImportError: cannot import name 'datos'`

- [ ] **Step 4: Implementación**

`herramientas/datos.py`:
```python
"""Carga y valida datos/. Si algo no cuadra, lanza ErrorDatos con todos los
problemas juntos, para arreglarlos de una vez."""
import json
from pathlib import Path

from herramientas.config import IDIOMAS

NOMBRES = ("negocio", "textos", "servicios", "categorias", "piezas", "promos")
NEGOCIO_OBLIGATORIO = ("nombre", "direccion", "dentro_de", "telefono",
                       "telefono_visible", "dias", "instagram", "pagos")


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
```

- [ ] **Step 5: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 17 tests OK

- [ ] **Step 6: Commit**

```bash
git add datos herramientas/datos.py tests/test_datos.py
git commit -m "Datos del negocio, catálogo y servicios provisionales, con validación

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Comprobaciones (contraste, rayas, enlaces)

**Files:**
- Create: `herramientas/comprobar.py`, `tests/test_comprobar.py`

**Interfaces:**
- Produces: `comprobar.contraste(a_hex, b_hex) -> float`, `comprobar.tokens_css(texto) -> dict[str, str]`, `comprobar.PARES_TEXTO: list[tuple[str, str]]`, `comprobar.comprobar_contraste(css_texto) -> list[str]`, `comprobar.comprobar_rayas(archivos) -> list[str]`, `comprobar.comprobar_enlaces(publico: Path) -> list[str]`, `comprobar.todo(raiz: Path, publico: Path) -> list[str]`.

- [ ] **Step 1: Prueba que falla**

`tests/test_comprobar.py`:
```python
import tempfile
import unittest
from pathlib import Path

from herramientas import comprobar

CSS_BUENO = """:root{--aqua:#CFF2F6;--oro-claro:#DEAC3B;--oro:#BA8621;--oro-tinta:#7A5716;
--tinta:#1A1408;--blanco:#FFFFFF;--gris:#5C5446}"""


class TestContraste(unittest.TestCase):
    def test_blanco_negro(self):
        self.assertAlmostEqual(comprobar.contraste("#FFFFFF", "#000000"), 21.0, places=1)

    def test_tokens(self):
        self.assertEqual(comprobar.tokens_css(CSS_BUENO)["oro-tinta"], "#7A5716")

    def test_paleta_buena_pasa(self):
        self.assertEqual(comprobar.comprobar_contraste(CSS_BUENO), [])

    def test_oro_como_tinta_falla(self):
        malo = CSS_BUENO.replace("--oro-tinta:#7A5716", "--oro-tinta:#BA8621")
        problemas = comprobar.comprobar_contraste(malo)
        self.assertTrue(any("oro-tinta" in p for p in problemas))

    def test_token_ausente_es_problema(self):
        problemas = comprobar.comprobar_contraste(":root{--tinta:#000000}")
        self.assertTrue(any("falta" in p for p in problemas))


class TestRayas(unittest.TestCase):
    def test_detecta_raya(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.html"
            f.write_text("hola — mundo", encoding="utf-8")
            self.assertEqual(len(comprobar.comprobar_rayas([f])), 1)

    def test_sin_raya(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.html"
            f.write_text("hola - mundo · bien", encoding="utf-8")
            self.assertEqual(comprobar.comprobar_rayas([f]), [])


class TestEnlaces(unittest.TestCase):
    def _sitio(self, html):
        tmp = tempfile.TemporaryDirectory()
        raiz = Path(tmp.name)
        (raiz / "a").mkdir()
        (raiz / "a" / "index.html").write_text("ok", encoding="utf-8")
        (raiz / "css").mkdir()
        (raiz / "css" / "sitio.css").write_text("", encoding="utf-8")
        (raiz / "index.html").write_text(html, encoding="utf-8")
        return tmp, raiz

    def test_enlace_roto(self):
        tmp, raiz = self._sitio('<a href="falta/">x</a>')
        with tmp:
            problemas = comprobar.comprobar_enlaces(raiz)
            self.assertEqual(len(problemas), 1)
            self.assertIn("falta/", problemas[0])

    def test_enlaces_buenos(self):
        html = ('<a href="a/">x</a><a href="a/#sec">y</a><link href="css/sitio.css?v=1">'
                '<a href="https://example.com/">e</a><a href="tel:+1">t</a><a href="#">z</a>'
                '<img srcset="css/sitio.css 480w, a/index.html 960w">')
        tmp, raiz = self._sitio(html)
        with tmp:
            self.assertEqual(comprobar.comprobar_enlaces(raiz), [])

    def test_srcset_roto(self):
        tmp, raiz = self._sitio('<img srcset="img/no.webp 480w">')
        with tmp:
            self.assertEqual(len(comprobar.comprobar_enlaces(raiz)), 1)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Verificar que falla**

Run: `python -m unittest tests.test_comprobar -v`
Expected: ERROR `ImportError: cannot import name 'comprobar'`

- [ ] **Step 3: Implementación**

`herramientas/comprobar.py`:
```python
"""Comprobaciones antes de publicar: contraste de la paleta, raya larga en
textos y enlaces internos rotos en publico/."""
import html
import re
from pathlib import Path

RAYA = "—"
MINIMO_AA = 4.5
# (texto, fondo): cada par que el CSS usa para texto debe cumplir AA.
PARES_TEXTO = [
    ("tinta", "blanco"), ("tinta", "aqua"), ("tinta", "oro"),
    ("oro-tinta", "blanco"), ("oro-tinta", "aqua"),
    ("gris", "blanco"), ("gris", "aqua"),
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
```

- [ ] **Step 4: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 27 tests OK

- [ ] **Step 5: Commit**

```bash
git add herramientas/comprobar.py tests/test_comprobar.py
git commit -m "Comprobaciones: contraste AA de la paleta, raya larga y enlaces rotos

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: Estáticos (fuentes, marca, CSS y JS)

**Files:**
- Create: `estaticos/fuentes/playfair-display-latin-600-normal.woff2`, `estaticos/fuentes/montserrat-latin-400-normal.woff2`, `estaticos/fuentes/montserrat-latin-600-normal.woff2`, `estaticos/fuentes/OFL.txt`, `herramientas/fuentes/PlayfairDisplay.ttf`, `estaticos/img/insignia.jpg`, `estaticos/favicon.svg`, `herramientas/marca.py`, `tests/test_marca.py`, `estaticos/css/sitio.css`, `estaticos/js/sitio.js`, `img/originales/.gitkeep`
- Generated (committed): `estaticos/favicon-32.png`, `estaticos/apple-touch-icon.png`, `estaticos/icon-192.png`, `estaticos/icon-512.png`, `estaticos/img/og.png`

**Interfaces:**
- Produces: `marca.generar(destino: Path, fuente: Path) -> list[Path]`. Los archivos estáticos con las rutas exactas de arriba, que usarán `plantilla.py` y `paginas.py`. Clases CSS: `envoltura`, `seccion`, `seccion-aqua`, `portada`, `insignia`, `ornamento`, `lema`, `acciones`, `boton`, `boton-oro`, `boton-borde`, `rejilla`, `tarjeta`, `tarjeta-foto`, `material`, `precio`, `marco`, `marco-a`, `marco-t`, `filtros`, `categoria`, `ficha`, `ficha-foto`, `miga`, `servicios`, `servicio`, `pagos`, `promo`, `datos`, `lista`, `entradilla`, `mas`, `cabecera`, `marca`, `menu-boton`, `pie`, `pie-fila`, `pie-legal`, `contacto-fijo`, `saltar`.

- [ ] **Step 1: Descargar fuentes (pedir permiso al usuario antes de descargar)**

Las fuentes tienen licencia OFL y vienen de fuentes de confianza (npm @fontsource vía jsDelivr y el repo google/fonts). Desde la raíz del repo:
```bash
mkdir -p estaticos/fuentes herramientas/fuentes estaticos/img img/originales
curl -sfLo estaticos/fuentes/playfair-display-latin-600-normal.woff2 https://cdn.jsdelivr.net/npm/@fontsource/playfair-display/files/playfair-display-latin-600-normal.woff2
curl -sfLo estaticos/fuentes/montserrat-latin-400-normal.woff2 https://cdn.jsdelivr.net/npm/@fontsource/montserrat/files/montserrat-latin-400-normal.woff2
curl -sfLo estaticos/fuentes/montserrat-latin-600-normal.woff2 https://cdn.jsdelivr.net/npm/@fontsource/montserrat/files/montserrat-latin-600-normal.woff2
curl -sfLo herramientas/fuentes/PlayfairDisplay.ttf "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf"
curl -sfLo estaticos/fuentes/OFL.txt https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt
touch img/originales/.gitkeep
ls -la estaticos/fuentes herramientas/fuentes
```
Expected: los cinco archivos existen y no están vacíos (cada woff2 pesa entre 15 y 60 KB; el TTF, unos 300 KB).

- [ ] **Step 2: Insignia provisional**

La mejor versión disponible del logo es el avatar de TikTok @ashajewelryshop (807×807, esquinas blancas; en el sitio se muestra recortado en círculo). Está en el scratchpad de la sesión como `tiktok_avatar.jpg`; si no está, vuelve a descargarlo desde la foto de perfil de https://www.tiktok.com/@ashajewelryshop. Redúcelo a 480 px:
```bash
python -c "from PIL import Image; Image.open(r'RUTA/tiktok_avatar.jpg').convert('RGB').resize((480, 480), Image.LANCZOS).save('estaticos/img/insignia.jpg', quality=88, optimize=True)"
python -c "from PIL import Image; print(Image.open('estaticos/img/insignia.jpg').size)"
```
Expected: `(480, 480)`

- [ ] **Step 3: Favicon SVG**

`estaticos/favicon.svg`:
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#CFF2F6" stroke="#BA8621" stroke-width="3"/><text x="32" y="44" text-anchor="middle" font-family="'Playfair Display', Georgia, 'Times New Roman', serif" font-size="36" font-weight="600" fill="#7A5716">A</text></svg>
```

- [ ] **Step 4: Prueba de marca que falla**

`tests/test_marca.py`:
```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from herramientas import marca

RAIZ = Path(__file__).resolve().parent.parent


class TestMarca(unittest.TestCase):
    def test_genera_iconos_y_og(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            marca.generar(destino, RAIZ / "herramientas" / "fuentes" / "PlayfairDisplay.ttf")
            esperados = {
                "favicon-32.png": (32, 32), "apple-touch-icon.png": (180, 180),
                "icon-192.png": (192, 192), "icon-512.png": (512, 512),
                "img/og.png": (1200, 630),
            }
            for nombre, tam in esperados.items():
                with Image.open(destino / nombre) as im:
                    self.assertEqual(im.size, tam, nombre)


if __name__ == "__main__":
    unittest.main()
```

Run: `python -m unittest tests.test_marca -v`
Expected: ERROR `ImportError: cannot import name 'marca'`

- [ ] **Step 5: Implementar marca.py**

`herramientas/marca.py`:
```python
"""Genera los iconos (la "A" dorada sobre círculo aqua, como en sus
historias destacadas de Instagram) y la imagen para redes sociales.

Se ejecuta a mano cuando cambie la marca y la salida se versiona:
    python herramientas/marca.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUA = "#CFF2F6"
ORO = "#BA8621"
ORO_TINTA = "#7A5716"
TINTA = "#1A1408"
RAIZ = Path(__file__).resolve().parent.parent


def _fuente(ruta, tam):
    f = ImageFont.truetype(str(ruta), tam)
    try:
        f.set_variation_by_name("SemiBold")
    except (OSError, ValueError):
        pass
    return f


def icono(tam, fuente):
    """Círculo aqua con borde dorado y una A centrada, con supermuestreo."""
    escala = 4
    t = tam * escala
    im = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    dib = ImageDraw.Draw(im)
    borde = max(escala, round(t * 0.05))
    dib.ellipse((borde // 2, borde // 2, t - borde // 2 - 1, t - borde // 2 - 1),
                fill=AQUA, outline=ORO, width=borde)
    f = _fuente(fuente, round(t * 0.6))
    dib.text((t / 2, t / 2), "A", font=f, fill=ORO_TINTA, anchor="mm")
    return im.resize((tam, tam), Image.LANCZOS)


def og(fuente):
    im = Image.new("RGB", (1200, 630), AQUA)
    circulo = icono(240, fuente)
    im.paste(circulo, (480, 70), circulo)
    dib = ImageDraw.Draw(im)
    dib.text((600, 400), "Asha Jewelry Miami", font=_fuente(fuente, 76), fill=TINTA, anchor="mm")
    dib.line((540, 462, 660, 462), fill=ORO, width=3)
    dib.text((600, 515), "Mercado Fresco y Más · Kiosk 2 · Miami, FL",
             font=_fuente(fuente, 34), fill=ORO_TINTA, anchor="mm")
    return im


def generar(destino, fuente):
    destino = Path(destino)
    (destino / "img").mkdir(parents=True, exist_ok=True)
    salidas = []
    for nombre, tam in (("favicon-32.png", 32), ("apple-touch-icon.png", 180),
                        ("icon-192.png", 192), ("icon-512.png", 512)):
        ruta = destino / nombre
        im = icono(tam, fuente)
        if nombre == "apple-touch-icon.png":
            fondo = Image.new("RGB", im.size, AQUA)
            fondo.paste(im, (0, 0), im)
            im = fondo
        im.save(ruta, optimize=True)
        salidas.append(ruta)
    ruta = destino / "img" / "og.png"
    og(fuente).save(ruta, optimize=True)
    salidas.append(ruta)
    return salidas


if __name__ == "__main__":
    for s in generar(RAIZ / "estaticos", RAIZ / "herramientas" / "fuentes" / "PlayfairDisplay.ttf"):
        print(s.relative_to(RAIZ))
    sys.exit(0)
```

- [ ] **Step 6: Verificar y generar**

Run: `python -m unittest tests.test_marca -v`
Expected: 1 test OK
Run: `python herramientas/marca.py`
Expected: imprime las 5 rutas en `estaticos/`. Abre `estaticos/img/og.png` y `estaticos/icon-512.png` con la herramienta Read para comprobarlas a ojo: la A debe quedar centrada y el texto no debe salirse.

- [ ] **Step 7: CSS**

`estaticos/css/sitio.css`:
```css
@font-face{font-family:"Playfair Display";src:url(../fuentes/playfair-display-latin-600-normal.woff2) format("woff2");font-weight:600;font-style:normal;font-display:swap}
@font-face{font-family:Montserrat;src:url(../fuentes/montserrat-latin-400-normal.woff2) format("woff2");font-weight:400;font-style:normal;font-display:swap}
@font-face{font-family:Montserrat;src:url(../fuentes/montserrat-latin-600-normal.woff2) format("woff2");font-weight:600;font-style:normal;font-display:swap}

:root{
  --aqua:#CFF2F6;
  --oro-claro:#DEAC3B;
  --oro:#BA8621;
  --oro-tinta:#7A5716;
  --tinta:#1A1408;
  --blanco:#FFFFFF;
  --gris:#5C5446;
  --ancho:72rem;
  --radio:14px;
}

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--blanco);color:var(--tinta);font:400 1rem/1.6 Montserrat,system-ui,-apple-system,"Segoe UI",sans-serif}
h1,h2,h3{font-family:"Playfair Display",Georgia,"Times New Roman",serif;font-weight:600;line-height:1.2;margin:0 0 .5em}
h1{font-size:clamp(2rem,6vw,3.25rem)}
h2{font-size:clamp(1.5rem,4vw,2.25rem)}
h3{font-size:1.2rem}
a{color:var(--oro-tinta)}
img{max-width:100%;height:auto;display:block}
:focus-visible{outline:3px solid var(--oro-tinta);outline-offset:2px}
.saltar{position:absolute;left:-999px;top:0}
.saltar:focus{left:1rem;top:1rem;background:var(--blanco);padding:.5rem 1rem;z-index:10}

.envoltura{max-width:var(--ancho);margin:0 auto;padding:0 1rem}
.seccion{padding:3rem 0}
.seccion.envoltura{padding:3rem 1rem}
.seccion-aqua{background:var(--aqua)}

/* Cabecera */
.cabecera{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.75rem 1.5rem;max-width:var(--ancho);margin:0 auto;padding:.75rem 1rem}
.marca{display:flex;align-items:center;gap:.75rem;text-decoration:none;color:var(--tinta);font-family:"Playfair Display",Georgia,serif;font-size:1.3rem;font-weight:600}
.marca img{border-radius:50%}
.marca small{display:block;font-family:Montserrat,sans-serif;font-size:.7rem;font-weight:600;letter-spacing:.25em;text-transform:uppercase;color:var(--oro-tinta)}
#menu ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.25rem 1.25rem}
#menu a{display:inline-block;text-decoration:none;color:var(--tinta);font-weight:600;font-size:.95rem;padding:.35rem 0;border-bottom:2px solid transparent}
#menu a:hover,#menu a[aria-current=page]{border-bottom-color:var(--oro)}
#menu a.idioma{color:var(--oro-tinta)}
.menu-boton{font:inherit;font-weight:600;background:none;border:2px solid var(--oro);border-radius:999px;padding:.35rem 1rem;color:var(--tinta);cursor:pointer}
@media (max-width:47.99rem){
  .con-js #menu{display:none;width:100%}
  .con-js #menu.abierto{display:block}
  .con-js #menu ul{flex-direction:column;padding:.5rem 0 1rem}
}
@media (min-width:48rem){.menu-boton{display:none}}

/* Portada */
.portada{padding:3.5rem 1rem 3rem;text-align:center}
.portada .insignia{margin:0 auto 1.5rem;border-radius:50%}
.ornamento{width:4rem;height:2px;background:var(--oro);border:0;margin:1.25rem auto}
.lema{font-size:1.15rem;max-width:36rem;margin:0 auto 1.75rem}
.acciones{display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center}
.entradilla{font-size:1.1rem;max-width:42rem}

/* Botones */
.boton{display:inline-block;padding:.85rem 1.4rem;border-radius:999px;font-weight:600;text-decoration:none;line-height:1.2}
.boton-oro{background:var(--oro);color:var(--tinta)}
.boton-oro:hover{background:var(--oro-claro)}
.boton-borde{border:2px solid var(--oro);color:var(--tinta);background:var(--blanco)}
.boton-borde:hover{background:var(--aqua)}
.mas{margin-top:2rem}

/* Catálogo */
.rejilla{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,14rem),1fr));gap:1.5rem}
.tarjeta a{display:block;text-decoration:none;color:var(--tinta)}
.tarjeta-foto,.ficha-foto{aspect-ratio:1;border-radius:var(--radio);overflow:hidden;background:var(--aqua)}
.tarjeta-foto img,.ficha-foto img{width:100%;height:100%;object-fit:cover}
.tarjeta h3{margin:.75rem 0 .25rem}
.tarjeta a:hover h3{text-decoration:underline;text-decoration-color:var(--oro)}
.material{color:var(--gris);font-size:.9rem;margin:0}
.precio{color:var(--oro-tinta);font-weight:600;margin:.25rem 0 0}
.marco{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.75rem;background:var(--aqua);color:var(--oro-tinta)}
.marco-a{font-family:"Playfair Display",Georgia,serif;font-size:2.5rem;width:4.5rem;height:4.5rem;border:2px solid var(--oro);border-radius:50%;display:flex;align-items:center;justify-content:center}
.marco-t{font-size:.75rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase}
.filtros{display:flex;flex-wrap:wrap;gap:.5rem;margin:1.5rem 0 0}
.filtros a{border:2px solid var(--oro);border-radius:999px;padding:.35rem 1rem;text-decoration:none;color:var(--tinta);font-weight:600;font-size:.9rem}
.filtros a[aria-pressed=true]{background:var(--oro)}
.categoria{margin-top:2.5rem}
.ficha{display:grid;gap:2rem;align-items:start}
@media (min-width:48rem){.ficha{grid-template-columns:1fr 1fr}}
.miga{font-size:.9rem;margin:1.5rem 0}

/* Servicios, pagos, datos */
.servicios{list-style:none;padding:0;margin:0;display:grid;gap:1.25rem;grid-template-columns:repeat(auto-fill,minmax(min(100%,16rem),1fr))}
.servicio{border:1px solid var(--oro);border-radius:var(--radio);padding:1.5rem;background:var(--blanco)}
.servicio h2,.servicio h3{font-size:1.2rem}
.lista{padding-left:1.25rem}
.pagos{list-style:none;padding:0;margin:1rem 0;display:flex;flex-wrap:wrap;gap:.75rem}
.pagos li{background:var(--blanco);border:1px solid var(--oro);border-radius:999px;padding:.4rem 1rem;font-weight:600}
.promo{border:2px dashed var(--oro);border-radius:var(--radio);padding:1rem 1.5rem;margin:0 auto 1rem}
.datos dt{font-weight:600;color:var(--oro-tinta);margin-top:1rem}
.datos dd{margin:0}

/* Pie y contacto fijo */
.pie{background:var(--tinta);color:var(--blanco);margin-top:4rem;padding:2.5rem 1rem 6rem}
.pie a{color:var(--oro-claro)}
.pie-fila{max-width:var(--ancho);margin:0 auto;display:grid;gap:1.5rem;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr))}
.pie-legal{max-width:var(--ancho);margin:2rem auto 0;font-size:.85rem}
.contacto-fijo{position:fixed;right:1rem;bottom:1rem;z-index:5;background:var(--oro);color:var(--tinta);font-weight:600;text-decoration:none;padding:.85rem 1.25rem;border-radius:999px;box-shadow:0 4px 14px rgb(26 20 8 / .25)}
@media (min-width:48rem){.contacto-fijo{display:none}.pie{padding-bottom:2.5rem}}
@media (prefers-reduced-motion:no-preference){.boton,#menu a,.filtros a{transition:background-color .2s,border-color .2s}}
```

- [ ] **Step 8: JS**

`estaticos/js/sitio.js`:
```js
// Menú del móvil y filtro del catálogo. Sin JavaScript todo funciona igual:
// el menú se ve entero y los filtros son anclas a cada categoría.
(function () {
  var boton = document.querySelector('.menu-boton');
  var menu = document.getElementById('menu');
  if (boton && menu) {
    document.documentElement.classList.add('con-js');
    boton.hidden = false;
    boton.addEventListener('click', function () {
      var abierto = boton.getAttribute('aria-expanded') === 'true';
      boton.setAttribute('aria-expanded', String(!abierto));
      menu.classList.toggle('abierto', !abierto);
    });
  }

  var filtros = Array.prototype.slice.call(document.querySelectorAll('[data-filtro]'));
  var secciones = Array.prototype.slice.call(document.querySelectorAll('.categoria'));
  filtros.forEach(function (f) {
    f.setAttribute('role', 'button');
    f.setAttribute('aria-pressed', String(f.getAttribute('data-filtro') === 'todas'));
    f.addEventListener('click', function (e) {
      e.preventDefault();
      var c = f.getAttribute('data-filtro');
      secciones.forEach(function (s) {
        s.hidden = c !== 'todas' && s.getAttribute('data-categoria') !== c;
      });
      filtros.forEach(function (o) { o.setAttribute('aria-pressed', String(o === f)); });
    });
  });
})();
```

- [ ] **Step 9: Contraste del CSS real**

Añade esta prueba al final de la clase `TestContraste` en `tests/test_comprobar.py`:
```python
    def test_css_del_sitio_pasa(self):
        raiz = Path(__file__).resolve().parent.parent
        css = (raiz / "estaticos" / "css" / "sitio.css").read_text(encoding="utf-8")
        self.assertEqual(comprobar.comprobar_contraste(css), [])
```
Run: `python -m unittest discover -s tests -t . -v`
Expected: 29 tests OK

- [ ] **Step 10: Commit**

```bash
git add estaticos herramientas/marca.py herramientas/fuentes tests/test_marca.py tests/test_comprobar.py img/originales/.gitkeep
git commit -m "Estáticos: fuentes autoalojadas, iconos y OG de la marca, CSS y JS

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Datos estructurados (JSON-LD)

**Files:**
- Create: `herramientas/schema.py`, `tests/test_schema.py`

**Interfaces:**
- Consumes: `config.url_publica()`, `rutas.ruta`, `rutas.ruta_pieza`, `rutas.ruta_servicio`, `datos.cargar`.
- Produces: `schema.id_tienda() -> str`, `schema.tienda(d, l) -> dict`, `schema.producto(d, l, pieza, imagen=None) -> dict` (`imagen`: ruta relativa a la raíz del sitio o `None`), `schema.servicio(d, l, servicio) -> dict`.

- [ ] **Step 1: Prueba que falla**

`tests/test_schema.py`:
```python
import copy
import unittest
from pathlib import Path

from herramientas import config, datos, schema

RAIZ = Path(__file__).resolve().parent.parent
D = datos.cargar(RAIZ / "datos")


class TestSchema(unittest.TestCase):
    def test_tienda_dentro_de_fresco(self):
        t = schema.tienda(D, "es")
        self.assertEqual(t["@type"], "JewelryStore")
        self.assertEqual(t["@id"], config.url_publica() + "#tienda")
        self.assertEqual(t["containedInPlace"]["@type"], "GroceryStore")
        self.assertEqual(t["containedInPlace"]["name"], "Mercado Fresco y Más")
        self.assertEqual(t["address"]["postalCode"], "33177")
        self.assertIn("Klarna", t["paymentAccepted"])
        self.assertIn("https://www.instagram.com/ashajewelryshop/", t["sameAs"])

    def test_sin_horas_no_hay_horario(self):
        self.assertNotIn("openingHoursSpecification", schema.tienda(D, "es"))

    def test_con_horas_hay_horario(self):
        d = copy.deepcopy(D)
        d["negocio"]["horas"] = {"abre": "10:00", "cierra": "20:00"}
        h = schema.tienda(d, "en")["openingHoursSpecification"][0]
        self.assertIn("https://schema.org/Tuesday", h["dayOfWeek"])
        self.assertNotIn("https://schema.org/Monday", h["dayOfWeek"])
        self.assertEqual(h["opens"], "10:00")

    def test_sin_geo_no_hay_geo(self):
        self.assertNotIn("geo", schema.tienda(D, "es"))

    def test_producto_sin_precio_sin_offer(self):
        o = schema.producto(D, "es", D["piezas"][0])
        self.assertEqual(o["@type"], "Product")
        self.assertNotIn("offers", o)
        self.assertNotIn("image", o)

    def test_producto_con_precio_e_imagen(self):
        p = dict(D["piezas"][0], precio=250)
        o = schema.producto(D, "en", p, "img/fotos/x-960.webp")
        self.assertEqual(o["offers"]["price"], "250.00")
        self.assertEqual(o["offers"]["priceCurrency"], "USD")
        self.assertEqual(o["offers"]["seller"]["@id"], schema.id_tienda())
        self.assertEqual(o["image"], config.url_publica() + "img/fotos/x-960.webp")
        self.assertTrue(o["url"].endswith("en/catalog/name-pendant/"))

    def test_servicio(self):
        s = schema.servicio(D, "es", D["servicios"][0])
        self.assertEqual(s["@type"], "Service")
        self.assertEqual(s["provider"]["@id"], schema.id_tienda())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Verificar que falla**

Run: `python -m unittest tests.test_schema -v`
Expected: ERROR `ImportError: cannot import name 'schema'`

- [ ] **Step 3: Implementación**

`herramientas/schema.py`:
```python
"""JSON-LD de schema.org: la tienda (dentro de Fresco y Más), productos y
servicios. Lo que no está verificado (horas, geo) no se emite."""
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
        "sameAs": [n["instagram"]],
    }
    if n.get("apertura"):
        t["foundingDate"] = n["apertura"]
    if n.get("geo"):
        t["geo"] = {"@type": "GeoCoordinates", "latitude": n["geo"]["lat"],
                    "longitude": n["geo"]["lon"]}
    if n.get("horas"):
        t["openingHoursSpecification"] = [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [f"https://schema.org/{DIAS[x]}" for x in n["dias"]],
            "opens": n["horas"]["abre"],
            "closes": n["horas"]["cierra"],
        }]
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
```

- [ ] **Step 4: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 36 tests OK

- [ ] **Step 5: Commit**

```bash
git add herramientas/schema.py tests/test_schema.py
git commit -m "JSON-LD: JewelryStore dentro de Fresco y Más, productos y servicios

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Plantilla común

**Files:**
- Create: `herramientas/plantilla.py`, `tests/test_plantilla.py`

**Interfaces:**
- Consumes: `config`, `rutas.rel`, `rutas.ruta`, `datos.cargar`.
- Produces: `plantilla.esc(s) -> str`, `plantilla.tx(d, clave, l, **campos) -> str`, `plantilla.enlace_contacto(d, l, mensaje=None) -> tuple[str, str]` (href, etiqueta), `plantilla.url_mapa(d) -> str`, `plantilla.direccion_corta(d) -> str`, `plantilla.jsonld(objetos) -> str`, `plantilla.pagina(d, l, aqui, alternos, titulo, descripcion, cuerpo, schema, actual=None, indexable=True, absoluto=False) -> str`.

- [ ] **Step 1: Prueba que falla**

`tests/test_plantilla.py`:
```python
import copy
import unittest
from pathlib import Path
from unittest import mock

from herramientas import config, datos, plantilla

RAIZ = Path(__file__).resolve().parent.parent
D = datos.cargar(RAIZ / "datos")
ALT = {"es": "catalogo/", "en": "en/catalog/"}


def html(**kw):
    base = dict(d=D, l="es", aqui="catalogo/", alternos=ALT, titulo="T", descripcion="Desc",
                cuerpo="<p>cuerpo</p>", schema=[{"@type": "Thing"}], actual="catalogo")
    base.update(kw)
    return plantilla.pagina(**base)


class TestPlantilla(unittest.TestCase):
    def test_noindex_mientras_no_lanzado(self):
        with mock.patch.object(config, "LANZADO", False):
            self.assertIn('<meta name="robots" content="noindex, nofollow">', html())

    def test_sin_noindex_lanzado(self):
        with mock.patch.object(config, "LANZADO", True):
            h = html()
            self.assertNotIn("noindex", h)
            self.assertIn('<link rel="canonical" href="https://ashajewelryusa.com/catalogo/">', h)

    def test_404_siempre_noindex_y_sin_canonica(self):
        with mock.patch.object(config, "LANZADO", True):
            h = html(indexable=False)
            self.assertIn("noindex", h)
            self.assertNotIn('rel="canonical"', h)

    def test_hreflang_y_selector(self):
        h = html()
        self.assertIn('hreflang="en" href="' + config.url_publica() + 'en/catalog/"', h)
        self.assertIn('hreflang="x-default"', h)
        self.assertIn('<a class="idioma" href="../en/catalog/" hreflang="en" lang="en">English</a>', h)

    def test_enlaces_relativos(self):
        h = html()
        self.assertIn('href="../css/sitio.css?v=' + config.VERSION + '"', h)
        self.assertIn('href="../servicios/"', h)
        self.assertIn('aria-current="page"', h)

    def test_absoluto(self):
        h = html(absoluto=True)
        self.assertIn('href="' + config.url_publica() + 'css/sitio.css?v=', h)

    def test_contacto_sin_whatsapp_llama(self):
        href, etiqueta = plantilla.enlace_contacto(D, "es")
        self.assertEqual(href, "tel:+17869781981")
        self.assertEqual(etiqueta, "Llámanos")

    def test_contacto_con_whatsapp(self):
        d = copy.deepcopy(D)
        d["negocio"]["whatsapp"] = "+17865550000"
        href, etiqueta = plantilla.enlace_contacto(d, "en", "Hi there")
        self.assertEqual(href, "https://wa.me/17865550000?text=Hi%20there")
        self.assertEqual(etiqueta, "Message us on WhatsApp")

    def test_jsonld_escapa_cierre(self):
        s = plantilla.jsonld([{"name": "</script>"}])
        self.assertNotIn("</script>\"", s)
        self.assertIn("<\\/script>", s)

    def test_credito_index01(self):
        self.assertIn('Sitio por <a href="https://index01.net">Index01</a>', html())
        self.assertIn('Website by <a href="https://index01.net">Index01</a>', html(l="en", aqui="en/catalog/"))

    def test_tx_con_campos(self):
        self.assertEqual(plantilla.tx(D, "msg_pieza", "es", nombre="Anillo", id="a1"),
                         "Hola, me interesa esta pieza de su web: Anillo (a1)")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Verificar que falla**

Run: `python -m unittest tests.test_plantilla -v`
Expected: ERROR `ImportError: cannot import name 'plantilla'`

- [ ] **Step 3: Implementación**

`herramientas/plantilla.py`:
```python
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
```

- [ ] **Step 4: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 47 tests OK

- [ ] **Step 5: Commit**

```bash
git add herramientas/plantilla.py tests/test_plantilla.py
git commit -m "Plantilla común: head con noindex/hreflang, cabecera, pie y contacto

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Imágenes

**Files:**
- Create: `herramientas/imagenes.py`, `tests/test_imagenes.py`

**Interfaces:**
- Produces: `imagenes.ANCHOS = (480, 960, 1600)`, `imagenes.procesar(origen: Path, destino: Path, prefijo="img/fotos/") -> dict[str, list[list]]`, donde cada valor es una lista de `[ancho, ruta]` en orden creciente y `ruta` es relativa a la raíz del sitio (`"img/fotos/anillo-480.webp"`). Borra de `destino` los `.webp` que ya no correspondan a ningún original.

- [ ] **Step 1: Prueba que falla**

`tests/test_imagenes.py`:
```python
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from herramientas import imagenes


class TestImagenes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        self.origen = raiz / "originales"
        self.destino = raiz / "fotos"
        self.origen.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def _foto(self, nombre, ancho, alto, exif=False):
        im = Image.new("RGB", (ancho, alto), "#BA8621")
        ruta = self.origen / nombre
        if exif:
            e = Image.Exif()
            e[0x010F] = "CamaraSecreta"
            im.save(ruta, exif=e)
        else:
            im.save(ruta)
        return ruta

    def test_tres_anchos(self):
        self._foto("grande.jpg", 2000, 1500)
        m = imagenes.procesar(self.origen, self.destino)
        self.assertEqual([w for w, _ in m["grande"]], [480, 960, 1600])
        self.assertEqual(m["grande"][0][1], "img/fotos/grande-480.webp")
        with Image.open(self.destino / "grande-960.webp") as im:
            self.assertEqual(im.size, (960, 720))

    def test_no_amplia(self):
        self._foto("media.png", 600, 600)
        self._foto("chica.jpg", 300, 200)
        m = imagenes.procesar(self.origen, self.destino)
        self.assertEqual([w for w, _ in m["media"]], [480, 600])
        self.assertEqual([w for w, _ in m["chica"]], [300])

    def test_quita_exif(self):
        self._foto("con-exif.jpg", 800, 600, exif=True)
        imagenes.procesar(self.origen, self.destino)
        with Image.open(self.destino / "con-exif-480.webp") as im:
            self.assertEqual(len(im.getexif()), 0)

    def test_borra_huerfanas(self):
        ruta = self._foto("vieja.jpg", 500, 500)
        imagenes.procesar(self.origen, self.destino)
        ruta.unlink()
        imagenes.procesar(self.origen, self.destino)
        self.assertEqual(list(self.destino.glob("vieja-*.webp")), [])

    def test_ignora_otros_archivos(self):
        (self.origen / ".gitkeep").write_text("")
        self.assertEqual(imagenes.procesar(self.origen, self.destino), {})


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Verificar que falla**

Run: `python -m unittest tests.test_imagenes -v`
Expected: ERROR `ImportError: cannot import name 'imagenes'`

- [ ] **Step 3: Implementación**

`herramientas/imagenes.py`:
```python
"""De img/originales/ a WebP en varios anchos, sin metadatos EXIF (que
pueden llevar ubicación). Solo re-codifica lo que cambió."""
from pathlib import Path

from PIL import Image, ImageOps

ANCHOS = (480, 960, 1600)
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}


def procesar(origen, destino, prefijo="img/fotos/"):
    origen, destino = Path(origen), Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    manifiesto = {}
    vivos = set()
    for f in sorted(origen.iterdir()):
        if f.suffix.lower() not in EXTENSIONES:
            continue
        with Image.open(f) as abierta:
            im = ImageOps.exif_transpose(abierta).convert("RGB")
        variantes = []
        for w in ANCHOS:
            ancho = min(w, im.width)
            salida = destino / f"{f.stem}-{ancho}.webp"
            vivos.add(salida.name)
            if not salida.exists() or salida.stat().st_mtime < f.stat().st_mtime:
                alto = round(im.height * ancho / im.width)
                im.resize((ancho, alto), Image.LANCZOS).save(salida, "WEBP", quality=82, method=6)
            variantes.append([ancho, prefijo + salida.name])
            if ancho == im.width:
                break
        manifiesto[f.stem] = variantes
    for vieja in destino.glob("*.webp"):
        if vieja.name not in vivos:
            vieja.unlink()
    return manifiesto
```

- [ ] **Step 4: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 52 tests OK

- [ ] **Step 5: Commit**

```bash
git add herramientas/imagenes.py tests/test_imagenes.py
git commit -m "Imágenes: WebP en 480/960/1600 sin EXIF, sin ampliar ni dejar huérfanas

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Páginas y generador

**Files:**
- Create: `herramientas/paginas.py`, `herramientas/sitio.py`, `tests/test_sitio.py`
- Generated (committed): `publico/`

**Interfaces:**
- Consumes: todo lo anterior.
- Produces: `paginas.todas(d, man, hoy) -> list[tuple[str, str]]` (archivo relativo a `publico/`, html), `paginas.robots() -> str`, `paginas.sitemap(d) -> str`, `paginas.llms(d) -> str`. `sitio.generar(raiz=RAIZ, publico=None, hoy=None) -> tuple[dict, list]`, `sitio.main() -> int`.

- [ ] **Step 1: Prueba que falla**

`tests/test_sitio.py`:
```python
import copy
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from herramientas import comprobar, config, datos, paginas, sitio

RAIZ = Path(__file__).resolve().parent.parent


class TestSitio(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.publico = Path(self.tmp.name) / "publico"

    def tearDown(self):
        self.tmp.cleanup()

    def test_genera_todo_y_pasa_comprobaciones(self):
        d, pags = sitio.generar(publico=self.publico, hoy="2026-10-02")
        por_idioma = 1 + 1 + len(d["piezas"]) + 1 + len(d["servicios"]) + 1 + 1
        self.assertEqual(len(pags), 2 * por_idioma + 1)
        for f in ("index.html", "en/index.html", "catalogo/index.html", "en/catalog/gold-ring/index.html",
                  "servicios/grabado/index.html", "en/visit/index.html", "financiamiento/index.html",
                  "404.html", "robots.txt", "llms.txt", "css/sitio.css", "favicon.svg", "img/og.png"):
            self.assertTrue((self.publico / f).is_file(), f)
        self.assertEqual(comprobar.todo(RAIZ, self.publico), [])

    def test_vista_previa_sin_cname_ni_sitemap(self):
        sitio.generar(publico=self.publico, hoy="2026-10-02")
        self.assertFalse((self.publico / "CNAME").exists())
        self.assertFalse((self.publico / "sitemap.xml").exists())
        self.assertIn("Disallow: /", (self.publico / "robots.txt").read_text(encoding="utf-8"))
        self.assertIn("noindex", (self.publico / "index.html").read_text(encoding="utf-8"))

    def test_lanzado(self):
        with mock.patch.object(config, "LANZADO", True):
            sitio.generar(publico=self.publico, hoy="2026-10-02")
        self.assertEqual((self.publico / "CNAME").read_text(encoding="utf-8"), "ashajewelryusa.com\n")
        mapa = (self.publico / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("<loc>https://ashajewelryusa.com/en/catalog/gold-ring/</loc>", mapa)
        self.assertNotIn("404", mapa)
        self.assertNotIn("noindex", (self.publico / "index.html").read_text(encoding="utf-8"))
        self.assertIn("Sitemap: https://ashajewelryusa.com/sitemap.xml",
                      (self.publico / "robots.txt").read_text(encoding="utf-8"))

    def test_jsonld_valido_en_todas(self):
        sitio.generar(publico=self.publico, hoy="2026-10-02")
        for f in self.publico.rglob("index.html"):
            bloques = re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                 f.read_text(encoding="utf-8"), re.S)
            self.assertEqual(len(bloques), 1, f)
            json.loads(bloques[0])

    def test_portada_espanol_y_marco_provisional(self):
        sitio.generar(publico=self.publico, hoy="2026-10-02")
        h = (self.publico / "index.html").read_text(encoding="utf-8")
        self.assertIn('<html lang="es">', h)
        self.assertIn("Oro auténtico 10K, 14K y 18K", h)
        self.assertIn("Foto próximamente", h)
        self.assertIn("tel:+17869781981", h)

    def test_promo_vigente_aparece(self):
        d = datos.cargar(RAIZ / "datos")
        d["promos"] = [{"id": "oct", "texto": {"es": "Dijes en oferta", "en": "Pendants on sale"},
                        "desde": "2026-10-01", "hasta": "2026-10-31"}]
        pags = dict(paginas.todas(d, {}, "2026-10-02"))
        self.assertIn("Dijes en oferta", pags["index.html"])
        pags = dict(paginas.todas(d, {}, "2026-11-02"))
        self.assertNotIn("Dijes en oferta", pags["index.html"])

    def test_precio_y_foto_real(self):
        d = datos.cargar(RAIZ / "datos")
        d = copy.deepcopy(d)
        d["piezas"][0]["precio"] = 1250
        d["piezas"][0]["fotos"] = ["dije"]
        man = {"dije": [[480, "img/fotos/dije-480.webp"], [960, "img/fotos/dije-960.webp"]]}
        pags = dict(paginas.todas(d, man, "2026-10-02"))
        ficha = pags["catalogo/dije-con-nombre/index.html"]
        self.assertIn("$1,250", ficha)
        self.assertIn('srcset="../../img/fotos/dije-480.webp 480w, ../../img/fotos/dije-960.webp 960w"', ficha)
        self.assertIn('"price": "1250.00"', ficha)

    def test_foto_inexistente_es_error(self):
        d = datos.cargar(RAIZ / "datos")
        d["piezas"][0]["fotos"] = ["no-existe"]
        with self.assertRaisesRegex(datos.ErrorDatos, "no-existe"):
            paginas.todas(d, {}, "2026-10-02")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Verificar que falla**

Run: `python -m unittest tests.test_sitio -v`
Expected: ERROR `ImportError: cannot import name 'paginas'`

- [ ] **Step 3: Implementar paginas.py**

`herramientas/paginas.py`:
```python
"""Contenido de cada página. `todas()` devuelve [(archivo, html), ...] de las
dos lenguas más la 404."""
from herramientas import config, schema
from herramientas.datos import ErrorDatos, promo_vigente
from herramientas.plantilla import direccion_corta, enlace_contacto, esc, pagina, tx, url_mapa
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
    return (f'<div class="marco" role="img" aria-label="{t}"><span class="marco-a" aria-hidden="true">A</span>'
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
            f'<dt>{esc(tx(d, "horario_t", l))}</dt><dd>{esc(tx(d, "horario", l))}</dd>'
            f'<dt>{esc(tx(d, "telefono_t", l))}</dt><dd><a href="tel:{esc(n["telefono"])}">{esc(n["telefono_visible"])}</a></dd>'
            f'</dl><p><a class="boton boton-borde" href="{esc(url_mapa(d))}" rel="noopener">{esc(tx(d, "abrir_mapa", l))}</a></p>')


def lista_pagos(d, l):
    return "".join(f"<li>{esc(x)}</li>" for x in d["negocio"]["pagos"]) + f"<li>{esc(tx(d, 'layaway', l))}</li>"


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
<img class="insignia" src="{esc(rel(aqui, "img/insignia.jpg"))}" width="120" height="120" alt="ASHA Jewelry">
<h1>Asha Jewelry Miami</h1>
<hr class="ornamento">
<p class="lema">{esc(tx(d, "lema", l))}</p>
<div class="acciones"><a class="boton boton-oro" href="{esc(href_c)}">{esc(etiqueta_c)}</a> <a class="boton boton-borde" href="{esc(rel(aqui, ruta("como_llegar", l)))}">{esc(tx(d, "cta_como_llegar", l))}</a></div>
</section>
{bloque_promo}
<section class="seccion envoltura"><h2>{esc(tx(d, "inicio_destacadas", l))}</h2><ul class="rejilla">{destacadas}</ul>
<p class="mas"><a class="boton boton-borde" href="{esc(rel(aqui, ruta("catalogo", l)))}">{esc(tx(d, "ver_catalogo", l))}</a></p></section>
<section class="seccion seccion-aqua"><div class="envoltura"><h2>{esc(tx(d, "inicio_financiamiento_t", l))}</h2>
<p>{esc(tx(d, "inicio_financiamiento_p", l))}</p><ul class="pagos">{lista_pagos(d, l)}</ul>
<p><a href="{esc(rel(aqui, ruta("financiamiento", l)))}">{esc(tx(d, "ver_mas", l))}</a></p></div></section>
<section class="seccion envoltura"><h2>{esc(tx(d, "inicio_servicios", l))}</h2><ul class="servicios">{servicios_}</ul></section>
<section class="seccion seccion-aqua"><div class="envoltura"><h2>{esc(tx(d, "inicio_visita_t", l))}</h2>
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
<p><a class="boton boton-oro" href="{esc(href_c)}">{esc(tx(d, "preguntar_pieza", l))}</a></p></div></article>
{relacionadas}</div>"""
    imagen = man[p["fotos"][0]][-1][1] if p.get("fotos") else None
    return pagina(d, l, aqui, {x: ruta_pieza(p, x) for x in config.IDIOMAS},
                  f'{p["nombre"][l]} · Asha Jewelry Miami', p["descripcion"][l], cuerpo,
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
<p><a class="boton boton-oro" href="{esc(href_c)}">{esc(etiqueta_c)}</a></p></div></article></div>"""
    return pagina(d, l, aqui, {x: ruta_servicio(s, x) for x in config.IDIOMAS},
                  f'{s["titulo"][l]} · Asha Jewelry Miami', s["intro"][l], cuerpo,
                  [schema.tienda(d, l), schema.servicio(d, l, s)], actual="servicios")


def financiamiento(d, l):
    aqui = ruta("financiamiento", l)
    href_c, etiqueta_c = enlace_contacto(d, l)
    cuerpo = f"""<div class="seccion envoltura"><h1>{esc(tx(d, "nav_financiamiento", l))}</h1>
<p class="entradilla">{esc(tx(d, "financiamiento_intro", l))}</p>
<h2>{esc(tx(d, "financiamiento_plataformas_t", l))}</h2><ul class="pagos">{"".join(f"<li>{esc(x)}</li>" for x in d["negocio"]["pagos"])}</ul>
<h2>{esc(tx(d, "financiamiento_layaway_t", l))}</h2><p>{esc(tx(d, "financiamiento_layaway_p", l))}</p>
<p><a class="boton boton-oro" href="{esc(href_c)}">{esc(etiqueta_c)}</a></p></div>"""
    return pagina(d, l, aqui, _alternos("financiamiento"), tx(d, "meta_financiamiento_t", l),
                  tx(d, "meta_financiamiento_d", l), cuerpo, [schema.tienda(d, l)], actual="financiamiento")


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
<p class="acciones" style="justify-content:flex-start"><a class="boton boton-oro" href="{esc(base)}">{esc(tx(d, "volver_inicio", "es"))}</a>
<a class="boton boton-borde" href="{esc(base)}en/" lang="en">{esc(tx(d, "volver_inicio", "en"))}</a></p></div>"""
    return pagina(d, "es", "", _alternos("inicio"), tx(d, "e404_t", "es") + " · Asha Jewelry Miami",
                  tx(d, "e404_t", "es"), cuerpo, [], indexable=False, absoluto=True)


def _comprobar_fotos(d, man):
    faltan = [f"{x.get('id', 'negocio')}: foto {f} no está en img/originales/"
              for x in d["piezas"] + d["servicios"] + [d["negocio"]]
              for f in x.get("fotos", []) if f not in man]
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
        salida.append((archivo(ruta("financiamiento", l)), financiamiento(d, l)))
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

> Joyería en un kiosko dentro de {n["dentro_de"]}, {direccion_corta(d)}. Oro 10K, 14K y 18K, reparación de joyas, ajuste de talla de anillos, grabado y joyas a medida. Financiamiento ({", ".join(n["pagos"])}) y layaway. Abre de martes a domingo; cerrado los lunes. Teléfono {n["telefono_visible"]}. Abrió en abril de 2026.

> Jewelry kiosk inside {n["dentro_de"]}, {direccion_corta(d)}. 10K, 14K and 18K gold, jewelry repair, ring sizing, engraving and custom jewelry. Financing ({", ".join(n["pagos"])}) and layaway. Open Tuesday to Sunday; closed on Mondays.

Desambiguación / Disambiguation: no es ASHA by Ashley McCormick (Palm Beach) ni Asha Jewelry de Adelaida, Australia (ashajewelry.com). Not affiliated with either.

- [Inicio]({base})
- [Home (English)]({base}en/)
- [Catálogo]({base}{ruta("catalogo", "es")})
- [Servicios]({base}{ruta("servicios", "es")})
- [Cómo llegar]({base}{ruta("como_llegar", "es")})
- [Instagram]({n["instagram"]})
"""
```

- [ ] **Step 4: Implementar sitio.py**

`herramientas/sitio.py`:
```python
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
```

- [ ] **Step 5: Verificar que pasa**

Run: `python -m unittest discover -s tests -t . -v`
Expected: 60 tests OK

- [ ] **Step 6: Generar el sitio real**

Run: `python herramientas/sitio.py`
Expected:
```
35 páginas generadas en publico/ · LANZADO=False · https://cisnerosmusic.github.io/ashajewelry-site/
Aviso: 13 elementos siguen con contenido provisional (ver PENDIENTES.md).
Comprobaciones: OK
```

- [ ] **Step 7: Revisión en el navegador**

Crea `.claude/launch.json` en la raíz del repo:
```json
{
  "version": "0.0.1",
  "configurations": [
    {"name": "asha", "runtimeExecutable": "python", "runtimeArgs": ["-m", "http.server", "8430", "--directory", "publico"], "port": 8430}
  ]
}
```
Abre la vista previa con `preview_start {name: "asha"}`. Revisa `/`, `/en/`, `/catalogo/` (prueba los filtros), una ficha, `/servicios/grabado/` y `/como-llegar/`, en escritorio y con `resize_window` en modo `mobile` (prueba el menú y el botón fijo). Mira la consola por si hay errores. Haz una captura de la portada en móvil y otra en escritorio para enseñárselas a Ernesto.

- [ ] **Step 8: Commit**

```bash
git add herramientas/paginas.py herramientas/sitio.py tests/test_sitio.py publico .claude/launch.json
git commit -m "Páginas ES/EN, 404, robots, llms y primera generación de publico/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Documentación, GitHub Pages y verificación en vivo

**Files:**
- Create: `README.md` (reemplaza el actual), `CLAUDE.md`, `PENDIENTES.md`, `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: `publico/` generado.
- Produces: la vista previa pública en `https://cisnerosmusic.github.io/ashajewelry-site/`.

- [ ] **Step 1: Workflow**

`.github/workflows/pages.yml`:
```yaml
name: Publicar en GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  publicar:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.despliegue.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: publico
      - id: despliegue
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: README.md**

```markdown
# Asha Jewelry Miami · sitio web

Sitio de [Asha Jewelry Miami](https://www.instagram.com/ashajewelryshop/), joyería en el kiosko 2 dentro de Mercado Fresco y Más (12107 SW 152nd St, Miami, FL 33177). Hecho por [Index01](https://index01.net).

- **Vista previa:** https://cisnerosmusic.github.io/ashajewelry-site/ (con `noindex` hasta el lanzamiento)
- **Dominio:** ashajewelryusa.com (GoDaddy, del cliente; aún sin conectar)
- **Diseño:** `docs/superpowers/specs/2026-10-02-ashajewelry-site-design.md`
- **Pendientes:** `PENDIENTES.md`

## Cómo funciona

Todo el contenido vive en `datos/*.json` (español e inglés en cada campo). `herramientas/sitio.py` lo convierte en `publico/`, que es lo único que se publica: cada push a `main` lo sube a GitHub Pages con `.github/workflows/pages.yml`.

| Quiero... | Toco... |
|---|---|
| Añadir una pieza | `datos/piezas.json` y su foto en `img/originales/<nombre>.jpg` (en `fotos` va el nombre sin extensión) |
| Poner precio | `"precio": 250` en la pieza (`null` muestra "Consultar precio") |
| Anunciar una promo | `datos/promos.json` con `desde` y `hasta`; se oculta sola al vencer |
| Cambiar horario, teléfono, WhatsApp | `datos/negocio.json` |
| Cambiar un texto | `datos/textos.json` |
| Cambiar colores o diseño | `estaticos/css/sitio.css` y subir `VERSION` en `herramientas/config.py` |

Después de cualquier cambio:

    python herramientas/sitio.py
    python -m unittest discover -s tests -t .

y push. Para verlo en local: `python -m http.server 8430 --directory publico`.

## Lanzamiento (conectar ashajewelryusa.com)

1. Dar de alta la zona en Cloudflare (cuenta de Index01) y que el cliente cambie los NS en GoDaddy.
2. En Cloudflare, registros hacia GitHub Pages: `A` en `@` a 185.199.108.153, .109.153, .110.153 y .111.153, y `CNAME` en `www` a `cisnerosmusic.github.io`, todos sin proxy.
3. `LANZADO = True` en `herramientas/config.py`, regenerar y push (se escriben `CNAME` y `sitemap.xml` y desaparece el `noindex`).
4. En Settings > Pages del repo, dominio personalizado `ashajewelryusa.com` y "Enforce HTTPS".
```

- [ ] **Step 3: CLAUDE.md**

```markdown
# Asha Jewelry Miami · contexto para IA

Sitio estático generado desde datos. Lee [README.md](README.md) antes de tocar nada y [PENDIENTES.md](PENDIENTES.md) para lo que falta.

- Nunca editar `publico/` a mano: se cambia `datos/`, `estaticos/` o `herramientas/` y se regenera con `python herramientas/sitio.py`.
- Nunca editar texto con Get-Content/Set-Content de PowerShell (rompe el UTF-8): usar herramientas de edición de archivos.
- Sin raya larga en textos públicos.
- No publicar datos sin fuente: horas, WhatsApp y coordenadas están en `null` hasta que el dueño los confirme. Lo no verificado va a PENDIENTES.md.
- Sin fotos de stock ni generadas con IA: si falta una foto, el sitio pone el marco "Foto próximamente".
- Español en la raíz, inglés en `/en/`. Toda cadena nueva lleva las dos lenguas.
- Dorado para texto solo `--oro-tinta`; `--oro` y `--oro-claro` no pasan AA como texto sobre claro.
- No es ASHA by Ashley McCormick (Palm Beach) ni Asha Jewelry de Australia (ashajewelry.com).
- Antes de push: `python -m unittest discover -s tests -t .`, regenerar y revisar en el navegador (`python -m http.server 8430 --directory publico`).
```

- [ ] **Step 4: PENDIENTES.md**

```markdown
# Pendientes

## Del cliente
- [ ] Logo original en vector o PNG transparente (SVG o el diseño de Canva). Hoy se usa el avatar de TikTok de 807 px reducido a 480 (`estaticos/img/insignia.jpg`), suficiente para la web pero con fondo blanco.
- [ ] Envíos: su TikTok dice "Shipping available" y "USA". ¿Envía a todo EE. UU.? ¿Con qué condiciones? Si se confirma, añadirlo al sitio (texto y `llms.txt`).
- [ ] Nombre de la serif del logo. Montserrat confirmada para "JEWELRY"; en la web se usa Playfair Display en los títulos.
- [ ] Horas exactas de apertura: van en `negocio.json` como `"horas": {"abre": "10:00", "cierra": "19:00"}`.
- [ ] ¿786-978-1981 es su WhatsApp? Si lo es: `"whatsapp": "+17869781981"`. Hasta entonces los botones llaman por teléfono.
- [ ] ¿Precios visibles, rangos o "Consultar precio"?
- [ ] ¿Usa Shopify POS? (acepta Shop Pay). Si lo usa, se podría importar el catálogo.
- [ ] Su historia: si tiene oficio previo y de dónde viene el nombre "Asha".
- [ ] Confirmar qué incluye cada servicio (`servicios.json`, hoy provisional).
- [ ] Fotos de piezas reales (sustituyen a las 8 piezas provisionales).
- [ ] Permiso para mencionar y fotografiar Mercado Fresco y Más.
- [ ] ¿Ficha de Google Business? Si no hay, crearla y verificarla.

## De Index01
- [ ] Fotos del kiosko y de la entrada de Fresco y Más (Ernesto). Van a `img/originales/` y a `"fotos"` en `negocio.json`.
- [ ] Coordenadas exactas del kiosko para `negocio.json` (`"geo": {"lat": ..., "lon": ...}`), tomadas en el sitio.
- [ ] Lanzamiento: ver README, sección "Lanzamiento".
```

- [ ] **Step 5: Commit y push**

```bash
git add README.md CLAUDE.md PENDIENTES.md .github/workflows/pages.yml
git commit -m "Documentación (README, CLAUDE, PENDIENTES) y despliegue a GitHub Pages

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push origin main
```

- [ ] **Step 6: Activar Pages con fuente "GitHub Actions"**

Con el token del almacén de credenciales de git (nunca mostrarlo en la salida):
```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n\n" | git credential fill | sed -n 's/^password=//p')
curl -s -o /dev/null -w "%{http_code}\n" -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/cisnerosmusic/ashajewelry-site/pages -d '{"build_type":"workflow"}'
```
Expected: `201` (o `409` si ya existía; en ese caso, `PUT` al mismo endpoint con el mismo cuerpo, que devuelve `204`).
Después relanza el workflow: `curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" https://api.github.com/repos/cisnerosmusic/ashajewelry-site/actions/workflows/pages.yml/dispatches -d '{"ref":"main"}'`.

- [ ] **Step 7: Verificación en vivo**

Cuando el workflow termine (consultar `GET /repos/cisnerosmusic/ashajewelry-site/actions/runs?per_page=1` hasta que `conclusion` sea `success`):
```bash
for p in "" en/ catalogo/ en/catalog/gold-ring/ servicios/grabado/ como-llegar/ css/sitio.css README.md CLAUDE.md PENDIENTES.md datos/negocio.json; do
  echo "$(curl -s -o /dev/null -w '%{http_code}' https://cisnerosmusic.github.io/ashajewelry-site/$p) $p"; done
```
Expected: `200` en las seis páginas y en el CSS; `404` en `README.md`, `CLAUDE.md`, `PENDIENTES.md` y `datos/negocio.json`.
Abre `https://cisnerosmusic.github.io/ashajewelry-site/` en el navegador integrado y haz una captura en móvil para Ernesto.

Esa es la vista previa que Ernesto le enseña a su amigo.
