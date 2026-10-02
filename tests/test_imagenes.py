import tempfile
import unittest
from pathlib import Path

from PIL import Image

from herramientas import imagenes


class TestImagenes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        raiz = Path(self.tmp.name)
        self.origen = raiz / "originales"
        self.destino = raiz / "fotos"
        self.origen.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def _foto(self, nombre, ancho, alto, exif=False):
        im = Image.new("RGB", (ancho, alto), "#BA8621")
        ruta = self.origen / nombre
        if exif:
            e = Image.Exif()
            e[0x010F] = "CamaraSecreta"
            im.save(ruta, exif=e)
        else:
            im.save(ruta)
        return ruta

    def test_tres_anchos(self):
        self._foto("grande.jpg", 2000, 1500)
        m = imagenes.procesar(self.origen, self.destino)
        self.assertEqual([w for w, _ in m["grande"]], [480, 960, 1600])
        self.assertEqual(m["grande"][0][1], "img/fotos/grande-480.webp")
        with Image.open(self.destino / "grande-960.webp") as im:
            self.assertEqual(im.size, (960, 720))

    def test_no_amplia(self):
        self._foto("media.png", 600, 600)
        self._foto("chica.jpg", 300, 200)
        m = imagenes.procesar(self.origen, self.destino)
        self.assertEqual([w for w, _ in m["media"]], [480, 600])
        self.assertEqual([w for w, _ in m["chica"]], [300])

    def test_quita_exif(self):
        self._foto("con-exif.jpg", 800, 600, exif=True)
        imagenes.procesar(self.origen, self.destino)
        with Image.open(self.destino / "con-exif-480.webp") as im:
            self.assertEqual(len(im.getexif()), 0)

    def test_borra_huerfanas(self):
        ruta = self._foto("vieja.jpg", 500, 500)
        imagenes.procesar(self.origen, self.destino)
        ruta.unlink()
        imagenes.procesar(self.origen, self.destino)
        self.assertEqual(list(self.destino.glob("vieja-*.webp")), [])

    def test_ignora_otros_archivos(self):
        (self.origen / ".gitkeep").write_text("")
        self.assertEqual(imagenes.procesar(self.origen, self.destino), {})


if __name__ == "__main__":
    unittest.main()
