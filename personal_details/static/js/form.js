holidays = [
  '2018-12-25', '2018-12-26',
  '2019-1-1', '2019-2-5', '2019-2-6', '2019-2-7', '2019-4-5', '2019-4-19', '2019-4-22', '2019-5-1', '2019-5-13', '2019-6-7', '2019-7-1', '2019-10-1', '2019-10-7', '2019-12-25', '2019-12-26',
  '2020-1-1', '2020-1-27', '2020-1-28', '2020-4-10', '2020-4-13', '2020-4-30', '2020-5-1', '2020-6-25', '2020-7-1', '2020-10-1', '2020-10-2', '2020-10-26', '2020-12-25',
]

// Datepicker options
$.fn.datepicker.defaults.format = "yyyy-mm-dd";
$.fn.datepicker.defaults.autoclose = true;
$.fn.datepicker.defaults.daysOfWeekDisabled = '06';
$.fn.datepicker.defaults.todayBtn = true;
$.fn.datepicker.defaults.todayHighlight = true;

$(document).ready(function() {
  // Check if holidays are weekends
  // for (var i in holidays) {
  //   array = holidays[i].split('-');
  //   date = new Date(array[0], array[1] - 1, array[2]);
  //   if (date.getDay() == 0 || date.getDay() == 6) {
  //     console.log(holidays[i]);
  //   }
  // }

  // Initialize Timepicker
  // $(".timepicker").timepicker({
  //   timeFormat: 'H:i',
  //   step: 30,
  //   minTime: '09:00',
  //   maxTime: '18:00',
  //   disableTimeRanges: [
  //     ['12:00', '14:00']
  //   ],
  // });
  //
  // $('#id_from_time').timepicker('option', {
  //   maxTime: '17:30'
  // });
  // $("#id_from_time").prop('disabled', true);
  //
  // $('#id_to_time').timepicker('option', {
  //   minTime: '09:30'
  // });
  // $("#id_to_time").prop('disabled', true);

  // Initialize Datepicker
  $(".datepicker").datepicker();
  // If form has end date picker
  if (document.getElementById('id_end_date')) {
    $("#id_end_date").prop('disabled', true);
    $("#id_day_type").prop('disabled', true);
    $(".datepicker").datepicker("setStartDate", new Date());

    var endDate = new Date();
    endDate.setMonth(endDate.getMonth() + 6);
    $(".datepicker").datepicker("setEndDate", endDate);
  }
});

// From time picker on change
// $('#id_from_time').on("change", function() {
//   // Set to time picker minTime and enable it
//   minTime = $('#id_from_time').timepicker('getTime');
//   minTime.setMinutes(minTime.getMinutes() + 30);
//   $("#id_to_time").timepicker('option', 'minTime', minTime);
//   $("#id_to_time").prop('disabled', false);
//
//   // If to time picker has set time
//   if ($("#id_to_time").timepicker('getTime')) {
//     diff = (($('#id_to_time').timepicker('getTime') - $('#id_from_time').timepicker('getTime')) / (1000 * 60 * 60 * 8));
//     spend = document.getElementById('id_spend');
//     spend.value = diff;
//   }
// })
//
// // To time picker on change
// $('#id_to_time').on("change", function() {
//   // Set from time picker maxTime
//   maxTime = $('#id_to_time').timepicker('getTime');
//   maxTime.setMinutes(maxTime.getMinutes() - 30);
//   $("#id_from_time").timepicker('option', 'maxTime', maxTime);
//
//   // Must have from time set
//   diff = (($('#id_to_time').timepicker('getTime') - $('#id_from_time').timepicker('getTime')) / (1000 * 60 * 60 * 8));
//   spend = document.getElementById('id_spend');
//   spend.value = diff;
// })

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
      diff = (($('#id_end_date').datepicker('getDate') - $('#id_start_date').datepicker('getDate')) / (1000 * 60 * 60 * 24));
      spend = document.getElementById('id_spend');

      // Enable from time picker if same date
      // Enable day type
      if (diff == 0) {
        $("#id_day_type").prop('disabled', false);
        // $("#id_from_time").prop('disabled', false);
        spend.value = 1;
      } else {
        $("#id_day_type").prop('disabled', true);
        // $("#id_from_time").prop('disabled', true);
        // $("#id_to_time").prop('disabled', true);
        spend.value = diff + 1;
      }
    }
  }
});

// End date picker on change
$('#id_end_date').datepicker().on("changeDate", function(e) {
  // Must have start date picker, so no need if case
  $('#id_start_date').datepicker("setEndDate", e.date);

  // Calculate days spend
  diff = (($('#id_end_date').datepicker('getDate') - $('#id_start_date').datepicker('getDate')) / (1000 * 60 * 60 * 24));
  spend = document.getElementById('id_spend');

  // Enable from time picker if same date
  // Enable day type
  if (diff == 0) {
    $("#id_day_type").prop('disabled', false);
    // $("#id_from_time").prop('disabled', false);
    spend.value = 1;
  } else {
    $("#id_day_type").prop('disabled', true);
    // $("#id_from_time").prop('disabled', true);
    // $("#id_to_time").prop('disabled', true);
    spend.value = diff + 1;
  }
});