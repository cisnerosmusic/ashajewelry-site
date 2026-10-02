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
