/*
 * Lee todo el contenido editable de /content (lo que se carga desde el CMS)
 * y lo prepara para las plantillas.
 *
 * No hace falta tocar este archivo para agregar contenido: alcanza con
 * crear entradas desde /admin/.
 */
const fs = require("fs");
const path = require("path");
const matter = require("gray-matter");
const md = require("../../lib/markdown");
const { accionProducto, precioTexto } = require("../../lib/venta");
const { slugify, normalizar } = require("../../lib/utilidades");

const RAIZ = path.join(__dirname, "..", "..", "content");

function leerCarpeta(rel) {
  const dir = path.join(RAIZ, rel);
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".md"))
    .map((archivo) => {
      const crudo = fs.readFileSync(path.join(dir, archivo), "utf8");
      const { data, content } = matter(crudo);
      const base = archivo.replace(/\.md$/, "");
      return {
        ...data,
        slug: slugify(data.slug || base),
        archivo_base: base,
        archivo_origen: `${rel}/${archivo}`,
        cuerpo: content.trim(),
        cuerpo_html: content.trim() ? md.render(content) : "",
      };
    })
    .filter((x) => x.visible !== false);
}

const lista = (v) => (Array.isArray(v) ? v.filter(Boolean) : v ? [v] : []);
const porOrden = (a, b) => (a.orden ?? 999) - (b.orden ?? 999) || String(a.titulo).localeCompare(String(b.titulo), "es");

/* ---------------------------------------------------------------- productos */
const TIPOS_PRODUCTO = {
  curso: { carpeta: "productos/cursos", ruta: "/formacion/cursos/", etiqueta: "Curso", plural: "Cursos" },
  masterclass: { carpeta: "productos/masterclasses", ruta: "/formacion/masterclasses/", etiqueta: "Masterclass", plural: "Masterclasses" },
  material: { carpeta: "productos/materiales", ruta: "/materiales/", etiqueta: "Material", plural: "Materiales" },
  experiencia: { carpeta: "productos/experiencias", ruta: "/experiencias/", etiqueta: "Experiencia", plural: "Experiencias" },
  recurso: { carpeta: "productos/recursos", ruta: "/recursos-gratuitos/", etiqueta: "Recurso", plural: "Recursos gratuitos" },
};

function cargarProductos(sitio) {
  const todos = [];
  for (const [tipo, def] of Object.entries(TIPOS_PRODUCTO)) {
    for (const p of leerCarpeta(def.carpeta)) {
      const item = {
        ...p,
        tipo,
        tipo_etiqueta: def.etiqueta,
        tema: lista(p.tema),
        publico: lista(p.publico),
        gratuito: tipo === "recurso" ? true : Boolean(p.gratuito),
        estado: p.estado || "disponible",
        url: `${def.ruta}${slugify(p.slug)}/`,
        descripcion_larga: p.cuerpo_html,
      };
      item.precio_texto = precioTexto(item);
      item.accion = accionProducto(item, sitio);
      todos.push(item);
    }
  }
  return todos.sort(porOrden);
}

/* ------------------------------------------------------------ publicaciones */
const TIPOS_PUBLICACION = {
  libro: { carpeta: "publicaciones/libros", ruta: "/publicaciones/libros/", etiqueta: "Libro", plural: "Libros" },
  capitulo: { carpeta: "publicaciones/capitulos", ruta: "/publicaciones/capitulos/", etiqueta: "Capítulo", plural: "Capítulos" },
  articulo: { carpeta: "publicaciones/articulos", ruta: "/publicaciones/articulos/", etiqueta: "Artículo científico", plural: "Artículos científicos" },
  otra: { carpeta: "publicaciones/otras", ruta: "/publicaciones/otras/", etiqueta: "Otra publicación", plural: "Otras publicaciones" },
};

function enlaceDoi(doi) {
  if (!doi) return "";
  const limpio = String(doi).trim().replace(/^https?:\/\/(dx\.)?doi\.org\//i, "").replace(/^doi:\s*/i, "");
  return `https://doi.org/${limpio}`;
}

function cargarPublicaciones() {
  const todas = [];
  for (const [tipo, def] of Object.entries(TIPOS_PUBLICACION)) {
    for (const p of leerCarpeta(def.carpeta)) {
      const autores = lista(p.autores);
      todas.push({
        ...p,
        tipo,
        tipo_etiqueta: def.etiqueta,
        autores,
        autores_texto: autores.join(", "),
        integrantes: lista(p.integrantes),
        tema: lista(p.tema),
        url: `${def.ruta}${slugify(p.slug)}/`,
        doi_url: enlaceDoi(p.doi),
        enlace: p.enlace || enlaceDoi(p.doi) || "",
        enlace_propio: Boolean(p.enlace),
      });
    }
  }
  return todas.sort((a, b) => (Number(b.anio) || 0) - (Number(a.anio) || 0) || porOrden(a, b));
}

/* ------------------------------------------------------- equipo y proyectos */
function cargarEquipo() {
  return leerCarpeta("equipo")
    .map((m) => ({
      ...m,
      titulo: m.nombre,
      enlaces: lista(m.enlaces),
      url: `/quienes-somos/equipo/${slugify(m.slug)}/`,
    }))
    .sort(porOrden);
}

function cargarProyectos() {
  return leerCarpeta("proyectos")
    .map((p) => ({
      ...p,
      titulo: p.nombre,
      integrantes: lista(p.integrantes),
      url: `/quienes-somos/proyectos/${slugify(p.slug)}/`,
    }))
    .sort((a, b) => (Number(b.anio) || 0) - (Number(a.anio) || 0) || porOrden(a, b));
}

/* ---------------------------------------------------------- páginas simples */
function leerPagina(nombre) {
  const f = path.join(RAIZ, "pages", nombre);
  if (!fs.existsSync(f)) return {};
  if (nombre.endsWith(".json")) return JSON.parse(fs.readFileSync(f, "utf8"));
  const { data, content } = matter(fs.readFileSync(f, "utf8"));
  return { ...data, cuerpo_html: content.trim() ? md.render(content) : "" };
}

module.exports = function () {
  const sitio = JSON.parse(fs.readFileSync(path.join(RAIZ, "settings", "site.json"), "utf8"));
  const productos = cargarProductos(sitio);
  const publicaciones = cargarPublicaciones();
  const equipo = cargarEquipo();
  const proyectos = cargarProyectos();

  // Relaciones: publicaciones y proyectos de cada integrante
  for (const m of equipo) {
    const ids = [m.slug, m.archivo_base, m.nombre];
    m.publicaciones = publicaciones.filter((p) => p.integrantes.some((i) => ids.includes(i)));
    m.proyectos = proyectos.filter((p) => p.integrantes.some((i) => ids.includes(i)));
  }
  const porSlug = Object.fromEntries(equipo.flatMap((m) => [[m.archivo_base, m], [m.slug, m]]));
  const porNombre = Object.fromEntries(equipo.map((m) => [m.nombre, m]));
  const resolver = (ids) => ids.map((id) => porSlug[id] || porNombre[id]).filter(Boolean);
  for (const p of publicaciones) p.integrantes_equipo = resolver(p.integrantes);
  for (const p of proyectos) p.integrantes_equipo = resolver(p.integrantes);

  const deTipo = (t) => productos.filter((p) => p.tipo === t);

  // Valores presentes (para mostrar solo filtros con contenido)
  const valores = (arr, campo) => [...new Set(arr.flatMap((x) => lista(x[campo])))];

  return {
    tiposProducto: TIPOS_PRODUCTO,
    tiposPublicacion: TIPOS_PUBLICACION,
    productos,
    cursos: deTipo("curso"),
    masterclasses: deTipo("masterclass"),
    formacion: productos.filter((p) => p.tipo === "curso" || p.tipo === "masterclass"),
    materiales: deTipo("material"),
    experiencias: deTipo("experiencia"),
    recursos: productos.filter((p) => p.tipo === "recurso" || (p.gratuito && p.tipo !== "recurso" && p.tambien_en_recursos)),
    destacados: productos.filter((p) => p.destacado),
    publicaciones,
    publicacionesPorTipo: Object.fromEntries(Object.keys(TIPOS_PUBLICACION).map((t) => [t, publicaciones.filter((p) => p.tipo === t)])),
    equipo,
    proyectos,
    paginas: {
      home: leerPagina("home.json"),
      secciones: leerPagina("secciones.json"),
      quienes: leerPagina("quienes-somos.md"),
      cuenta: leerPagina("mi-cuenta.md"),
      legal: leerPagina("aviso-legal.md"),
      privacidad: leerPagina("privacidad.md"),
    },
    temasPresentes: valores(productos, "tema"),
    publicosPresentes: valores(productos, "publico"),
    normalizar,
  };
};
