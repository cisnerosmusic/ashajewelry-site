import tempfile
import unittest
from pathlib import Path

from herramientas import comprobar

CSS_BUENO = """:root{--claro:#CFF2F6;--oscuro:#102A43;--oro-claro:#DEAC3B;--oro:#BA8621;
--tinta:#1A1408;--blanco:#FFFFFF;--gris:#4A4438}"""


class TestContraste(unittest.TestCase):
    def test_blanco_negro(self):
        self.assertAlmostEqual(comprobar.contraste("#FFFFFF", "#000000"), 21.0, places=1)

    def test_tokens(self):
        self.assertEqual(comprobar.tokens_css(CSS_BUENO)["oscuro"], "#102A43")

    def test_paleta_buena_pasa(self):
        self.assertEqual(comprobar.comprobar_contraste(CSS_BUENO), [])

    def test_oro_claro_sobre_oscuro_claro_falla(self):
        malo = CSS_BUENO.replace("--oscuro:#102A43", "--oscuro:#5A7A93")
        problemas = comprobar.comprobar_contraste(malo)
        self.assertTrue(any("--oro-claro sobre --oscuro" in p for p in problemas))

    def test_token_ausente_es_problema(self):
        problemas = comprobar.comprobar_contraste(":root{--tinta:#000000}")
        self.assertTrue(any("falta" in p for p in problemas))

    def test_css_del_sitio_pasa(self):
        raiz = Path(__file__).resolve().parent.parent
        css = (raiz / "estaticos" / "css" / "sitio.css").read_text(encoding="utf-8")
        self.assertEqual(comprobar.comprobar_contraste(css), [])


class TestRayas(unittest.TestCase):
    def test_detecta_raya(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "a.html"
            f.write_text("hola \u2014 mundo", encoding="utf-8")
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
