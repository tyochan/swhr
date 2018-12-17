function calculateSalary() {
  var form = $(this).closest("form");
  $.ajax({
    url: "ajax/getSalary",
    data: {
      'staff_no': $('#id_employee').val(),
      'period_start': getStartDateText(),
      'period_end': getEndDateText(),
    },
    dataType: 'json',
    type: "GET",

    // handle a successful response
    success: function(json) {
      data = json.content
      $('#id_basic_salary').val(data.basic_salary.toFixed(2))
      $('#id_net_pay').val(data.net_pay.toFixed(2))
      $('#id_mpf_employer').val(data.mpf_employer.toFixed(2))
      $('#id_mpf_employee').val(data.mpf_employee.toFixed(2))

      log("ajax success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("ajax error");
    }
  })
}