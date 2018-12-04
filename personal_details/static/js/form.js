// Datepicker options
$.fn.datepicker.defaults.format = "yyyy-mm-dd";
$.fn.datepicker.defaults.autoclose = true;
$.fn.datepicker.defaults.daysOfWeekDisabled = '06';
$.fn.datepicker.defaults.todayBtn = true;
$.fn.datepicker.defaults.todayHighlight = true;

$(document).ready(function() {
  // Initialize Timepicker
  $(".timepicker").timepicker({
    timeFormat: 'H:i',
    step: 30,
    minTime: '09:00',
    maxTime: '18:00',
    disableTimeRanges: [
      ['12:00', '14:00']
    ],
  });

  $('#id_from_time').timepicker('option', {
    maxTime: '17:30'
  });
  $("#id_from_time").prop('disabled', true);

  $('#id_to_time').timepicker('option', {
    minTime: '09:30'
  });
  $("#id_to_time").prop('disabled', true);

  // Initialize Datepicker
  $(".datepicker").datepicker();
  // If form has end date picker
  if (document.getElementById('id_end_date')) {
    $("#id_end_date").prop('disabled', true);
    $(".datepicker").datepicker("setStartDate", new Date());

    var endDate = new Date();
    endDate.setMonth(endDate.getMonth() + 6);
    $(".datepicker").datepicker("setEndDate", endDate);
  }
});

// From time picker on change
$('#id_from_time').on("change", function() {
  $("#id_to_time").timepicker('option', 'minTime', $('#id_from_time').timepicker('getTime'));
  $("#id_to_time").prop('disabled', false);
})

// To time picker on change
$('#id_to_time').on("change", function() {
  $("#id_from_time").timepicker('option', 'maxTime', $('#id_to_time').timepicker('getTime'));
})

// Start date picker on change
$('#id_start_date').datepicker().on("changeDate", function(e) {
  // If end date picker exists
  if (document.getElementById('id_end_date')) {
    // First time input
    if (document.getElementById('id_end_date').value == '') {
      $('#id_end_date').datepicker("setStartDate", e.date);
      $("#id_end_date").prop('disabled', false);
    } else {
      // Calculate days spend
      end_date = $('#id_end_date').datepicker('getDate');
      diff = ((end_date - e.date) / (1000 * 60 * 60 * 24));
      spend = document.getElementById('id_spend');

      // Enable from time picker if same date
      if (diff == 0) {
        $("#id_from_time").prop('disabled', false);
        spend.value = '';
      } else {
        $("#id_from_time").prop('disabled', true);
        $("#id_to_time").prop('disabled', true);
        spend.value = diff;
      }
    }
  }
});

// End date picker on change
$('#id_end_date').datepicker().on("changeDate", function(e) {
  // Must have start date picker, so no need if case
  $('#id_start_date').datepicker("setEndDate", e.date);

  // Calculate days spend
  start_date = $('#id_start_date').datepicker('getDate')
  diff = ((e.date - start_date) / (1000 * 60 * 60 * 24));
  spend = document.getElementById('id_spend');
  console.log(document.getElementById('id_from_time'));

  // Enable from time picker if same date
  if (diff == 0) {
    $("#id_from_time").prop('disabled', false);
    spend.value = '';
  } else {
    $("#id_from_time").prop('disabled', true);
    $("#id_to_time").prop('disabled', true);
    spend.value = diff;
  }
});