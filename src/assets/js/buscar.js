/* Buscador global de ADNCognitivo. Lee /buscar/indice.json (generado al publicar). */
(function () {
  "use strict";
  var form = document.querySelector("[data-buscador]");
  var caja = document.querySelector("[data-resultados]");
  if (!form || !caja) return;
  var input = form.querySelector("input");
  var indice = null;

  function norm(s) { return String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase(); }
  function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function resaltar(texto, terminos) {
    var t = esc(texto);
    terminos.forEach(function (w) {
      if (w.length < 2) return;
      var n = norm(t), i = n.indexOf(w);
      if (i > -1) t = t.slice(0, i) + "<mark>" + t.slice(i, i + w.length) + "</mark>" + t.slice(i + w.length);
    });
    return t;
  }
  function cargar() {
    if (indice) return Promise.resolve(indice);
    return fetch("/buscar/indice.json").then(function (r) { return r.json(); }).then(function (d) {
      indice = d.map(function (it) { it._t = norm(it.t); it._b = norm([it.t, it.d, it.k, it.x].join(" ")); return it; });
      return indice;
    });
  }
  function buscar(q) {
    var terminos = norm(q).split(/\s+/).filter(Boolean);
    if (!terminos.length) { caja.innerHTML = ""; return; }
    cargar().then(function (idx) {
      var res = idx.filter(function (it) { return terminos.every(function (w) { return it._b.indexOf(w) > -1; }); })
        .map(function (it) { var s = 0; terminos.forEach(function (w) { if (it._t.indexOf(w) > -1) s += 3; }); return [s, it]; })
        .sort(function (a, b) { return b[0] - a[0]; }).map(function (x) { return x[1]; });
      var html = '<p class="resultados__cuenta">' + res.length + (res.length === 1 ? " resultado" : " resultados") + " para “" + esc(q) + "”</p>";
      if (!res.length) {
        html += '<p class="mano" style="font-size:1.35rem">Nada por acá. Probá con otra palabra o recorré las secciones.</p>';
      } else {
        html += '<ul class="renglones">' + res.map(function (it) {
          return '<li class="renglon resultado" style="grid-template-columns:minmax(0,1fr) auto"><div>' +
            '<span class="sticker sticker--contorno sticker--recto">' + esc(it.k) + "</span>" +
            '<h2 class="renglon__titulo mt-1"><a href="' + esc(it.u) + '">' + resaltar(it.t, terminos) + "</a></h2>" +
            (it.d ? '<p class="renglon__desc">' + resaltar(it.d, terminos) + "</p>" : "") + "</div></li>";
        }).join("") + "</ul>";
      }
      caja.innerHTML = html;
    }).catch(function () { caja.innerHTML = "<p>No se pudo cargar el buscador. Probá recargar la página.</p>"; });
  }
  var t;
  input.addEventListener("input", function () { clearTimeout(t); t = setTimeout(function () { buscar(input.value); }, 160); });
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    buscar(input.value);
    var u = new URL(location.href); u.searchParams.set("q", input.value); history.replaceState(null, "", u);
  });
  var q = new URLSearchParams(location.search).get("q");
  if (q) { input.value = q; buscar(q); }
  input.focus();
})();
