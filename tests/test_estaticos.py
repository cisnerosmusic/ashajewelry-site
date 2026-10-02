import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def reglas(nombre):
    css = (RAIZ / "estaticos" / "css" / nombre).read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


class TestEstaticos(unittest.TestCase):
    def test_boton_flotante_sigue_fijo(self):
        # Regresión: la capa de movimiento le puso position:relative y dejó de flotar.
        for nombre in ("sitio.css", "movimiento.css"):
            for selector, cuerpo in reglas(nombre):
                propios = [x.strip() for x in selector.split(",")]
                if ".contacto-fijo" in propios and "position:" in cuerpo.replace(" ", ""):
                    self.assertIn("position:fixed", cuerpo.replace(" ", ""), f"{nombre}: {selector.strip()}")

    def test_pie_pegado_abajo(self):
        cuerpos = {sel.strip(): c.replace(" ", "") for sel, c in reglas("sitio.css")}
        self.assertIn("min-height:100vh", cuerpos["body"])
        self.assertIn("flex-direction:column", cuerpos["body"])
        self.assertIn("flex:10auto", cuerpos["main"])


if __name__ == "__main__":
    unittest.main()
