const es_en_empresa = document.getElementById('es_en_empresa')
const div_datos_empresa = document.getElementById('datos_empresa')
const rsu_form = document.getElementById('rsu-form')

const titulo = document.getElementById('id_titulo')
const lugar = document.getElementById('id_lugar')
const descripcion = document.getElementById('id_descripcion')
const fecha_inicio = document.getElementById('id_fecha_inicio')
const fecha_fin = document.getElementById('id_fecha_fin')
const ruc = document.getElementById('id_ruc')
const empresa = document.getElementById('id_empresa')

function limpiarTexto(texto){
    texto = texto.replaceAll('/', '');
    texto = texto.replaceAll('\\', '');
    texto = texto.replaceAll('"', '');
    texto = texto.replaceAll('&', '');
    texto = texto.replaceAll('\'', '');
    return texto;
}

window.onload = function () {
    es_en_empresa.addEventListener('change', () => {
        div_datos_empresa.style.display = es_en_empresa.checked ? "block" : "none";
    })

    var table_rsu = $("#tabla-rsu").DataTable({
        language: {
            "url": datatablesES
        },
        ajax: urlListarRsu,
        searching: false,
        processing: true,
        serverSide: true,
        ordering: false,
    });

    table_rsu.on("draw", function () {
        $("tbody tr").each(function () {
            $(this).find('td').eq(4).attr("align", 'center');
            $(this).find('td').eq(5).attr("align", 'center');
            $(this).find('td').eq(6).attr("align", 'center');
            $(this).find('td').eq(7).attr("align", 'center');
            $(this).find('td').eq(8).attr("align", 'center');
            $(this).find('td').eq(9).attr("align", 'center');
        });
    })


    rsu_form.addEventListener('submit', function (event) {
        event.preventDefault();

        if (es_en_empresa.checked && (ruc.value.trim().length === 0 || empresa.value.trim().length === 0)) {
            swal({text: 'Es necesario completar los campos RUC y Nombre de Empres', type: "error"});
            ruc.focus();
            return;
        }

        let elements = document.getElementsByName('csrfmiddlewaretoken');
        csrf_token = elements[0].value;

        fetch(urlGuardarRsu
                .replace('1111', limpiarTexto(titulo.value.trim()))
                .replace('2222', limpiarTexto(lugar.value.trim()))
                .replace('3333', limpiarTexto(descripcion.value.trim()))
                .replace('4444', fecha_inicio.value)
                .replace('5555', fecha_fin.value)
                .replace('6666', es_en_empresa.checked)
                .replace('7777', ruc.value.trim().length > 0 ? ruc.value : 'none')
                .replace('8888', empresa.value.trim().length > 0 ? limpiarTexto(empresa.value) : 'none')
            , {
                method: 'POST', // or 'PUT'
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrf_token
                }
            }).then(res => res.json())
            .then(res => {
                console.log(res);
                swal({text: res.msg, type: res.type});
                if (res.type === 'success') {
                    table_rsu.ajax.reload();
                    $('#modalRsu').modal('hide');
                }
            })
            .catch(error => swal({text: 'Se produjo un error:\n' + error, type: "error"}));
    })
};
