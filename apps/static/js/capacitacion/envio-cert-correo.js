$("#list-capacitacion").on('click', '.enviar-correo-unico-miembro', function() {
  const id = $(this).attr("data-id");
  const miembro_id = $(this).attr("data-mi");
  const persona_id = $(this).attr("data-persona");
  const cargo = $(this).attr("data-cargo") ? $(this).attr("data-cargo") : '';
  swal({
    title: "Importante",
    html: `Está seguro que desea enviar por correo el certificado?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $(`#list-capacitacion .emv-${miembro_id}`).html("Enviando....");
    var url = urlEnviaCertCorreo.replace('999999999', id).replace('888888888', persona_id)
    $.ajax({
      url : `${url}?cargo=${cargo}`,
      type : "GET",
      success : function(data) {
        console.log(data)
      },
      error : function(xhr,errmsg,err) {
        swal({
          text: "Ocurrio un error intente nuevamente",
          type: "warning"
        });
      }
    })
  }).catch(() => {
    return false;
  });
});

$("#list-capacitacion").on('click', '.enviar-correo-unico', function() {
  const id = $(this).attr("data-id");
  const acta_id = $(this).attr("data-li");
  const persona_id = $(this).attr("data-persona");
  const cargo = $(this).attr("data-cargo") ? $(this).attr("data-cargo") : '';
  swal({
    title: "Importante",
    html: `Está seguro que desea enviar por correo el certificado?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $(`#list-capacitacion .elv-${acta_id}`).html("Enviando....");
    var url = urlEnviaCertCorreo.replace('999999999', id).replace('888888888', persona_id)
    $.ajax({
      url : `${url}?cargo=${cargo}`,
      type : "GET",
      success : function(data) {
        $(`#list-capacitacion .elv-${acta_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
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
          text: "Ocurrio un error intente nuevamente",
          type: "warning"
        });
        $(`#list-capacitacion .elv-${acta_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
      }
    })
  }).catch(() => {
    return false;
  });
});

$("#list-capacitacion").on('click', '.enviar-correo-por-mod-miembro', function() {
  const id = $(this).attr("data-id");
  const miembro_id = $(this).attr("data-mi");
  const persona_id = $(this).attr("data-persona");
  const modulo_id = $(this).attr("data-modulo");
  const cargo = $(this).attr("data-cargo") ? $(this).attr("data-cargo") : '';
  swal({
    title: "Importante",
    html: `Está seguro que desea enviar por correo el certificado?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $(`#list-capacitacion .emv-${miembro_id}`).html("Enviando....");
    var url = urlEnviaCertPorModCorreo.replace('999999999', id).replace('888888888', modulo_id).replace('777777777', persona_id)
    $.ajax({
      url : `${url}?cargo=${cargo}`,
      type : "GET",
      success : function(data) {
        $(`#list-capacitacion .emv-${miembro_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
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
          text: "Ocurrio un error intente nuevamente",
          type: "warning"
        });
        $(`#list-capacitacion .emv-${miembro_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
      }
    })
  }).catch(() => {
    return false;
  });
});

$("#list-capacitacion").on('click', '.enviar-correo-por-mod', function() {
  const id = $(this).attr("data-id");
  const acta_id = $(this).attr("data-li");
  const persona_id = $(this).attr("data-persona");
  const modulo_id = $(this).attr("data-modulo");
  const cargo = $(this).attr("data-cargo") ? $(this).attr("data-cargo") : '';
  swal({
    title: "Importante",
    html: `Está seguro que desea enviar por correo el certificado?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $(`#list-capacitacion .elv-${acta_id}`).html("Enviando....");
    var url = urlEnviaCertPorModCorreo.replace('999999999', id).replace('888888888', modulo_id).replace('777777777', persona_id)
    $.ajax({
      url : `${url}?cargo=${cargo}`,
      type : "GET",
      success : function(data) {
        $(`#list-capacitacion .elv-${acta_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
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
          text: "Ocurrio un error intente nuevamente",
          type: "warning"
        });
        $(`#list-capacitacion .elv-${acta_id}`).html("<i class='fa fa-envelope'>Enviar</i>");
      }
    })
  }).catch(() => {
    return false;
  });
});