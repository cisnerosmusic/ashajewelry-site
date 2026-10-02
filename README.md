# ASHA Jewelry Miami · sitio web

Sitio de ASHA Jewelry Miami ([Instagram](https://www.instagram.com/ashajewelryshop/) · [TikTok](https://www.tiktok.com/@ashajewelryshop)), joyería en el kiosko 2 dentro de Mercado Fresco y Más (12107 SW 152nd St, Miami, FL 33177). Hecho por [Index01](https://index01.net).

- **Vista previa:** https://cisnerosmusic.github.io/ashajewelry-site/ (con `noindex` hasta el lanzamiento)
- **Dominio principal:** ashajewelryusa.com (GoDaddy, del cliente; aún sin conectar)
- **Dominios secundarios:** ashajewelrymiami.com y ashamiami.com (comprados el 2-oct-2026; se redirigen al principal en el lanzamiento)
- **Diseño:** `docs/superpowers/specs/2026-10-02-ashajewelry-site-design.md`
- **Pendientes:** `PENDIENTES.md`

## Cómo funciona

Todo el contenido vive en `datos/*.json` (español e inglés en cada campo). `herramientas/sitio.py` lo convierte en `publico/`, que es lo único que se publica: cada push a `main` lo sube a GitHub Pages con `.github/workflows/pages.yml`.

| Quiero... | Toco... |
|---|---|
| Añadir una pieza | `datos/piezas.json` y su foto en `img/originales/<nombre>.jpg` (en `fotos` va el nombre sin extensión) |
| Poner precio | `"precio": 250` en la pieza (`null` muestra "Consultar precio") |
| Anunciar una promo | `datos/promos.json` con `desde` y `hasta` (AAAA-MM-DD). La fecha se mira al generar: regenerar y hacer push el día que empieza y el día que termina |
| Cambiar horario, teléfono, WhatsApp | `datos/negocio.json` |
| Cambiar un texto | `datos/textos.json` |
| Cambiar colores o diseño | `estaticos/css/sitio.css` y subir `VERSION` en `herramientas/config.py` |
| Rehacer iconos o imagen para redes | `python herramientas/marca.py` |

Después de cualquier cambio:

    python herramientas/sitio.py
    python -m unittest discover -s tests -t .

y push. Para verlo en local: `python -m http.server 8430 --directory publico`.

## Lanzamiento (conectar ashajewelryusa.com)

1. Dar de alta la zona en Cloudflare (cuenta de Index01) y que el cliente cambie los NS en GoDaddy.
2. En Cloudflare, registros hacia GitHub Pages: `A` en `@` a 185.199.108.153, 185.199.109.153, 185.199.110.153 y 185.199.111.153, y `CNAME` en `www` a `cisnerosmusic.github.io`, todos sin proxy.
3. `LANZADO = True` en `herramientas/config.py`, regenerar y push (se escriben `CNAME` y `sitemap.xml` y desaparece el `noindex`).
4. En Settings > Pages del repo, dominio personalizado `ashajewelryusa.com` y "Enforce HTTPS".
5. ashajewelrymiami.com y ashamiami.com: zonas en Cloudflare y una regla de redirección 301 de cada una (con y sin `www`) a `https://ashajewelryusa.com/`, conservando la ruta.
