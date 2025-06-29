document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector('nav.navbar');
    const wrapper = document.getElementById('app-wrapper');

    function adjustHeight() {
        const navHeight = navbar.offsetHeight;
        const windowHeight = window.innerHeight;
        wrapper.style.height = (windowHeight - navHeight) + 'px';
    }

    adjustHeight();               // Ustaw przy starcie
    window.addEventListener('resize', adjustHeight); // Dopasuj przy zmianie okna
});