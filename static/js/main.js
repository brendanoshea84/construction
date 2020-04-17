// Change active tabs in main pages


let home_tab = document.getElementById("home_tab");
let time_tab = document.getElementById("time_tab");
let projects_tab = document.getElementById("projects_tab");
let employees_tab = document.getElementById("employees_tab");

window.onload = (function() {
    if (window.location.href.indexOf("home") > -1) {
        home_tab.classList.add('active')
        time_tab.classList.remove('active')
        projects_tab.classList.remove('active')
        employees_tab.classList.remove('active')

    } else if (window.location.href.indexOf("time_log") > -1) {
        home_tab.classList.remove('active')
        time_tab.classList.add('active')
        projects_tab.classList.remove('active')
        employees_tab.classList.remove('active')

    } else if (window.location.href.indexOf("projects") > -1) {
        home_tab.classList.remove('active')
        time_tab.classList.remove('active')
        projects_tab.classList.add('active')
        employees_tab.classList.remove('active')

    } else if (window.location.href.indexOf("employees") > -1) {
        home_tab.classList.remove('active')
        time_tab.classList.remove('active')
        projects_tab.classList.remove('active')
        employees_tab.classList.add('active')
    }
})

function goBack() {
    window.history.back();
}