document.getElementById("OOO-form1").addEventListener("click", function(event) {
    let date = document.getElementById("meeting_date").value;
    let date_error;
    if (date == '') {
        event.preventDefault()
        document.getElementById("date-error").innerHTML = "<li>Enter a valid date</li>";
        $(window).scrollTop(0);
    }

    var r1_selected = document.querySelector('input[name="r1"]:checked');
    if (r1_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r1-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r2_selected = document.querySelector('input[name="r2"]:checked');
    if (r2_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r2-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r2_selected = document.querySelector('input[name="r2"]:checked');
    if (r2_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r2-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r3_selected = document.querySelector('input[name="r3"]:checked');
    if (r3_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r3-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r4_selected = document.querySelector('input[name="r4"]:checked');
    if (r4_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r4-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r5_selected = document.querySelector('input[name="r5"]:checked');
    if (r5_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r5-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r6_selected = document.querySelector('input[name="r6"]:checked');
    if (r6_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r6-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }

    var r7_selected = document.querySelector('input[name="r7"]:checked');
    if (r7_selected == null) {
       event.preventDefault()
       const element = document.getElementById("r7-error");
       element.innerHTML = "Please choose a response:";
       element.scrollIntoView();
    }
});