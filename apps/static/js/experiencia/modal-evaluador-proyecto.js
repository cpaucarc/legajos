$(document).ready(function() {
  $(".met_evaluacion").hide();
  $("#agrega-evaluador-proyecto").on( "click", function() {
    $(".add-item-evaluador").html("Agregar");
    $("#modal-evaluador .modal-title").html("Nueva Experiencia Como Evaluador y/o formulador de proyectos");
    $("#formEvaluador")[0].reset();
    $("#errores_list_evaluador").html("");
    $('#modal-evaluador').modal('show');
    $("#id_evaluador").val("");
  });

  $("#btnCerrarHeaderModalEvaluador").click(function(){
    $("#modal-evaluador").modal("hide");
  });

  $("#btnCerrarModalEvaluador").click(function(){
    $("#modal-evaluador").modal("hide");
  });

  $("#id_ep-experiencia").on( "click", function() {
    if($(this).val() === "evaluador"){
      $(".met_evaluacion").show();
      $("#div_id_ep-tipo_proyecto_formulado > label").html("Tipo de proyecto evaluado");
      $("#div_id_ep-presupuesto_proyecto > label").html("Presupuesto total del proyecto evaluado");
    }else if($(this).val() === "formulador") {
      $(".met_evaluacion").hide();
      $("#div_id_ep-tipo_proyecto_formulado > label").html("Tipo de proyecto formulado");
      $("#div_id_ep-presupuesto_proyecto > label").html("Presupuesto total del proyecto formulado");
    }else{
      $(".met_evaluacion").hide();
      $("#div_id_ep-tipo_proyecto_formulado > label").html("Tipo de proyecto formulado/evaluado");
      $("#div_id_ep-presupuesto_proyecto > label").html("Presupuesto total del proyecto formulado/evaluado");
    }
  });

});

var table_evaluador = $("#tabla-evaluador-proyecto").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaEvaluadorProyecto,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_evaluador.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
  });
})

$(document).on('click', '.carga-editarep', function(e) {
  $form = $("#formEvaluador");
  $form [0].reset();
  $form.valid()
  $("#errores_list_evaluador").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaEvaluadorProyecto.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_evaluador").val(data.id);
      $("#id_ep-anio").val(data.anio);
      $("#id_ep-pais").val(data.pais);
      $("#id_ep-tipo_proyecto_formulado").val(data.tipo_proyecto_formulado);
      $("#id_ep-experiencia").val(data.experiencia);
      $("#id_ep-metodologia_evaluacion").val(data.metodologia_evaluacion);
      $("#id_ep-entidad_financiadora").val(data.entidad_financiadora);
      $("#id_ep-nombre_concurso").val(data.nombre_concurso);
      $("#id_ep-url_concurso").val(data.url_concurso);
      $("#id_ep-presupuesto_proyecto").val(data.presupuesto_proyecto);
      $('#modal-evaluador').modal('show');
      $(".add-item-evaluador").html("Editar");
      $("#modal-evaluador .modal-title").html("Editar Experiencia Como Evaluador y/o formulador de proyectos");
    },
    error : function(xhr,errmsg,err) {
      cerrarBlock();
      swal({
        title: "Error",
        html: "Ocurrio un error intente nuevamente",
        type: "warning"
      });
    }
  });
});

$(document).on('click', 'a.add-item-evaluador', function(e) {
  $form = $("#formEvaluador");
  if($form.valid()){
    cargarBlock();
    var id_evaluador = $("#id_evaluador").val() ? $("#id_evaluador").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarEvaluadorProyecto}?evaluador_id=${id_evaluador}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list_evaluador").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_evaluador.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-evaluador").modal("hide");
        }
        cerrarBlock();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        swal({
          text: jqXHR,
          type: "error"
        });
       cerrarBlock();
      }
    });
  }
});

