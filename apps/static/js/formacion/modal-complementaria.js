$(document).ready(function() {
  $("#agrega-complementaria").on( "click", function() {
    $(".add-item-complementaria").html("Agregar");
    $("#modal-complementaria .modal-title").html("Nueva formacion complementaria");
    $("#formComplementaria")[0].reset();
    $("#errores_list2").html("");
    $('#modal-complementaria').modal('show');
    $("#id_complementaria").val("");
  });

  $("#btnCerrarHeaderModalComplementaria").click(function(){
    $("#modal-complementaria").modal("hide");
  });

  $("#btnCerrarModalComplementaria").click(function(){
    $("#modal-complementaria").modal("hide");
  });

});

var table_complementaria = $("#tabla-complementaria").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaComplementaria,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_complementaria.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(7).attr("align",'center');
    $(this).find('td').eq(8).attr("align",'center');
    $(this).find('td').eq(9).attr("align",'center');
  });
})

$(document).on('click', '.carga-editarc', function(e) {
  $form = $("#formComplementaria");
  $form [0].reset();
  $form.valid()
  $("#errores_list2").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaComplementaria.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_complementaria").val(data.id);
      $("#id_c-capacitacion_complementaria").val(data.capacitacion_complementaria);
      $("#id_c-centro_estudios").val(data.centro_estudios_id);
      $("#id_c-pais_estudios").val(data.pais_estudios_id);
      $("#id_c-frecuencia").val(data.frecuencia);
      $("#id_c-cantidad").val(data.cantidad);
      $("#id_c-fecha_inicio").val(data.fecha_inicio);
      $("#id_c-fecha_fin").val(data.fecha_fin);
      $('#modal-complementaria').modal('show');
      $(".add-item-complementaria").html("Editar");
      $("#modal-complementaria .modal-title").html("Editar formación Complementaria");
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

$(document).on('click', 'a.add-item-complementaria', function(e) {
  $form = $("#formComplementaria");
  if($form.valid()){
    cargarBlock();
    var id_complementaria = $("#id_complementaria").val() ? $("#id_complementaria").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarComplementaria}?complementaria_id=${id_complementaria}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list2").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_complementaria.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-complementaria").modal("hide");
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

$(document).on('click', '.eliminar-complementaria', function(e) {
  const id = $(this).attr("data-id");
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar a la experiencia complementaria seleccionada?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.get(urlEliminarComplementaria.replace("id", id), function(data) {
    table_complementaria.ajax.reload();
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