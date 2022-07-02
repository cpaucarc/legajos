from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.common.models import Institucion
from apps.cursos.forms import CursosCrearForm
from apps.persona.models import Persona
from .models import CursoDictado, Semestre


# Registra multiples cursos para un docente.
def cursos_create_view(request, pk):
    mensaje = None
    # Si el docente quiere registrar sus cursos, envia la peticion POST
    if request.method == "POST":

        cant = int(request.POST['cantidad'])  # Cantidad de cursos

        escuela = request.POST['escuela'].upper()
        institucion_id = request.POST['institucion']
        persona_id = pk
        semestre_id = request.POST['semestre']

        cant_registrados = 0
        for i in range(1, cant + 1):
            curso = request.POST['curso-' + str(i)].upper()

            existe = CursoDictado.objects.filter(
                escuela=escuela, curso=curso, institucion_id=institucion_id,
                persona_id=persona_id, semestre_id=semestre_id,
            ).exists()

            if existe is False:
                CursoDictado.objects.create(
                    escuela=request.POST['escuela'].upper(),
                    curso=request.POST['curso-' + str(i)].upper(),
                    institucion_id=request.POST['institucion'],
                    persona_id=pk,
                    semestre_id=request.POST['semestre'],
                )
                cant_registrados += 1

        mensaje = "¡La información de los {} cursos fue registrado con éxito!".format(
            cant_registrados) if cant_registrados > 0 else None

    form = CursosCrearForm(None)
    cursos_registrados = CursoDictado.objects.filter(persona_id=pk).order_by("institucion_id", "semestre_id", "escuela",
                                                                             "curso")

    context = {
        'pk': pk,
        'cursos_registrados': cursos_registrados,
        'form': form,
        'mensaje': mensaje
    }
    return render(request, 'cursos/agregar_cursos.html', context)
