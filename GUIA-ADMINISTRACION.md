# Guía de administración de ADNCognitivo

Todo se hace desde el administrador, sin tocar código.

**Cómo entrar:** abrí `https://TU-SITIO.netlify.app/admin/` → **Iniciar sesión con GitHub**.
A la izquierda vas a ver las colecciones: Cursos, Masterclasses, Materiales, Experiencias, Recursos gratuitos, Publicaciones (Libros, Capítulos, Artículos, Otras), Equipo, Proyectos, Páginas generales y Configuración del sitio.

**Cómo se publica:** cuando tocás **Publicar → Publicar ahora**, el cambio se guarda y la web se actualiza sola en un minuto aproximadamente. Si no lo ves, recargá la página con `Ctrl + F5` (Windows) o `Cmd + Shift + R` (Mac).

> Cada publicación consume créditos del plan gratuito de Netlify (ver README, sección 7). Conviene preparar varias cosas y publicarlas en tandas, no guardar veinte veces por día.

---

## Si mañana querés agregar un nuevo curso, hacé esto

1. Entrá a **/admin/**.
2. Elegí **Cursos** en la columna izquierda.
3. Tocá **+ Curso** (crear nuevo).
4. **Imagen:** tocá *Elegir una imagen* → *Subir* → elegí el archivo (JPG o PNG, horizontal, idealmente 1600×1000). Escribí en *Descripción de la imagen* qué se ve. Si no subís imagen, la web arma una portada tipográfica automática.
5. **Descripción:** completá *Título*, *Descripción breve* (una a tres líneas, aparece en los listados) y, más abajo, *Descripción larga* (el contenido completo: objetivos, programa, destinatarios, docentes…). Elegí *Temas* y *Público*, y completá *Modalidad* y *Duración*.
6. **Precio:** escribí solo el número (por ejemplo `45`) y elegí la *Moneda*. Dejá desactivado *¿Es gratuito?*.
7. **URL de Payhip:** pegá el enlace de compra en *URL de compra (Payhip u otra plataforma)*.
8. Elegí el **Estado** (*Disponible* para vender, *Próximamente* si todavía no abrió) → **Publicar → Publicar ahora**.

Listo: el curso aparece en **Formación**, en **Cursos**, en el **Catálogo** y en el buscador. Si activás *Destacado*, también aparece en la página de inicio.

---

## Masterclass

Igual que un curso, pero en la colección **Masterclasses** → **+ Masterclass**.

## Material

1. **Materiales** → **+ Material**.
2. Título, descripción breve, *Categoría* (Para el aula / Para profesionales / Guías / Recursos descargables), temas, público y *Formato* (por ejemplo, PDF de 30 páginas).
3. Imagen.
4. **Si es pago:** precio, moneda y URL de compra de Payhip. El archivo lo entrega Payhip, no hace falta subirlo acá.
5. **Si es gratuito:** activá *¿Es gratuito?* y subí el archivo en *Archivo descargable* (el botón dice DESCARGAR) o pegá un enlace en *URL de acceso* (el botón dice ACCEDER).
6. Estado → **Publicar**.

## Experiencia interactiva

1. **Experiencias** → **+ Experiencia**.
2. Título, descripción breve, *Categoría / tipo* (texto libre: simulación, escenario interactivo, juego…), temas y público.
3. **URL de la experiencia:** pegá la dirección donde ya está publicada (por ejemplo, la de Netlify). La web **no la modifica**: el botón EXPLORAR la abre tal cual, en otra pestaña.
4. Imagen (una captura de la experiencia queda muy bien).
5. Dejá activado *¿Es gratuito?*. Si alguna fuera paga, desactivalo y pegá la URL de compra.
6. **Publicar**.

## Recurso gratuito

1. **Recursos gratuitos** → **+ Recurso gratuito**.
2. Título, descripción, *Categoría* (PDF, Guía, Actividad, Experiencia, Artículo, Material, Herramienta), temas.
3. Subí el archivo en *Archivo descargable* **o** pegá un enlace en *URL de acceso*.
4. **Publicar**.

Tip: si una experiencia o un material gratuito también tiene que aparecer en *Recursos gratuitos*, activá **Mostrar también en Recursos gratuitos** en su ficha. No hace falta cargarlo dos veces.

---

## Publicación (artículo científico)

1. **Publicaciones · Artículos científicos** → **+ Artículo**.
2. *Título*.
3. *Autores*: tocá **Añadir** una vez por autor, en el orden de la publicación (por ejemplo `Apellido, N.`).
4. *Año*, *Revista*, *Volumen*, *Número*, *Páginas*.
5. *DOI*: solo el código (por ejemplo `10.1016/j.xxxx.2024.01.001`). La web arma el enlace a doi.org. Si preferís otro enlace (repositorio, PDF de la editorial), pegalo en *Enlace*.
6. *Integrantes del equipo que son autores*: elegí a las personas del equipo; la publicación aparece sola en su ficha.
7. Opcional: resumen breve, temas, imagen, PDF (solo si la licencia lo permite).
8. **Publicar**. Las publicaciones se ordenan solas por año, de la más nueva a la más vieja.

## Libro

**Publicaciones · Libros** → **+ Libro** → título, autores, año, *Editorial*, *ISBN*, *Rol* (autoría, compilación…), imagen de tapa, enlace → **Publicar**.

## Capítulo

**Publicaciones · Capítulos** → **+ Capítulo** → título del capítulo, autores, año, *Título del libro*, *Editores/as del libro*, editorial, páginas, DOI o enlace → **Publicar**.

## Otras publicaciones

**Publicaciones · Otras** → para tesis, informes, divulgación, ponencias, podcasts… En *Tipo de publicación* escribís cuál es.

---

## Integrante del equipo

1. **Equipo** → **+ Integrante**.
2. *Nombre*, *Foto* (se muestra en blanco y negro, formato vertical), *Descripción de la foto*.
3. *Profesión / cargo* y *Breve descripción*.
4. *Enlaces*: **Añadir** por cada uno (ORCID, Google Scholar, ResearchGate, LinkedIn…) con su texto y URL.
5. *Trayectoria*: texto libre, con formato.
6. *Orden*: número menor = aparece primero.
7. **Publicar**. Sus publicaciones y proyectos se listan solos en su página si están vinculados.

## Proyecto

**Proyectos** → **+ Proyecto** → nombre, descripción, integrantes del equipo, otras personas participantes, institución, año, estado, enlace, imagen → **Publicar**.

---

## Tareas rápidas

| Quiero… | Dónde |
|---|---|
| **Cambiar un precio** | Abrir el producto → *Precio* → Publicar |
| **Cambiar una imagen** | Abrir el contenido → *Imagen* → quitar y elegir otra → Publicar |
| **Cambiar un texto** | Abrir el contenido o **Páginas generales** → Publicar |
| **Cambiar el enlace de compra** | Abrir el producto → *URL de compra* → Publicar |
| **Destacar en la home** | Activar *Destacado* → Publicar |
| **Poner "Próximamente"** | *Estado* → Próximamente → Publicar |
| **Ocultar sin borrar** | Desactivar *Visible en la web* → Publicar |
| **Borrar** | Abrir → **Eliminar entrada** (arriba) |
| **Cambiar el orden** | Campo *Orden* (1, 2, 3…) |
| **Textos de la home** | Páginas generales → Inicio |
| **Presentación de Quiénes somos** | Páginas generales → Quiénes somos |
| **Títulos e introducciones de secciones** | Páginas generales → Títulos e introducciones de secciones |
| **Email, Instagram, LinkedIn, logo, favicon, pie** | Configuración del sitio |
| **Aviso legal y privacidad** | Páginas generales → Aviso legal / Privacidad |
| **Activar suscripción por email** | Configuración del sitio → Suscripción → Activar formulario |

## Direcciones de la web

| Página | Dirección |
|---|---|
| Inicio | `/` |
| Formación · Cursos · Masterclasses | `/formacion/` · `/formacion/cursos/` · `/formacion/masterclasses/` |
| Materiales | `/materiales/` |
| Experiencias | `/experiencias/` |
| Publicaciones | `/publicaciones/` (y `/libros/`, `/capitulos/`, `/articulos/`, `/otras/`) |
| Quiénes somos · Proyectos | `/quienes-somos/` · `/quienes-somos/proyectos/` |
| Recursos gratuitos | `/recursos-gratuitos/` |
| Catálogo con filtros | `/catalogo/` |
| Buscador | `/buscar/` |
| Mi cuenta | `/mi-cuenta/` |
| Administrador | `/admin/` |

Los filtros se pueden compartir: por ejemplo `/catalogo/?tema=memoria&publico=salud`.

## Si algo no aparece

- Esperá un minuto y recargá sin caché.
- Revisá que *Visible en la web* esté activado.
- En Netlify → **Deploys** podés ver si la última publicación terminó bien. Si falló, la web sigue mostrando la versión anterior (nunca se rompe) y el error dice qué archivo revisar.
