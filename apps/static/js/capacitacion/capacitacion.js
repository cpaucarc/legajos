$(document).ready(function () {
  $("#id_cargo_select").select2({width: '100%'});
  $("#id_persona_select").select2({width: '100%'});
  var $btnAgregarFirmante = $("#btn-agregar-firmante");
  var $cargoSelect = $("#id_cargo_select");

  //ocultar en el formset los forms con el check eliminar
  $("#formset-parent tr").each(function(){
    var estado = $(this).closest("tr").find('input[type="checkbox"]').is(':checked');
    if (estado){
      $(this).closest('tr').hide();
    }
  });

  $("#formset-parent1 tr").each(function(){
    var estado = $(this).closest("tr").find('input[type="checkbox"]').is(':checked');
    if (estado){
      $(this).closest('tr').hide();
    }
  });

  $('#id_persona_select').select2({
    placeholder: 'Escriba el número de documento del miembro',
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

  $("#btn-agregar").on("click", function () {
    addToFormset(
      "#formset-parent", "#formset-empty", "modulo_set",
      function (node) {
        var persona = $personaSelect.select2("data")[0];
        var cargo = $cargoSelect.select2("data")[0];
        node.find(".persona-id").val(persona.id);
        node.find(".cargo-id").val(cargo.id);
        node.find(".cargo-firmante").val(cargo.text);
        node.find(".persona-firmante").val(persona.text);
        $personaSelect.val("").trigger("change");
        $(".form-firmante .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
      }
    );
  });

  $("#btn-agregar-miembro").on("click", function () {
    addToFormset(
      "#formset-parent1", "#formset-empty1", "equipoproyecto_set",
      function (node) {
        var persona = $("#id_persona_select").select2("data")[0];
        var cargo = $("#id_cargo_select").select2("data")[0];
        node.find(".persona-id").val(persona.id);
        node.find(".cargo-id").val(cargo.id);
        node.find(".cargo-equipo").val(cargo.text);
        node.find(".persona-equipo").val(persona.text);
        $("#id_persona_select").val("").trigger("change");
        $(".form-equipo .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
      }
    );
  });

  var table_lista_capacitacion = $("#lista-capacitacion").DataTable({
    language: {
      "url":  datatablesES
    },
    ajax: urlListarCapacitacion,
    searching: true,
    processing: true,
    serverSide: true,
    ordering: false,
  });

  $("#ver_pdf_cargado").on('click', function() {
    const archivo_paquete = $(this).attr("data-archivo");
    var url = urlProyectoDescargaPdf.replace('archivo', archivo_paquete)
    $("#iframe-proyecto-pdf").attr("src", url);
    $("#modal-proyecto-pdf").modal("show");
    $("#modal-proyecto-pdf").modal("show");
  });

  $("#lista-capacitacion").on('click', '#ver_archivo_pdf', function() {
    const archivo_paquete = $(this).attr("data-archivo");
    var archivo =  archivo_paquete.replace('proyectos/', '');
    var url = urlProyectoDescargaPdf.replace('archivo', archivo).replace('.pdf', '')
    $("#iframe-proyecto-pdf").attr("src", url);
    $("#modal-proyecto-pdf").modal("show");
    $("#modal-proyecto-pdf").modal("show");
  });

  $("#lista-capacitacion").on("click", ".eliminarc", function() {
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

  $(".form-firmante .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
  $(".form-firmante").on('click', '.elimina-formset', function() {
    //$(this).prop("checked", false);
   $(this).closest('tr').hide();
  });

  $(".form-equipo .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
  $(".form-equipo").on('click', '.elimina-formset', function() {
    //$(this).prop("checked", false);
   $(this).closest('tr').hide();
  });

  $btnAgregarFirmante.on("click", function () {
    var cont = 0
    var carg = 0
    $("#formset-parent tr").each(function(){
      var estado = $(this).closest("tr").find('input[type="checkbox"]').is(':checked');
      var firmante = $(this).closest("tr").find('td').eq(1).find('input[type=text]').val();
      var cargo = $(this).closest("tr").find('td').eq(0).find('input[type=text]').val();
      if (!estado && $personaSelect.find(":selected").text() === firmante){
        cont++;
      }else if (!estado && $cargoSelect.find(":selected").text() === cargo){
        carg++;
      }
    });
    if ($personaSelect.val() && $cargoSelect.val() && cont == 0 && carg == 0) {
      addToFormset(
        "#formset-parent", "#formset-empty", "responsablefirma_set",
        function (node) {
          var persona = $personaSelect.select2("data")[0];
          var cargo = $cargoSelect.select2("data")[0];
          node.find(".persona-id").val(persona.id);
          node.find(".cargo-id").val(cargo.id);
          node.find(".cargo-firmante").val(cargo.text);
          node.find(".persona-firmante").val(persona.text);
          $personaSelect.val("").trigger("change");
          $(".form-firmante .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
        }
      );
    }else{
      if(cont > 0){
        swal({
          type: 'warning',
          html: 'Ya existe el firmante seleccionado'
        });
      }else if (carg > 0){
        swal({
          type: 'warning',
          html: 'Ya existe el Cargo seleccionado'
        });
      }
    }
  });

  $("#lista-capacitacion").on("click", ".parevision", function() {
    const id = $(this).attr("data-id");
    swal({
      title: "Importante",
      text: `¿Está seguro que desea enviar el registro para revisión?`,
      type: "question",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "<i class='fa fa-check'></i> SI",
      cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function() {
      $.get(urlEnviaParaRevision.replace("id", id), function(data) {
        tipoMsg = data["tipo_msg"] ? 'warning': 'success';
        swal({
          text: data["msg"],
          type: tipoMsg
        }).then(function() {
          if (!data["tipo_msg"]){
            window.location.href = "/capacitacion";
          }
        });
      }).fail(function(error) {
        swal({
          text: "Ocurrio un error al cambiar el estado, intente nuevamente",
          type: "error"
        });
      });
    }).catch(() => {
      return;
    });
  });

});
