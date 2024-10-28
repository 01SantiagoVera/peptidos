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


let lastKnownScrollPosition = 0;
let ticking = false;

document.addEventListener("scroll", function() {
    lastKnownScrollPosition = window.scrollY;

    if (!ticking) {
        window.requestAnimationFrame(function() {
            const aboutUsSection = document.getElementById("aboutUs");
            const sectionPosition = aboutUsSection.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2; // Cambia esto a 1.2 para que espere un poco más

            // Si la posición de la sección es visible en el viewport
            if (sectionPosition < screenPosition && !aboutUsSection.classList.contains("show")) {
                aboutUsSection.classList.add("show");
            }

            ticking = false;
        });

        ticking = true;
    }
});


