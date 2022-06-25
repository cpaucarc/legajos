var table_idiomas = $("#lista-idiomas").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListarIdiomas,
  searching: true,
  processing: true,
  serverSide: true,
  ordering: false,
});

$(document).on('click', '.eliminar-idioma', function(e) {
  const id = $(this).attr("data-id");
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar el idioma seleccionado?`,
    type: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.get(urlEliminarIdioma.replace("pk", id), function(data) {
    table_idiomas.ajax.reload();
      swal({
        text: data["msg"],
        type: 'success'
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