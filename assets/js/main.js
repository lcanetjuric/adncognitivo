/* ADNCognitivo — interacción mínima: menú móvil y filtros. Sin dependencias. */
(function () {
  "use strict";

  /* ---------- menú móvil ---------- */
  var boton = document.querySelector(".menu-movil");
  var nav = document.getElementById("nav-principal");
  if (boton && nav) {
    var usoAbrir = '<svg class="dib" aria-hidden="true"><use href="#d-menu"/></svg>';
    var usoCerrar = '<svg class="dib" aria-hidden="true"><use href="#d-cerrar"/></svg>';
    function cerrar() {
      nav.classList.remove("abierto");
      document.body.classList.remove("menu-abierto");
      boton.setAttribute("aria-expanded", "false");
      boton.setAttribute("aria-label", "Abrir menú");
      boton.innerHTML = usoAbrir;
    }
    boton.addEventListener("click", function () {
      var abierto = nav.classList.toggle("abierto");
      document.body.classList.toggle("menu-abierto", abierto);
      boton.setAttribute("aria-expanded", String(abierto));
      boton.setAttribute("aria-label", abierto ? "Cerrar menú" : "Abrir menú");
      boton.innerHTML = abierto ? usoCerrar : usoAbrir;
      if (abierto) { var p = nav.querySelector("a"); if (p) p.focus(); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("abierto")) { cerrar(); boton.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) cerrar(); });
  }

  /* ---------- filtros (tipo / tema / público) ----------
     Dentro de un grupo: cualquiera de los valores elegidos (O).
     Entre grupos: deben cumplirse todos (Y).
     El estado se refleja en la URL (?tema=memoria&publico=salud) para poder compartirla. */
  document.querySelectorAll("[data-filtrable]").forEach(function (zona) {
    var caja = zona.querySelector("[data-filtros]");
    if (!caja) return;
    var items = zona.querySelectorAll("[data-item]");
    var contador = caja.querySelector("[data-contador]");
    var limpiar = zona.querySelectorAll("[data-limpiar]");
    var vacio = zona.querySelector("[data-sin-resultados]");
    var grupos = caja.querySelectorAll("[data-grupo]");

    function elegidos() {
      var sel = {};
      grupos.forEach(function (g) {
        var v = [];
        g.querySelectorAll('[aria-pressed="true"]').forEach(function (b) { v.push(b.dataset.valor); });
        if (v.length) sel[g.dataset.grupo] = v;
      });
      return sel;
    }
    function aplicar(actualizarUrl) {
      var sel = elegidos();
      var visibles = 0;
      items.forEach(function (it) {
        var ok = Object.keys(sel).every(function (g) {
          var valores = (it.dataset[g] || "").split(" ");
          return sel[g].some(function (v) { return valores.indexOf(v) > -1; });
        });
        it.hidden = !ok;
        if (ok) visibles++;
      });
      var hay = Object.keys(sel).length > 0;
      if (contador) contador.textContent = visibles + (visibles === 1 ? " resultado" : " resultados");
      limpiar.forEach(function (b) { if (b.closest("[data-filtros]")) b.hidden = !hay; });
      if (vacio) vacio.hidden = visibles !== 0;
      if (actualizarUrl && window.history && history.replaceState) {
        var u = new URL(location.href);
        ["tipo", "tema", "publico"].forEach(function (g) { u.searchParams.delete(g); });
        Object.keys(sel).forEach(function (g) { u.searchParams.set(g, sel[g].join(",")); });
        history.replaceState(null, "", u.pathname + u.search + u.hash);
      }
    }
    caja.addEventListener("click", function (e) {
      var b = e.target.closest(".chip");
      if (!b) return;
      b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
      aplicar(true);
    });
    limpiar.forEach(function (b) {
      b.addEventListener("click", function () {
        caja.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
        aplicar(true);
      });
    });
    // estado inicial desde la URL
    var params = new URLSearchParams(location.search);
    grupos.forEach(function (g) {
      var v = (params.get(g.dataset.grupo) || "").split(",");
      g.querySelectorAll(".chip").forEach(function (c) { if (v.indexOf(c.dataset.valor) > -1) c.setAttribute("aria-pressed", "true"); });
    });
    aplicar(false);
  });
})();
