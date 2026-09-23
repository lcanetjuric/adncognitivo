// Configuración general (editable en /admin/ → Configuración del sitio)
const fs = require("fs");
const path = require("path");

module.exports = function () {
  const s = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "..", "content", "settings", "site.json"), "utf8"));
  // En Netlify la variable URL contiene la dirección pública del sitio
  const url = (s.url_sitio || process.env.URL || "").replace(/\/$/, "");
  return { ...s, url, anio: new Date().getFullYear() };
};
