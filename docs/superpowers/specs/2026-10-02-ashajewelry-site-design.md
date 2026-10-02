# Asha Jewelry Miami · diseño del sitio

Fecha: 2026-10-02 · Estado: aprobado por Ernesto, pendiente de plan de implementación.

## 1. Contexto

Asha Jewelry Miami es una joyería en un kiosko dentro del supermercado Mercado Fresco y Más (12107 SW 152nd St, Kiosk 2, Miami, FL 33177). Abrió el 14 de abril de 2026. El dueño es amigo de Ernesto y el local queda junto a su casa. Cliente de Index01.

Hoy no tiene web ni ficha de Google detectable. Su única presencia es Instagram [@ashajewelryshop](https://www.instagram.com/ashajewelryshop/): unos 163 seguidores, solo reels y textos en español.

El objetivo del sitio, por orden de importancia:

1. **Que lo encuentren y sepan llegar**: Google, mapa y la referencia "dentro de Fresco y Más, kiosko 2".
2. **Que confíe quien llega**: oro auténtico, servicios reales, fotos reales.
3. **Que escriba o vaya**: WhatsApp en todas partes.

No es una tienda online. En esta fase es una vitrina.

**Decisión de Ernesto:** construir la web **definitiva** desde el principio, con contenido provisional donde falten materiales, y enseñársela al dueño desde la vista previa de GitHub Pages. El dominio `ashajewelryusa.com` (GoDaddy, del cliente, sin uso, vence el 14-jun-2029) se conecta al final, delegando los NS a Cloudflare.

## 2. Datos verificados (fuente: Instagram, 2-oct-2026)

| Dato | Valor |
|---|---|
| Nombre público | Asha Jewelry Miami (marca: ASHA Jewelry) |
| Ubicación | Dentro de Mercado Fresco y Más · 12107 SW 152nd St, Kiosk 2, Miami, FL 33177 |
| Horario | Martes a domingo. Cerrado los lunes. **Horas exactas: pendiente** |
| Teléfono | 786-978-1981 (**¿es también su WhatsApp?: pendiente**) |
| Productos | Oro 10K, 14K y 18K (en algunos textos, "oro auténtico"), plata, piezas a medida |
| Servicios | Reparación de joyería, ajuste de talla de anillos, grabado, fabricación y piezas personalizadas (dijes con nombre, iniciales) |
| Pago | Affirm, Afterpay, Shop Pay, Klarna, Zip. Financiamiento y layaway |
| Promos ya hechas | Sorteo del Día de las Madres (por cada $150 de compra), dijes en agosto, iniciales y aretes para el regreso a clases |
| Tono | Cercano y juguetón ("Si pasas por aquí te garantizo que no te vas con las manos vacías") |

Lo que no está verificado no se publica: se anota en `PENDIENTES.md`.

**Desambiguación.** Existen otras dos marcas con nombre parecido, con las que no hay que confundirlo:

- ASHA by Ashley McCormick (Palm Beach).
- Asha Jewelry de Adelaida, Australia, dueña de `ashajewelry.com`.

En el sitio, la identidad siempre incluye "Miami" y "dentro de Fresco y Más".

## 3. Idiomas

- **Español en la raíz (`/`)**: el 66 % de su público en persona habla español.
- **Inglés en `/en/`**, como espejo completo.
- Cada página enlaza a su equivalente en el otro idioma (selector visible y `hreflang`).

## 4. Mapa del sitio

| Página | ES | EN |
|---|---|---|
| Inicio | `/` | `/en/` |
| Catálogo | `/catalogo/` | `/en/catalog/` |
| Ficha de pieza | `/catalogo/<slug_es>/` | `/en/catalog/<slug_en>/` |
| Servicios | `/servicios/` | `/en/services/` |
| Reparación de joyas | `/servicios/reparacion-de-joyas/` | `/en/services/jewelry-repair/` |
| Ajuste de anillos | `/servicios/ajuste-de-anillos/` | `/en/services/ring-sizing/` |
| Grabado | `/servicios/grabado/` | `/en/services/engraving/` |
| Joyas a medida | `/servicios/joyas-a-medida/` | `/en/services/custom-jewelry/` |
| Financiamiento | `/financiamiento/` | `/en/financing/` |
| Cómo llegar | `/como-llegar/` | `/en/visit/` |
| 404 | `/404.html` (bilingüe) | |

**Inicio.** Gancho "Oro auténtico 10K, 14K y 18K, con financiamiento, dentro de Fresco y Más". Botones de WhatsApp y de Cómo llegar. Debajo: piezas destacadas, servicios, bloque de financiamiento, promo vigente y un resumen de cómo llegar.

**Catálogo.**
- Rejilla filtrable por categoría: anillos, pulseras, cadenas, dijes, aretes.
- El filtro funciona sin JavaScript, porque cada categoría tiene ancla o sección propia; con JavaScript solo mejora.
- Cada tarjeta muestra la foto, el nombre, el material y quilataje, y el precio, o "Consultar precio" si no lo tiene.

**Ficha de pieza.**
- Fotos, material, quilataje y precio opcional.
- Botón "Pregunta por esta pieza", que abre `https://wa.me/<número>?text=<mensaje con nombre e id de la pieza>`.
- Enlaces a las piezas relacionadas de la misma categoría.

**En todas las páginas:**
- Cabecera con la insignia, la navegación y el selector ES/EN.
- Botón fijo de WhatsApp en el móvil.
- Pie con dirección, horario, teléfono, Instagram, `© 2026 Asha Jewelry Miami` y el crédito "Sitio por Index01" / "Website by Index01", enlazado a https://index01.net.

**Fuera de alcance en esta fase:** carrito y pagos online, blog, reseñas incrustadas (se enlazarán a Google cuando exista la ficha), formularios.

## 5. Arquitectura

Es un sitio estático generado desde datos, con el mismo patrón que `haiti-web`.

```
datos/
  negocio.json     # nombre, dirección, kiosko, geo, horario, teléfono, whatsapp, instagram, pagos, fecha de apertura
  textos.json      # cada cadena visible en {es, en}
  servicios.json   # slug_es, slug_en, título, intro, qué incluye {es,en}, foto, provisional
  categorias.json  # id, slug_es, slug_en, nombre {es,en}
  piezas.json      # id, categoria, slug_es, slug_en, nombre {es,en}, descripcion {es,en}, material, quilataje,
                   # precio (opcional, número en USD), fotos[], destacada, disponible, provisional
  promos.json      # texto {es,en}, desde, hasta (fuera de fechas no se muestra)
img/originales/    # fotos tal como llegan; no se publican
herramientas/
  sitio.py         # genera publico/ entero y valida
  imagenes.py      # de originales a WebP en 2-3 anchos, sin EXIF, en publico/img/
publico/           # salida generada y versionada: lo único que se sirve
docs/              # specs y planes
README.md · CLAUDE.md · PENDIENTES.md
.github/workflows/pages.yml
```

**Reglas:**
- **Nunca editar HTML a mano**: se cambian `datos/` o `herramientas/` y se regenera con `python herramientas/sitio.py`.
- **`BASE`**: prefijo de rutas configurable. Vale `/ashajewelry-site/` en la vista previa de GitHub Pages y `/` con el dominio.
- **`LANZADO`**:
  - Con `LANZADO = False` (el estado actual), cada página lleva `<meta name="robots" content="noindex">` y `robots.txt` bloquea a todos los buscadores.
  - Con `LANZADO = True`: se quita el `noindex`, se genera el `sitemap.xml` con URLs absolutas de `https://ashajewelryusa.com` y se escribe `publico/CNAME`.
- **Solo Python con la librería estándar**, más Pillow en `imagenes.py`. Sin dependencias de Node.
- **Fuentes autoalojadas en WOFF2** (sin Google Fonts en tiempo de ejecución): Playfair Display para títulos y Montserrat para texto.
- **JavaScript mínimo**, solo como mejora: filtro del catálogo y menú del móvil. El sitio funciona sin JavaScript.

## 6. Datos estructurados y SEO

- **En todas las páginas**: `JewelryStore` (con `@id` estable), nombre, dirección, `geo`, teléfono, `openingHoursSpecification` (lunes cerrado; horas pendientes), `paymentAccepted`, `sameAs` con Instagram y `containedInPlace` con un `GroceryStore` "Fresco y Más" en la misma dirección.
- **Ficha de pieza**: `Product`. Lleva `Offer` (precio en USD) solo si la pieza tiene precio.
- **Servicios**: `Service`, con `provider` apuntando al `@id` de la tienda.
- **En cada página**: `hreflang` es/en/x-default, `canonical`, título y descripción propios por idioma, Open Graph con la imagen de la insignia y `llms.txt` con la descripción y la desambiguación.

## 7. Identidad visual

**Paleta, medida en el logo de Instagram:**

| Token | Hex | Uso |
|---|---|---|
| `--aqua` | `#CFF2F6` | Fondos de sección alternos y la insignia. Es un acento, no el fondo de todo, para que no se lea como Tiffany |
| `--oro-claro` | `#DEAC3B` | Brillos y adornos. Nunca texto (contraste 2.1) |
| `--oro` | `#BA8621` | Bordes, iconos y botones con texto oscuro. Nunca texto sobre blanco (contraste 3.2) |
| `--oro-tinta` | `#7A5716` | Texto y enlaces dorados (6.6 sobre blanco, 5.5 sobre aqua) |
| `--tinta` | `#1A1408` | Texto principal (18.3 sobre blanco) |
| `--blanco` | `#FFFFFF` | Fondo base |

**Tipografía:** Playfair Display en los títulos (estilo del "ASHA" del logo) y Montserrat en el texto (la de "JEWELRY", confirmada por Ernesto).

**Logo y favicon:**
- Mientras llega el original, se usa la foto de perfil de Instagram (150×150, marcada como provisional).
- El favicon es la "A" dorada sobre un círculo aqua, como en sus historias destacadas, en SVG, PNG de 192 y 512 y `apple-touch-icon`.

**Imágenes provisionales:** marcos aqua con la "A" dorada y el texto "Foto próximamente / Photo coming soon". Sin fotos de stock ni generadas con IA.

**Tono de los textos:** cercano, como en su Instagram, sin exagerar con los emojis.

## 8. Contenido provisional del catálogo

Todo va con `provisional: true` y sin precio:

- Dije con nombre personalizado (dijes)
- Inicial (dijes)
- Aretes de botón de 4, 5 y 6 mm (aretes)
- Argollas pequeñas (*huggies*) de 10, 12 y 14 mm (aretes)
- Set de regalo (cadenas)
- Una pieza genérica de anillos y otra de pulseras

## 9. Publicación

- **GitHub Actions** (`pages.yml`): en cada push a `main` sube `publico/` como artefacto y lo despliega en Pages. La fuente de Pages se configura en el repo como "GitHub Actions".
- **Vista previa**: `https://cisnerosmusic.github.io/ashajewelry-site/`.
- **Conexión del dominio** (fase posterior):
  1. Añadir la zona en Cloudflare (cuenta de Index01) y que el cliente cambie los NS en GoDaddy.
  2. Crear los registros DNS hacia GitHub Pages y poner el dominio personalizado.
  3. `BASE = "/"`, `LANZADO = True`, regenerar y push.

## 10. Verificación

`sitio.py` falla (código de salida distinto de 0) si:

- falta una cadena en algún idioma,
- hay un enlace interno roto,
- aparece una raya larga en un texto,
- un par de color definido como texto baja de AA,
- o una pieza apunta a una categoría inexistente.

Además, imprime cuántos elementos siguen como provisionales.

Antes de cada push:
- Revisión en el navegador local (`python -m http.server` sobre `publico/`) en escritorio y móvil.
- Tras el despliegue, comprobar que `README.md`, `CLAUDE.md` y `PENDIENTES.md` dan 404 en la vista previa.

## 11. Pendientes del cliente (van a PENDIENTES.md)

1. Logo original en alta resolución (PNG grande, SVG o Canva) y nombre de la serif del logo.
2. Horas de apertura exactas.
3. Si 786-978-1981 es su WhatsApp, o cuál lo es.
4. Si quiere precios visibles, rangos o "Consultar precio".
5. Si usa Shopify POS (lo sugiere Shop Pay). Si lo usa, se podría importar el catálogo más adelante.
6. Su historia: si tiene oficio previo y de dónde viene el nombre "Asha".
7. Fotos: piezas reales, el kiosko, la entrada de Fresco y Más y el dueño trabajando. Ernesto puede hacer las del local.
8. Permiso para mencionar y fotografiar Fresco y Más.
9. Si existe ficha de Google Business; si no, crearla y verificarla.
