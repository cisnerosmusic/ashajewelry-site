# ASHA Jewelry Miami · contexto para IA

Sitio estático generado desde datos. Antes de tocar nada lee, en este orden: [CONTEXTO.md](CONTEXTO.md) (estado, decisiones y por qué), [README.md](README.md) (cómo funciona) y [PENDIENTES.md](PENDIENTES.md) (lo que falta).

## Reglas de trabajo
- Nunca editar `publico/` a mano: se cambia `datos/`, `estaticos/` o `herramientas/` y se regenera con `python herramientas/sitio.py`.
- Nunca editar texto con Get-Content/Set-Content de PowerShell ni con `sed -i` (rompen el UTF-8): usar herramientas de edición de archivos o un script de Python que lea y escriba en UTF-8.
- Si un plan trae el código exacto, copiarlo con un script, no transcribirlo con un modelo barato: los subagentes rápidos estropean tildes y rayas.
- Antes de push: `python -m unittest discover -s tests -t .`, regenerar, revisar en el navegador (`python -m http.server 8430 --directory publico`) y subir `VERSION` en `herramientas/config.py` si cambió CSS o JS.
- Trabajo en la rama `sitio-v1`; se pasa a `main` (fast-forward) solo con el visto bueno de Ernesto. Cada push a `main` publica.

## Convenciones de Ernesto
- La marca se escribe siempre **ASHA**, en mayúsculas (ASHA Jewelry Miami), en textos, títulos y datos.
- Sin raya larga (U+2014) en ningún texto ni archivo; en código Python, solo como escape unicode, nunca el carácter.
- **El oro nunca va sobre el azul claro.** Fondo claro (`--claro`, aqua) con texto negro; bloques oscuros (`--oscuro`, azul marino) y negros (`--tinta`) con texto blanco u oro.
- **Transiciones cinematográficas**: es una joyería. Tiempos largos y curvas suaves, nunca cambios secos. Todo el movimiento vive en la capa separable `estaticos/css/movimiento.css` + `estaticos/js/movimiento.js`.
- El logo es el **original de Adys** en vector (`marca/`); no se redibuja. El diamante y la estrella son subtrazados del propio logo (`herramientas/adornos.py`).
- En las imágenes (redes sociales, iconos) solo la marca y "MIAMI": la dirección, el kiosko y Fresco y Más van en el texto, no en la imagen.
- Tipografías: **Raleway** para el texto (la de "JEWELRY" en el logo) y Playfair Display para los títulos. Jitter ("ASHA") no se usa como fuente.

## Datos y privacidad
- No publicar datos sin fuente: horas, WhatsApp, coordenadas y envíos no se publican hasta que el dueño los confirme. Lo no verificado va a PENDIENTES.md.
- Sin fotos de stock ni generadas con IA: si falta una foto, el sitio pone el marco "Foto próximamente". Excepción decidida por Ernesto: `img/originales/muestra-joyas.jpg`, la foto de la pancarta de la tienda, en la portada. Su origen y licencia están por confirmar; no describir sus piezas como productos de la tienda.
- Contexto interno, no para la web: "ASHA" combina los nombres de la familia del dueño (Billy). Los nombres de los hijos no se publican nunca en ningún lugar público, y la anécdota no va al sitio.
- El repo es **público**: nada de precios acordados con el cliente, datos personales ni rutas privadas.
- No es ASHA by Ashley McCormick (Palm Beach) ni Asha Jewelry de Australia (ashajewelry.com).
