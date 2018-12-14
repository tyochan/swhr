MSPERDAY = (1000 * 60 * 60 * 24)

HOLIDAYS = [
  '2018-12-25', '2018-12-26',
  '2019-1-1', '2019-2-5', '2019-2-6', '2019-2-7', '2019-4-5', '2019-4-19', '2019-4-22', '2019-5-1', '2019-5-13', '2019-6-7', '2019-7-1', '2019-10-1', '2019-10-7', '2019-12-25', '2019-12-26',
  '2020-1-1', '2020-1-27', '2020-1-28', '2020-4-10', '2020-4-13', '2020-4-30', '2020-5-1', '2020-6-25', '2020-7-1', '2020-10-1', '2020-10-2', '2020-10-26', '2020-12-25',
  '2021-1-1', '2021-2-12', '2021-2-15', '2021-4-2', '2021-4-5', '2021-5-19', '2021-6-14', '2021-7-1', '2021-9-22', '2021-10-1', '2021-10-14', '2021-12-27',
  '2022-1-1', '2022-2-1', '2022-2-2', '2022-2-3', '2022-4-5', '2022-4-15', '2022-4-18', '2022-5-2', '2022-5-9', '2022-6-3', '2022-7-1', '2022-9-10', '2022-10-4', '2022-12-26',
  '2023-1-2', '2023-1-23', '2023-1-24', '2023-4-5', '2023-4-7', '2023-4-10', '2023-5-1', '2023-5-26', '2023-6-22', '2023-10-2', '2023-10-23', '2023-12-25', '2023-12-26',
]

log = console.log.bind(console)

function enable(object) {
  object.prop('disabled', false)
}

function disable(object) {
  object.prop('disabled', true)
}

// Datepicker options
$.fn.datepicker.defaults.format = "yyyy-mm-dd"
$.fn.datepicker.defaults.autoclose = true
$.fn.datepicker.defaults.todayBtn = true
$.fn.datepicker.defaults.todayHighlight = true
$.fn.datepicker.defaults.daysOfWeekDisabled = '06'
$.fn.datepicker.defaults.datesDisabled = HOLIDAYS

// $().ready(function() {
// Check if holidays are weekends
// for (var i in HOLIDAYS) {
//   array = HOLIDAYS[i].split('-');
//   date = new Date(array[0], array[1] - 1, array[2]);
//   if (date.getDay() == 0 || date.getDay() == 6) {
//     console.log(holidays[i]);
//   }
// }
// });