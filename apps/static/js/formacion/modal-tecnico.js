$(document).ready(function() {
  $("#agrega-tecnico").on( "click", function() {
    $(".add-item-tecnico").html("Agregar");
    $("#modal-tecnico .modal-title").html("Nueva formacion técnica");
    $("#formTecnico")[0].reset();
    $("#errores_list1").html("");
    $('#modal-tecnico').modal('show');
    $("#id_tecnico").val("");
  });

  $("#btnCerrarHeaderModalTecnico").click(function(){
    $("#modal-tecnico").modal("hide");
  });

  $("#btnCerrarModalTecnico").click(function(){
    $("#modal-tecnico").modal("hide");
  });

});

var table_tecnico = $("#tabla-tecnico").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaTecnico,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_tecnico.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
  });
})

$(document).on('click', '.carga-editart', function(e) {
  $form = $("#formTecnico");
  $form [0].reset();
  $form.valid()
  $("#errores_list1").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaTecnico.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_tecnico").val(data.id);
      $("#id_t-centro_estudios").val(data.centro_estudios_id);
      $("#id_t-fecha_inicio").val(data.fecha_inicio);
      $("#id_t-fecha_fin").val(data.fecha_fin);
      $("#id_t-nombre_carrera").val(data.nombre_carrera);
      $('#modal-tecnico').modal('show');
      $(".add-item-tecnico").html("Editar");
      $("#modal-tecnico .modal-title").html("Editar formación técnica");
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

$(document).on('click', 'a.add-item-tecnico', function(e) {
  $form = $("#formTecnico");
  if($form.valid()){
    cargarBlock();
    var id_tecnico = $("#id_tecnico").val() ? $("#id_tecnico").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarTecnico}?tecnico_id=${id_tecnico}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list1").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_tecnico.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-tecnico").modal("hide");
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

$(document).on('click', '.eliminar-tecnico', function(e) {
  const id = $(this).attr("data-id");
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar a la experiencia técnica seleccionada?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.get(urlEliminarTecnico.replace("id", id), function(data) {
    table_tecnico.ajax.reload();
      swal({
        text: data["msg"],
        type: 'success'
      });
    }).fail(function(error) {
      swal({
        text: "Ocurrio un error al eliminar, intente nuevamente",
        type: "error"
      });
    });
  }).catch(() => {
    return;
  });
});