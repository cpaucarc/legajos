  function convierteMayuscula(valor){
    valor.inputmask({regex: "^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$", placeholder:''});
    valor.on("keypress", function () {
      valor=$(this);
      setTimeout(function () {
        valor.val(valor.val().toUpperCase());
     },50);
    });
  }
  convierteMayuscula($("#id_apellido_paterno"));
  convierteMayuscula($("#id_cargo"));
  convierteMayuscula($("#id_apellido_materno"));
  // convierteMayuscula($("#id_d-descripcion_cargo"));
  convierteMayuscula($("#id_nombres"));
  convierteMayuscula($("#id_u-nombre_grado"));
  convierteMayuscula($("#id_u-facultad"));
  convierteMayuscula($("#id_t-nombre_carrera"));
  convierteMayuscula($("#id_c-capacitacion_complementaria"));
  convierteMayuscula($("#id_titulo"));
  convierteMayuscula($("#id_sub_titulo"));
  convierteMayuscula($("#id_revista"));
  convierteMayuscula($("#formCientifica #id_descripcion"));
  convierteMayuscula($("#id_autor"));
  convierteMayuscula($("#id_distincion"));
  $("#id_resumen").inputmask({
    regex: "^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ()0123456789-]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ()0123456789-]+)*$", placeholder:''
  });
  $("#id_descripcion_cargo").inputmask({
    // regex: "^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$", placeholder:''
  });
  $("#formDistincion #id_descripcion").inputmask({
    regex: "^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+(?: [a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+)*$", placeholder:''
  });
  $("#id_celular").inputmask({
    regex: "^([0-9]{1,9})$"
  });
  $("#id_numero_documento").inputmask({
    regex: "^([0-9]{1,8})$"
  });
  $("#id_rango_paginas").inputmask({
    regex: "^([0-9]{1,5}[-][0-9]{1,5})$", placeholder:''
  });