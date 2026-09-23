const md = require("./lib/markdown");
const { slugify, normalizar } = require("./lib/utilidades");
const indiceBusqueda = require("./lib/busqueda");

module.exports = function (eleventyConfig) {
  // Archivos que se copian tal cual
  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/admin": "admin" });
  eleventyConfig.addPassthroughCopy({ "src/assets/img/marca/favicon.svg": "favicon.svg" });

  // Recompilar cuando cambia el contenido del CMS o la lógica
  eleventyConfig.addWatchTarget("./content/");
  eleventyConfig.addWatchTarget("./lib/");

  eleventyConfig.addFilter("md", (s) => (s ? md.render(String(s)) : ""));
  eleventyConfig.addFilter("mdInline", (s) => (s ? md.renderInline(String(s)) : ""));
  eleventyConfig.addFilter("slug", slugify);
  eleventyConfig.addFilter("normalizar", normalizar);
  eleventyConfig.addFilter("json", (v) => JSON.stringify(v));
  eleventyConfig.addFilter("abs", (ruta, base) => {
    if (!ruta) return "";
    if (/^https?:\/\//.test(ruta)) return ruta;
    return (base || "") + ruta;
  });
  eleventyConfig.addFilter("recortar", (s, n = 160) => {
    s = String(s || "").replace(/\s+/g, " ").trim();
    return s.length > n ? s.slice(0, n - 1).replace(/\s\S*$/, "") + "…" : s;
  });
  eleventyConfig.addFilter("sinHtml", (s) => String(s || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim());
  eleventyConfig.addFilter("dosDigitos", (n) => String(n).padStart(2, "0"));
  eleventyConfig.addFilter("fechaISO", (d) => new Date(d || Date.now()).toISOString());
  eleventyConfig.addFilter("unir", (arr, sep = " ") => (Array.isArray(arr) ? arr.join(sep) : arr || ""));
  eleventyConfig.addFilter("slugs", (arr) => (Array.isArray(arr) ? arr.map(slugify).join(" ") : ""));
  // Valores presentes en una lista de ítems, en el orden de referencia (+ los que no estén en él)
  eleventyConfig.addFilter("valoresFiltro", (items, campo, orden = []) => {
    const pres = new Set((items || []).flatMap((x) => (Array.isArray(x[campo]) ? x[campo] : x[campo] ? [x[campo]] : [])));
    return [...orden.filter((v) => pres.has(v)), ...[...pres].filter((v) => !orden.includes(v))];
  });
  eleventyConfig.addFilter("indiceBusqueda", indiceBusqueda);
  eleventyConfig.addFilter("pluck", (arr, k) => (Array.isArray(arr) ? arr.map((x) => x && x[k]).filter(Boolean) : []));
  eleventyConfig.addFilter("dominio", (u) => {
    try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return ""; }
  });

  return {
    dir: { input: "src", includes: "_includes", layouts: "_includes/layouts", data: "_data", output: "_site" },
    templateFormats: ["njk", "md", "11ty.js"],
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
  };
};
