import tempfile
import unittest
from pathlib import Path

from PIL import Image

from herramientas import marca

RAIZ = Path(__file__).resolve().parent.parent


class TestMarca(unittest.TestCase):
    def test_genera_iconos_y_og(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp)
            marca.generar(destino)
            esperados = {
                "favicon-32.png": (32, 32), "apple-touch-icon.png": (180, 180),
                "icon-192.png": (192, 192), "icon-512.png": (512, 512),
                "img/og.png": (1200, 630),
            }
            for nombre, tam in esperados.items():
                with Image.open(destino / nombre) as im:
                    self.assertEqual(im.size, tam, nombre)


if __name__ == "__main__":
    unittest.main()
