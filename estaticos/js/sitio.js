// Menú del móvil y filtro del catálogo. Sin JavaScript todo funciona igual:
// el menú se ve entero y los filtros son anclas a cada categoría.
(function () {
  var boton = document.querySelector('.menu-boton');
  var menu = document.getElementById('menu');
  if (boton && menu) {
    document.documentElement.classList.add('con-js');
    boton.hidden = false;
    boton.addEventListener('click', function () {
      var abierto = boton.getAttribute('aria-expanded') === 'true';
      boton.setAttribute('aria-expanded', String(!abierto));
      menu.classList.toggle('abierto', !abierto);
    });
  }

  var filtros = Array.prototype.slice.call(document.querySelectorAll('[data-filtro]'));
  var secciones = Array.prototype.slice.call(document.querySelectorAll('.categoria'));
  filtros.forEach(function (f) {
    f.setAttribute('role', 'button');
    f.setAttribute('aria-pressed', String(f.getAttribute('data-filtro') === 'todas'));
    f.addEventListener('click', function (e) {
      e.preventDefault();
      var c = f.getAttribute('data-filtro');
      secciones.forEach(function (s) {
        s.hidden = c !== 'todas' && s.getAttribute('data-categoria') !== c;
      });
      filtros.forEach(function (o) { o.setAttribute('aria-pressed', String(o === f)); });
    });
  });
})();
