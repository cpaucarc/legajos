$(document).ready(function () {

  var table_lista_capacitacion = $("#lista-capacitacion-validar").DataTable({
    language: {
      "url":  datatablesES
    },
    ajax: urlListarCapacitacionValidar,
    searching: true,
    processing: true,
    serverSide: true,
    ordering: false,
  });

  $("#lista-capacitacion-validar").on('click', '#ver_archivo_pdf', function() {
    const archivo_paquete = $(this).attr("data-archivo");
    var archivo =  archivo_paquete.replace('proyectos/', '');
    var url = urlProyectoDescargaPdf.replace('archivo', archivo).replace('.pdf', '')
    $("#iframe-proyecto-pdf").attr("src", url);
    $("#modal-proyecto-pdf").modal("show");
    $("#modal-proyecto-pdf").modal("show");
  });

  $("#lista-capacitacion-validar").on("click", ".eliminarc", function() {
    const id = $(this).attr("data-id");
    swal({
      title: "Importante",
      text: `¿Está seguro que desea eliminar el proyecto de capacitación?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $.get(eliminarCapacitacion.replace("id", id), function(data) {
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

  $("#lista-capacitacion-validar").on('click', '#accion_revisar', function() {
    var selectedOption = $(this).find('option:selected').val();
    var id=$(this).attr("data-id");
    $(`#lista-capacitacion-validar #msje1_${id}`).html("");
    var array_estado = ["validado", "culminado", "cancelado"];
    if(selectedOption && selectedOption === "observado"){
      observarCapacitacion($(this),id);
    }else if (selectedOption && array_estado.indexOf(selectedOption)>=0){
      revisarCapacitacion($(this),id, selectedOption);
    }else{
      swal({
        title: "Alerta",
        html: "No puede cambiar a estado por validar",
        type: "warning"
      });
      $(this).val($(`#estado-${id}`).val());
    }
  });

  function revisarCapacitacion($selector, id, estado) {
    var msj = (estado == 'culminado') ? 'ya no podrá realizar alguna modificación':''
    swal({
      title: "Importante",
      html: `Está a punto cambiar el estado del proyecto de capacitación a ${estado} ${msj}, ¿Está seguro?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $(`#lista-capacitacion-validar #msje1_${id}`).html("<i class='fa fa-spinner'></i>&nbsp;");
      $.ajax({
        method: "POST",
        url : urlrevisarCapacitacion,
        data: {
          'csrfmiddlewaretoken': csrf_token,
          'estado': estado,
          'id': id,
        },
        success : function(result) {
          table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
        },
        error : function(e) {
          swal({
            title: "Alerta",
            html: e.responseJSON.error,
            type: "warning"
          });
          $selector.val($(`#estado-${id}`).val())
          $(`#lista-capacitacion-validar #msje1_${id}`).html("<i class='fa fa-warning'></i>&nbsp;");
        }
      });
    }).catch(() => {
      $selector.val($(`#estado-${id}`).val())
      return false;
    });
  }

  function observarCapacitacion($selector, id) {
    swal({
      title: "Agregar Observación al proyecto de capacitación",
      html: `<textarea id="swal-input1" name="swal-input1" rows="2" cols="100" class="form-control"></textarea>`,
      type: "input",
      showCancelButton: true,
        preConfirm: function() {
          return new Promise(function(resolve, reject) {
            if (true) {
              var obsv = document.getElementById('swal-input1').value;
              if(obsv.length>3){
                swal({
                  title: "Importante",
                  html: `Está a punto de observar el proyecto de capacitación, ¿Está seguro?`,
                  type: "question",
                  showCancelButton: true,
                  confirmButtonColor: "#3085d6",
                  cancelButtonColor: "#d33",
                  confirmButtonText: "<i class='fa fa-check'></i> SI",
                  cancelButtonText: "<i class='fa fa-times'></i> NO"
                }).then(function() {
                    $(`#lista-capacitacion-validar #msje1_${id}`).html("<i class='fa fa-spinner'></i>&nbsp;");
                    $.ajax({
                      method: "POST",
                      url : urlObservarCapacitacion,
                      data: {
                        'csrfmiddlewaretoken': csrf_token,
                        'observacion': obsv,
                        'id': id,
                      },
                      success : function(result) {
                        table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
                      },
                      error : function(e) {
                        swal({
                          title: "Alerta",
                          html: e.responseJSON.error,
                          type: "warning"
                        });
                        $selector.val($(`#estado-${id}`).val())
                        $(`#lista-capacitacion-validar #msje1_${id}`).html("<i class='fa fa-warning'></i>&nbsp;")
                      }
                    });
                  }).catch(() => {
                  $selector.val($(`#estado-${id}`).val())
                  return false;
                });
              }else{
                reject("Ingrese como mínimo 4 caracteres");
                return false
              }
            }
          });
        }
    }).then(function(result) {
       swal(JSON.stringify(result));
    }).catch(() => {
      $selector.val($(`#estado-${id}`).val())
      return false;
    });
  }
  $("#lista-capacitacion-validar").on("click", ".v-acta", function() {
    const id = $(this).attr("data-id");
    const capacitacion_id = $(this).attr("capacitacion-id");
    var url = urlVerActa.replace('999999999', id).replace('capacitacion_id', capacitacion_id)
    $("#iframe-acta").attr("src", url);
    $("#modal-acta").modal("show");
  });

  $("#lista-capacitacion-validar").on('click', '.enviar-correo', function() {
    const id = $(this).attr("data-id");
    var url = urlEnviaCertificadoCorreo.replace('999999999', id)
    swal({
      title: "Importante",
      html: `Está seguro que desea enviar por correo los certificados?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $(`#lista-capacitacion-validar .ev-${id}`).html("Enviando....");
      $.ajax({
        url : url,
        type : "GET",
        success : function(data) {
          table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
          if(data.errores.length){
            msj = `Error al enviar correo(s): \n ${data.errores}`;
            tipo_error = "warning";
            titulo = "Alerta";
          }else{
            msj = "Se realizó el envío de correo(s) exitosamente";
            tipo_error = "success";
            titulo = "Éxito";
          }
          swal({
            text: msj,
            type: tipo_error
          })
        },
        error : function(xhr,errmsg,err) {
          swal({
            title: "Error",
            html: "Ocurrio un error intente nuevamente",
            type: "warning"
          });
          table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
        }
      });
    }).catch(() => {
      return false;
    });
  });

  $("#lista-capacitacion-validar").on('click', '.enviar-correo-mod', function() {
    const id = $(this).attr("data-id");
    const id_modulo = $(this).attr("data-modulo");
    var url = urlEnviaCertificadoCorreoMod.replace('999999999', id).replace('888888888', id_modulo)
    swal({
      title: "Importante",
      html: `Está seguro que desea enviar por correo los certificados del modulo seleccionado?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $(`#lista-capacitacion-validar .evm-${id_modulo}`).html("Enviando....");
      $.ajax({
        url : url,
        type : "GET",
        success : function(data) {
          table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
          if(data.errores.length){
            msj = `Error al enviar correo(s): \n ${data.errores}`;
            tipo_error = "warning";
            titulo = "Alerta";
          }else{
            msj = "Se realizó el envío de correo(s) exitosamente";
            tipo_error = "success";
            titulo = "Éxito";
          }
          swal({
            text: msj,
            type: tipo_error
          })
        },
        error : function(xhr,errmsg,err) {
          swal({
            title: "Error",
            html: "Ocurrio un error intente nuevamente",
            type: "warning"
          });
          table_lista_capacitacion.ajax.url(urlListarCapacitacionValidar).load();
        }
      });
    }).catch(() => {
      return false;
    });
  });

});