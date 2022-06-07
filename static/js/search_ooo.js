//Get Name on the basis of OHR entered

$(function() {
$('#search_ooo').bind('click', function(event) {
  event.preventDefault();
  $.ajax({
    type: "POST",
    url: '/search_meeting_list',
    data: {
      ohr: $('#emp_selected option:selected').val(),
    },
    success: function (response) {
        $('#search_result').replaceWith(response)
    },
    error: function (xhr, errmsg, err) {
        console.log(response)
    },
  });
});
});

