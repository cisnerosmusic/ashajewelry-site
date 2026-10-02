# Pendientes

## Del cliente
- [ ] Logo original en vector o PNG transparente (SVG o el diseño de Canva). Hoy se usa el avatar de TikTok de 807 px reducido a 480 (`estaticos/img/insignia.jpg`): sirve para la web, pero tiene fondo blanco.
- [ ] Nombre de la serif del logo. Montserrat confirmada para "JEWELRY"; en la web se usa Playfair Display en los títulos.
- [ ] Horas exactas de apertura: van en `negocio.json` como `"horas": {"abre": "10:00", "cierra": "19:00"}`.
- [ ] ¿786-978-1981 es su WhatsApp? Si lo es: `"whatsapp": "+17869781981"`. Hasta entonces los botones llaman por teléfono.
- [ ] Envíos: su TikTok dice "Shipping available" y "USA". ¿Envía a todo EE. UU.? ¿Con qué condiciones? Si se confirma, añadirlo al sitio (textos y `llms.txt`).
- [ ] ¿Precios visibles, rangos o "Consultar precio"?
- [ ] ¿Usa Shopify POS? (acepta Shop Pay). Si lo usa, se podría importar el catálogo.
- [ ] Su historia: si tiene oficio previo y de dónde viene el nombre "Asha".
- [ ] Confirmar qué incluye cada servicio (`servicios.json`, hoy provisional).
- [ ] Fotos de piezas reales (sustituyen a las 8 piezas provisionales).
- [ ] Permiso para mencionar y fotografiar Mercado Fresco y Más.
- [ ] ¿Ficha de Google Business? Si no hay, crearla y verificarla.

## De Index01
- [ ] Fotos del kiosko y de la entrada de Fresco y Más (Ernesto). Van a `img/originales/` y a `"fotos"` en `negocio.json`.
- [ ] Coordenadas exactas del kiosko para `negocio.json` (`"geo": {"lat": ..., "lon": ...}`), tomadas en el sitio.
- [ ] Lanzamiento: ver README, sección "Lanzamiento" (incluye la redirección de ashajewelrymiami.com y ashamiami.com).

## Mejoras menores anotadas en la revisión del código
- [ ] `llms.txt` repite a mano quilates, servicios y días: generarlo desde `datos/`.
- [ ] `sitio.py` vacía `publico/` antes de comprobar las fotos: comprobarlas antes.
- [ ] Foco visible con poco contraste sobre el pie oscuro y el botón dorado fijo.
- [ ] Filtros del catálogo con `role="button"`: falta activar con la barra espaciadora.
- [ ] `imagenes.py` convierte a RGB (pierde transparencia) y decide la caché solo por fecha de modificación.
- [ ] La "A" de los iconos queda un 3 % baja.
