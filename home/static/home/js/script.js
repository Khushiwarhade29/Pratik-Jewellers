const voiceBtn = document.getElementById("voiceSearchBtn");
const searchInput = document.getElementById("searchInput");

if (voiceBtn && searchInput) {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {

        const recognition = new SpeechRecognition();

        recognition.lang = "en-IN";
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        voiceBtn.addEventListener("click", () => {
            recognition.start();
        });

        recognition.onresult = function (event) {

            const text = event.results[0][0].transcript;

            searchInput.value = text;

            searchInput.form.submit();
        };

        recognition.onerror = function () {
            alert("Voice search failed. Please try again.");
        };

    } else {

        voiceBtn.style.display = "none";

    }
}

/* =========================================================
   20H-2 — HERO AUTO SLIDER
   ========================================================= */


/* =========================================================
   HERO AUTO SLIDER
========================================================= */

document.addEventListener("DOMContentLoaded", function () {
    

    const hero = document.querySelector(".hero");
    const heroSlider = document.getElementById("heroSlider");
    const slides = document.querySelectorAll(".hero-slide");
    const heroContent = document.getElementById("mainHeroContent");
    const heroDots = document.querySelectorAll(".hero-dot");
    

    if (!hero || !heroSlider || !slides.length) return;

    heroSlider.addEventListener("mousedown", function () {
    console.log("SLIDER MOUSE DOWN");
});

    let currentSlide = 0;
    let autoTimer = null;

    let startX = 0;
    let startY = 0;
    let isSwiping = false;

    const AUTO_TIME = 10000;
    const SWIPE_DISTANCE = 60;


    /* ===============================
       SHOW SLIDE
    =============================== */

    function showSlide(index) {

        slides.forEach((slide, i) => {

            slide.classList.toggle(
                "active",
                i === index
            );

        });

        heroDots.forEach((dot, i) => {

    dot.classList.toggle(
        "active",
        i === index
    );

});


        if (heroContent) {

            if (
                slides[index].classList.contains("saving-slide")
            ) {
                heroContent.style.visibility = "hidden";
            } else {
                heroContent.style.visibility = "visible";
            }

        }

    }


    /* ===============================
       NEXT
    =============================== */

    function nextSlide() {

        currentSlide++;

        if (currentSlide >= slides.length) {
            currentSlide = 0;
        }

        showSlide(currentSlide);

    }


    /* ===============================
       PREVIOUS
    =============================== */

    function previousSlide() {

        currentSlide--;

        if (currentSlide < 0) {
            currentSlide = slides.length - 1;
        }

        showSlide(currentSlide);

    }


    /* ===============================
       AUTO SLIDE
    =============================== */

    function restartAutoSlide() {

        clearTimeout(autoTimer);

        autoTimer = setTimeout(function () {

            nextSlide();

            restartAutoSlide();

        }, AUTO_TIME);

    }


    showSlide(currentSlide);
    restartAutoSlide();


    /* =================================
       MOBILE TOUCH
    ================================= */

    /* =========================================
   MOBILE SWIPE
========================================= */

hero.addEventListener("touchstart", function (event) {

    const touch = event.touches[0];

    startX = touch.clientX;
    startY = touch.clientY;

}, { passive: true });


hero.addEventListener("touchend", function (event) {

    const touch = event.changedTouches[0];

    const endX = touch.clientX;
    const endY = touch.clientY;

    const diffX = endX - startX;
    const diffY = endY - startY;


    /* Only horizontal swipe */

    if (Math.abs(diffX) < SWIPE_DISTANCE) {
        return;
    }

    if (Math.abs(diffX) <= Math.abs(diffY)) {
        return;
    }


    /* LEFT → NEXT */

    if (diffX < 0) {

        nextSlide();

    }

    /* RIGHT → PREVIOUS */

    else {

        previousSlide();

    }


    /* Restart automatic timer */

    restartAutoSlide();

});


    /* =================================
       DESKTOP MOUSE DRAG
    ================================= */

   /* =========================================
   DESKTOP MOUSE DRAG
========================================= */
/* =========================================
   DESKTOP MOUSE DRAG
========================================= */

let mouseDown = false;
let hasDragged = false;

hero.addEventListener("mousedown", function (event) {

    mouseDown = true;
    hasDragged = false;

    startX = event.clientX;
    startY = event.clientY;

});


hero.addEventListener("mousemove", function (event) {

    if (!mouseDown) return;

    const diffX = event.clientX - startX;
    const diffY = event.clientY - startY;

    if (
        Math.abs(diffX) > 10 &&
        Math.abs(diffX) > Math.abs(diffY)
    ) {
        hasDragged = true;
    }

});


hero.addEventListener("mouseup", function (event) {

    if (!mouseDown) return;

    mouseDown = false;

    const endX = event.clientX;
    const endY = event.clientY;

    const diffX = endX - startX;
    const diffY = endY - startY;


    /* Ignore vertical movement */

    if (Math.abs(diffX) <= Math.abs(diffY)) {
        return;
    }


    /* Ignore small movement */

    if (Math.abs(diffX) < SWIPE_DISTANCE) {
        return;
    }


    /* LEFT DRAG → NEXT */

    if (diffX < 0) {

        nextSlide();

    }


    /* RIGHT DRAG → PREVIOUS */

    else {

        previousSlide();

    }


    /* Restart 10 second timer */

    restartAutoSlide();

});


hero.addEventListener("mouseleave", function () {

    mouseDown = false;

});
});