import unittest
from pathlib import Path

from herramientas import adornos, datos, plantilla

RAIZ = Path(__file__).resolve().parent.parent


class TestAdornos(unittest.TestCase):
    def test_lee_el_vector_original(self):
        caja, trazo, regla = adornos.LOGO
        self.assertEqual(len(caja.split()), 4)
        self.assertGreater(trazo.count("M"), 30)
        self.assertEqual(regla, "evenodd")

    def test_diamante_y_estrella_son_parte_del_logo(self):
        self.assertTrue(adornos.DIAMANTE)
        self.assertTrue(adornos.ESTRELLA)
        for sub in (adornos.DIAMANTE + adornos.ESTRELLA).split("M")[1:]:
            self.assertIn("M" + sub, adornos.LOGO[1])

    def test_subtrazos_descarta_lo_que_sale_del_poligono(self):
        trazo = "M1 1L2 1L2 2ZM5 5L9 9L5 9Z"
        caja = [(0, 0), (3, 0), (3, 3), (0, 3)]
        self.assertEqual(adornos.subtrazos(trazo, caja), "M1 1L2 1L2 2Z")

    def test_todo_pinta_con_el_degradado(self):
        for svg in (adornos.logo(), adornos.letras(), adornos.diamante(),
                    adornos.estrella(), adornos.separador()):
            self.assertIn('fill="url(#oro)"', svg)

    def test_etiqueta_accesible(self):
        self.assertIn('role="img" aria-label="ASHA Jewelry"', adornos.logo(etiqueta="ASHA Jewelry"))
        self.assertIn('aria-hidden="true"', adornos.diamante())

    def test_la_pagina_define_trazados_una_vez(self):
        d = datos.cargar(RAIZ / "datos")
        h = plantilla.pagina(d, "es", "", {"es": "", "en": "en/"}, "T", "D",
                             adornos.logo() + adornos.diamante() + adornos.diamante(), [])
        for ident in ("oro", "asha-logo", "asha-letras", "asha-diamante", "asha-estrella"):
            self.assertEqual(h.count(f'id="{ident}"'), 1, ident)


if __name__ == "__main__":
    unittest.main()
