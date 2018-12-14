function calculateSalary() {
  var form = $(this).closest("form");
  $.ajax({
    url: "ajax/getSalary",
    data: {
      'staff_no': $('#id_employee').val()
    },
    dataType: 'json',
    type: "GET",

    // handle a successful response
    success: function(json) {
      data = json.content
      $('#id_basic_salary').val(data.basic_salary)
      $('#id_net_pay').val(data.net_pay)
      $('#id_mpf_employer').val(data.mpf_employer)
      $('#id_mpf_employee').val(data.mpf_employee)

      log("success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("error");
    }
  })
}