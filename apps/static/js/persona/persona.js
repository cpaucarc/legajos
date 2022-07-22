$(document).ready(function () {
    $("#id_colegio_profesional_select").select2({width: '100%'});
    $("#id_estado_colegiado_select").select2({width: '100%'});
    var $colegioProfesionalSelect = $("#id_colegio_profesional_select");
    var $sedeColegioInput = $("#id_sede_colegio_input");
    var $codigoColegiadoInput = $("#id_codigo_colegiado_input");
    var $estadoColegiadoSelect = $("#id_estado_colegiado_select");

    //ocultar en el formset los forms con el check eliminar
    $("#formset-parent tr").each(function () {
        var estado = $(this).closest("tr").find('input[type="checkbox"]').is(':checked');
        if (estado) {
            $(this).closest('tr').hide();
        }
    });

    $("#btn-agregar-colegiatura").on("click", function () {
        addToFormset(
            "#formset-parent", "#formset-empty", "colegiatura_set",
            function (node) {
                var colegio_profesional = $colegioProfesionalSelect.select2("data")[0];
                var estado_colegiado = $estadoColegiadoSelect.select2("data")[0];

                var sede_colegio = $sedeColegioInput.val();
                var codigo_colegiado = $codigoColegiadoInput.val();

                node.find(".colegio-profesional-id").val(colegio_profesional.id);
                node.find(".colegio-profesional-persona").val(colegio_profesional.text);
                node.find(".sede-colegio-id").val(sede_colegio);
                node.find(".sede-colegio-persona").val(sede_colegio);
                node.find(".codigo-colegiado-id").val(codigo_colegiado);
                node.find(".codigo-colegiado-persona").val(codigo_colegiado);
                node.find(".estado-colegiado-id").val(estado_colegiado.id);
                node.find(".estado-colegiado-persona").val(estado_colegiado.text);

                $(".form-colegiatura .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
            }
        );
    });

    $(".form-colegiatura .form-check > label").html(`<i class='fa fa-trash elimina-formset'></i>`);
    $(".form-colegiatura").on('click', '.elimina-formset', function () {
        $(this).prop("checked", false);
        $(this).closest('tr').hide();
    });

    if (tipPersona == "registrador") {
        $("#id_tipo_persona option[value='registrador']").remove();
        $("#id_tipo_persona option[value='autoridad']").remove();
    }
    $("#dgenerales").hide();
    $("#dcolegiatura").hide();
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
    if ($tipoPersona.val() === 'docente' || $tipoPersona.val() === 'administrativo') {
        $("#dgenerales").show();
        $("#div_resumen").show();
        if ($tipoPersona.val() === 'docente') {
            $("#dcolegiatura").show();
        }
    } else {
        $("#dgenerales").hide();
        $("#div_resumen").hide();
        $("#dcolegiatura").hide();
    }

    $btnLimpiar.click(function () {
        window.location = urlCrearPersonal
    });

    $tipoBusqueda.on('change', function () {
        var selectedOption = $(this).find('option:selected').val();
        verificarTipoDocumento(selectedOption);
    });

    verificarTipoDocumento($tipoBusqueda.val());
    $valor.keyup(function () {
        this.value = this.value.toUpperCase();
    });

    function verificarTipoDocumento(tipoDocumento) {
        if (tipoDocumento === '01') { //dni
            $valor.inputmask({regex: "^([0-9]{1,8})$", placeholder: ""});
        } else if (tipoDocumento === '03') { //carnet extranjeria
            $valor.inputmask({regex: "^([0-9]{1,9})$", placeholder: ""});
        } else if (tipoDocumento === '02') {//pasaporte
            $valor.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder: ""});
        } else if (tipoDocumento === '04') {//cedula de identidad
            $valor.inputmask({regex: "^([0-9A-Za-z]{1,12})$", placeholder: ""});
        } else if (tipoDocumento === '05') {//carnet de solicitante
            $valor.inputmask({regex: "^([0-9-]{5,11})$", placeholder: ""});
        } else if (tipoDocumento === '00') {//sin documento
            $valor.inputmask({regex: "^([0-9A-Za-z-]{1,12})$", placeholder: ""});
        }
    }

    var table_lista_persona = $("#lista-persona").DataTable({
        language: {
            "url": datatablesES
        },
        ajax: urlListarPersona,
        searching: true,
        processing: true,
        serverSide: true,
        ordering: false,
    });

    if ($tipoPersona.val() && $tipoPersona.val() === "docente") {
        $(".f-ext").show();
    } else {
        $(".f-ext").hide();
    }

    $tipoPersona.on("change", function () {
        var selectedOption = $(this).find('option:selected').val();
        if (selectedOption && selectedOption === "docente") {
            $(".f-ext").show();
        } else {
            $(".f-ext").hide();
            $("#id_facultad").val("");
            $("#id_departamento").val("");
        }
        if ($(this).val() === 'docente' || $(this).val() === 'administrativo') {
            $("#dgenerales").show();
            $("#div_resumen").show();
            if ($(this).val() === 'docente') {
                $("#dcolegiatura").show();
            }
        } else {
            $("#dgenerales").hide();
            $("#dcolegiatura").hide();
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
                "required": function () {
                    return $("#id_tipo_persona").val() == "docente";
                }
            },
            'facultad': {
                "required": function () {
                    return $("#id_tipo_persona").val() == "docente";
                }
            }
        }
    });

    $("#lista-persona").on("click", ".eliminarc", function () {
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
        }).then(function () {
            $.get(eliminarPersona.replace("id", id), function (data) {
                tipoMsg = data["tipo_msg"] ? 'warning' : 'success';
                swal({
                    text: data["msg"],
                    type: tipoMsg
                }).then(function () {
                    if (!data["tipo_msg"]) {
                        window.location.href = "/";
                    }
                });
            }).fail(function (error) {
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
        } else {
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
            var url = urls_ubigeo.distritos + '?dep_id=' + departamento_id + '&prov_id=' + selectedOption;
            $.getJSON(url, function (res) {
                $idDistrito.html(buildSelect(res.data));
            });
        } else {
            $idDistrito.find('option').remove();
            $idDistrito.val('');
        }
    });

    $("#id_facultad").change(function () {
        var selectedOption = $(this).find('option:selected').val();
        if (selectedOption.length) {
            var url = urlDepartamento + '?facultad_id=' + selectedOption;
            $.getJSON(url, function (res) {
                $("#id_departamento").html(buildSelect1(res.data));
            });
        } else {
            $("#id_departamento").find('option').remove();
            $("#id_departamento").val('');
        }
    });

    // Bloquear algunos inputs si esta en la ruta de editar
    if (window.location.pathname.startsWith("/editar-persona/")) {
        $('#id_tipo_documento').prop('readonly', true);
        $('#id_numero_documento').prop('readonly', true);
        $('#id_apellido_paterno').prop('readonly', true);
        $('#id_apellido_materno').prop('readonly', true);
        $('#id_nombres').prop('readonly', true);
    }

});
