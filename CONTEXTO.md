# ASHA Jewelry Miami · contexto del proyecto

Estado al 2 de octubre de 2026, al cerrar la sesión en la Máquina 2 (UW). Este archivo existe porque la memoria de las sesiones no viaja entre máquinas: lo que haga falta para seguir está aquí, en el repo.

## El cliente
- **ASHA Jewelry Miami**: joyería en el kiosko 2 dentro de Mercado Fresco y Más, 12107 SW 152nd St, Miami, FL 33177 (zona de Ernesto). Abrió el 14 de abril de 2026. Martes a domingo; cerrado los lunes. Teléfono 786-978-1981.
- Dueño: **Billy**, amigo de Ernesto. Cliente de Index01.
- Público en persona: 66 % hispanohablante, por eso el español va en la raíz y el inglés en `/en/`.
- Oro 10K, 14K y 18K, plata, reparación, ajuste de anillos, grabado y piezas a medida (dijes con nombre, iniciales). Financiamiento con Affirm, Afterpay, Klarna, Zip y Shop Pay, más layaway.
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
- Pruebas: `python -m unittest discover -s tests -t .` (68 pruebas, todas en verde al cerrar).
- Ramas: `main` (publicado) y `sitio-v1` (trabajo), iguales al cerrar.

## Cómo retomar en la Máquina 1
1. `git pull` en el clon del repo (o `git clone https://github.com/cisnerosmusic/ashajewelry-site.git` si no existe).
2. Python 3.12 con Pillow. Solo para `herramientas/marca.py` (iconos e imagen para redes) hace falta además PyMuPDF (`pip install pymupdf`).
3. Comprobar la identidad de git del repo: `git config user.email`. Los commits van como Ernesto Cisneros con el correo de negocio de Index01.
4. Vista previa local: `python -m http.server 8430 --directory publico`. Si se usa el panel de vista previa de Claude, añadir una entrada `asha` al `.claude/launch.json` del espacio de trabajo apuntando a `ashajewelry-site/publico`.
5. Leer PENDIENTES.md y seguir por lo que Ernesto decida.

## EN CURSO al cerrar la Máquina 2 (2-oct-2026): conectar ashamiami.com

La rama `sitio-v1` va un commit por delante de `main` (dda228b): la web ya usa `https://ashamiami.com/` como dirección base. **No pasar a `main` hasta que los DNS respondan**, o el sitio publicado apuntará a un dominio que todavía no funciona.

1. **Ernesto, en GoDaddy** (`ashamiami.com` → DNS): borrar los A de aparcamiento (`15.197.148.33`, `3.33.130.190`) y cualquier reenvío; añadir 4 registros A en `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; CNAME `www` → `cisnerosmusic.github.io`.
2. Comprobar: `nslookup ashamiami.com 8.8.8.8` debe devolver las IP 185.199.x.153.
3. Poner el dominio en Pages: `PUT https://api.github.com/repos/cisnerosmusic/ashajewelry-site/pages` con `{"cname":"ashamiami.com"}` (token del almacén de credenciales de git; nunca mostrarlo), o en Settings > Pages > Custom domain.
4. Pasar `sitio-v1` a `main` (fast-forward) y push: se publica con la nueva base.
5. Cuando GitHub emita el certificado (minutos u horas), activar "Enforce HTTPS" (`{"https_enforced":true}` en el mismo endpoint).
6. Verificar: `https://ashamiami.com/` y `https://www.ashamiami.com/` cargan; `cisnerosmusic.github.io/ashajewelry-site/` redirige; las páginas siguen con `noindex`.

## Siguiente paso probable
Enseñar la vista previa a Billy y recoger las respuestas de PENDIENTES.md (horas, WhatsApp, precios, envíos, fotos reales, licencia de Jitter, origen de la foto). Después, el lanzamiento con el dominio (README, sección "Lanzamiento").
