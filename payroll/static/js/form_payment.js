$.fn.datepicker.defaults.daysOfWeekDisabled = '06'

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
  // If no date input
  if (!getStartDate() && !getEndDate()) {
    disable($("#id_period_end"))
  } else { // Has input
    // Set start date and end date
    $('#id_period_start').datepicker("setEndDate", getEndDate())
    $('#id_period_end').datepicker("setStartDate", new Date())
  }

  array = location.pathname.split("/")
  id = array[array.length - 1]
  // Change export url
  // if (array.indexOf("last") > -1){
  $('#id_export_pdf').attr("href", "../payslipPDF/" + id)
  // }

  if (!$('#id_employee').val()) {
    $('.payment').val((0).toFixed(2))
    $('.deduction').val((0).toFixed(2))
  } else {
    calculateSalary()
  }

  $('#id_pay_date').datepicker("setStartDate", getStartDate())
  $('#id_pay_date').datepicker("setEndDate", getEndDate())

  readonly($("#id_net_pay"))
  readonly($("#id_total_payments"))
  readonly($("#id_total_deductions"))
});

// start_date change
$('#id_period_start').datepicker().on("changeDate", function(e) {
  // If has end_date
  if (getEndDateText()) {
    // Calculate payment
  } else {
    enable($("#id_period_end"))
  }
});

// end_date change
$('#id_period_end').datepicker().on("changeDate", function(e) {
  if ($('#id_employee').val()) {
    calculateSalary()
  }
})

// Employee Chosen
$('#id_employee').change(function() {
  if ($(this).val()) {
    calculateSalary()
  }
})

$(':input[type=number]').change(function() {
  if (!$(this).val().trim()) {
    $(this).val((0).toFixed(2))
  } else {
    $(this).val(parseInt($(this).val()).toFixed(2))
  }

  if ($(this).hasClass('payment')) { // payment
    total = parseInt($('#id_basic_salary').val()) + parseInt($('#id_allowance').val()) + parseInt($('#id_other_payments').val())
    $('#id_total_payments').val(total.toFixed(2))
  } else { // deduction & net pay
    total = parseInt($('#id_mpf_employee').val()) + parseInt($('#id_np_leave').val()) + parseInt($('#id_other_deductions').val())
    $('#id_total_deductions').val(total.toFixed(2))
  }
  net_pay = parseInt($('#id_total_payments').val() - parseInt($('#id_total_deductions').val()))
  $('#id_net_pay').val(net_pay.toFixed(2))
})