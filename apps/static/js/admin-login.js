$("#user_form>p"). css("display", "none");
$("#id_persona").select2({width: '100%'});
$("#id_persona").select2({
  placeholder: 'Escriba el número de documento de la persona',
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
  width: '50%',
  height: '20%',
  minimumInputLength: 8,
  allowClear: true
});
