# ASHA Jewelry Miami · contexto del proyecto

Estado al 2 de octubre de 2026, al cerrar la sesión en la Máquina 2 (UW). Este archivo existe porque la memoria de las sesiones no viaja entre máquinas: lo que haga falta para seguir está aquí, en el repo.

## El cliente
- **ASHA Jewelry Miami**: joyería en el kiosko 2 dentro de Mercado Fresco y Más, 12107 SW 152nd St, Miami, FL 33177 (zona de Ernesto). Abrió el 14 de abril de 2026. Martes a domingo; cerrado los lunes. Teléfono 786-978-1981.
- Dueño: **Billy**, amigo de Ernesto. Cliente de Index01. Lleva el negocio a distancia.
- **Quien atiende el kiosko y está en funciones es su esposa**: las preguntas del día a día (horario, pagos, layaway, fotos, piezas) se le hacen a ella en la tienda. A Billy, lo que sea de cuentas suyas (Google Business, dominios, redes).
- Público en persona: 66 % hispanohablante, por eso el español va en la raíz y el inglés en `/en/`.
- Oro 10K, 14K y 18K, plata, reparación, ajuste de anillos, grabado y piezas a medida (dijes con nombre, iniciales). Efectivo, tarjeta y layaway. **Sin financiamiento propio** (confirmado en la tienda el 2-oct-2026): sus redes anunciaban Affirm, Afterpay, Klarna, Zip y Shop Pay, pero no tienen acuerdo con ninguna; el cliente usa la tarjeta virtual de su app de pago a plazos y para la tienda es un pago con tarjeta. La web no nombra esas marcas y lo aclara en "Formas de pago". Cuando tengan web piensan pedir el alta como comercio; si llega, se anuncia con los logos oficiales.
- Redes: Instagram y TikTok @ashajewelryshop. El TikTok dice "Shipping available · USA" (envíos sin confirmar).
- Dominios: **ashajewelryusa.com** (del cliente, definitivo, GoDaddy, sin uso, vence el 14-jun-2029). **ashamiami.com** (de Ernesto, GoDaddy, comprado el 2-oct-2026): vista previa provisional. ashajewelrymiami.com: comprado según Ernesto, pero el registro público no lo mostraba el 2-oct-2026; revisar.

## Marca
- Logo diseñado por **Adys**. El kit completo (`.ai`, PDF, PNG y Ficha Gráfica) está en `marca/LOGO-kit-Adys.zip` (y en el Drive de Ernesto, carpeta `ASHA Joyeria/Logo/De Adys`). La Ficha Gráfica es un primer intento de guía, no una norma cerrada.
- `marca/asha-logo.svg` y `marca/asha-solo-letras.svg` son los vectores extraídos del PDF del kit. `marca/LEEME.md` tiene los colores oficiales y las tipografías.
- Colores oficiales: oro `#D5A332`, oro claro `#FDCF55`, negro, aqua `#CEF2F5`. El degradado metálico del logo (bronce, oro, reflejo claro en la S y la H, oro, bronce) está medido de la versión dorada de Adys y vive en `herramientas/adornos.py` (`GRADIENTE`).
- Tipografías del logo: Jitter ("ASHA") y Raleway ("JEWELRY"). La ficha usa **JitterDEMO**: la licencia comercial está por confirmar con Adys.

## Decisiones tomadas (y por qué)
| Decisión | Motivo |
|---|---|
| Web definitiva desde el principio, con contenido provisional | Enseñársela a Billy ya y rellenarla con sus materiales sin rehacer nada |
| Generador Python desde `datos/` a `publico/`; solo `publico/` se publica | Mismo patrón que haiti-web; los documentos internos nunca llegan a la web |
| Enlaces internos relativos | El mismo `publico/` funciona en la vista previa y en el dominio |
| Paleta: claro aqua con texto negro, bloques azul marino, pie negro, oro solo sobre oscuro | Gusto de Ernesto: el oro sobre azul claro no le funciona |
| Logo original de Adys en vector, nunca redibujado | Fidelidad a la marca; el diamante y la estrella son subtrazados suyos |
| Raleway en lugar de Montserrat | Es la tipografía oficial ("JEWELRY") según la ficha |
| Capa de movimiento separable, ritmo cinematográfico | Es una joyería: elegancia; y se puede quitar sin romper nada |
| Botones: resplandor al pasar, reflejo metálico que los cruza y destello con el degradado del logo al pulsar | Que cada gesto combine con el oro de la portada; el halo es azul sobre fondo claro (regla del oro) |
| Foto de la pancarta en la portada | Decisión de Ernesto; origen y licencia por confirmar |
| `noindex` hasta conectar el dominio | Que Google no indexe la vista previa |

## Estado
- **Vista previa en vivo**: https://ashamiami.com/ (GitHub Pages vía Actions; `noindex`). Es un dominio **provisional** de Ernesto (GoDaddy, DNS apuntando a GitHub Pages); el definitivo será ashajewelryusa.com. GitHub Pages admite un solo dominio: al lanzar, se cambia el dominio personalizado en Settings > Pages, `LANZADO = True` y `ashamiami.com` puede quedar redirigiendo.
- 35 páginas (ES y EN), 13 elementos provisionales (8 piezas, 4 servicios y la ficha del negocio).
- Pruebas: `python -m unittest discover -s tests -t .` (74 pruebas, todas en verde).
- Ramas: `main` (publicado) y `sitio-v1` (trabajo); `main` avanza solo por fast-forward con push, nunca con merge desde la web.

## Cómo retomar en la Máquina 1
1. `git pull` en el clon del repo (o `git clone https://github.com/cisnerosmusic/ashajewelry-site.git` si no existe).
2. Python 3.12 con Pillow. Solo para `herramientas/marca.py` (iconos e imagen para redes) hace falta además PyMuPDF (`pip install pymupdf`).
3. Comprobar la identidad de git del repo: `git config user.email`. Los commits van como Ernesto Cisneros con el correo de negocio de Index01.
4. Vista previa local: `python -m http.server 8430 --directory publico`. Si se usa el panel de vista previa de Claude, añadir una entrada `asha` al `.claude/launch.json` del espacio de trabajo apuntando a `ashajewelry-site/publico`.
5. Leer PENDIENTES.md y seguir por lo que Ernesto decida.

## ashamiami.com conectado (2-oct-2026)
- DNS en GoDaddy (zona de `ashamiami.com`): 4 A en `@` (185.199.108-111.153), 4 AAAA en `@` (2606:50c0:8000-8003::153) y CNAME `www` → `cisnerosmusic.github.io`. Se conservan NS, SOA, `_domainconnect` y el TXT `_dmarc`.
- Dominio personalizado en Settings > Pages, certificado aprobado y HTTPS forzado. `www`, `http://` y `cisnerosmusic.github.io/ashajewelry-site/` redirigen (301) a `https://ashamiami.com/`.
- Dominio verificado en la cuenta de GitHub de Ernesto (TXT `_github-pages-challenge-cisnerosmusic` en GoDaddy): no borrarlo.
- Al lanzar ashajewelryusa.com, ashamiami.com deja de servir el sitio y pasa a ser una redirección 301 (README, "Lanzamiento", paso 5): hay que quitar sus registros de GitHub y moverlo a Cloudflare.

## Ficha de Google Business (existe)
- Google Maps: https://www.google.com/maps?cid=7586306600511357337 (4,5 ★, 8 opiniones al 2-oct-2026). Nombre "Asha Jewelry", categoría "Jewelry manufacturer", sin sitio web.
- La web usa su chincheta (25.6278829, -80.3887829) en `geo` y su enlace en `mapa` (botón "Cómo llegar" y `hasMap`).
- Horario confirmado en la tienda el 2-oct-2026: martes a sábado de 10 a. m. a 7 p. m. (el oficial era hasta las 8, pero de 7 a 8 no entra nadie), domingo de 10 a. m. a 5 p. m., lunes cerrado. La ficha de Google todavía dice hasta las 8 de martes a sábado: Billy tiene que cambiarla.

## Siguiente paso probable
Enseñar la vista previa en la tienda y recoger las respuestas de PENDIENTES.md (WhatsApp, precios, envíos, fotos reales, licencia de Jitter, origen de la foto). Después, el lanzamiento con el dominio (README, sección "Lanzamiento").
