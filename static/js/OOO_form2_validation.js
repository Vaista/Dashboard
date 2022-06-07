document.getElementById("OOO-form2").addEventListener("click", function(event) {
    let date = document.getElementById("meeting_date").value;
    let date_error;
    if (date == '') {
        event.preventDefault()
        document.getElementById("date-error2").innerHTML = "<li>Enter a valid date</li>";
        $(window).scrollTop(0);
    }

});