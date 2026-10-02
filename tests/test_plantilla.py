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

    def test_redes_en_el_pie(self):
        h = html()
        self.assertIn('href="https://www.instagram.com/ashajewelryshop/"', h)
        self.assertIn('href="https://www.tiktok.com/@ashajewelryshop"', h)

    def test_tx_con_campos(self):
        self.assertEqual(plantilla.tx(D, "msg_pieza", "es", nombre="Anillo", id="a1"),
                         "Hola, me interesa esta pieza de su web: Anillo (a1)")


if __name__ == "__main__":
    unittest.main()
