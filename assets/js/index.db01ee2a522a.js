const menuIcon = document.querySelector('.menu-icon');
const navLinks = document.querySelector('.nav-links');

menuIcon.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});

function previous_events() {
    document.querySelector(".previous").style.display = "block";
    document.querySelector(".home").style.display = "none";
    document.querySelector(".login_form").style.display = "none";
    document.querySelector(".register_form").style.display = "none";
}

function login_form() {
    document.querySelector(".login_form").style.display = "block";
    document.querySelector(".register_form").style.display = "none";
    document.querySelector(".previous").style.display = "none";
    document.querySelector(".home").style.display = "none";
}

function register_form() {
    document.querySelector(".register_form").style.display = "block";
    document.querySelector(".login_form").style.display = "none";
    document.querySelector(".previous").style.display = "none";
    document.querySelector(".home").style.display = "none";
}

function form_close() {
    document.querySelector(".previous").style.display = "none";
    document.querySelector(".login_form").style.display = "none";
    document.querySelector(".register_form").style.display = "none";
    document.querySelector(".home").style.display = "block";
}
