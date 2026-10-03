# Pendientes

## Del cliente
- [ ] Logo original en vector (SVG o el diseño de Canva). Mientras tanto, el diamante, las estrellas y las florituras están redibujados en SVG (`herramientas/adornos.py`) a partir de la versión dorada sobre oscuro, y "ASHA" se compone con Playfair Display. Si llega el original, comparar y ajustar.
- [ ] Licencia de Jitter (la letra de "ASHA"): la ficha de Adys usa JitterDEMO. Preguntar a Adys si se compró la licencia comercial. La web no la usa como fuente (el logo va en trazos; los títulos, en Playfair Display); el texto va en Raleway, la de "JEWELRY".
- [ ] ¿786-978-1981 es su WhatsApp? Si lo es: `"whatsapp": "+17869781981"`. Hasta entonces los botones llaman por teléfono.
- [ ] Envíos: su TikTok dice "Shipping available" y "USA". ¿Envía a todo EE. UU.? ¿Con qué condiciones? Si se confirma, añadirlo al sitio (textos y `llms.txt`).
- [ ] Confirmar plataformas de financiamiento: un texto de IG de agosto dice solo Affirm y Afterpay; los de septiembre, Affirm, Afterpay, Shop Pay, Klarna y Zip (la web usa la lista reciente).
- [ ] Quilataje de cada pieza (10K, 14K o 18K): hoy las fichas dicen solo "Oro". Requiere añadir el campo `quilataje` a `piezas.json` y mostrarlo.
- [ ] ¿Precios visibles, rangos o "Consultar precio"? Sin precio, Google marcará las fichas `Product` como incompletas tras el lanzamiento.
- [ ] ¿Usa Shopify POS? (acepta Shop Pay). Si lo usa, se podría importar el catálogo.
- [ ] Su historia: ¿tiene oficio previo? (El origen del nombre ya está resuelto como contexto interno; ver CLAUDE.md.)
- [ ] Confirmar qué incluye cada servicio (`servicios.json`, hoy provisional).
- [ ] Fotos de piezas reales (sustituyen a las 8 piezas provisionales).
- [ ] Foto de la portada (`muestra-joyas.jpg`, sacada de la pancarta de la tienda): confirmar de dónde salió y si se puede usar en la web. Si es de un banco de imágenes, hace falta la licencia.
- [ ] Permiso para mencionar y fotografiar Mercado Fresco y Más.
- [ ] Ficha de Google Business (existe, ver CONTEXTO.md): cambiar el horario de martes a sábado a 10 a. m. a 7 p. m. para que coincida con la web; categoría principal "Joyería" (Jewelry store) en vez de "Jewelry manufacturer", y como secundarias "Servicio de reparación de joyas" y "Joyero"; sitio web `https://ashamiami.com` (al lanzar seguirá funcionando por la 301); nombre "ASHA Jewelry" como en el letrero; fotos del kiosko, la entrada y piezas.

## De Index01
- [ ] Fotos del kiosko y de la entrada de Fresco y Más (Ernesto). Van a `img/originales/` y a `"fotos"` en `negocio.json`.
- [ ] Coordenadas: la web usa la chincheta de la ficha de Google. Si se toman en el kiosko y difieren, corregir `geo` en `negocio.json` y la chincheta de la ficha a la vez.
- [ ] Lanzamiento: ver README, sección "Lanzamiento" (incluye la redirección de ashajewelrymiami.com y ashamiami.com).

## Mejoras menores anotadas en la revisión del código
- [ ] `llms.txt` repite a mano quilates y servicios: generarlo desde `datos/` (el horario ya sale de `textos.json`).
- [ ] `sitio.py` vacía `publico/` antes de comprobar las fotos: comprobarlas antes.
- [ ] Promos: la fecha se evalúa al generar, no al visitar. Antes de la primera promo, añadir un `schedule` diario al workflow que regenere, o validar fechas ISO y ocultarlas también con JS.
- [ ] El workflow publica `publico/` tal cual: añadir pruebas y regeneración en CI.
- [ ] "Pregunta por esta pieza" llama por teléfono mientras no haya WhatsApp (se pierde el nombre de la pieza).
- [ ] Filtros del catálogo con `role="button"`: falta activar con la barra espaciadora.
- [ ] `imagenes.py` convierte a RGB (pierde transparencia) y decide la caché solo por fecha de modificación.
- [ ] La "A" de los iconos queda un 3 % baja.
