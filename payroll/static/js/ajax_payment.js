function calculateSalary() {
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
      $('#id_np_leave').val(data.no_pay_leave.toFixed(2))
      $('#id_total_payments').val(data.total_payments.toFixed(2))
      $('#id_total_deductions').val(data.total_deductions.toFixed(2))

      array = location.pathname.split("/")
      if (array.indexOf("last") > -1) {
        $('#id_join_date').val(data.join_date)
        if (data.join_date > getStartDate()) {
          $('#id_period_end').datepicker("setStartDate", data.join_date)
        }
        $('#id_leaves_unused').val(data.leaves_unused.toFixed(1))
      }


      log("ajax: calculate salary success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("ajax: calculate salary error");
    }
  })
}