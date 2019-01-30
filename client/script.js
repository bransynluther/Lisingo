function checkScroll(){
    var startY = $('.nav').height(); //The point where the navbar changes in px

    if($(window).scrollTop() > startY){
        $('.nav').addClass("scrolled");
        $('.nav-link').addClass("scrolled");
        $('#logo').addClass("scrolled");
    }else{
        $('.nav').removeClass("scrolled");
        $('.nav-link').removeClass("scrolled");
        $('#logo').removeClass("scrolled");
    }
}

if($('.nav').length > 0){
    $(window).on("scroll load resize", function(){
        checkScroll();
    });
}
//----------------------------------------------------//
//----------------^^^ NAV BAR STUFF ^^^---------------//
//----------------------------------------------------//

var searchButton = document.getElementById("searchButton")
var submitButton = document.getElementById("submitButton")
var bar = document.getElementById("searchBar")
var downloadButton = document.getElementById("downloadButton")
var url = document.getElementById("url_search")
const form = document.getElementById("search-form")

function startSearch() {
    var url_heading = document.getElementById("form_url");
    url_heading.innerHTML = bar.value;
    url.value = bar.value;
    bar.value = ""
}

function searchAfterClick() {
    if (bar.value != ""){
      startSearch()
    }
}

function searchAfterEnter(event) {
    if (bar.value != "" && event.which === 13){
      startSearch()
    }
}

function fire_the_json() {
  make_post_request()
}

function make_post_request() {
    var api_gateway_url = "https://thg7ymbqcj.execute-api.us-east-1.amazonaws.com/alpha/execution"
    var email_input = document.getElementById("email_input").value
    var voice = document.getElementById("voice").value
    var url_search = document.getElementById("url_search").value
    var input = `{"email": "${email_input}", "voice": "${voice}", "url_search": "${url_search}"}`
    var data_to_send = {"input":input,
                         "stateMachineArn":"arn:aws:states:us-east-1:477650777108:stateMachine:Lisingo_Pipeline"}
    var sendable_json = JSON.stringify(data_to_send)
    $.ajax({
        url: "https://thg7ymbqcj.execute-api.us-east-1.amazonaws.com/alpha/execution",
        type: "POST",
        data: sendable_json,
        crossDomain: true,
        dataType: "json",
        contentType: "application/json",
        success: function(data) {
            data = [data, 'Your Lisingo mp3 has been sent to the provided email =)']
            alert(JSON.stringify(data[1]));
        },
        error: function(e) {
            alert("failed" + JSON.stringify(e));
        }
    });
}



//form.addEventListener('submit', handleFormSubmit)
submitButton.addEventListener("click", fire_the_json);
searchButton.addEventListener("click", searchAfterClick);
bar.addEventListener("keypress", searchAfterEnter);
