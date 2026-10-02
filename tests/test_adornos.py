import unittest
from pathlib import Path

from herramientas import adornos, datos, plantilla

RAIZ = Path(__file__).resolve().parent.parent


class TestAdornos(unittest.TestCase):
    def test_trazos_del_diamante_salen_de_las_lineas(self):
        self.assertTrue(adornos.DIAMANTE_TRAZOS.startswith("M22 3L78 3L97 26"))
        self.assertEqual(adornos.DIAMANTE_TRAZOS.count("M"), len(adornos.DIAMANTE_LINEAS))

    def test_todo_pinta_con_el_degradado(self):
        for svg in (adornos.diamante(), adornos.estrella(), adornos.corona(), adornos.separador()):
            self.assertIn("url(#oro)", svg)
            self.assertIn('aria-hidden="true"', svg)

    def test_la_pagina_define_el_degradado_una_vez(self):
        d = datos.cargar(RAIZ / "datos")
        h = plantilla.pagina(d, "es", "", {"es": "", "en": "en/"}, "T", "D",
                             adornos.corona() + adornos.diamante(), [])
        self.assertEqual(h.count('id="oro"'), 1)


if __name__ == "__main__":
    unittest.main()
