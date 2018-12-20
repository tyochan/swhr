function getStartDateText() {
  return $('#id_join_date').val()
}

function getEndDateText() {
  return $('#id_leave_date').val()
}

function getStartDate() {
  return $('#id_join_date').datepicker('getDate')
}

function getEndDate() {
  return $('#id_leave_date').datepicker('getDate')
}

$().ready(function() {
  // Initialize All Datepicker
  $(".dateinput").datepicker()

  $('#id_leave_date').datepicker("setStartDate", getStartDate())

  if ($("#id_active").is(":checked")) {
    disable($("#id_leave_date"))
  } else {
    enable($("#id_leave_date"))
  }
});

// Toggle leave_date
$("#id_active").on('click', function() {
  if (this.checked) {
    disable($("#id_leave_date"))
  } else {
    $('#id_leave_date').datepicker("setStartDate", getStartDate())
    enable($("#id_leave_date"))
  }
})