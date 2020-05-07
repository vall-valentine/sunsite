const navbar = document.querySelectorAll('.punct');
for (var i = 0; i < navbar.length; i++) {
    navbar[i].addEventListener('mousemove', navHoov);
    navbar[i].addEventListener('mouseout', outHoov);
}

function navHoov(event) {
    this.style.backgroundColor = '#fff176';
}

function outHoov(event) {
    this.style.backgroundColor = '#fff59d';
}

function redirect(url) {
    window.location.href = url;
}