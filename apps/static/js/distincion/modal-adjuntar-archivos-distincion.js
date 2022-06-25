var table_archivos = $("#tabla-archivos").DataTable({
  language: {
    "url":  datatablesES
  },
  ajax: urlListaArchivos,
  searching: false,
  processing: true,
  serverSide: true,
  ordering: false,
  lengthMenu: [[5, 10, 15], [5, 10, 15]]
});

table_archivos.on("draw", function(){
  $("tbody tr").each(function(){
    $(this).find('td').eq(2).attr("align",'center');
  });
})

$("#btnCerrarHeaderModalArchivos").click(function(){
  $("#modal-archivos").modal("hide");
});

$("#btnCerrarModalArchivos").click(function(){
  $("#modal-archivos").modal("hide");
});

$(document).on('click', '.archivosd', function(e) {
  $("#cargando-archivos").hide();
  var id = $(this).attr('data-id');
  $("#modal-archivos").modal('show');
  $("#myDropzone").attr('action', urlSubirArchivos.replace('id', id));
  table_archivos.ajax.url(urlListaArchivos.replace('id', id)).load();
});

Dropzone.options.myDropzone = {
    autoProcessQueue : false,
    addRemoveLinks: true,
    timeout:false,
    parallelUploads: 4,
    maxFilesize: 500,
    maxFiles: 4,
    acceptedFiles: ".jpg,.jpeg,.png,.pdf,.txt,.docx,.xlsx,.zip",
    init: function() {
      this.on("processing", function(file) {
        this.options.url = $("#myDropzone").attr("action");
      });
      this.on("success", function(file, responseText) {
        $("#cargando-archivos").hide();
        table_archivos.ajax.reload();
      });
      this.on('error', function(file, errorMessage) {
        $("#cargando-archivos").hide();
        var errorDisplay = document.querySelectorAll('[data-dz-errormessage]');
        errorDisplay[errorDisplay.length - 1].innerHTML = 'Error en cargar el documento';
      });
      this.on("complete", function (file) {
        $("#cargando-archivos").hide();
        this.removeFile(file);
        if (this.getUploadingFiles().length === 0 && this.getQueuedFiles().length === 0) {
          $("#btnCerrarHeaderModalArchivos").removeClass("inactiveLink");
          $("#subir-archivos").removeClass("inactiveLink");
          $("#btnCerrarModalArchivos").removeClass("inactiveLink");
          swal({
            text: "Se subieron correctamente los archivos seleccionados",
            type: 'success'
          })
        }else{
            Dropzone.forElement("#myDropzone").processQueue();
        }
      });
    }
};

Dropzone.prototype.defaultOptions.dictDefaultMessage = "Arrastra los archivos aquí para subirlos";
Dropzone.prototype.defaultOptions.dictCancelUpload = "Cancelar carga";
Dropzone.prototype.defaultOptions.dictCancelUploadConfirmation = "¿Está seguro que desea cancelar la carga actual?";
Dropzone.prototype.defaultOptions.dictRemoveFile = "Quitar Archivo";
Dropzone.prototype.defaultOptions.dictRemoveFile = "Quitar Archivo";

$("#subir-archivos").on( "click", function() {
var filess = Dropzone.forElement("#myDropzone").files
var conta = 0;
for(var i=0;i<filess.length;i++){if(filess[i].status == 'queued'){conta++;}}
if(Dropzone.forElement("#myDropzone").files.length > 0 && conta > 0){
   swal({
    title: "Importante",
    text: `¿Está seguro que desea subir los archivos seleccionados?`,
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $("#btnCerrarHeaderModalArchivos").addClass("inactiveLink");
    $("#subir").addClass("inactiveLink");
    $("#btnCerrarModalArchivos").addClass("inactiveLink");
    $("#cargando-archivos").show();
    Dropzone.forElement("#myDropzone").processQueue();
  }).catch(() => {
      return;
    });
 }else{
  swal({text:"Seleccione un archivo como mínimo", type: "warning"});
  $("#cargando-archivos").hide();
  $("#btnCerrarModalArchivos").removeClass("InactiveLink");
  $("#subir-archivos").removeClass("InactiveLink");
 }
});

$(document).on('click', '.eliminara', function(e) {
  var id = $(this).attr('data-id');
  var tipo = $(this).attr('data-tipo');
  swal({
    title: "Importante",
    text: `¿Está seguro que desea eliminar el documento?`,
    type: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa fa-check'></i> SI",
    cancelButtonText: "<i class='fa fa-times'></i> NO"
  }).then(function() {
    $.ajax({
      url : urlEliminarArchivo.replace('id', id),
      type : "GET",
      success : function(data) {
        table_archivos.ajax.reload();
        swal({
          text: "Se eliminó correctamente",
          type: 'success'
        })
      },
      error : function(xhr,errmsg,err) {
        swal({
          title: "Error",
          html: "Ocurrio un error intente nuevamente",
          type: "warning"
        });
      }
    });
  }).catch(() => {
    return;
  });
});