function startVoice(targetId) {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    const icon = document.querySelector(`#${targetId}`).nextElementSibling;
    
    recognition.lang = 'ur-PK'; // Urdu support by default
    recognition.start();
    icon.classList.add('active');

    recognition.onresult = (event) => {
        const text = event.results[0][0].transcript;
        document.getElementById(targetId).value = text;
        icon.classList.remove('active');
    };

    recognition.onerror = () => icon.classList.remove('active');
}

// Attach event listeners to all mic buttons
document.querySelectorAll('.mic-icon').forEach(btn => {
    btn.onclick = function() {
        const inputId = this.previousElementSibling.id;
        startVoice(inputId);
    };
});
