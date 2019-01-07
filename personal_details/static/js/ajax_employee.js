function annual_leave_calculation() {
  $.ajax({
    url: "ajax/annual_leave_calculation",
    data: {
      'date_joined': getStartDateText(),
    },
    dataType: 'json',
    type: "GET",

    // handle a successful response
    success: function(json) {
      data = json.content
      $('#id_annual_leave').val(data.annual_leave.toFixed(1))

      log("ajax: calculate annual leave success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("ajax: calculate annual leave error");
    }
  })
}