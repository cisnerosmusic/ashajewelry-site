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
