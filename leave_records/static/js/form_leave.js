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

// Calculate spend days
function updateSpendDays() {
  start_date = getStartDate()
  end_date = getEndDate()

  // Calculate workdays with weekends
  diff = (end_date - start_date) / MSPERDAY
  weeks = Math.floor(diff / 7)
  diff -= weeks * 2
  if (start_date.getDay() - end_date.getDay() >= 1) {
    diff -= 2
  }

  // Calculate workdays with holidays
  for (var i in HOLIDAYS) {
    array = HOLIDAYS[i].split('-');
    date = new Date(array[0], array[1] - 1, array[2]);
    if (date >= start_date && (date <= end_date)) {
      diff--
    }
  }

  // Update days spend
  diff += 1
  $('input[name=spend]').val(diff)
}

// Toggle Day type
function toggleDayType() {
  // If start_date == end_date
  if (getStartDateText() === getEndDateText()) {
    enable($("#id_day_type"))
  } else {
    disable($("#id_day_type"))
  }
}


$().ready(function() {
  // Initialize All Datepicker
  $(".dateinput").datepicker()

  // Initialize  picking date
  var endDate = new Date()
  endDate.setMonth(endDate.getMonth() + 3)
  $(".dateinput").datepicker("setEndDate", endDate)

  // If no date input
  if (!getStartDate() && !getEndDate()) {
    disable($("#id_end_date"))
    disable($("#id_day_type"))
  } else { // Has input
    // Set start date and end date
    $('#id_start_date').datepicker("setEndDate", getEndDate())
    $('#id_end_date').datepicker("setStartDate", getStartDate())

    // If start_date = end_date
    if (getStartDateText() === getEndDateText()) {
      enable($("#id_day_type"))
    } else {
      disable($("#id_day_type"))
    }
  }
});

// start_date change
$('#id_start_date').datepicker().on("changeDate", function(e) {
  // Set min end_date
  $('#id_end_date').datepicker("setStartDate", e.date)

  // If has end_date
  if ($('#id_end_date').val()) {
    updateSpendDays() // Calculate spend
    toggleDayType() // Toggle day_type
  } else {
    enable($("#id_end_date"))
  }
});

// end_date change
$('#id_end_date').datepicker().on("changeDate", function(e) {
  // Set max start_date
  $('#id_start_date').datepicker("setEndDate", e.date)
  updateSpendDays() // Calculate spend
  toggleDayType() // Toggle day_type
});

// day_type change
$('#id_day_type').on('change', function() {
  if (this.value == 'HD') { // Half day spend = 0.5
    $('input[name=spend]').val(0.5)
  } else { // Full day spend = 1 OR Blank
    $('input[name=spend]').val(1)
  }
})