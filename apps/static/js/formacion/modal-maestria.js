$(document).ready(function() {
  $("#agrega-maestria").on( "click", function() {
    $(".add-item-maestria").html("Agregar");
    $("#modal-maestria .modal-title").html("Nueva Maestría");
    $("#formMaestria")[0].reset();
    $("#errores_list3").html("");
    $('#modal-maestria').modal('show');
    $("#id_maestria").val("");
  });

  $("#btnCerrarHeaderModalMaestria").click(function(){
    $("#modal-maestria").modal("hide");
  });

  $("#btnCerrarModalMaestria").click(function(){
    $("#modal-maestria").modal("hide");
  });

});

var table_maestria = $("#tabla-maestria").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaMaestria,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_maestria.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(7).attr("align",'center');
    $(this).find('td').eq(8).attr("align",'center');
    $(this).find('td').eq(9).attr("align",'center');
  });
})

$(document).on('click', '.carga-editar-maestria', function(e) {
  $form = $("#formMaestria");
  $form [0].reset();
  $form.valid()
  $("#errores_list3").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaMaestria.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_maestria").val(data.id);
      $("#id_m-denominacion").val(data.denominacion);
      $("#id_m-centro_estudios").val(data.centro_estudios_id);
      $("#id_m-pais_estudios").val(data.pais_estudios_id);
      $("#id_m-modalidad").val(data.modalidad);
      $("#id_m-duracion").val(data.duracion);
      $("#id_m-fecha_inicio").val(data.fecha_inicio);
      $("#id_m-fecha_fin").val(data.fecha_fin);
      $('#modal-maestria').modal('show');
      $(".add-item-maestria").html("Editar");
      $("#modal-maestria .modal-title").html("Editar Maestría");
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

$(document).on('click', 'a.add-item-maestria', function(e) {
  $form = $("#formMaestria");
  if($form.valid()){
    cargarBlock();
    var id_maestria = $("#id_maestria").val() ? $("#id_maestria").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarMaestria}?maestria_id=${id_maestria}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list3").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_maestria.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-maestria").modal("hide");
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

$(document).on('click', '.eliminar-maestria', function(e) {
  const id = $(this).attr("data-id");
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar el registro de la maestría seleccionada?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.get(urlEliminarMaestria.replace("id", id), function(data) {
    table_maestria.ajax.reload();
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