# ADNCognitivo

Formación y recursos basados en evidencia para profesionales que trabajan con cognición, desarrollo y aprendizaje.

Esta carpeta es la web completa: diseño, páginas, administrador de contenidos (Decap CMS) y configuración para publicarla gratis con **GitHub + Netlify**. El contenido está separado del código, así que agregar un curso, una publicación o una persona del equipo **no requiere programar**: se hace desde `/admin/`.

> Para el uso diario (agregar cursos, materiales, publicaciones, etc.) leé **[GUIA-ADMINISTRACION.md](GUIA-ADMINISTRACION.md)**. Este README cubre la instalación y la publicación, que se hacen una sola vez.

---

## 1. Qué hay en esta carpeta

```
adncognitivo/
├── content/                 ← TODO el contenido editable (lo escribe el CMS)
│   ├── productos/
│   │   ├── cursos/          ← CUFE-2
│   │   ├── masterclasses/   ← Memoria de trabajo
│   │   ├── materiales/      ← Estrategias para el aula
│   │   ├── experiencias/    ← Sentir, saber, hacer
│   │   └── recursos/        ← recursos gratuitos
│   ├── publicaciones/
│   │   ├── libros/  capitulos/  articulos/  otras/
│   ├── equipo/              ← integrantes
│   ├── proyectos/
│   ├── pages/               ← textos de Inicio, Quiénes somos, Mi cuenta, legales, secciones
│   └── settings/site.json   ← Configuración del sitio (nombre, redes, email, venta…)
│
├── src/                     ← diseño y plantillas (código)
│   ├── admin/               ← panel /admin/ (Decap CMS) y su config.yml
│   ├── _data/               ← lee /content y lo prepara para las páginas
│   ├── _includes/           ← cabecera, pie, piezas reutilizables, dibujos
│   ├── assets/css/main.css  ← estilos
│   ├── assets/js/           ← menú, filtros, buscador (sin dependencias)
│   ├── assets/img/marca/    ← logos y favicons
│   ├── assets/img/dibujos/  ← marcos y trazos dibujados
│   ├── assets/uploads/      ← imágenes y archivos que subís desde el CMS
│   └── *.njk                ← páginas
│
├── lib/                     ← lógica: botones de venta, búsqueda, utilidades
├── scripts/                 ← generadores de logos, dibujos y config del CMS (opcionales)
├── docs/                    ← referencia de identidad visual
├── eleventy.config.js       ← configuración del generador (Eleventy)
├── netlify.toml             ← configuración de Netlify
└── package.json
```

**Tecnología:** [Eleventy](https://www.11ty.dev/) genera páginas HTML estáticas a partir del contenido. No hay servidor, ni base de datos, ni backend: por eso es gratis y rápida. JavaScript solo se usa para el menú móvil, los filtros y el buscador.

---

## 2. Probar la web en tu computadora (opcional)

Necesitás [Node.js](https://nodejs.org/) 18 o superior.

```bash
npm install
npm start            # abre la web en http://localhost:8080
```

Para usar el administrador **sin conexión a GitHub** (en tu compu):

```bash
npm start            # en una terminal
npm run cms          # en otra terminal
```

y entrá a `http://localhost:8080/admin/`. Los cambios se guardan directo en la carpeta `content/`.

---

## 3. Subir el proyecto a GitHub

1. Creá una cuenta en [github.com](https://github.com) (gratis).
2. Arriba a la derecha: **+ → New repository**. Nombre: `adncognitivo`. Puede ser **privado**. No agregues README ni .gitignore. **Create repository**.
3. Subí los archivos de esta carpeta. Dos formas:
   - **Sin terminal:** en la página del repositorio recién creado, *uploading an existing file* → arrastrá **todo el contenido** de la carpeta (menos `node_modules` y `_site`, si existieran) → **Commit changes**.
   - **Con terminal:**
     ```bash
     git init
     git add .
     git commit -m "Primera versión de ADNCognitivo"
     git branch -M main
     git remote add origin https://github.com/TU-USUARIO/adncognitivo.git
     git push -u origin main
     ```

> Si usás la subida por navegador, asegurate de que la carpeta oculta `.github` y el archivo `.gitignore` también se suban (en Mac: `Cmd + Shift + .` muestra archivos ocultos).

---

## 4. Publicar en Netlify (gratis)

1. Creá una cuenta en [netlify.com](https://www.netlify.com) usando **"Sign up with GitHub"**.
2. **Add new project → Import an existing project → GitHub** → elegí `adncognitivo`.
3. Netlify lee `netlify.toml` y completa todo solo:
   - Build command: `npm run build`
   - Publish directory: `_site`
4. **Deploy**. En uno o dos minutos la web queda en una dirección como `https://nombre-al-azar.netlify.app`.
5. Para cambiar el nombre: **Project configuration → General → Change project name** → por ejemplo `adncognitivo` → la web queda en `https://adncognitivo.netlify.app` (si el nombre está libre).

No hace falta comprar un dominio. Cuando quieras usar uno propio, ver la sección 8.

---

## 5. Conectar el administrador (/admin/)

El administrador guarda los cambios directamente en tu repositorio de GitHub; Netlify los detecta y republica la web sola (tarda ~1 minuto).

Para iniciar sesión se usa tu cuenta de GitHub, a través del servicio de autenticación gratuito de Netlify. Se configura **una sola vez**:

### 5.1 Crear la "OAuth App" en GitHub

1. En GitHub: foto de perfil → **Settings → Developer settings → OAuth Apps → New OAuth App**.
2. Completar:
   - **Application name:** `ADNCognitivo CMS`
   - **Homepage URL:** `https://adncognitivo.netlify.app` (tu dirección de Netlify)
   - **Authorization callback URL:** `https://api.netlify.com/auth/done`
3. **Register application**. Copiá el **Client ID**. Tocá **Generate a new client secret** y copiá el **Client secret** (se muestra una sola vez).

### 5.2 Pegarla en Netlify

1. En Netlify, dentro del proyecto: **Project configuration → Security → OAuth** (en algunas cuentas figura como *Access & security → OAuth*).
2. **Authentication providers → Install provider → GitHub**.
3. Pegá el **Client ID** y el **Client secret** → **Install**.

### 5.3 Decirle al CMS cuál es tu repositorio

Abrí `src/admin/config.yml` (en GitHub podés editarlo con el lápiz ✏️) y cambiá esta línea:

```yaml
  repo: USUARIO-DE-GITHUB/adncognitivo
```

por tu usuario real, por ejemplo `repo: lorenacanet/adncognitivo`. Guardá (**Commit changes**).

### 5.4 Entrar

Entrá a **`https://TU-SITIO.netlify.app/admin/`** → **Iniciar sesión con GitHub** → autorizá. Listo.

**Otras personas que editen:** necesitan una cuenta de GitHub y que las invites al repositorio (**Settings → Collaborators → Add people**, con permiso *Write*).

> **Por qué no Netlify Identity:** el método viejo (Netlify Identity + Git Gateway) está en retirada; Netlify marca Git Gateway como obsoleto. El acceso con GitHub es el método estable de Decap CMS. Si en el futuro preferís que el equipo entre con **email y contraseña** en lugar de GitHub, existe [DecapBridge](https://decapbridge.com), gratuito; solo cambia el bloque `backend` de `config.yml`.

---

## 6. Vender con Payhip

La web **no cobra**: funciona como catálogo y escaparate. El pago, la entrega de archivos, el acceso y la cuenta del comprador los maneja Payhip.

1. Creá una cuenta en [payhip.com](https://payhip.com) y conectá **Stripe** y/o **PayPal** para cobrar.
2. Creá el producto en Payhip (archivo descargable, curso, membresía, etc.) con su precio.
3. Copiá el enlace del producto (algo como `https://payhip.com/b/AbC12`).
4. En `/admin/`, abrí el producto → campo **"URL de compra"** → pegá el enlace → **Publicar**.

El botón **COMPRAR** aparece solo cuando el producto:
- no es gratuito,
- está en estado **Disponible**,
- y tiene una URL de compra.

| Situación | Botón |
|---|---|
| Estado **Próximamente** | PRÓXIMAMENTE (desactivado) |
| Estado **Finalizado** | NO DISPONIBLE |
| Gratuito + archivo subido | DESCARGAR |
| Gratuito + URL de acceso | ACCEDER |
| Experiencia gratuita | EXPLORAR (abre la URL original en otra pestaña) |
| Pago + URL de compra | COMPRAR (va a Payhip) |
| Pago sin URL todavía | "Enlace de compra en preparación" |

En **Configuración del sitio → Venta** podés cambiar el texto del botón, el nombre de la plataforma y el enlace de "Mi cuenta" (por ejemplo, tu tienda de Payhip).

### Costos de Payhip (sin ocultar nada)

La web no tiene costo mensual, pero **vender sí tiene comisiones**. Según la [página de planes de Payhip](https://help.payhip.com/article/102-billing-and-upgrading) (consultada en septiembre de 2026):

- **Plan gratuito:** USD 0 por mes + **5 % de comisión** por venta.
- **Plus:** USD 29/mes + 2 %. **Pro:** USD 99/mes + 0 %.
- En todos los planes se suman las **comisiones del procesador de pago** (Stripe o PayPal).

Verificá los valores actuales antes de empezar a vender; pueden cambiar.

### Cambiar de plataforma en el futuro

No hay que tocar código. Pegá los nuevos enlaces de checkout (Hotmart, Gumroad, Lemon Squeezy, Mercado Pago, Stripe Payment Links…) en el campo **URL de compra** de cada producto y cambiá el nombre en **Configuración del sitio → Venta → Plataforma**. La lógica de los botones está aislada en `lib/venta.js`.

---

## 7. Créditos de Netlify: cuánto se puede publicar gratis

**Importante.** Las cuentas nuevas de Netlify usan un sistema de créditos. Según la [documentación de Netlify](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/) (septiembre de 2026):

- El plan gratuito trae **300 créditos por mes**.
- **Cada publicación a producción cuesta 15 créditos.** Cada vez que guardás algo en el CMS, se publica → 15 créditos.
- El tráfico consume **20 créditos por GB** transferido.
- Si se agotan, **la web se pausa** hasta el mes siguiente (en el plan gratuito no se pueden comprar créditos extra).

En números: si no tuvieras tráfico, alcanzaría para unas 20 publicaciones por mes. Esta web es muy liviana (las páginas pesan pocos KB), pero conviene **cargar contenido en tandas** y no guardar veinte veces el mismo día.

**Si necesitás más margen**, hay un **modo ahorro** ya preparado:

1. En GitHub, creá una rama llamada `contenido` (desplegable de ramas → escribir `contenido` → *Create branch*).
2. En `src/admin/config.yml` cambiá `branch: main` por `branch: contenido`.
3. En Netlify: **Project configuration → Build & deploy → Branches and deploy contexts → Branch deploys → Let me add individual branches** → `contenido`.

Desde ese momento el CMS guarda en `contenido`, que se ve en `https://contenido--TU-SITIO.netlify.app` (las vistas previas **no consumen créditos**). Cuando quieras publicar todo junto: GitHub → **Actions → Publicar contenido → Run workflow**. Una sola publicación, 15 créditos, sin importar cuántos cambios hayas hecho.

Las cuentas de Netlify creadas antes del cambio de precios pueden tener el plan anterior (por minutos de compilación), que es más holgado. Lo ves en **Team settings → Billing**.

---

## 8. Dominio propio (más adelante)

1. Comprá el dominio donde prefieras.
2. Netlify → **Domain management → Add a domain** → seguí las instrucciones (cambiar DNS o nameservers). El certificado HTTPS es automático y gratuito.
3. En `/admin/` → **Configuración del sitio → Dirección del sitio** → `https://tudominio.com`.
4. En GitHub → OAuth App (sección 5.1) → actualizá la **Homepage URL**.

---

## 9. SEO incluido

- Título y descripción por página (editables en Configuración del sitio y en cada contenido).
- Open Graph y Twitter Card (imagen `src/assets/img/og-adncognitivo.png`, reemplazable desde el CMS).
- Favicon SVG + PNG + ícono para iPhone.
- URLs legibles (`/formacion/cursos/cufe-2/`).
- `sitemap.xml` y `robots.txt` automáticos; el administrador está excluido de buscadores.
- Datos estructurados (Schema.org): Organization, Course, Book / ScholarlyArticle, Person.

## 10. Accesibilidad

HTML semántico, enlace "Saltar al contenido", foco visible, navegación completa por teclado (incluido el menú móvil con Escape), textos alternativos editables, `aria-pressed` en filtros, `aria-live` en resultados, contraste AA en textos y soporte de `prefers-reduced-motion`.

## 11. Identidad visual

- Logos en `src/assets/img/marca/`: horizontal, horizontal con tagline, compacto, isotipo, monocromo, versiones para fondo oscuro, favicon y avatares 1080×1080 para Instagram. Todos son vectoriales (SVG, con el texto convertido a trazos) salvo los PNG.
- Tipografías: **Outfit** (títulos, navegación y textos), **Newsreader** itálica (bajadas editoriales) y **Kalam** (solo anotaciones manuscritas). Todas con licencia libre (SIL OFL) e incluidas en el proyecto, sin depender de Google Fonts.
- Paleta: negro `#1F1F1F`, marfil `#F7F4EC`, gris `#D8D5CC`; acentos teal `#8FAEB2` y coral `#D99B8D` usados solo en etiquetas.
- Los trazos (marcos, flechas, subrayados, dibujos de cada área) se generan con el mismo pincel que el logo: `scripts/marca/generar_dibujos.py`.

Para regenerar logos o dibujos (solo si querés modificarlos): `pip install fonttools brotli uharfbuzz playwright`, `npm install` y luego `python3 scripts/marca/generar_logos.py`, `generar_dibujos.py`, `generar_png.py`.

## 12. Cambios que sí requieren tocar código

Casi todo se edita desde el CMS. Las excepciones:

- **Agregar un tema o un público nuevo a los filtros:** editar las listas `TEMAS` y `PUBLICOS` en `scripts/cms/generar_config.py` y correr `python3 scripts/cms/generar_config.py` (o agregar la opción a mano en `src/admin/config.yml`, en cada colección).
- **Cambiar el menú principal:** `src/_data/navegacion.js`.
- **Agregar un tipo de contenido nuevo:** colección en `config.yml` + entrada en `src/_data/contenido.js`.
