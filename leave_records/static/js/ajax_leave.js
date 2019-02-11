function leave_calculation() {
  $.ajax({
    url: "../ajax/leave_calculation",
    data: {
      'start_date': getStartDateText(),
      'end_date': getEndDateText(),
      'day_type': $('#id_day_type').val(),
    },
    dataType: 'json',
    type: "GET",

    // handle a successful response
    success: function(json) {
      data = json.content
      $('#id_spend').val(data.days_spend.toFixed(1))
      log("ajax: calculate leave spend success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("ajax: calculate leave spend error");
    }
  })
}