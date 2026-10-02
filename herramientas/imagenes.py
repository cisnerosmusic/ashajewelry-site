"""De img/originales/ a WebP en varios anchos, sin metadatos EXIF (que
pueden llevar ubicación). Solo re-codifica lo que cambió."""
from pathlib import Path

from PIL import Image, ImageOps

ANCHOS = (480, 960, 1600)
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}


def procesar(origen, destino, prefijo="img/fotos/"):
    origen, destino = Path(origen), Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    manifiesto = {}
    vivos = set()
    for f in sorted(origen.iterdir()):
        if f.suffix.lower() not in EXTENSIONES:
            continue
        with Image.open(f) as abierta:
            im = ImageOps.exif_transpose(abierta).convert("RGB")
        variantes = []
        for w in ANCHOS:
            ancho = min(w, im.width)
            salida = destino / f"{f.stem}-{ancho}.webp"
            vivos.add(salida.name)
            if not salida.exists() or salida.stat().st_mtime < f.stat().st_mtime:
                alto = round(im.height * ancho / im.width)
                im.resize((ancho, alto), Image.LANCZOS).save(salida, "WEBP", quality=82, method=6)
            variantes.append([ancho, prefijo + salida.name])
            if ancho == im.width:
                break
        manifiesto[f.stem] = variantes
    for vieja in destino.glob("*.webp"):
        if vieja.name not in vivos:
            vieja.unlink()
    return manifiesto
