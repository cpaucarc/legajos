const cursos_form = document.getElementById("cursos-form");

const select_institucion = document.getElementById("id_institucion");
const select_semestre = document.getElementById("id_semestre");
const input_pk = document.getElementById("input-pk");
const input_curso = document.getElementById("input-curso");
const input_escuela = document.getElementById("id_escuela");
const input_cantidad = document.getElementById("input-cantidad");

const btn_agregar_curso = document.getElementById("btn-agregar-curso");
const btn_guardar_cursos = document.getElementById("btn-guardar-cursos");

const error_message = document.getElementById('error-message');
const cursos_agregados = document.getElementById('cursos-agregados');

const cursos_inputs = document.getElementById('cursos-inputs');
var cursos = [];

btn_guardar_cursos.onclick = (e) => {
    if (cursos.length === 0) {
        error_message.innerText = '• No has registrado ningún curso dictado';
        input_curso.focus();
        e.preventDefault();
    }
}

btn_agregar_curso.onclick = (e) => {
    e.preventDefault();
    let nuevo_curso = input_curso.value;
    nuevo_curso = nuevo_curso.substring(0, 99).toUpperCase();

    if (nuevo_curso.length === 0) {
        error_message.innerText = '• Ingrese el nombre del curso dictado';
        input_curso.focus();
        return;
    }

    if (agregarCurso(nuevo_curso)) {
        crearFilas();
    }
    input_curso.focus();
};

function agregarCurso(curso) {
    if (cursos.includes(curso)) {
        error_message.innerText = `• ¡El curso ${curso} ya fue registrado como dictado este semestre!`;
        input_curso.focus();
        return;
    }
    input_curso.value = '';
    input_curso.focus();
    error_message.innerText = ``;
    cursos.push(curso);
    console.log('Cursos', cursos)
    return true;
}

function eliminarCurso(curso) {
    cursos = cursos.filter(function (value) {
        return value !== curso;
    });
    console.log('Eliminado: ', curso, cursos);
    crearFilas();
}

function crearFilas() {

    cursos_agregados.innerHTML = '';
    cursos_inputs.innerHTML = '';

    ind = 1
    cursos.forEach(curso => {
        fila = document.createElement('tr');

        columna1 = document.createElement('td');
        texto1 = document.createTextNode(ind);
        columna1.appendChild(texto1);

        columna2 = document.createElement('td');
        texto2 = document.createTextNode(curso);
        columna2.appendChild(texto2);

        columna3 = document.createElement('td');
        boton_eliminar = document.createElement('button');
        boton_eliminar.setAttribute('class', 'btn btn-danger btn-sm pull-right');
        boton_eliminar.setAttribute('type', 'button');
        boton_eliminar.setAttribute('onClick', `eliminarCurso('${curso}')`);
        boton_eliminar.innerHTML = 'Quitar curso';
        columna3.appendChild(boton_eliminar);

        fila.appendChild(columna1);
        fila.appendChild(columna2);
        fila.appendChild(columna3);

        cursos_agregados.appendChild(fila);


        input = document.createElement('input');
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', `curso-${ind}`)
        input.value = curso;
        ind += 1
        cursos_inputs.appendChild(input);
    });
    input_cantidad.value = (ind - 1);
}

var table_cursos = $("#tabla-cursos").DataTable({
    language: {
        "url": datatablesES
    },
    ajax: urlListarCursos,
    searching: false,
    processing: true,
    serverSide: true,
    ordering: false,
});

table_cursos.on("draw", function () {
    $("tbody tr").each(function () {
        $(this).find('td').eq(4).attr("align", 'center');
        $(this).find('td').eq(5).attr("align", 'center');
        $(this).find('td').eq(6).attr("align", 'center');
        $(this).find('td').eq(7).attr("align", 'center');
    });
})

cursos_form.addEventListener('submit', function (event) { // 1
    event.preventDefault();

    let data = new FormData();
    data.append("institucion_id", select_institucion.value)
    data.append("semestre_id", select_semestre.value)
    data.append("escuela", input_escuela.value.trim())
    data.append("cursos", cursos)
    data.append("cantidad", cursos.length)

    let elements = document.getElementsByName('csrfmiddlewaretoken');
    csrf_token = elements[0].value;

    fetch(urlGuardarCursos.replace('11111', select_institucion.value)
            .replace('22222', select_semestre.value)
            .replace('33333', input_escuela.value.trim())
            .replace('44444', cursos.join('|||'))
        , {
            method: 'POST', // or 'PUT'
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrf_token
            }
        }).then(res => res.json())
        .then(res => {
            swal({text: res.msg, type: "success"})
            cursos = []
            table_cursos.ajax.reload();
            $('#exampleModal').modal('hide');
        })
        .catch(error => swal({text: 'Se produjo un error:\n' + error, type: "error"}));
})