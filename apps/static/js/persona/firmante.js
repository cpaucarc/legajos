$(document).ready(function () {
  var $valor = $('#id_numero_documento');
  var $tipoBusqueda = $('#id_tipo_documento');
  var $btnLimpiar = $("#limpiar-dni");
  var $btnAsignarPersonal = $("#btn-asignar-personal");
  var $tipoPersonal = $("#id_tipo_personal");
  var $idPersona = $("#id_persona");
  $("#id_profesion").select2({theme: 'bootstrap'});
  //$idPersona.select2({theme: 'bootstrap'});
  $btnLimpiar.click(function () {
    window.location = urlCrearPersonal
  });
  $tipoBusqueda.on('change', function () {
    var selectedOption = $(this).find('option:selected').val();
    verificarTipoDocumento(selectedOption);
  });
   verificarTipoDocumento($tipoBusqueda.val());
  $valor.keyup(function() {
    this.value = this.value.toUpperCase();
  });
  function verificarTipoDocumento(tipoDocumento) {
    if (tipoDocumento === '01'){ //dni
      $valor.inputmask({regex: "^([0-9]{1,8})$", placeholder:""});
    }
    else if (tipoDocumento === '03'){ //carnet extranjeria
      $valor.inputmask({regex: "^([0-9]{1,9})$", placeholder:""});
    }
    else if (tipoDocumento === '02'){//pasaporte
      $valor.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder:""});
    }
    else if (tipoDocumento === '04'){//cedula de identidad
      $valor.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder:""});
    }
    else if (tipoDocumento === '05'){//carnet de solicitante
      $valor.inputmask({regex: "^([0-9-]{5,11})$", placeholder:""});
    }
    else if (tipoDocumento === '00'){//sin documento
      $valor.inputmask({regex: "^([0-9A-Za-z-]{1,12})$", placeholder:""});
    }
  }

  var table_lista_firmante = $("#lista-firmante").DataTable({
    language: {
      "url":  datatablesES
    },
    ajax: urlListarFirmante,
    searching: true,
    processing: true,
    serverSide: true,
    ordering: false,
  });

  if(ambitoFirmante === "facultad"){
    $("#div_id_facultad").show();
  }else{
    $("#div_id_facultad").hide();
  }

  $("#id_ambito").on("change", function () {
   var selectedOption = $(this).find('option:selected').val();
    if(selectedOption && selectedOption === "unasam"){
      $("#div_id_facultad").hide();
    }else{
    $("#div_id_facultad").show();
    }
  });

  $idPersona.select2({
    placeholder: 'Escriba el número de documento del firmante',
    ajax: {
      url: buscarPersonaUrl,
      dataType: 'json',
      delay: 250,
      data: function (params) {
        return {
          q: params.term, // search term
          page: params.page
        };
      },
      processResults: function (data, params) {
        params.page = params.page || 1;
        return {
          results: data,
          pagination: {
            more: (params.page * 30) < data.total_count
          }
        };
      },
      cache: true
    },
    theme: "bootstrap",
    minimumInputLength: 8,
    allowClear: true
  });

  $("form").validate({
    rules: {
      'facultad': {
          "required": function(){
              return $("#id_ambito").val() == "facultad";
          }
      }
    }
  });

  $("#lista-firmante").on("click", ".eliminarc", function() {
    const id = $(this).attr("data-id");
    swal({
      title: "Importante",
      text: `¿Está seguro que desea eliminar al firmante seleccionado?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $.get(eliminarFirmante.replace("id", id), function(data) {
        tipoMsg = data["tipo_msg"] ? 'warning': 'success';
        swal({
          text: data["msg"],
          type: tipoMsg
        }).then(function() {
          if (!data["tipo_msg"]){
            window.location.href = "/crear-firmante";
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

  function buildSelect(data) {
    return data.map(function (elem) {
      return '<option value="' + elem.id + '">' + elem.nombre + '</option>';
    }).join('');
  }

  $("#ver_firma_cargado").on('click', function() {
    //const archivo_paquete = $(this).attr("data-archivo");
   //var url = urlProyectoDescargaPdf.replace('archivo', archivo_paquete)
    //$("#iframe-proyecto-pdf").attr("src", url);
    $("#modal-firma-pdf").modal("show");
  });

});
