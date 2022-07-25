from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.common.models import Institucion
from apps.cursos.forms import CursosCrearForm, RsuCrearForm
from apps.persona.models import Persona
from .models import CursoDictado, Semestre, ResponsabilidadSocial
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

class RsuCreateView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'cursos/agregar_rsu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_rsu': RsuCrearForm(),
        })
        return context

class ListaRsuView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        rsus = ResponsabilidadSocial.objects.filter(persona_id=kwargs.get('pk'))
        draw, page = datatable_page(rsus, request)
        lista_rsus_data = []
        for rsu in page.object_list:
            lista_rsus_data.append([
                rsu.titulo,
                rsu.fecha_inicio,
                rsu.fecha_fin,
                rsu.lugar,
                rsu.ruc,
                rsu.empresa,
            ])
        data = {
            'draw': draw,
            'recordsTotal': rsus.count(),
            'recordsFiltered': rsus.count(),
            'data': lista_rsus_data
        }
        return JsonResponse(data)

class RsuGuardarView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            persona = get_object_or_404(Persona, pk=kwargs.get('pk'))

            titulo = kwargs.get('titulo')
            lugar = kwargs.get('lugar')
            descripcion = kwargs.get('descripcion')
            inicio = kwargs.get('inicio')
            fin = kwargs.get('fin')
            ruc = kwargs.get('ruc')
            empresa = kwargs.get('empresa')
            en_empresa = kwargs.get('en_empresa')

            if en_empresa == 'true' and ruc:
                ruc = ruc.replace(' ', '')

                if ruc.isalpha():
                    return JsonResponse({'msg': 'El número de RUC solo debe contener digitos numericos', 'type': 'error'})

                if len(ruc) != 11:
                    return JsonResponse({'msg': 'El número de RUC debe contener 11 digitos', 'type': 'error'})

                if ruc.startswith('20') is False:
                    return JsonResponse({'msg': 'El número de RUC debe iniciar con 20', 'type': 'error'})
            else:
                ruc = None
                empresa = None

            ResponsabilidadSocial.objects.create(
                titulo=titulo,
                lugar=lugar,
                descripcion=descripcion,
                fecha_inicio=inicio,
                fecha_fin=fin,
                ruc=ruc,
                empresa=empresa,
                persona=persona
            )
            return JsonResponse({'msg': '¡La responsabilidad social fue registrado con éxito!', 'type': 'success'})
        except Exception as e:
            return JsonResponse({'error': f"{e}", 'type': 'error'})