// Menú principal. Para agregar o quitar una sección del menú, editar esta lista.
module.exports = [
  { texto: "Inicio", url: "/" },
  {
    texto: "Formación", url: "/formacion/",
    sub: [
      { texto: "Cursos", url: "/formacion/cursos/" },
      { texto: "Masterclasses", url: "/formacion/masterclasses/" },
    ],
  },
  { texto: "Materiales", url: "/materiales/" },
  { texto: "Experiencias", url: "/experiencias/" },
  {
    texto: "Publicaciones", url: "/publicaciones/",
    sub: [
      { texto: "Libros", url: "/publicaciones/libros/" },
      { texto: "Capítulos", url: "/publicaciones/capitulos/" },
      { texto: "Artículos", url: "/publicaciones/articulos/" },
      { texto: "Otros", url: "/publicaciones/otras/" },
      { texto: "Todas las publicaciones", url: "/publicaciones/" },
    ],
  },
  {
    texto: "Quiénes somos", url: "/quienes-somos/",
    sub: [
      { texto: "Presentación", url: "/quienes-somos/" },
      { texto: "Equipo", url: "/quienes-somos/#equipo" },
      { texto: "Proyectos", url: "/quienes-somos/proyectos/" },
    ],
  },
  { texto: "Recursos gratuitos", url: "/recursos-gratuitos/" },
];
