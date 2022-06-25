$(document).ready(function () {
  const $btnBuscarCiudadano = $(".btn-buscar-ciudadano");
  var $tipoBusqueda = $('#id_tipo_documento');
  const $numeroDoc = $("#id_numero_documento");
  const $tipoDoc = $("#id_tipo_documento");
  const $apellidoNombre = $("#id_apellido_nombre");
  const $btnLimpiarForm = $(".btn-limpiar-form");
  const $btnResetPass = $(".btn-reset-pass");
  const $btnSaveUser = $("#save-user-info");
  const $unidadEjecutora = $("#id_unidad_ejecutora");
  const $diresa = $("#id_diresa");
  const $puntoVacunacion = $("#id_punto_vacunacion");
  const $perfiles = $("#id_perfiles");
  const $formUser = $("#form-user");
  $perfiles.select2({width: '100%'});
  $unidadEjecutora.select2({width: '100%'});
  $diresa.select2({width: '100%'});
  $puntoVacunacion.select2({width: '100%'});
  verificarTipoDocumento($tipoDoc.val());
  $tipoDoc.on('change', function () {
    var selectedOption = $(this).find('option:selected').val();
    verificarTipoDocumento(selectedOption);
  });

  verificarTipoDocumento($tipoDoc.val());
  function verificarTipoDocumento(tipoDocumento) {
    if (tipoDocumento === '01'){ //dni
      $numeroDoc.mask("00000000");
    }
    else if (tipoDocumento === '03'){ //carnet extranjeria
      $numeroDoc.mask("000000000");
    }
    else if (tipoDocumento === '02'){//pasaporte
      $numeroDoc.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder:""});
    }
    else if (tipoDocumento === '04'){//cedula de identidad
      $numeroDoc.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder:""});
    }
    else if (tipoDocumento === '05'){//carnet de solicitante
      $numeroDoc.inputmask({regex: "^([0-9-]{5,11})$", placeholder:""});
    }
    else if (tipoDocumento === '00'){//sin documento
      $numeroDoc.inputmask({regex: "^([0-9A-Za-z-]{1,12})$", placeholder:""});
    }
  }

  function buildSelect(data) {
    return data.map(function (elem) {
      return '<option value="' + elem.id + '">' + elem.nombre + '</option>';
    }).join('');
  }

  function getSorted(selector, attrName) {
    return $($(selector).toArray().sort(function(a, b){
      var aVal = parseInt(a.getAttribute(attrName)), bVal = parseInt(b.getAttribute(attrName));
      return aVal - bVal;
    }));
  }

  $btnLimpiarForm.on("click", function () {
    limpiarFormUser();
  });

  function initToogleButton(){
    $('.col_estado_user').bootstrapToggle();
    $('.toggle').on("click", function (e) {
      e.stopPropagation();
      const $checkbox = $(this).find("input[type='checkbox']");
      if ($checkbox.prop("checked")) {
        swal({
          title: "Importante",
          text: "¿Está seguro que desea inactivar al usuario?",
          type: "question",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "<i class='fa fa-check'></i> SI",
          cancelButtonText: "<i class='fa fa-times'></i> NO"
        }).then(function () {
          const url = $checkbox.data('url')
          .replace(/__estado__/, 0)
          $.get(url, function(){
            $checkbox.bootstrapToggle("off");
            tblUsuarios.ajax.url(`${urls["listarUsuarios"]}?format=json`).load();
          });
        }).catch(() => {
          return;
        });
      } else {
        swal({
          title: "Importante",
          type: "question",
          text: "¿Desea continuar con la activación del usuario?",
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "<i class='fa fa-check'></i> SI",
          cancelButtonText: "<i class='fa fa-times'></i> NO"
        }).then(function () {
          const url = $checkbox.data('url')
          .replace(/__estado__/, 1)
          $.get(url, function(){
            $checkbox.bootstrapToggle("on");
          });
        }).catch(() => {
          return;
        });
      }
    })
  }

  $("#form-user").validate({
    rules: {
      'numero_documento': "required",
      'perfil': "required",
      'tipo_documento': "required",
      'punto_vacunacion': {'required': false},
      'unidad_ejecutora': {'required': false},
      'diresa': {'required': false},
    },
    submitHandler: function(form) {
      if($formUser.find("#user_id").val()){
        actualizarUsuario();
      }else{
        crearUsuario();
      }
    },
    errorPlacement: function(error, element) {
      if(element.parent().hasClass("perfil")){
        error.insertAfter(element.siblings(":last"))
      }else{
        error.insertAfter(element);
      }
    }
  })

})
