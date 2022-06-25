/**
 * Created by cj on 3/31/17.
 */
function alertMessage(title, message, type) {
  swal({
    title: title,
    html: message,
    type: type
  });
  NProgress.done();
}

function get_data_api(url) {
  var json_data = null;
  $.ajax({
    async: false,
    global: false,
    url: url,
    dataType: "json",
    success: function (data) {
      json_data = data.data;
    }
  });
  NProgress.done();
  return json_data;
}

$.datepicker.regional['es'] = {
  closeText: 'Cerrar',
  prevText: '<Ant',
  nextText: 'Sig>',
  currentText: 'Hoy',
  monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
  monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
  dayNames: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
  dayNamesShort: ['Dom', 'Lun', 'Mar', 'Mié', 'Juv', 'Vie', 'Sáb'],
  dayNamesMin: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sá'],
  weekHeader: 'Sm',
  dateFormat: 'dd/mm/yy',
  firstDay: 1,
  isRTL: false,
  showMonthAfterYear: false,
  yearSuffix: ''
};
$.datepicker.setDefaults($.datepicker.regional['es']);

$.validator.addMethod("validDate", function(value, element) {
  return this.optional(element) || moment().isSameOrAfter(moment(value,"DD/MM/YYYY"), 'day');
}, "Fecha inválida");

