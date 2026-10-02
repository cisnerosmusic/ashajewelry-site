# ASHA Jewelry Miami · contexto para IA

Sitio estático generado desde datos. Lee [README.md](README.md) antes de tocar nada y [PENDIENTES.md](PENDIENTES.md) para lo que falta.

- Nunca editar `publico/` a mano: se cambia `datos/`, `estaticos/` o `herramientas/` y se regenera con `python herramientas/sitio.py`.
- Nunca editar texto con Get-Content/Set-Content de PowerShell ni con `sed -i` (rompen el UTF-8): usar herramientas de edición de archivos.
- La marca se escribe siempre ASHA, en mayúsculas (ASHA Jewelry Miami), en textos, títulos y datos. Convención de Ernesto (2-oct-2026).
- Sin raya larga en textos públicos; en código Python, escrita como `"—"`.
- No publicar datos sin fuente: horas, WhatsApp, coordenadas y envíos no se publican hasta que el dueño los confirme. Lo no verificado va a PENDIENTES.md.
- Sin fotos de stock ni generadas con IA: si falta una foto, el sitio pone el marco "Foto próximamente".
- Español en la raíz, inglés en `/en/`. Toda cadena nueva lleva las dos lenguas.
- Dorado para texto solo `--oro-tinta`; `--oro` y `--oro-claro` no pasan AA como texto sobre claro.
- Contexto interno, no para la web: "ASHA" combina los nombres de la familia del dueño (Billy). Decisión de Ernesto (2-oct-2026): los nombres de los hijos no se publican nunca en ningún lugar público, y la anécdota no va al sitio; se guarda solo como contexto para cuando haga falta.
- No es ASHA by Ashley McCormick (Palm Beach) ni Asha Jewelry de Australia (ashajewelry.com).
- Antes de push: `python -m unittest discover -s tests -t .`, regenerar y revisar en el navegador (`python -m http.server 8430 --directory publico`).
