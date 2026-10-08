# Publicar adncognitivo en tac.com.ar/adncognitivo

> Estado: publicado en `https://tac.com.ar/adncognitivo/`. El detalle de la puesta en marcha está en [CHECKLIST-DEPLOY.md](CHECKLIST-DEPLOY.md). Cómo se edita y cómo llega al sitio, acá abajo.

## Cómo se edita y cómo se publica

Quien administra el contenido entra a `https://adncognitivo.netlify.app/admin/` con el mismo login de GitHub de siempre. El CMS guarda en la rama `main`. Netlify compila con `eleventy`, sin `--pathprefix`, así que el sitio de Netlify se ve igual que antes.

Ese push a `main` también dispara el Action, que compila de nuevo con `--pathprefix=/adncognitivo/` y suma un commit en la rama `deploy`, encima del anterior. Ferozo no se entera solo: hay que entrar al panel, Git, y apretar Desplegar en la entrada que apunta a la carpeta `public_html/adncognitivo` y a la rama `deploy`. Ese botón hace un pull y, como el commit nuevo sigue la historia anterior, el pull entra. Hasta que `lcanetjuric` cargue el webhook, ese clic es obligatorio. Si no se aprieta, `tac.com.ar/adncognitivo/` queda en la versión anterior.

El formulario de inscripción ya no usa Netlify Forms. Envía a `/adncognitivo-api/inscripcion.php`, que solo existe en `tac.com.ar`. Probar una inscripción en `adncognitivo.netlify.app` no funciona. Editar cursos, textos e imágenes no pasa por ese formulario.

La tabla `adncognitivo_inscripciones` está en la base `c1402662_tac`. El aviso de prueba llegó a `germanesalinas@gmail.com` desde `no-responder@tac.com.ar`. La casilla definitiva, para más adelante, es `adncognitivo@gmail.com`.

No apretar Desplegar en la entrada de Git que instala el repo entero en `public_html`. Esa carpeta no es un repositorio git y el layout del repo no coincide con la web.

## Pedido original

Meter la web de ADNCognitivo (este repo, Eleventy + Decap CMS, pensada para Netlify) dentro del sitio online de la TAC, en `tac.com.ar/adncognitivo` (subruta, no subdominio — pedido explícito).

## Primer enfoque (descartado): copiar el build estático al hosting de la TAC

La idea original era: seguir editando contenido desde el CMS en Netlify, y que un GitHub Action compile el sitio (`npx eleventy --pathprefix=/adncognitivo/`) y suba el resultado (`_site/`) al hosting de la TAC por SSH/FTP/cPanel Git, quedando publicado en `tac.com.ar/adncognitivo/`.

**Por qué se descartó**: `src/producto.njk` (cada curso/masterclass) y el bloque de newsletter en `recursos-gratuitos.njk` usan **Netlify Forms** (`data-netlify="true"`) para procesar las inscripciones/compras y las suscripciones. Netlify Forms es una función exclusiva de la infraestructura de Netlify — si el sitio se sirve desde cualquier otro lado, esos formularios simplemente no funcionan (el POST no lo procesa nadie). Como esas dos páginas son centrales (comprar un curso, suscribirse), no tenía sentido migrar todo el sitio a una copia estática fuera de Netlify.

Antes de descartar el enfoque llegamos a tocar varios archivos para que el sitio soportara un `pathPrefix` (filtro `enlace`, `sitio.prefijo`, ediciones en `base.njk`, `cabecera.njk`, `cabeza.njk`, `pie.njk`, `index.njk`, etc.). **Todo eso se revirtió.** Lo único que quedó de ese intento es la conversión de `src/assets/css/main.css` a rutas relativas para fuentes/dibujos (`url("../fonts/...")` en vez de `url("/assets/fonts/...")`) — es una mejora válida de todos modos, no depende de la estrategia de publicación.

## Enfoque actual: reverse proxy desde Apache

En vez de copiar archivos, Apache (en el hosting de la TAC) reenvía por detrás las visitas a `tac.com.ar/adncognitivo/*` hacia el sitio real en Netlify, sin cambiar la URL que ve el visitante. Ventajas sobre el enfoque anterior:

- El contenido servido siempre es el build real de Netlify — CMS, formularios (Netlify Forms) y todo lo demás siguen funcionando exactamente como están diseñados, sin tocar código.
- No hace falta GitHub Actions, ni credenciales de deploy, ni mantener dos copias del sitio sincronizadas.
- No hace falta excluir `/admin/` de nada (nunca se copia código a la TAC).

### Confirmado hasta ahora

- adncognitivo ya está publicado en Netlify: `https://adncognitivo.netlify.app/`.
- El hosting de la TAC usa el panel de **Ferozo** (no cPanel — corrección respecto a una suposición anterior de este documento), que tiene su propia sección de Git: repo `git@github.com:gercho25/ConicetTAC.git`, rama `master`, ruta de instalación `/public_html/`. Coincide con las credenciales de DB con prefijo `c1402662_` que aparecen (comentadas) en `var/www/html/.htaccess` del repo ConicetTAC.
- **Confirmado: el deploy es manual, no automático.** El panel de Git de Ferozo tiene una acción (ícono de lista, junto a terminal/editar/borrar) que ejecuta un pull real desde GitHub hacia `/public_html/` en el momento en que se aprieta — no hay webhook ni deploy automático al hacer push. Probado en vivo: mostró "Already up-to-date." (sin cambios pendientes, sin efecto). Esto significa que después de mergear el PR del sync a `master`, alguien con acceso a este panel tiene que entrar y apretar esa acción para que el cambio llegue de verdad a `tac.com.ar`.
- No parece haber, en esta vista, un mecanismo de "tareas de deploy por carpeta" (tipo `.cpanel.yml` de cPanel) — Ferozo deploya el repo completo a `/public_html/` tal cual. No es un problema: la protección real ya está en que el PR que se mergea a `master` solo contiene cambios dentro de `var/www/html/adncognitivo/` y `var/www/html/adncognitivo-api/` (lo garantiza `check-adncognitivo-scope.yml`), así que aunque Ferozo espeje el repo entero, lo único que cambia en el servidor son esas dos carpetas.
- El `.htaccess` real de producción es `ConicetTAC/var/www/html/.htaccess` (no el de la raíz del repo ConicetTAC, que es un boilerplate viejo sin usar — referencia un dominio `miporton.com` que no es el real). Ese `.htaccess` real tiene el bloque estándar de WordPress: todo lo que no sea archivo/directorio existente se redirige a `/index.php`.

### Punto crítico: `mod_proxy_http` NO está disponible — confirmado con certeza

**Primera prueba** (subcarpeta `prueba-proxy`, ya eliminada): con la regla dentro de `<IfModule mod_proxy_http.c>` y sin `index.html`, daba 403 Forbidden; con un `index.html` de prueba, se veía normalmente. Indicaba módulo ausente, pero no descartaba del todo que el `.htaccess` de esa subcarpeta simplemente no se estuviera leyendo (`AllowOverride` limitado habría dado el mismo resultado).

**Segunda prueba, definitiva:** misma regla mismo `RewriteRule ... [P,L]`, pero **sin** el `<IfModule>` que la envuelve. Resultado: **500 Internal Server Error**. Esto prueba que el `.htaccess` sí se procesa (`AllowOverride` está bien) y que el flag `[P]` falla en tiempo de ejecución — o sea, `mod_proxy_http` no está cargado en este servidor. Sin ambigüedad: el enfoque de reverse proxy vía Apache **queda descartado**.

### La regla que se probó (Apache, hosting Ferozo)

En `var/www/html/.htaccess` (repo ConicetTAC), **antes** del bloque `# BEGIN WordPress` (si no, WordPress se la come primero):

```apache
<IfModule mod_proxy_http.c>
RewriteEngine On
RewriteRule ^adncognitivo/?(.*)$ https://NOMBRE-DEL-SITIO.netlify.app/$1 [P,L]
</IfModule>

# BEGIN WordPress
...
```

`NOMBRE-DEL-SITIO.netlify.app` se reemplaza por `adncognitivo.netlify.app` (URL real, confirmada — ver "Confirmado hasta ahora").

**Todavía no se tocó este archivo** — es el que gobierna la TAC en producción, así que cualquier cambio ahí se prueba con cuidado antes de aplicarlo de verdad.

## Rollout

1. ~~Confirmar si `mod_proxy_http` está disponible~~ — **hecho, no está disponible.** Enfoque de reverse proxy vía Apache descartado.
2. ~~Publicar adncognitivo en Netlify~~ — **hecho**: `https://adncognitivo.netlify.app/`.
3. ~~Elegir enfoque~~ — **decidido: Camino B-mixta**, retomando la idea original de este documento (sección "Primer enfoque"), resolviendo esta vez el motivo por el que se había descartado.

## Camino B-mixta — copia sincronizada dentro de la TAC

Netlify se mantiene vivo **solo como entorno de edición** — quien administra contenido sigue entrando a `adncognitivo.netlify.app/admin/` con el mismo login de GitHub, sin ningún cambio. Un GitHub Action nuevo compila el sitio con `--pathprefix=/adncognitivo/` en cada guardado del CMS.

**Importante sobre permisos:** GitHub no tiene forma de dar "permiso de escritura limitado a una carpeta" de un repo — un token con escritura sobre `gercho25/ConicetTAC` puede tocar cualquier archivo del repo. Por eso el Action **no** pushea directo a `master` (la rama que gobierna el deploy de TODA la TAC, no solo esto): en cambio, abre/actualiza un Pull Request desde la rama `sync/adncognitivo`, y un chequeo aparte (`check-adncognitivo-scope.yml`, en ConicetTAC) bloquea ese PR si el diff toca algo fuera de `var/www/html/adncognitivo/`, `var/www/html/adncognitivo-api/` o `modificaciones/`. El merge a `master` lo sigue haciendo una persona, a mano. Ese chequeo solo se activa para PRs que vienen de `sync/adncognitivo` — a propósito, para no interferir con otros deploys de la TAC que también pasen por `master`.

Lo que resuelve el motivo del descarte original: el único formulario activo hoy (`suscripcion.njk` está desactivado por config) es el de inscripción, y en vez de depender de Netlify Forms, ahora manda a un endpoint PHP propio (`var/www/html/adncognitivo-api/inscripcion.php`, en el repo ConicetTAC) que guarda en una tabla nueva y avisa por mail.

### Ya hecho (en el código)

- **pathPrefix con el filtro `url` incorporado de Eleventy**, no un filtro propio — si no se pasa `--pathprefix` (como en el build de Netlify), no cambia nada. Verificado con un build local: `_site/` sin el flag da rutas idénticas a hoy; `_site/` con `--pathprefix=/adncognitivo/` prefija todo correctamente (se revisó con grep que no quedó ninguna ruta absoluta suelta).
- Tocados: `base.njk`, `cabecera.njk`, `cabeza.njk`, `pie.njk`, `macros.njk`, `subcats.njk`, y las páginas con rutas propias (`index.njk`, `404.njk`, `mi-cuenta.njk`, `gracias.njk`, `buscar.njk`, `pagar.njk`, `publicaciones/*.njk`, `quienes-somos/*.njk`, `proyectos-bloque.njk`, `inscripcion.njk`).
- `inscripcion.njk`: `action` ahora apunta a `/adncognitivo-api/inscripcion.php` (ruta fija, sin prefijo — esa carpeta no vive dentro de `adncognitivo/`, así que no la toca el sync). Se agregó un campo oculto `producto_url` para que el script sepa a qué ficha volver. Se sacaron los atributos de Netlify Forms.
- `var/www/html/adncognitivo-api/inscripcion.php` (repo ConicetTAC, nuevo): valida honeypot + campos obligatorios, guarda en `adncognitivo_inscripciones` (base `sitioweb`, mismas credenciales que WordPress vía `DB_WP_*`) guardando también el POST completo como JSON (así un campo nuevo en el formulario se seguiría capturando sin tocar el script), manda mail de aviso, y redirige a `.../pagar/` — la misma página de "último paso" que ya existía (`src/pagar.njk`), preservando el flujo actual.
- `modificaciones/2026-09-29/crear_adncognitivo_inscripciones.sql.txt` (repo ConicetTAC, nuevo): migración para crear esa tabla.
- `.github/workflows/sync-tac.yml` (repo adncognitivo, nuevo): compila, excluye `/admin/` de la copia pública, y abre/actualiza un PR desde `sync/adncognitivo` hacia `master` en `gercho25/ConicetTAC`, en cada push a `main`.
- `.github/workflows/check-adncognitivo-scope.yml` (repo ConicetTAC, nuevo): bloquea ese PR si se sale de las carpetas permitidas (ver arriba).
- `.gitignore` (repo adncognitivo, nuevo — no existía): ignora `node_modules/` y `_site/`.

La puesta en marcha, en orden reversible, está en [CHECKLIST-DEPLOY.md](CHECKLIST-DEPLOY.md). Ese archivo es el registro: se marca cada casilla y se anota la fecha al completarla.
