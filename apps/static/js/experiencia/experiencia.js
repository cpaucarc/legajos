$(document).ready(function () {
  $("form").validate({
    rules: {
      'departamento': {
          "required": function(){
              return $("#id_tipo_persona").val() == "docente";
          }
      },
      'facultad': {
          "required": function(){
              return $("#id_tipo_persona").val() == "docente";
          }
      }
    }
  });

  $("#lista-persona").on("click", ".eliminarc", function() {
    const id = $(this).attr("data-id");
    swal({
      title: "Importante",
      text: `¿Está seguro que desea eliminar a la persona seleccionada?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $.get(eliminarPersona.replace("id", id), function(data) {
        tipoMsg = data["tipo_msg"] ? 'warning': 'success';
        swal({
          text: data["msg"],
          type: tipoMsg
        }).then(function() {
          if (!data["tipo_msg"]){
            window.location.href = "/";
          }
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

});

function cerrarBlock(){
  $.blockUI({
      message: '<i style="font-size:36px;" class="fa fa-spinner fa-pulse fa-fw"></i>',
      timeout: 1,
      overlayCSS: {
          backgroundColor: '#000',
          opacity: 0.5,
          cursor: 'wait'
      },
      css: {
          border: 0,
          padding: 0,
          color: '#333',
          backgroundColor: 'transparent'
      }
  });
}

function cargarBlock(){
  $.blockUI({
      message: '<i style="font-size:36px;" class="fa fa-spinner fa-pulse fa-fw"></i>',
      timeout: 1000000,
      overlayCSS: {
          backgroundColor: '#000',
          opacity: 0.5,
          cursor: 'wait'
      },
      css: {
          border: 0,
          padding: 0,
          backgroundColor: 'transparent'
      }
  });
}