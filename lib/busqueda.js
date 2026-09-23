// Índice del buscador global: productos, publicaciones, experiencias, recursos, equipo y proyectos.
const corto = (s, n = 500) => String(s || "").replace(/\s+/g, " ").slice(0, n);
const unir = (a) => (Array.isArray(a) ? a.join(" ") : a || "");

module.exports = function indiceBusqueda(c) {
  const out = [];
  for (const p of c.productos) {
    out.push({ t: p.titulo, d: p.descripcion || "", k: p.tipo_etiqueta, u: p.url,
      x: corto([unir(p.tema), unir(p.publico), p.categoria, p.cuerpo].join(" ")) });
  }
  for (const p of c.publicaciones) {
    out.push({ t: p.titulo, d: [p.autores_texto, p.anio].filter(Boolean).join(" · "), k: p.tipo_etiqueta, u: p.url,
      x: corto([p.revista, p.editorial, p.libro, p.descripcion, unir(p.tema), p.doi].join(" ")) });
  }
  for (const m of c.equipo) {
    out.push({ t: m.nombre, d: m.cargo || "", k: "Equipo", u: m.url, x: corto([m.descripcion, m.cuerpo].join(" ")) });
  }
  for (const pr of c.proyectos) {
    out.push({ t: pr.nombre, d: pr.descripcion || "", k: "Proyecto", u: pr.url, x: corto([pr.institucion, pr.anio, pr.cuerpo].join(" ")) });
  }
  return out;
};
