
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
