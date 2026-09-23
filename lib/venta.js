/*
 * VENTA — lógica del botón de cada producto.
 *
 * La web NO cobra: cada producto tiene un campo `url_compra` donde se pega
 * el enlace de checkout de la plataforma externa (hoy Payhip).
 * Para cambiar de plataforma (Hotmart, Gumroad, Lemon Squeezy, Mercado Pago,
 * Stripe Payment Links, etc.) alcanza con pegar los enlaces nuevos en el CMS
 * y cambiar el nombre de la plataforma en Configuración del sitio.
 * No hay que modificar este archivo.
 */

function accionProducto(p, sitio = {}) {
  const venta = sitio.venta || {};
  const nuevaPestana = venta.abrir_en_nueva_pestana !== false;
  const propio = (p.texto_boton || "").trim();

  if (p.estado === "finalizado") {
    return { tipo: "finalizado", texto: "No disponible", href: null };
  }
  if (p.estado === "proximamente") {
    return { tipo: "proximamente", texto: "Próximamente", href: null };
  }

  if (p.gratuito) {
    if (p.tipo === "experiencia" && p.url_acceso) {
      return { tipo: "explorar", texto: propio || "Explorar", href: p.url_acceso, externo: true, nuevaPestana: true };
    }
    if (p.archivo) {
      return { tipo: "descargar", texto: propio || "Descargar", href: p.archivo, externo: false, descarga: true };
    }
    if (p.url_acceso) {
      return { tipo: "acceder", texto: propio || "Acceder", href: p.url_acceso, externo: /^https?:/.test(p.url_acceso), nuevaPestana: true };
    }
    return { tipo: "pendiente", texto: "Acceso en preparación", href: null };
  }

  if (p.url_compra) {
    return {
      tipo: "comprar",
      texto: propio || venta.texto_comprar || "Comprar",
      href: p.url_compra,
      externo: true,
      nuevaPestana,
      plataforma: venta.plataforma || "",
    };
  }
  return { tipo: "pendiente", texto: "Enlace de compra en preparación", href: null };
}

function precioTexto(p) {
  if (p.gratuito) return "Gratuito";
  const bruto = p.precio === 0 ? "0" : String(p.precio ?? "").trim();
  if (!bruto) return "";
  const num = Number(bruto.replace(/\./g, "").replace(",", "."));
  const valor = Number.isFinite(num) && /^[\d.,\s]+$/.test(bruto)
    ? num.toLocaleString("es-AR", { maximumFractionDigits: 2 })
    : bruto;
  return [p.moneda, valor].filter(Boolean).join(" ");
}

module.exports = { accionProducto, precioTexto };
