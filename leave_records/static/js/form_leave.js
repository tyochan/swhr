$.fn.datepicker.defaults.startDate = new Date()

function getStartDateText() {
  return $('#id_start_date').val()
}

function getEndDateText() {
  return $('#id_end_date').val()
}

function getStartDate() {
  return $('#id_start_date').datepicker('getDate')
}

function getEndDate() {
  return $('#id_end_date').datepicker('getDate')
}

// Toggle Day type
function toggleDayType() {
  // If start_date == end_date
  if (getStartDateText() === getEndDateText() && !$('#id_user').is(':disabled')) {
    enable($("#id_day_type"))
  } else {
    disable($("#id_day_type"))
  }
}

$().ready(function() {
  // Initialize  picking date
  endDate = new Date()
  endDate.setMonth(endDate.getMonth() + 3)
  $(".dateinput").datepicker("setEndDate", endDate)

  // If have both date input
  if (getStartDate() && getEndDate()) {
    // Set start date and end date
    $('#id_start_date').datepicker("setEndDate", getEndDate())
    $('#id_end_date').datepicker("setStartDate", getStartDate())
    toggleDayType()
  }
});

// start_date change
$('#id_start_date').datepicker().on("changeDate", function(e) {
  // Set min end_date
  $('#id_end_date').datepicker("setStartDate", e.date)

  // If has end_date
  if ($('#id_end_date').val()) {
    leave_calculation() // Calculate spend
    toggleDayType() // Toggle day_type
  } else {
    readok($("#id_end_date"))
  }
});

// end_date change
$('#id_end_date').datepicker().on("changeDate", function(e) {
  // Set max start_date
  $('#id_start_date').datepicker("setEndDate", e.date)

  leave_calculation() // Calculate spend
  toggleDayType() // Toggle day_type
});

// day_type change
$('#id_day_type').on('change', function() {
  leave_calculation()
})