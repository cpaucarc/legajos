$(document).ready(function () {
  if(tipPersona == "registrador"){
    $("#id_tipo_persona option[value='registrador']").remove();
    $("#id_tipo_persona option[value='autoridad']").remove();
  }
  $("#dgenerales").hide();
  $("#div_resumen").hide();
  var $valor = $('#id_numero_documento');
  var $tipoPersona = $('#id_tipo_persona');
  var $tipoBusqueda = $('#id_tipo_documento');
  var $btnLimpiar = $("#limpiar-dni");
  var $btnAsignarPersonal = $("#btn-asignar-personal");
  var $tipoPersonal = $("#id_tipo_personal");
  var $idDepartamento = $("#id_ubigeo_departamento");
  var $idProvincia = $("#id_ubigeo_provincia");
  var $idDistrito = $("#id_ubigeo_distrito");
  $("#id_profesion").select2({theme: 'bootstrap'});
  if($tipoPersona.val() === 'docente' || $tipoPersona.val() === 'administrativo'){
    $("#dgenerales").show();
    $("#div_resumen").show();
  }else{
    $("#dgenerales").hide();
    $("#div_resumen").hide();
  }

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

  var table_lista_persona = $("#lista-persona").DataTable({
    language: {
      "url":  datatablesES
    },
    ajax: urlListarPersona,
    searching: true,
    processing: true,
    serverSide: true,
    ordering: false,
  });

  if($tipoPersona.val() && $tipoPersona.val() === "docente"){
    $(".f-ext").show();
  }else{
    $(".f-ext").hide();
  }

  $tipoPersona.on("change", function () {
   var selectedOption = $(this).find('option:selected').val();
    if(selectedOption && selectedOption === "docente"){
      $(".f-ext").show();
    }else{
      $(".f-ext").hide();
      $("#id_facultad").val("");
      $("#id_departamento").val("");
    }
    if($(this).val() === 'docente' || $(this).val() === 'administrativo'){
      $("#dgenerales").show();
      $("#div_resumen").show();
    }else{
      $("#dgenerales").hide();
      $("#div_resumen").hide();
      $("#id_facultad").val("");
      $("#id_departamento").val("");
      $("#id_resumen").val("");
      $("#dgenerales input[type=text], #dgenerales select").val("");
    }
  });

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

  function buildSelect(data) {
    return data.map(function (elem) {
      return '<option value="' + elem.codigo + '">' + elem.nombre + '</option>';
    }).join('');
  }

  function buildSelect1(data) {
    return data.map(function (elem) {
      return '<option value="' + elem.id + '">' + elem.nombre + '</option>';
    }).join('');
  }

  $idDepartamento.click(function (e) {
    var selectedOption = $(this).find('option:selected').val();
    if (selectedOption.length) {
      var url = urls_ubigeo.provincias + '?dep_id=' + selectedOption;
      $.getJSON(url, function (res) {
        $idProvincia.html(buildSelect(res.data));
        $idProvincia.trigger('click');
      });
    }else{
      $idProvincia.find('option').remove();
      $idProvincia.val('');
      $idDistrito.find('option').remove();
      $idDistrito.val('');
    }
  });

  $idProvincia.click(function () {
    var departamento_id = $idDepartamento.find('option:selected').val();
    var selectedOption = $(this).find('option:selected').val();
    if (selectedOption) {
      var url = urls_ubigeo.distritos + '?dep_id='+ departamento_id + '&prov_id=' + selectedOption;
      $.getJSON(url, function (res) {
        $idDistrito.html(buildSelect(res.data));
      });
    }else{
      $idDistrito.find('option').remove();
      $idDistrito.val('');
    }
  });

  $("#id_facultad").change(function() {
    var selectedOption = $(this).find('option:selected').val();
    if (selectedOption.length) {
      var url = urlDepartamento + '?facultad_id=' + selectedOption;
      $.getJSON(url, function (res) {
        $("#id_departamento").html(buildSelect1(res.data));
      });
    }else{
      $("#id_departamento").find('option').remove();
      $("#id_departamento").val('');
    }
  });

});
