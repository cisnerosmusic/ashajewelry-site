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
