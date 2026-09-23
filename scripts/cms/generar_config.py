"""
Genera src/admin/config.yml (configuración de Decap CMS).
Editar este script solo si se quieren agregar campos o colecciones nuevas;
después correr:  python3 scripts/cms/generar_config.py
"""
import os, yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

TEMAS = ["Cognición", "Desarrollo", "Aprendizaje", "Funciones ejecutivas", "Memoria", "Metacognición", "Evaluación"]
PUBLICOS = ["Salud", "Educación", "Investigación", "Profesionales"]
MONEDAS = ["USD", "ARS", "EUR"]
ESTADOS = [
    {"label": "Disponible", "value": "disponible"},
    {"label": "Próximamente", "value": "proximamente"},
    {"label": "Finalizado / no disponible", "value": "finalizado"},
]


def campo(label, name, widget="string", **kw):
    d = {"label": label, "name": name, "widget": widget}
    d.update(kw)
    return d


def campos_producto(tipo, categorias=None, extra=None, es_experiencia=False, es_recurso=False):
    c = [
        campo("Título", "titulo"),
        campo("Slug (dirección web)", "slug", required=False,
              hint="Opcional. Final de la URL, sin espacios ni acentos (ej: cufe-2). Si queda vacío se genera desde el título."),
        campo("Tipo", "tipo", "hidden", default=tipo),
    ]
    if categorias:
        c.append(campo("Categoría", "categoria", "select", options=categorias, required=False))
    else:
        c.append(campo("Categoría / tipo", "categoria", required=False,
                       hint="Texto libre (ej: Simulación, Escenario interactivo, Juego)."))
    c += [
        campo("Descripción breve", "descripcion", "text", hint="Una a tres líneas. Aparece en los listados."),
        campo("Temas", "tema", "select", multiple=True, options=TEMAS, required=False),
        campo("Público", "publico", "select", multiple=True, options=PUBLICOS, required=False,
              hint="Podés elegir varios. Si no aplica a un público en particular, dejalo vacío."),
    ]
    if extra:
        c += extra
    c += [
        campo("Imagen", "imagen", "image", required=False,
              hint="Opcional. Si no hay imagen se muestra una portada tipográfica automática."),
        campo("Descripción de la imagen (texto alternativo)", "imagen_alt", required=False,
              hint="Qué se ve en la imagen, para personas que usan lectores de pantalla."),
    ]
    if es_recurso:
        c.append(campo("Gratuito", "gratuito", "hidden", default=True))
    else:
        c.append(campo("¿Es gratuito?", "gratuito", "boolean", default=es_experiencia, required=False,
                       hint="Gratuito → botón ACCEDER / DESCARGAR / EXPLORAR. Pago → botón COMPRAR."))
        c += [
            campo("Precio", "precio", required=False, hint="Solo el número (ej: 45 o 25000). Vacío = no se muestra precio."),
            campo("Moneda", "moneda", "select", options=MONEDAS, required=False),
            campo("URL de compra (Payhip u otra plataforma)", "url_compra", required=False,
                  hint="Pegá el enlace de checkout del producto. El botón COMPRAR lleva a esta dirección."),
        ]
    c += [
        campo("URL de la experiencia" if es_experiencia else "URL de acceso (gratuitos)", "url_acceso", required=False,
              hint="Dirección donde está la experiencia; se abre tal cual, sin modificarla." if es_experiencia
              else "Para productos gratuitos: enlace a la página, video, formulario o archivo externo."),
    ]
    if not es_experiencia:
        c.append(campo("Archivo descargable (gratuitos)", "archivo", "file", required=False,
                       hint="Si subís un archivo (PDF, etc.) el botón pasa a ser DESCARGAR."))
    c += [
        campo("Texto del botón (opcional)", "texto_boton", required=False,
              hint="Solo si querés reemplazar el texto automático (Comprar / Acceder / Descargar / Explorar)."),
        campo("Estado", "estado", "select", options=ESTADOS, default="disponible"),
        campo("Destacado", "destacado", "boolean", default=False, required=False,
              hint="Los destacados aparecen en la página de inicio."),
    ]
    if not es_recurso:
        c.append(campo("Mostrar también en Recursos gratuitos", "tambien_en_recursos", "boolean", default=False,
                       required=False, hint="Solo tiene efecto si el producto es gratuito."))
    c += [
        campo("Orden", "orden", "number", default=10, value_type="int", required=False,
              hint="Número menor = aparece primero."),
        campo("Visible en la web", "visible", "boolean", default=True, required=False,
              hint="Desactivalo para ocultar sin borrar."),
        campo("Descripción larga", "body", "markdown", required=False),
    ]
    return c


FORMACION_EXTRA = [
    campo("Modalidad", "modalidad", required=False, hint="Ej: en línea, asincrónica, presencial."),
    campo("Duración", "duracion", required=False),
    campo("Fechas / inicio", "fechas", required=False),
]
MATERIAL_EXTRA = [campo("Formato", "formato", required=False, hint="Ej: PDF, kit imprimible, fichas.")]


def coleccion_producto(nombre, label, singular, carpeta, **kw):
    return {
        "name": nombre, "label": label, "label_singular": singular,
        "folder": f"content/productos/{carpeta}", "create": True, "extension": "md", "format": "frontmatter",
        "slug": "{{slug}}", "identifier_field": "titulo",
        "summary": "{{titulo}} · {{estado}}", "editor": {"preview": False},
        "sortable_fields": ["titulo", "orden", "estado"],
        "fields": campos_producto(**kw),
    }


def campos_publicacion(tipo, extra):
    return [
        campo("Título", "titulo"),
        campo("Slug (dirección web)", "slug", required=False, hint="Opcional. Si queda vacío se genera desde el título."),
        campo("Tipo", "tipo", "hidden", default=tipo),
        campo("Autores", "autores", "list", hint="Un autor por línea, en el orden de la publicación (ej: Apellido, N.)",
              field=campo("Autor/a", "autor")),
        campo("Año", "anio", "number", value_type="int", required=False),
        *extra,
        campo("Descripción / resumen breve", "descripcion", "text", required=False),
        campo("Temas", "tema", "select", multiple=True, options=TEMAS, required=False),
        campo("Integrantes del equipo que son autores", "integrantes", "relation", collection="equipo",
              search_fields=["nombre"], value_field="{{slug}}", display_fields=["nombre"], multiple=True, required=False,
              hint="Vincula la publicación con la ficha del integrante (aparece en su página)."),
        campo("Imagen (tapa, figura)", "imagen", "image", required=False),
        campo("Descripción de la imagen", "imagen_alt", required=False),
        campo("DOI", "doi", required=False, hint="Ej: 10.1016/j.xxxx.2024.01.001 (sin https://doi.org/)."),
        campo("Enlace", "enlace", required=False, hint="URL a la publicación, repositorio o editorial. Si está vacío se usa el DOI."),
        campo("Archivo PDF (si la licencia lo permite)", "pdf", "file", required=False),
        campo("Destacada", "destacado", "boolean", default=False, required=False),
        campo("Orden (dentro del mismo año)", "orden", "number", default=10, value_type="int", required=False),
        campo("Visible en la web", "visible", "boolean", default=True, required=False),
        campo("Texto adicional", "body", "markdown", required=False),
    ]


def coleccion_publicacion(nombre, label, singular, carpeta, tipo, extra):
    return {
        "name": nombre, "label": label, "label_singular": singular,
        "folder": f"content/publicaciones/{carpeta}", "create": True, "extension": "md", "format": "frontmatter",
        "slug": "{{slug}}", "identifier_field": "titulo", "summary": "{{anio}} · {{titulo}}", "editor": {"preview": False},
        "sortable_fields": ["anio", "titulo"],
        "fields": campos_publicacion(tipo, extra),
    }


EDITORIAL = campo("Editorial", "editorial", required=False)
REVISTA = campo("Revista", "revista", required=False)

config = {
    "backend": {
        "name": "github",
        "repo": "USUARIO-DE-GITHUB/adncognitivo",
        "branch": "main",
        "base_url": "https://api.netlify.com",
        "commit_messages": {
            "create": "Crear {{collection}} “{{slug}}”",
            "update": "Actualizar {{collection}} “{{slug}}”",
            "delete": "Eliminar {{collection}} “{{slug}}”",
            "uploadMedia": "Subir archivo “{{path}}”",
            "deleteMedia": "Eliminar archivo “{{path}}”",
        },
    },
    "local_backend": True,
    "locale": "es",
    "logo_url": "/assets/img/marca/logo-horizontal.svg",
    "media_folder": "src/assets/uploads",
    "public_folder": "/assets/uploads",
    "slug": {"encoding": "ascii", "clean_accents": True, "sanitize_replacement": "-"},
    "collections": [
        # --- Formación
        coleccion_producto("cursos", "Cursos", "Curso", "cursos", tipo="curso", categorias=["Curso"], extra=FORMACION_EXTRA),
        coleccion_producto("masterclasses", "Masterclasses", "Masterclass", "masterclasses", tipo="masterclass",
                           categorias=["Masterclass"], extra=FORMACION_EXTRA),
        # --- Materiales
        coleccion_producto("materiales", "Materiales", "Material", "materiales", tipo="material",
                           categorias=["Para el aula", "Para profesionales", "Guías", "Recursos descargables"],
                           extra=MATERIAL_EXTRA),
        # --- Experiencias
        coleccion_producto("experiencias", "Experiencias", "Experiencia", "experiencias", tipo="experiencia",
                           es_experiencia=True),
        # --- Recursos gratuitos
        coleccion_producto("recursos", "Recursos gratuitos", "Recurso gratuito", "recursos", tipo="recurso",
                           categorias=["PDF", "Guía", "Actividad", "Experiencia", "Artículo", "Material", "Herramienta"],
                           es_recurso=True),
        # --- Publicaciones
        coleccion_publicacion("libros", "Publicaciones · Libros", "Libro", "libros", "libro",
                              [EDITORIAL, campo("ISBN", "isbn", required=False), campo("Rol (autoría, compilación…)", "rol", required=False)]),
        coleccion_publicacion("capitulos", "Publicaciones · Capítulos", "Capítulo", "capitulos", "capitulo",
                              [campo("Título del libro", "libro", required=False),
                               campo("Editores/as o compiladores/as del libro", "editores", required=False),
                               EDITORIAL, campo("Páginas", "paginas", required=False)]),
        coleccion_publicacion("articulos", "Publicaciones · Artículos científicos", "Artículo", "articulos", "articulo",
                              [REVISTA, campo("Volumen", "volumen", required=False), campo("Número", "numero", required=False),
                               campo("Páginas", "paginas", required=False)]),
        coleccion_publicacion("otras", "Publicaciones · Otras", "Publicación", "otras", "otra",
                              [campo("Tipo de publicación", "subtipo", required=False,
                                     hint="Ej: tesis, informe técnico, divulgación, ponencia, podcast."),
                               campo("Medio / editorial / evento", "editorial", required=False)]),
        # --- Equipo
        {
            "name": "equipo", "label": "Equipo", "label_singular": "Integrante",
            "folder": "content/equipo", "create": True, "extension": "md", "format": "frontmatter",
            "slug": "{{slug}}", "identifier_field": "nombre", "summary": "{{nombre}} · {{cargo}}", "editor": {"preview": False},
            "fields": [
                campo("Nombre", "nombre"),
                campo("Slug (dirección web)", "slug", required=False),
                campo("Foto", "foto", "image", required=False),
                campo("Descripción de la foto", "foto_alt", required=False),
                campo("Profesión / cargo", "cargo", required=False),
                campo("Breve descripción", "descripcion", "text", required=False),
                campo("Enlaces", "enlaces", "list", required=False,
                      fields=[campo("Texto (ej: ORCID, Google Scholar, LinkedIn)", "etiqueta"), campo("URL", "url")]),
                campo("Publicaciones destacadas (texto libre)", "publicaciones_texto", "markdown", required=False,
                      hint="Opcional. Las publicaciones cargadas en el CMS y vinculadas a esta persona se listan solas."),
                campo("Orden", "orden", "number", default=10, value_type="int", required=False),
                campo("Visible en la web", "visible", "boolean", default=True, required=False),
                campo("Trayectoria", "body", "markdown", required=False),
            ],
        },
        # --- Proyectos
        {
            "name": "proyectos", "label": "Proyectos", "label_singular": "Proyecto",
            "folder": "content/proyectos", "create": True, "extension": "md", "format": "frontmatter",
            "slug": "{{slug}}", "identifier_field": "nombre", "summary": "{{nombre}} · {{anio}}", "editor": {"preview": False},
            "fields": [
                campo("Nombre", "nombre"),
                campo("Slug (dirección web)", "slug", required=False),
                campo("Descripción breve", "descripcion", "text", required=False),
                campo("Integrantes del equipo", "integrantes", "relation", collection="equipo", search_fields=["nombre"],
                      value_field="{{slug}}", display_fields=["nombre"], multiple=True, required=False),
                campo("Otras personas participantes", "participantes", required=False, hint="Texto libre."),
                campo("Institución", "institucion", required=False),
                campo("Año", "anio", required=False, hint="Ej: 2024 o 2022–2025"),
                campo("Estado", "estado", "select", required=False,
                      options=["En curso", "Finalizado", "En preparación"]),
                campo("Enlace", "enlace", required=False),
                campo("Imagen", "imagen", "image", required=False),
                campo("Descripción de la imagen", "imagen_alt", required=False),
                campo("Orden", "orden", "number", default=10, value_type="int", required=False),
                campo("Visible en la web", "visible", "boolean", default=True, required=False),
                campo("Descripción completa", "body", "markdown", required=False),
            ],
        },
        # --- Páginas generales
        {
            "name": "paginas", "label": "Páginas generales", "label_singular": "Página",
            "editor": {"preview": False},
            "files": [
                {
                    "name": "home", "label": "Inicio", "file": "content/pages/home.json",
                    "fields": [
                        campo("Etiqueta del encabezado", "hero_etiqueta"),
                        campo("Texto del encabezado", "hero_texto", "text"),
                        campo("Nota manuscrita", "hero_nota", required=False),
                        campo("Botón 1 · texto", "boton_1_texto"), campo("Botón 1 · enlace", "boton_1_url"),
                        campo("Botón 2 · texto", "boton_2_texto"), campo("Botón 2 · enlace", "boton_2_url"),
                        campo("Idea central · título", "idea_titulo"),
                        campo("Idea central · texto", "idea_texto", "text"),
                        campo("Grandes áreas", "areas", "list", fields=[
                            campo("Título", "titulo"), campo("Texto", "texto"), campo("Enlace", "url"),
                            campo("Dibujo", "icono", "select",
                                  options=["formacion", "materiales", "experiencias", "publicaciones", "recursos"]),
                        ]),
                        campo("Quiénes somos · título", "quienes_titulo"),
                        campo("Quiénes somos · texto", "quienes_texto", "text"),
                    ],
                },
                {
                    "name": "secciones", "label": "Títulos e introducciones de secciones", "file": "content/pages/secciones.json",
                    "fields": [
                        campo(lab, key, "object", collapsed=True, fields=[
                            campo("Título", "titulo"), campo("Bajada", "bajada", required=False),
                            campo("Introducción", "intro", "markdown", required=False)])
                        for key, lab in [("formacion", "Formación"), ("cursos", "Cursos"), ("masterclasses", "Masterclasses"),
                                         ("materiales", "Materiales"), ("experiencias", "Experiencias"),
                                         ("publicaciones", "Publicaciones"), ("recursos", "Recursos gratuitos"),
                                         ("proyectos", "Proyectos"), ("catalogo", "Catálogo completo")]
                    ],
                },
                {
                    "name": "quienes", "label": "Quiénes somos", "file": "content/pages/quienes-somos.md",
                    "fields": [campo("Título", "titulo"), campo("Bajada", "bajada", required=False),
                               campo("Imagen", "imagen", "image", required=False),
                               campo("Presentación", "body", "markdown")],
                },
                {
                    "name": "cuenta", "label": "Mi cuenta", "file": "content/pages/mi-cuenta.md",
                    "fields": [campo("Título", "titulo"), campo("Bajada", "bajada", required=False),
                               campo("Texto", "body", "markdown")],
                },
                {
                    "name": "legal", "label": "Aviso legal", "file": "content/pages/aviso-legal.md",
                    "fields": [campo("Título", "titulo"), campo("Bajada", "bajada", required=False), campo("Texto", "body", "markdown")],
                },
                {
                    "name": "privacidad", "label": "Privacidad", "file": "content/pages/privacidad.md",
                    "fields": [campo("Título", "titulo"), campo("Bajada", "bajada", required=False), campo("Texto", "body", "markdown")],
                },
            ],
        },
        # --- Configuración
        {
            "name": "configuracion", "label": "Configuración del sitio", "editor": {"preview": False},
            "files": [{
                "name": "sitio", "label": "Configuración general", "file": "content/settings/site.json",
                "fields": [
                    campo("Nombre", "nombre"),
                    campo("Tagline", "tagline"),
                    campo("Frase del proyecto", "frase", "text"),
                    campo("Título para buscadores (SEO)", "titulo_seo"),
                    campo("Descripción para buscadores (SEO)", "descripcion_seo", "text"),
                    campo("Dirección del sitio", "url_sitio", required=False,
                          hint="Ej: https://adncognitivo.netlify.app o tu dominio propio. Si queda vacío se usa la de Netlify."),
                    campo("Logo", "logo", "image"),
                    campo("Logo para fondo oscuro", "logo_oscuro", "image"),
                    campo("Favicon (SVG o PNG cuadrado)", "favicon", "image"),
                    campo("Imagen para compartir en redes (1200×630)", "imagen_og", "image"),
                    campo("Email de contacto", "email", required=False),
                    campo("Instagram (URL)", "instagram", required=False),
                    campo("LinkedIn (URL)", "linkedin", required=False),
                    campo("Otras redes", "otras_redes", "list", required=False,
                          fields=[campo("Nombre", "nombre"), campo("URL", "url")]),
                    campo("Texto del pie de página", "footer_texto", "text"),
                    campo("Nota del pie (opcional)", "footer_nota", required=False),
                    campo("Venta", "venta", "object", fields=[
                        campo("Plataforma de venta", "plataforma", hint="Ej: Payhip. Solo informativo."),
                        campo("Texto del botón de compra", "texto_comprar", default="Comprar"),
                        campo("Enlace para 'Mi cuenta' (opcional)", "url_cuenta", required=False,
                              hint="Por ejemplo, la página de tu tienda en Payhip."),
                        campo("Abrir el checkout en una pestaña nueva", "abrir_en_nueva_pestana", "boolean", default=True),
                    ]),
                    campo("Suscripción por email (futuro)", "suscripcion", "object", collapsed=True, fields=[
                        campo("Activar formulario", "activa", "boolean", default=False),
                        campo("Título", "titulo"), campo("Texto", "texto", "text"),
                        campo("Modo", "modo", "select", options=[
                            {"label": "Formularios de Netlify (gratis, sin otra cuenta)", "value": "netlify"},
                            {"label": "Formulario externo (Mailchimp, MailerLite, Brevo…)", "value": "externo"}]),
                        campo("URL del formulario externo", "url_externa", required=False),
                    ]),
                ],
            }],
        },
    ],
}

cabecera = """# ==========================================================
#  Decap CMS · ADNCognitivo
#  Archivo generado por scripts/cms/generar_config.py
#  IMPORTANTE: reemplazar USUARIO-DE-GITHUB por tu usuario
#  (ver README, paso "Conectar el administrador").
# ==========================================================
"""
with open(os.path.join(RAIZ, "src", "admin", "config.yml"), "w", encoding="utf-8") as f:
    f.write(cabecera)
    yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False, width=110)
print("config.yml generado")
