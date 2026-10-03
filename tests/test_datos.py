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

    def test_horas_lunes_cerrado(self):
        d = reales()
        d["negocio"]["horas"][0]["dias"].append("Mo")
        with self.assertRaisesRegex(ErrorDatos, "Mo no está en negocio.dias"):
            datos.validar(d)

    def test_horas_dia_repetido(self):
        d = reales()
        d["negocio"]["horas"][1]["dias"].append("Tu")
        with self.assertRaisesRegex(ErrorDatos, "más de un tramo"):
            datos.validar(d)

    def test_horas_formato(self):
        d = reales()
        d["negocio"]["horas"][0]["cierra"] = "7pm"
        with self.assertRaisesRegex(ErrorDatos, "HH:MM"):
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
