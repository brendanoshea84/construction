// new member
var new_member_form = document.getElementById("new_member_form");
var btn_new_member = document.getElementById("btn_new_member");

btn_new_member.addEventListener("click", function() {
    new_member_form.classList.remove('hide');
    btn_new_member.classList.add('hide');
    if (btn_login.classList.contains('hide')) {
        btn_login.classList.remove('hide');
        login_form.classList.add('hide');
    }
});

// login
var btn_login = document.getElementById("btn_login");
var login_form = document.getElementById("login_form");

btn_login.addEventListener("click", function() {
    login_form.classList.remove('hide');
    btn_login.classList.add('hide');
    if (btn_new_member.classList.contains('hide')) {
        new_member_form.classList.add('hide');
        btn_new_member.classList.remove('hide');
    }
});