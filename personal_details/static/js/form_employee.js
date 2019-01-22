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
  $('#id_password').val('abcd1234')

  $('#id_last_date').datepicker("setStartDate", getStartDate())

  if ($("#id_is_active").is(":checked")) {
    disable($("#id_last_date"))
  } else {
    enable($("#id_last_date"))
  }

  if ($("#id_marital_status").val() == 'SI') {
    disable($("#id_spouse_name"))
    disable($("#id_spouse_identity_type"))
    disable($("#id_spouse_identity_no"))
  } else {
    enable($("#id_spouse_name"))
    enable($("#id_spouse_identity_type"))
    enable($("#id_spouse_identity_no"))
  }

  $("#id_date_joined").datepicker().trigger("changeDate")

  $(".dateinput").datepicker("setEndDate", new Date())
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

$("#id_marital_status").on('change', function() {
  log($("#id_marital_status").val() == 'SI')
  if ($("#id_marital_status").val() == 'SI') {
    disable($("#id_spouse_name"))
    disable($("#id_spouse_identity_type"))
    disable($("#id_spouse_identity_no"))
  } else {
    enable($("#id_spouse_name"))
    enable($("#id_spouse_identity_type"))
    enable($("#id_spouse_identity_no"))
  }
})