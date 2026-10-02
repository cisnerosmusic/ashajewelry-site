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

// Destello al pulsar un botón: sale del punto tocado (o del centro con el
// teclado) y se abre con el degradado del logo. Sin movimiento reducido.
(function () {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var BOTONES = '.boton, .contacto-fijo, .menu-boton, .filtros a';
  var destellar = function (boton, x, y) {
    boton.style.setProperty('--x', x + 'px');
    boton.style.setProperty('--y', y + 'px');
    boton.classList.remove('destello');
    void boton.offsetWidth; // reinicia la animación si se pulsa seguido
    boton.classList.add('destello');
  };
  document.addEventListener('pointerdown', function (e) {
    var boton = e.target.closest(BOTONES);
    if (!boton) return;
    var r = boton.getBoundingClientRect();
    destellar(boton, e.clientX - r.left, e.clientY - r.top);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var boton = e.target.closest && e.target.closest(BOTONES);
    if (!boton) return;
    destellar(boton, boton.offsetWidth / 2, boton.offsetHeight / 2);
  });
  document.addEventListener('animationend', function (e) {
    if (e.animationName === 'destello') e.target.classList.remove('destello');
  });
})();
