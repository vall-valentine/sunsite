const navbar = document.querySelectorAll('.punct');
for (var i = 0; i < navbar.length; i++) {
    navbar[i].addEventListener('mousemove', navHoov);
    navbar[i].addEventListener('mouseout', outHoov);
}
const edit_btn = document.querySelector('.edit');
edit_btn.addEventListener('click', edit_clicked);
const save_btn = document.querySelector('.accept');
save_btn.addEventListener('click', accept_clicked);
const fields = document.querySelectorAll('.field');
const titles = document.querySelectorAll('.answer');


function accept_clicked(event) {
    this.style.display = "none";
    edit_btn.style.display = "block";
}

function edit_clicked(event) {
    document.querySelector('.img_btn').style.display = "flex";
    this.style.display = "none";
    save_btn.style.display = "block";
    for (i = 0; i < fields.length; i++) {
        console.log(fields[i], titles[i], titles[i].textContent);
        titles[i].style.display = "none";
        fields[i].style.display = "block";
        fields[i].value = titles[i].textContent;
    }
}

function navHoov(event) {
    this.style.backgroundColor = '#ffee58';
}

function outHoov(event) {
    this.style.backgroundColor = '#fff59d';
}

function redirect(url) {
    window.location.href = url;
}