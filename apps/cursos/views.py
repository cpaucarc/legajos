from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.common.models import Institucion
from apps.cursos.forms import CursosCrearForm
from apps.persona.models import Persona
from .models import CursoDictado, Semestre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.login.views import BaseLogin, ControlDocenteAdministrativo
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from apps.common.datatables_pagination import datatable_page
from django.views import View


# Registra multiples cursos para un docente.
class CursosCreateView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'cursos/agregar_cursos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_cursos': CursosCrearForm(),
        })
        return context

class ListaCursosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        cursos = CursoDictado.objects.filter(persona_id=id_persona)
        draw, page = datatable_page(cursos, request)
        lista_cursos_data = []
        for curso in page.object_list:
            lista_cursos_data.append([
                curso.institucion.name,
                curso.escuela.upper(),
                curso.curso.upper(),
                curso.semestre.nombre,
            ])
        data = {
            'draw': draw,
            'recordsTotal': cursos.count(),
            'recordsFiltered': cursos.count(),
            'data': lista_cursos_data
        }
        return JsonResponse(data)

class CursosGuardarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))

        institucion_id = kwargs.get('inst_id')
        semestre_id = kwargs.get('sem_id')
        escuela = kwargs.get('esc')
        cursos = kwargs.get('cursos')
        cursos = cursos.split('|||')

        cant_registrados = 0
        for curso in cursos:
            existe = CursoDictado.objects.filter(
                escuela=escuela, curso=curso, institucion_id=institucion_id,
                persona=persona, semestre_id=semestre_id,
            ).exists()

            if existe is False:
                CursoDictado.objects.create(
                    escuela=escuela.upper(),
                    curso=curso.upper(),
                    institucion_id=institucion_id,
                    persona=persona,
                    semestre_id=semestre_id,
                )
                cant_registrados += 1
        mensaje = "¡Se registro {} cursos dictados con éxito!".format(cant_registrados)
        return JsonResponse({'msg': mensaje})
        # else:
        #     return JsonResponse({'error': f"{form.errors}"})

# @login_required
# def cursos_create_view(request, pk):
#     mensaje = None
#     # Si el docente quiere registrar sus cursos, envia la peticion POST
#     if request.method == "POST":
#
#         cant = int(request.POST['cantidad'])  # Cantidad de cursos
#
#         escuela = request.POST['escuela'].upper()
#         institucion_id = request.POST['institucion']
#         persona_id = pk
#         semestre_id = request.POST['semestre']
#
#         cant_registrados = 0
#         for i in range(1, cant + 1):
#             curso = request.POST['curso-' + str(i)].upper()
#
#             existe = CursoDictado.objects.filter(
#                 escuela=escuela, curso=curso, institucion_id=institucion_id,
#                 persona_id=persona_id, semestre_id=semestre_id,
#             ).exists()
#
#             if existe is False:
#                 CursoDictado.objects.create(
#                     escuela=request.POST['escuela'].upper(),
#                     curso=request.POST['curso-' + str(i)].upper(),
#                     institucion_id=request.POST['institucion'],
#                     persona_id=pk,
#                     semestre_id=request.POST['semestre'],
#                 )
#                 cant_registrados += 1
#
#         mensaje = "¡La información de los {} cursos fue registrado con éxito!".format(
#             cant_registrados) if cant_registrados > 0 else None
#
#     form = CursosCrearForm(None)
#     cursos_registrados = CursoDictado.objects.filter(persona_id=pk).order_by("institucion_id", "semestre_id", "escuela",
#                                                                              "curso")
#
#     context = {
#         'pk': pk,
#         'cursos_registrados': cursos_registrados,
#         'form': form,
#         'mensaje': mensaje
#     }
#     return render(request, 'cursos/agregar_cursos.html', context)
