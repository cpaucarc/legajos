$(document).ready(function () {
  $("#id_firmante").select2({width: '100%'});
  function buildSelect(data) {
    return data.map(function (elem) {
      return '<option value="' + elem.id + '">' + elem.nombre + '</option>';
    }).join('');
  }

  $("#id_ambito").on("click", function() {
    const ambito = $(this).val();
    $("#id_firmante").html("Consultando espere porfavor.....");
    $.getJSON(urlFirmanteAmbito + "?ambito="+ambito+"&id_facultad="+idFacultad, function (res) {
      $("#id_firmante").html(buildSelect(res.data));
    });
  });

  $("#asigna-firmante").on("click", function() {
    if($("#id_ambito").val()&&$("#id_firmante").val()&&$("#id_tipo_firma").val()){
      $.ajax({
        method: "POST",
        url: urlAsignarFirmante,
        data:  {
          'id_capacitacion': idCapacitacion,
          'id_firmante': $("#id_firmante").val(),
          'id_tipo_firma': $("#id_tipo_firma").val(),
          'csrfmiddlewaretoken': csrf_token
        },
        success: function(response){
          window.location.href = "/bandeja-asignar-firmante/"+idCapacitacion;
        },
        error: function(response){
            error = response.responseJSON["error"]
            info = response.responseJSON["info"]
            if(error){
                swal({
                    html: error,
                    type: "error"
                })
            }else{
                swal({
                    html: info,
                    type: "info"
                })
            }
        }
      });
    }else{
      swal({
          html: "Falta ingresar datos",
          type: "error"
      })
    }
  });

  $(".quitar-firmante").on("click", function() {
    const id = $(this).attr("data-id");
    swal({
      title: "Importante",
      text: `¿Está seguro que desea quitar la asignación del firmante?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $.get(urlQuitarResponsableFirma.replace("id", id), function(data) {
        window.location.href = "/bandeja-asignar-firmante/"+idCapacitacion;
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