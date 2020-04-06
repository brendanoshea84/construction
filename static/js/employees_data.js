// Change tabs in employees data

let personal_tab = document.getElementById("personal_tab");
let emergcy_tab = document.getElementById("emergcy_tab");
let bank_tab = document.getElementById("bank_tab");

window.onload = (function() {
    if (window.location.href.indexOf("personal_info") > -1) {
        personal_tab.classList.add('active')
        emergcy_tab.classList.remove('active')
        bank_tab.classList.remove('active')
        console.log("personal_info");
    } else if (window.location.href.indexOf("emergcy") > -1) {
        personal_tab.classList.remove('active')
        emergcy_tab.classList.add('active')
        bank_tab.classList.remove('active')
        console.log("emergcy");
    } else if (window.location.href.indexOf("bank_details") > -1) {
        personal_tab.classList.remove('active')
        emergcy_tab.classList.remove('active')
        bank_tab.classList.add('active')
        console.log("bank_details");
    }
})