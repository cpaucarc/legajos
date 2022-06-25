/**
 * Created by cj on 2/14/17.
 */
var dateFormat = "dd/mm/yy";

$.datepicker.regional['es'] = {
  dateFormat     : dateFormat,
  dayNames       : ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
  dayNamesMin    : ['Do', 'Lu', 'Ma', 'Mc', 'Ju', 'Vi', 'Sa'],
  dayNamesShort  : ['Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'],
  firstDay       : 1,
  monthNames     : ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
  monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
};
$.datepicker.setDefaults($.datepicker.regional['es']);

function rangoFechas(id_fecha_inicio, id_fecha_fin) {
  $(id_fecha_inicio)
    .datepicker({
      changeMonth: true,
      changeYear : true,
      dateFormat : dateFormat,
      defaultDate: "+1w",
      showAnim   : "slideDown"
    })
    .on("change", function () {
      $(id_fecha_fin).datepicker("option", "minDate", getDate(this));
    });
  $(id_fecha_fin)
    .datepicker({
      changeMonth: true,
      changeYear : true,
      dateFormat : dateFormat,
      defaultDate: "+1w",
      showAnim   : "slideDown"
    })
    .on("change", function () {
      $(id_fecha_inicio).datepicker("option", "maxDate", getDate(this));
    });
}

function getDate(element) {
  var date;
  try {
    date = $.datepicker.parseDate(dateFormat, element.value);
  } catch (error) {
    date = null;
  }
  return date;
}

$('.btn-calendar-addon').click(function () {
  $(".form-control", $(this).closest(".input-group")).focus();
});

$('.btn-calendar-addon-error').click(function () {
  $(".form-control", $(this).closest(".input-group")).focus();
});

function datePicker(element) {
  $(element).datepicker({
    changeMonth: true,
    changeYear : true,
    dateFormat : dateFormat,
    showAnim   : "slideDown"
  });
}

function datePickerMaxToday(element) {
  $(element).datepicker({
    changeMonth: true,
    changeYear : true,
    dateFormat : dateFormat,
    showAnim   : "slideDown",
    maxDate    : "+0D"
  });
}

function datePickerMinToday(element) {
  $(element).datepicker({
    changeMonth: true,
    changeYear : true,
    dateFormat : dateFormat,
    showAnim   : "slideDown",
    minDate    : "-0D"
  });
}
