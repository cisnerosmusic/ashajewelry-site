// Capa de movimiento: separable y reversible (va con css/movimiento.css).
// - La cabecera se desvanece al bajar y vuelve al subir, al llegar arriba,
//   con el menú abierto o cuando algo de ella recibe el foco.
// - Secciones y tarjetas aparecen con un fundido al entrar en pantalla.
(function () {
  var raiz = document.documentElement;
  var cabecera = document.querySelector('.cabecera-fondo');
  var menu = document.getElementById('menu');

  if (cabecera) {
    var ultimo = window.scrollY;
    var pendiente = false;
    var actualizar = function () {
      var y = window.scrollY;
      var abierto = menu && menu.classList.contains('abierto');
      var conFoco = cabecera.contains(document.activeElement);
      if (y < cabecera.offsetHeight || y < ultimo - 6 || abierto || conFoco) {
        cabecera.classList.remove('cabecera-oculta');
      } else if (y > ultimo + 6) {
        cabecera.classList.add('cabecera-oculta');
      }
      ultimo = y;
      pendiente = false;
    };
    window.addEventListener('scroll', function () {
      if (!pendiente) { pendiente = true; window.requestAnimationFrame(actualizar); }
    }, { passive: true });
    cabecera.addEventListener('focusin', function () { cabecera.classList.remove('cabecera-oculta'); });
  }

  // Las apariciones solo existen si <head> activó la clase con-movimiento.
  if (!raiz.classList.contains('con-movimiento')) return;
  raiz.classList.add('movimiento-activo');
  var piezas = document.querySelectorAll('main > section, .tarjeta, .servicio');
  var observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('visible'); observador.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  Array.prototype.forEach.call(piezas, function (p) { observador.observe(p); });
})();
