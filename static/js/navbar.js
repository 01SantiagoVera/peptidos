document.addEventListener("DOMContentLoaded", function () {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    mobileNavToggle.addEventListener('click', function () {
        navMenu.classList.toggle('d-none'); // Muestra/oculta el menú
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const header = document.getElementById('header');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 0) { // Cambia esto si deseas un umbral diferente
            header.classList.add('scrolled'); // Agrega clase al hacer scroll
        } else {
            header.classList.remove('scrolled'); // Elimina clase al volver arriba
        }
    });
});
