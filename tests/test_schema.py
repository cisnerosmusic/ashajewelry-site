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
        self.assertIn("https://www.tiktok.com/@ashajewelryshop", t["sameAs"])

    def test_sin_horas_no_hay_horario(self):
        d = copy.deepcopy(D)
        d["negocio"]["horas"] = None
        self.assertNotIn("openingHoursSpecification", schema.tienda(d, "es"))

    def test_horario_por_tramos(self):
        d = copy.deepcopy(D)
        d["negocio"]["horas"] = [
            {"dias": ["Tu", "We", "Th", "Fr", "Sa"], "abre": "10:00", "cierra": "19:00"},
            {"dias": ["Su"], "abre": "10:00", "cierra": "17:00"},
        ]
        semana, domingo = schema.tienda(d, "en")["openingHoursSpecification"]
        self.assertIn("https://schema.org/Tuesday", semana["dayOfWeek"])
        self.assertNotIn("https://schema.org/Monday", semana["dayOfWeek"])
        self.assertEqual(semana["closes"], "19:00")
        self.assertEqual(domingo["dayOfWeek"], ["https://schema.org/Sunday"])
        self.assertEqual(domingo["closes"], "17:00")

    def test_sin_geo_ni_mapa_no_se_emiten(self):
        d = copy.deepcopy(D)
        d["negocio"]["geo"] = None
        d["negocio"]["mapa"] = None
        t = schema.tienda(d, "es")
        self.assertNotIn("geo", t)
        self.assertNotIn("hasMap", t)

    def test_geo_y_mapa(self):
        t = schema.tienda(D, "es")
        self.assertEqual(t["geo"]["@type"], "GeoCoordinates")
        self.assertTrue(t["hasMap"].startswith("https://www.google.com/maps"))

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
