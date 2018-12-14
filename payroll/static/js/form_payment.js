$.fn.datepicker.defaults.daysOfWeekDisabled = ''
$.fn.datepicker.defaults.datesDisabled = ''

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
  // Initialize All Datepicker
  $(".datepicker").datepicker()

  // If no date input
  if (!getStartDate() && !getEndDate()) {
    disable($("#id_period_end"))
  } else { // Has input
    // Set start date and end date
    $('#id_period_start').datepicker("setEndDate", getEndDate())
    $('#id_period_end').datepicker("setStartDate", getStartDate())
  }
});

// start_date change
$('#id_period_start').datepicker().on("changeDate", function(e) {
  // Set min end_date
  $('#id_period_end').datepicker("setStartDate", e.date)

  // If has end_date
  if ($('#id_period_end').val()) {
    // Calculate payment
  } else {
    enable($("#id_period_end"))
  }
});

// end_date change
$('#id_period_end').datepicker().on("changeDate", function(e) {
  // Set max start_date
  $('#id_period_start').datepicker("setEndDate", e.date)
  // Calculate spend
});

// Employee Chosen
$('#id_employee').change(function() {
  calculateSalary()
})