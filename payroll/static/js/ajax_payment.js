function payment_calculation() {
  $.ajax({
    url: "../ajax/payment_calculation",
    data: {
      'user_id': $('#id_user').val(),
      'period_start': getStartDateText(),
      'period_end': getEndDateText(),
      'allowance': $('#id_allowance').val(),
      'other_payments': $('#id_other_payments').val(),
      'other_deductions': $('#id_other_deductions').val(),
      'is_last': $('#id_is_last').val(),
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

      if (name_in_path("last")) {
        $('#id_date_joined').val(data.date_joined)
        if (data.date_joined > getStartDate()) {
          $('#id_period_end').datepicker("setStartDate", data.join_date)
        }
        $('#id_unused_leave_days').val(data.unused_leave_days.toFixed(1))
        $('#id_unused_leave_pay').val(data.unused_leave_pay.toFixed(2))
      }

      log("ajax: calculate salary success"); // another sanity check
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      log("ajax: calculate salary error");
    }
  })
}