$(document).ready(function() {
  $("#agrega-docente").on( "click", function() {
    $(".add-item-docente").html("Agregar");
    $("#modal-docente .modal-title").html("Nueva Experiencia Como Docente");
    $("#formDocente")[0].reset();
    $("#errores_list").html("");
    $('#modal-docente').modal('show');
    $("#id_doc").val("");
  });

  $("#btnCerrarHeaderModalDocente").click(function(){
    $("#modal-docente").modal("hide");
  });

  $("#btnCerrarModalDocente").click(function(){
    $("#modal-docente").modal("hide");
  });

});

var table_docente = $("#tabla-docente").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaDocente,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_docente.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
  });
})

$(document).on('click', '.carga-editard', function(e) {
  $form = $("#formDocente");
  $form [0].reset();
  $form.valid()
  $("#errores_list_docente").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaDocente.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_doc").val(data.id);
      $("#id_d-tipo_institucion").val(data.tipo_institucion);
      $("#id_d-institucion").val(data.institucion_id);
      $("#id_d-tipo_docente").val(data.tipo_docente);
      $("#id_d-fecha_inicio").val(data.fecha_inicio);
      $("#id_d-fecha_fin").val(data.fecha_fin);
      $("#id_d-descripcion_cargo").val(data.descripcion_cargo);
      if (data.trabaja_actualmente){
        $("#id_d-trabaja_actualmente").prop('checked', true);
      }else{
        $("#id_d-trabaja_actualmente").prop('checked', false);
      }
      $('#modal-docente').modal('show');
      $(".add-item-docente").html("Editar");
      $("#modal-docente .modal-title").html("Editar Experiencia Como Docente");
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

$(document).on('click', 'a.add-item-docente', function(e) {
  $form = $("#formDocente");
  if($form.valid()){
    cargarBlock();
    var id_docente = $("#id_doc").val() ? $("#id_doc").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarDocente}?docente_id=${id_docente}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list_docente").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_docente.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-docente").modal("hide");
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

