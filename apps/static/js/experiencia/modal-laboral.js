$(document).ready(function() {
  $("#agrega-laboral").on( "click", function() {
    $(".add-item-laboral").html("Agregar");
    $("#modal-laboral .modal-title").html("Nueva Experiencia Laboral");
    $("#formLaboral")[0].reset();
    $("#errores_list").html("");
    $('#modal-laboral').modal('show');
    $("#id_lab").val("");
  });

  $("#btnCerrarHeaderModallaboral").click(function(){
    $("#modal-laboral").modal("hide");
  });

  $("#btnCerrarModalLaboral").click(function(){
    $("#modal-laboral").modal("hide");
  });

});

var table_laboral = $("#tabla-laboral").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaLaboral,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_laboral.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
  });
})

$(document).on('click', '.carga-editarl', function(e) {
  $form = $("#formLaboral");
  $form [0].reset();
  $form.valid()
  $("#errores_list").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaLaboral.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_lab").val(data.id);
      $("#formLaboral #id_cargo").val(data.cargo);
      $("#formLaboral #id_institucion").val(data.institucion_id);
      $("#formLaboral #id_fecha_inicio").val(data.fecha_inicio);
      $("#formLaboral #id_fecha_fin").val(data.fecha_fin);
      if (data.trabaja_actualmente){
        $("#formLaboral #id_trabaja_actualmente").prop('checked', true);
      }else{
        $("#formLaboral #id_trabaja_actualmente").prop('checked', false);
      }
      $("#formLaboral #id_descripcion_cargo").val(data.descripcion_cargo);
      $('#modal-laboral').modal('show');
      $(".add-item-laboral").html("Editar");
      $("#modal-laboral .modal-title").html("Editar Experiencia Laboral");
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

$(document).on('click', 'a.add-item-laboral', function(e) {
  $form = $("#formLaboral");
  if($form.valid()){
    cargarBlock();
    var id_laboral = $("#id_lab").val() ? $("#id_lab").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarLaboral}?laboral_id=${id_laboral}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_laboral.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-laboral").modal("hide");
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
