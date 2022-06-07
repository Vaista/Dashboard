//Get Name on the basis of OHR entered

$(function() {
$('#manager_change_start_button').bind('click', function(event) {
  event.preventDefault();
  $.ajax({
    type: "POST",
    url: '/get_emp_ohr',
    data: {
      ohr: $('#ohr_entry').val(),
    },
    success: function (response) {
      if(response.status == "ok"){
        $("#result_name").html(response.name);
        $("#result_ohr").html(response.ohr);
        $("#result_band").html(response.band);
        $("#result_process").html(response.process);
        $("#result_manager_name").html(response.manager_name);
        $("#result_manager_ohr").html(response.manager_ohr);
        $("#change_manager2").removeClass("invisible");
        $("#change_manager2").addClass("visible");
        $("#custom_invisible_alert").addClass("invisible");
        $("#custom_invisible_alert").removeClass("visible");
        console.log(response);
        var opt = '';
        for (var i = 0; i < response.dict.length; i++) {
          var opt = new Option(response.dict[i]);
          var opt = new Option(response.dict[i]);
          $("#manager_details").append(opt);
        }
      }
      else{
        $("#change_manager2").removeClass("visible");
        $("#custom_invisible_alert").removeClass("invisible");
        $("#change_manager2").addClass("invisible");
        $("#custom_invisible_alert").addClass("visible");
        console.log(response);
      }
    },
    error: function (xhr, errmsg, err) {},
  });
});
});

