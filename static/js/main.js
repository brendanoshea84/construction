// Change active tabs in main pages
var home_tab = document.getElementById("home_tab");
var time_tab = document.getElementById("time_tab");
var projects_tab = document.getElementById("projects_tab");
var employees_tab = document.getElementById("employees_tab");

window.onload = (function() {
    if (window.location.href.indexOf("home") > -1) {
        home_tab.classList.add('active');
        time_tab.classList.remove('active');
        projects_tab.classList.remove('active');
        employees_tab.classList.remove('active');


    } else if (window.location.href.indexOf("timelogs_info") > -1) {
        home_tab.classList.remove('active');
        time_tab.classList.add('active');
        projects_tab.classList.remove('active');
        employees_tab.classList.remove('active');

    } else if (window.location.href.indexOf("projects") > -1) {
        home_tab.classList.remove('active');
        time_tab.classList.remove('active');
        projects_tab.classList.add('active');
        employees_tab.classList.remove('active');


    } else if (window.location.href.indexOf("employees") > -1) {
        home_tab.classList.remove('active');
        time_tab.classList.remove('active');
        projects_tab.classList.remove('active');
        employees_tab.classList.add('active');
    }
});

// Change tabs for new_member_info.html
var personal_tab = document.getElementById("personal_tab");
var emergcy_tab = document.getElementById("emergcy_tab");
var bank_tab = document.getElementById("bank_tab");

window.onload = (function() {
    if (window.location.href.indexOf("personal_info") > -1) {
        console.log("peronsal")
        personal_tab.classList.add('active');
        emergcy_tab.classList.remove('active');
        bank_tab.classList.remove('active');



    } else if (window.location.href.indexOf("bank_details") > -1) {
        console.log("bank")
        personal_tab.classList.remove('active');
        bank_tab.classList.add('active');
        emergcy_tab.classList.remove('active');


    } else if (window.location.href.indexOf("emergcy") > -1) {
        console.log("emergcy")
        personal_tab.classList.remove('active');
        bank_tab.classList.remove('active');
        emergcy_tab.classList.add('active');
    }
});







//Change date from button click
var use_date;

$('.box').click(function() {
    $('.box').removeClass('highlight');
    use_date = $(this).attr('value');
    $(this).addClass('highlight');
    $("#date_timelog").val(use_date);
    $("#notes").val('project_number');
    $("#project_number").val('');
    $("#hours").val('');
    $("#notes").val('');
});

// Add hours for week
var hours = 0;
$(".hours_day").each(function() {
    hours += parseFloat($(this).html());
});
$('#hours_worked').append(hours);


// Home page news

var news_form = document.getElementById("new_form");

$("#more_news").click(function() {
    $("#new_form").removeClass('hidden')
});