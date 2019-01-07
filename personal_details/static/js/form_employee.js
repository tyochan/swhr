function getStartDateText() {
  return $('#id_date_joined').val()
}

function getEndDateText() {
  return $('#id_last_date').val()
}

function getStartDate() {
  return $('#id_date_joined').datepicker('getDate')
}

function getEndDate() {
  return $('#id_last_date').datepicker('getDate')
}

$().ready(function() {
  staff_id = $("#id_staff_id").val()
  $('#id_username').val(staff_id)
  $('#id_password').val(staff_id)

  $('#id_last_date').datepicker("setStartDate", getStartDate())

  if ($("#id_is_active").is(":checked")) {
    disable($("#id_last_date"))
  } else {
    enable($("#id_last_date"))
  }

  $("#id_date_joined").datepicker().trigger("changeDate")
});

// Toggle last_date
$("#id_is_active").on('click', function() {
  if (this.checked) {
    disable($("#id_last_date"))
  } else {
    $('#id_last_date').datepicker("setStartDate", getStartDate())
    enable($("#id_last_date"))
  }
})

// Join dateinput
$("#id_date_joined").datepicker().on("changeDate", function(e) {
  if (name_in_path("create")) {
    annual_leave_calculation()
  }
})