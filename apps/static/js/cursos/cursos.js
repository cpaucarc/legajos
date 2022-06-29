const cursos_form = document.getElementById("cursos-form");

const select_institucion = document.getElementById("select-institucion");
const select_semestre = document.getElementById("select-semestre");
const input_pk = document.getElementById("input-pk");
const input_curso = document.getElementById("input-curso");
const input_escuela = document.getElementById("input-escuela");
const input_cantidad = document.getElementById("input-cantidad");

const btn_agregar_curso = document.getElementById("btn-agregar-curso");
const btn_guardar_cursos = document.getElementById("btn-guardar-cursos");

const error_message = document.getElementById('error-message');
const cursos_agregados = document.getElementById('cursos-agregados');

const cursos_inputs = document.getElementById('cursos-inputs');
var cursos = [];

// cursos_form.addEventListener('submit', function(event) { // 1
//   event.preventDefault()
  
//   let data = new FormData(); // 2
  
//   data.append("escuela", input_escuela.value.trim())  
//   data.append("cursos", cursos)
  
// console.log('FormData', data.get('escuela'), data.get('cursos'));

  
//   let elements = document.getElementsByName('csrfmiddlewaretoken');
//   csrf_token = elements[0].value;

//    fetch(urlRegistrarCursos, {
//       method: 'POST', // or 'PUT'
//       body: data, // data can be `string` or {object}!
//           headers:{
//             'Content-Type': 'application/json',
//             "X-CSRFToken": csrf_token
//           }
//     }).then(res => res.text())
//     .then(res => console.log("Form Submitted\n", res))
//     .catch(error => console.error('Error:', error));
    
// })

btn_guardar_cursos.onclick = (e) => {  
  if (cursos.length === 0){
    error_message.innerText = '• No has registrado ningún curso dictado';
    input_curso.focus();
    e.preventDefault();
  }
}

btn_agregar_curso.onclick = (e) => {
  e.preventDefault();
  let nuevo_curso = input_curso.value;
  nuevo_curso = nuevo_curso.substring(0,99).toUpperCase();

  if (nuevo_curso.length === 0) {
    error_message.innerText = '• Ingrese el nombre del curso dictado';
    input_curso.focus();
    return;
  }

  if (agregarCurso(nuevo_curso)){crearFilas();}
  input_curso.focus();
};

function agregarCurso(curso) {
  if (cursos.includes(curso)){
    error_message.innerText = `• ¡El curso ${curso} ya fue registrado como dictado este semestre!`;
    input_curso.focus();
    return;
  }
  input_curso.value = '';
  input_curso.focus();
  error_message.innerText = ``;
  cursos.push(curso);
  return true;
}

function eliminarCurso(curso){
  cursos = cursos.filter(function(value){ 
    return value !== curso;
  });
  console.log('Eliminado: ', curso, cursos);
  crearFilas();
}

function crearFilas(){

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
