const form_colegiaturas = document.getElementById('colegiaturas-form')
const tbody_colegiaturas_agregados = document.getElementById('colegiaturas-agregados')

const colegio_profesional = document.getElementById('id_colegio_profesional')
const sede_colegio = document.getElementById('id_sede_colegio')
const codigo_colegiado = document.getElementById('id_codigo_colegiado')
const estado_colegiado = document.getElementById('id_estado_colegiado')

const btn_agregar_colegiatura = document.getElementById('agregar-colegiatura')

var colegiaturas = []

var table_colegiaturas = $("#tabla-colegiaturas").DataTable({
    language: {
        "url": datatablesES
    },
    ajax: urlListarColegiatura,
    searching: false,
    processing: true,
    serverSide: true,
    ordering: false,
});

table_colegiaturas.on("draw", function () {
    $("tbody tr").each(function () {
        $(this).find('td').eq(4).attr("align", 'center');
        $(this).find('td').eq(5).attr("align", 'center');
        $(this).find('td').eq(6).attr("align", 'center');
        $(this).find('td').eq(7).attr("align", 'center');
    });
})

form_colegiaturas.addEventListener('submit', function (e) {
    e.preventDefault();

    if (colegiaturas.length === 0) {
        swal({text: 'No hay ninguna colegiatura para guardar', type: "error"});
        return;
    }

    let colegios = ""
    let sedes = ""
    let codigos = ""
    let estados = ""

    colegiaturas.forEach(colegiatura => {
        colegios += colegiatura.colegio_id + '|||';
        sedes += colegiatura.sede + '|||';
        codigos += colegiatura.codigo + '|||';
        estados += colegiatura.estado + '|||';
    })

    let elements = document.getElementsByName('csrfmiddlewaretoken');
    csrf_token = elements[1].value;

    fetch(urlGuardarColegiatura
            .replace('11111', colegios.substring(0, colegios.length - 3))
            .replace('22222', sedes.substring(0, sedes.length - 3))
            .replace('33333', codigos.substring(0, codigos.length - 3))
            .replace('44444', estados.substring(0, estados.length - 3))
        , {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf_token
            }
        }).then(res => res.json())
        .then(res => {
            swal({text: res.msg, type: res.type})
            if (res.type === 'success') {
                colegiaturas = []
                table_colegiaturas.ajax.reload();
                $('#colegiaturaModal').modal('hide');
            }
        })
        .catch(error => swal({text: 'Se produjo un error:\n' + error, type: "error"}));
})


btn_agregar_colegiatura.addEventListener('click', () => {
    if (!validarEntrada())
        return;

    let colegiatura = {
        colegio_id: colegio_profesional.value,
        colegio: colegio_profesional.options[colegio_profesional.selectedIndex].text,
        sede: limpiarTexto(sede_colegio.value),
        codigo: limpiarTexto(codigo_colegiado.value).replaceAll(' ', ''),
        estado: estado_colegiado.value === 'True',
    }

    colegiaturas.push(colegiatura)

    limpiar();
    renderizarTabla();
})

function validarEntrada() {
    try {

        if (colegio_profesional.value.trim().length === 0 || parseInt(colegio_profesional.value) < 1) {
            swal({text: 'Selecciona un Colegio Profesional', type: "error"});
            colegio_profesional.focus();
            return false;
        }

        let existe = false;
        colegiaturas.forEach(cl => {
            if (cl.colegio_id === colegio_profesional.value) {
                existe = true;
            }
        })

        if (existe) {
            swal({
                text: `El Colegio Profesional ${colegio_profesional.options[colegio_profesional.selectedIndex].text} ya está agregado`,
                type: "error"
            });
            colegio_profesional.focus();
            return false;
        }

        if (sede_colegio.value.trim().length === 0) {
            swal({text: 'Ingresa el sede del Colegio Profesional', type: "error"});
            sede_colegio.focus();
            return false;
        }

        if (codigo_colegiado.value.trim().length === 0) {
            swal({text: 'Ingresa el código del Colegiado', type: "error"});
            codigo_colegiado.focus();
            return false;
        }

        if ( limpiarTexto(codigo_colegiado.value).replaceAll(' ', '').length > 15) {
            swal({text: `El Código del Colegiado debe contener menos de 15 caracteres, actualmente hay ${codigo_colegiado.value.length} caracteres`, type: "error"});
            codigo_colegiado.focus();
            return false;
        }

        if (!['True', 'False'].includes(estado_colegiado.value)) {
            swal({text: 'Selecciona el estado actual del colegiado', type: "error"});
            estado_colegiado.focus();
            return false;
        }

        return true;

    } catch (e) {
        console.log('error', e)
        return false;
    }
}

function renderizarTabla() {

    tbody_colegiaturas_agregados.innerHTML = '';

    colegiaturas.forEach((colg, id) => {
        let fila = document.createElement('tr');

        let col1 = document.createElement('td');
        col1.appendChild(document.createTextNode((id + 1).toString()));

        let col2 = document.createElement('td');
        col2.appendChild(document.createTextNode(colg.colegio));

        let col3 = document.createElement('td');
        col3.appendChild(document.createTextNode(colg.sede));

        let col4 = document.createElement('td');
        col4.appendChild(document.createTextNode(colg.codigo))

        let col5 = document.createElement('td');
        col5.appendChild(document.createTextNode(colg.estado ? 'Habilitado' : 'Inhabilitado'))

        let col6 = document.createElement('td');
        boton_eliminar = document.createElement('button');
        boton_eliminar.setAttribute('class', 'btn btn-danger btn-sm pull-right');
        boton_eliminar.setAttribute('type', 'button');
        boton_eliminar.setAttribute('onClick', `quitarColegiatura('${id}')`);
        boton_eliminar.innerHTML = 'Quitar';
        col6.appendChild(boton_eliminar);

        fila.appendChild(col1);
        fila.appendChild(col2);
        fila.appendChild(col3);
        fila.appendChild(col4);
        fila.appendChild(col5);
        fila.appendChild(col6);

        tbody_colegiaturas_agregados.appendChild(fila);
    })
}

function limpiar() {
    colegio_profesional.value = 0;
    sede_colegio.value = "";
    codigo_colegiado.value = "";
    estado_colegiado.value = "True";
}

function quitarColegiatura(id) {
    colegiaturas.splice(id, 1);
    renderizarTabla();
}

function limpiarTexto(texto){
    texto = texto.replaceAll('/', '');
    texto = texto.replaceAll('\\', '');
    texto = texto.replaceAll('"', '');
    texto = texto.replaceAll('&', '');
    texto = texto.replaceAll('\'', '');
    return texto;
}