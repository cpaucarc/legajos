$(document).ready(function() {
  $("#agrega-universitaria").on( "click", function() {
    $(".add-item-universitaria").html("Agregar");
    $("#modal-universitaria .modal-title").html("Nueva formacion universitaria");
    $("#formUniversitaria")[0].reset();
    $("#errores_list").html("");
    $('#modal-universitaria').modal('show');
    $("#id_universitaria").val("");
  });

  $("#btnCerrarHeaderModalUniversitaria").click(function(){
    $("#modal-universitaria").modal("hide");
  });

  $("#btnCerrarModalUniversitaria").click(function(){
    $("#modal-universitaria").modal("hide");
  });

});

var table_universitaria = $("#tabla-universitaria").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaUniversitaria,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_universitaria.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
    $(this).find('td').eq(7).attr("align",'center');
  });
})

$(document).on('click', '.carga-editaru', function(e) {
  $form = $("#formUniversitaria");
  $form [0].reset();
  $form.valid()
  $("#errores_list").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaUniversitaria.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_universitaria").val(data.id);
      $("#id_u-pais_estudios").val(data.pais_estudios);
      $("#id_u-centro_estudios").val(data.centro_estudios_id);
      $("#id_u-fecha_inicio").val(data.fecha_inicio);
      $("#id_u-fecha_fin").val(data.fecha_fin);
      $("#id_u-facultad").val(data.facultad);
      $("#id_u-nombre_grado").val(data.nombre_grado);
      $("#id_u-grado_obtenido").val(data.grado_obtenido);
      $('#modal-universitaria').modal('show');
      $(".add-item-universitaria").html("Editar");
      $("#modal-universitaria .modal-title").html("Editar formación universitaria");
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

$(document).on('click', 'a.add-item-universitaria', function(e) {
  $form = $("#formUniversitaria");
  if($form.valid()){
    cargarBlock();
    var id_universitaria = $("#id_universitaria").val() ? $("#id_universitaria").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarUniversitaria}?universitaria_id=${id_universitaria}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_universitaria.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-universitaria").modal("hide");
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

$(document).on('click', '.eliminar-universitaria', function(e) {
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
    $.get(urlEliminarUniversitaria.replace("id", id), function(data) {
    table_universitaria.ajax.reload();
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