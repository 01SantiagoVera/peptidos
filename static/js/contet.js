let lastKnownScrollPosition = 0;
let ticking = false;

document.addEventListener("scroll", function() {
    lastKnownScrollPosition = window.scrollY;

    if (!ticking) {
        window.requestAnimationFrame(function() {
            const aboutUsSection = document.getElementById("aboutUs");
            const sectionPosition = aboutUsSection.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.2;

            // Si la posición de la sección es visible en el viewport
            if (sectionPosition < screenPosition) {
                const elementsToAnimate = aboutUsSection.querySelectorAll(".animate-fade-in");
                elementsToAnimate.forEach((element) => {
                    element.classList.add("show");
                });
            }

            ticking = false;
        });

        ticking = true;
    }
});
