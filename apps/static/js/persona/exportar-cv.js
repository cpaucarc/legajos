$(document).ready(function () {
  $('#id_datos_personales').prop("checked", true);
  $('#id_experiencia_laboral').prop("checked", true);
  $('#id_formacion_academica').prop("checked", true);
  $('#id_idiomas').prop("checked", true);
  $('#id_produccion_cientifica').prop("checked", true);
  $('#id_premios').prop("checked", true);

  $("#btn-descarga-cv").on('click', function() {
    const id_persona = $(this).attr("data-id");
    array_filtros = []
    $("input:checkbox:checked").each(function() {
      opcion = $(this)[0].name
      valor = $(this).val()
      array_filtros.push({opcion, valor});
    });
    arreglo = JSON.stringify(array_filtros)
    window.location.href =`/descargar-cv/${id_persona}/?array_filtros=${arreglo}`;
  });

});