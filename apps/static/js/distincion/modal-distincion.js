$(document).ready(function () {
    $("#agrega-distincion").on("click", function () {
        $(".add-item-distincion").html("Agregar");
        $("#modal-distincion .modal-title").html("Nueva distinción o premio");
        $("#formularioDistincion")[0].reset();
        $("#errores_list").html("");
        $("#id_dist").val("");
        $('#modal-distincion').modal('show');
    });

    $("#btnCerrarHeaderModalDistincion").click(function () {
        $("#modal-distincion").modal("hide");
    });

    $("#btnCerrarModalDistincion").click(function () {
        $("#modal-distincion").modal("hide");
    });

});

var table_distincion = $("#tabla-distincion").DataTable({
    language: {
        "url": datatablesES
    },
    ajax: urlListaDistincion,
    searching: false,
    processing: true,
    serverSide: true,
    ordering: false,
});

table_distincion.on("draw", function () {
    $("tbody tr").each(function () {
        $(this).find('td').eq(4).attr("align", 'center');
        $(this).find('td').eq(5).attr("align", 'center');
        $(this).find('td').eq(6).attr("align", 'center');
        $(this).find('td').eq(7).attr("align", 'center');
    });
})

$(document).on('click', '.carga-editaru', function (e) {
    $form = $("#formularioDistincion");
    $form [0].reset();
    $form.valid()
    $("#errores_list").html("");
    var id = $(this).attr('data-id');
    cargarBlock();
    $.ajax({
        url: urlConsultaDistincion.replace('id', id),
        type: "GET",
        success: function (data) {
            cerrarBlock();
            $("#id_dist").val(data.id);
            $("#id_institucion").val(data.id_institucion);
            $("#id_distincion").val(data.distincion);
            $("#id_descripcion").val(data.descripcion);
            $("#id_pais").val(data.id_pais);
            $("#id_web_referencia").val(data.web_referencia);
            $("#id_fecha").val(data.fecha);
            $('#modal-distincion').modal('show');
            $(".add-item-distincion").html("Editar");
            $("#modal-distincion .modal-title").html("Editar distinción o premio");
        },
        error: function (xhr, errmsg, err) {
            cerrarBlock();
            swal({
                title: "Error",
                html: "Ocurrio un error intente nuevamente",
                type: "warning"
            });
        }
    });
});

$(document).on('click', 'a.add-item-distincion', function (e) {
    $form = $("#formularioDistincion");
    if ($form.valid()) {
        cargarBlock();
        var id_distincion = $("#id_dist").val() ? $("#id_dist").val() : '';
        $.ajax({
            method: "POST",
            url: `${urlGuardarDistincion}?distincion_id=${id_distincion}`,
            data: $form.serialize(),
            success: function (response) {
                if (response["error"]) {
                    $("#errores_list").html(`<div class="alert alert-warning">${response["error"]}</div>`).find("ul").addClass("errorlista");
                }
                if (response['msg']) {
                    table_distincion.ajax.reload();
                    swal({
                        text: response['msg'],
                        type: "success"
                    })
                    $("#modal-distincion").modal("hide");
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

$(document).on('click', '.eliminar-distincion', function (e) {
    const id = $(this).attr("data-id");
    swal({
        title: "Importante",
        text: `¿Está seguro que desea eliminar la distinción o premio seleccionada?`,
        type: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "<i class='fa fa-check'></i> SI",
        cancelButtonText: "<i class='fa fa-times'></i> NO"
    }).then(function () {
        $.get(urlEliminarDistincion.replace("id", id), function (data) {
            table_distincion.ajax.reload();
            swal({
                text: data["msg"],
                type: 'success'
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

$("#div_cita").hide();
$("#div_tipo_congreso").hide();
$("#id_categoria_trabajo").on('change', function () {
    var selectedOption = $(this).find('option:selected').val();
    $("#div_tipo_congreso").hide();
    $("#div_cita").hide();
    if (selectedOption == "otro") {
        $("#div_cita").show();
    } else if (selectedOption == "conferencia") {
        $("#div_tipo_congreso").show();
    }
});
