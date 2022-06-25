$(document).ready(function() {
  $("#agrega-cientifica").on( "click", function() {
    $(".add-item-cientifica").html("Agregar");
    $("#modal-cientifica .modal-title").html("Nueva producción científica");
    $("#formCientifica")[0].reset();
    $("#errores_list").html("");
    $('#modal-cientifica').modal('show');
    $("#id_cientifica").val("");
  });

  $("#btnCerrarHeaderModalCientifica").click(function(){
    $("#modal-cientifica").modal("hide");
  });

  $("#btnCerrarModalCientifica").click(function(){
    $("#modal-cientifica").modal("hide");
  });

});

var table_cientifica = $("#tabla-cientifica").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaCientifica,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
});

table_cientifica.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(4).attr("align",'center');
    $(this).find('td').eq(5).attr("align",'center');
    $(this).find('td').eq(6).attr("align",'center');
    $(this).find('td').eq(7).attr("align",'center');
  });
})

$(document).on('click', '.carga-editaru', function(e) {
  $form = $("#formCientifica");
  $form [0].reset();
  $form.valid()
  $("#errores_list").html("");
  var id = $(this).attr('data-id');
  cargarBlock();
  $.ajax({
    url : urlConsultaCientifica.replace('id', id),
    type : "GET",
    success : function(data) {
      cerrarBlock();
      $("#id_cientifica").val(data.id);
      $("#id_categoria_trabajo").val(data.categoria_trabajo);
      $("#id_tipo_obra").val(data.tipo_obra);
      $("#id_funcion").val(data.funcion);
      $("#id_titulo").val(data.titulo);
      $("#id_sub_titulo").val(data.sub_titulo);
      $("#id_revista").val(data.revista);
      $("#id_autor").val(data.autor);
      $("#id_volumen").val(data.volumen);
      $("#id_fasciculo").val(data.fasciculo);
      $("#id_rango_paginas").val(data.rango_paginas);
      $("#id_tipo_cita").val(data.tipo_cita);
      $("#id_cita").val(data.cita);
      $("#id_descripcion").val(data.descripcion);
      $("#id_orden_autoria").val(data.orden_autoria);
      $("#id_fecha_publicacion").val(data.fecha_publicacion);
      $("#id_pais_publicacion").val(data.id_pais_publicacion);
      if (data.tipo_congreso == 'nacional'){
        $('#id_tipo_congreso_1').prop('checked',true);
      }
      if (data.tipo_congreso == 'internacional'){
        $('#id_tipo_congreso_2').prop('checked',true);
      }
      $("#div_tipo_congreso").hide();
      $("#div_cita").hide();
      if (data.categoria_trabajo == 'conferencia'){
        $("#div_tipo_congreso").show();
      }else if(data.categoria_trabajo === 'otro'){
        $("#div_cita").show();
      }

      $('#modal-cientifica').modal('show');
      $(".add-item-cientifica").html("Editar");
      $("#modal-cientifica .modal-title").html("Editar producción científica");
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

$(document).on('click', 'a.add-item-cientifica', function(e) {
  $form = $("#formCientifica");
  if($form.valid()){
    cargarBlock();
    var id_cientifica= $("#id_cientifica").val() ? $("#id_cientifica").val() : '';
    $.ajax({
      method: "POST",
      url: `${urlGuardarCientifica}?cientifica_id=${id_cientifica}`,
      data: $form.serialize(),
      success: function (response) {
        if (response["error"]){
          $("#errores_list").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
        }
        if (response['msg']) {
          table_cientifica.ajax.reload();
          swal({
              text: response['msg'],
              type: "success"
          })
          $("#modal-cientifica").modal("hide");
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

$(document).on('click', '.eliminar-cientifica', function(e) {
  const id = $(this).attr("data-id");
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar la producción científica seleccionada?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.get(urlEliminarCientifica.replace("id", id), function(data) {
    table_cientifica.ajax.reload();
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

$("#div_cita").hide();
$("#div_tipo_congreso").hide();
$("#id_categoria_trabajo").on('change', function () {
  var selectedOption = $(this).find('option:selected').val();
  $("#div_tipo_congreso").hide();
  $("#div_cita").hide();
  if(selectedOption === "otro"){
    $("#div_cita").show();
  } else if(selectedOption === "conferencia"){
    $("#div_tipo_congreso").show();
  }
});
