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

    const heroSlides = document.querySelectorAll(".hero-slide");
    const heroContent = document.getElementById("mainHeroContent");

    if (!heroSlides.length) return;


    let currentSlide = 0;


    function showHeroSlide(index) {


        heroSlides.forEach((slide, i) => {

            slide.classList.remove("active");

            if(i === index){
                slide.classList.add("active");
            }

        });



        if(heroSlides[index].classList.contains("saving-slide")){

            heroContent.style.visibility = "hidden";

        }
        else{

            heroContent.style.visibility = "visible";

        }


    }


    showHeroSlide(currentSlide);



    setInterval(function(){

        currentSlide++;

        if(currentSlide >= heroSlides.length){

            currentSlide = 0;

        }


        showHeroSlide(currentSlide);


    },5000);


});