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