$(document).ready(function() {
  $("#agrega-asesor").on( "click", function() {
    $(".add-item-asesor").html("Agregar");
    $("#modal-asesor .modal-title").html("Nueva Experiencia Como Asesor de Tesis");
    $("#formAsesor")[0].reset();
    $("#errores_list").html("");
    $('#modal-asesor').modal('show');
    $("#id_asesor").val("");
  });

  $("#btnCerrarHeaderModalAsesor").click(function(){
    $("#modal-docente").modal("hide");
  });

  $("#btnCerrarModalAsesor").click(function(){
    $("#modal-docente").modal("hide");
  });

});

var table_asesor = $("#tabla-asesor").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaAsesorTesis,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_asesor.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
  });
})

$(document).on('click', '.carga-editara', function(e) {
  $form = $("#formAsesor");
  $form [0].reset();
  $form.valid()
  $("#errores_list_asesor").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaAsesorTesis.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_asesor").val(data.id);
      $("#id_a-universidad").val(data.universidad_id);
      $("#id_a-tesis").val(data.tesis);
      $("#id_a-fecha_aceptacion_tesis").val(data.fecha_aceptacion_tesis);
      $("#id_a-enlace_fuente_repositorio_academico").val(data.enlace_fuente_repositorio_academico);
      $("#id_a-tesista").val(data.tesista);
      $('#modal-asesor').modal('show');
      $(".add-item-asesor").html("Editar");
      $("#modal-asesor .modal-title").html("Editar Experiencia Como Asesor de Tesis");
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

$(document).on('click', 'a.add-item-asesor', function(e) {
  $form = $("#formAsesor");
  if($form.valid()){
    cargarBlock();
    var id_asesor = $("#id_asesor").val() ? $("#id_asesor").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarAsesorTesis}?asesor_id=${id_asesor}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list_asesor").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_docente.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-asesor").modal("hide");
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

