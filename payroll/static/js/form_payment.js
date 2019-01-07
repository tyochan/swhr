function getStartDateText() {
  return $('#id_period_start').val()
}

function getEndDateText() {
  return $('#id_period_end').val()
}

function getStartDate() {
  return $('#id_period_start').datepicker('getDate')
}

function getEndDate() {
  return $('#id_period_end').datepicker('getDate')
}

function basic_salary() {
  return $('#id_basic_salary').val()
}

$().ready(function() {
  // Set start date and end date
  $('.dateinput').datepicker("setEndDate", getEndDate())
  $('#id_period_end').datepicker("setStartDate", new Date())
  $('#id_pay_date').datepicker("setStartDate", getStartDate())

  // Change export pdf urls
  array = location.pathname.split("/")
  id = array[array.length - 1]
  $('#id_export_pdf').attr("href", "../payslipPDF/" + id)

  $('#id_user').trigger("change")
});

// end_date change
$('#id_period_end').datepicker().on("changeDate", function(e) {
  $('#id_user').trigger("change")
})

// Employee Chosen
$('#id_user').change(function() {
  if ($(this).val() && !$(this).is(':disabled')) {
    payment_calculation()
  }
})

$('.payment, .deduction').change(function() {
  value = 0
  $('.payment').each(function() {
    value += parseFloat(this.value)
  })
  $('#id_total_payments').val(value.toFixed(2))

  value = 0
  $('.deduction').each(function() {
    value += parseFloat(this.value)
  })
  $('#id_total_deductions').val(value.toFixed(2))

  net_pay = parseInt($('#id_total_payments').val() - parseInt($('#id_total_deductions').val()))
  $('#id_net_pay').val(net_pay.toFixed(2))
})