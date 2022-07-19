import os
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.common.constants import (TIPO_DOCUMENTO_DOCENTE, TIPO_DOCUMENTO_CHOICES, TIPO_DOCUMENTO_LABORAL,
                                   TIPO_DOCUMENTO_ASESOR_TESIS, TIPO_DOCUMENTO_EVALUADOR_PROYECTO)
from apps.common.datatables_pagination import datatable_page
from apps.experiencia.forms import LaboralForm, DocenteForm, AsesorTesisForm, EvaluadorProyectoForm
from apps.experiencia.models import (Laboral, AdjuntoLaboral, Docente, AdjuntoDocente, AsesorTesis, AdjuntoAsesorTesis,
                                     EvaluadorProyecto, AdjuntoEvaluadorProyecto)
from apps.login.views import BaseLogin, ControlDocenteAdministrativo
from apps.persona.models import Persona
from config import settings


class ExperienciaLaboralView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'experiencia/experiencia_laboral.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_laboral': LaboralForm(),
            'form_docente': DocenteForm(prefix='d'),
            'form_asesor': AsesorTesisForm(prefix='a'),
            'form_evaluador': EvaluadorProyectoForm(prefix='ep'),
            'tipo_persona_consultada': self.persona.tipo_persona,
        })
        return context


class EliminarLaboralView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        laboral = get_object_or_404(Laboral, id=self.kwargs.get('pk'))
        laboral.delete()
        msg = f'Registro eliminado correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class ListaLaboralView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        laboral = Laboral.objects.none()
        if id_persona:
            laboral = Laboral.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(laboral, request)
        lista_laboral_data = []
        for a in page.object_list:
            lista_laboral_data.append([
                '{}'.format(a.institucion),
                a.cargo,
                a.fecha_inicio or '-',
                a.fecha_fin or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': laboral.count(),
            'recordsFiltered': laboral.count(),
            'data': lista_laboral_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-laboral" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editarl" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_LABORAL)
        boton = '{0}'.format(boton)
        return boton


class GuardarLaboralView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_laboral = request.GET.get('laboral_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_laboral:
            laboral = get_object_or_404(Laboral, pk=id_laboral)
            form = LaboralForm(request.POST, instance=laboral)
            if form.is_valid():
                laboral = form.save(commit=False)
                laboral.modificado_por = self.request.user.username
                laboral.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = LaboralForm(request.POST)
            if form.is_valid():
                laboral = form.save(commit=False)
                laboral.persona = persona
                laboral.creado_por = self.request.user.username
                laboral.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ConsultaLaboralView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        laboral = get_object_or_404(Laboral, pk=kwargs.get('pk'))
        data = {
            'id': laboral.id,
            'cargo': laboral.cargo,
            'institucion': '{}'.format(laboral.institucion),
            'institucion_id': laboral.institucion.id,
            'fecha_inicio': laboral.fecha_inicio,
            'fecha_fin': laboral.fecha_fin,
            'trabaja_actualmente': laboral.trabaja_actualmente,
            'descripcion_cargo': laboral.descripcion_cargo
        }
        return JsonResponse(data)


class EliminarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tipo_documento = kwargs.get('tipo')
        if tipo_documento == TIPO_DOCUMENTO_LABORAL:
            laboral = get_object_or_404(AdjuntoLaboral, pk=kwargs.get('pk'))
            laboral.delete()
        elif tipo_documento == TIPO_DOCUMENTO_DOCENTE:
            docente = get_object_or_404(AdjuntoDocente, pk=kwargs.get('pk'))
            docente.delete()
        elif tipo_documento == TIPO_DOCUMENTO_ASESOR_TESIS:
            asesor_tesis = get_object_or_404(AdjuntoAsesorTesis, pk=kwargs.get('pk'))
            asesor_tesis.delete()
        elif tipo_documento == TIPO_DOCUMENTO_EVALUADOR_PROYECTO:
            evaluador_proyecto = get_object_or_404(AdjuntoEvaluadorProyecto, pk=kwargs.get('pk'))
            evaluador_proyecto.delete()
        return JsonResponse({'result': 'ok'})


class SubirArchivosView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carpeta = None
        modelo = None
        tipo_documento = kwargs.get('tipo')
        if tipo_documento == TIPO_DOCUMENTO_LABORAL:
            laboral = get_object_or_404(Laboral, pk=kwargs.get('pk'))
            carpeta = 'experiencia_laboral'
            modelo = AdjuntoLaboral()
            modelo.laboral = laboral
        elif tipo_documento == TIPO_DOCUMENTO_DOCENTE:
            docente = get_object_or_404(Docente, pk=kwargs.get('pk'))
            carpeta = 'experiencia_docente'
            modelo = AdjuntoDocente()
            modelo.docente = docente
        elif tipo_documento == TIPO_DOCUMENTO_ASESOR_TESIS:
            asesor_tesis = get_object_or_404(AsesorTesis, pk=kwargs.get('pk'))
            carpeta = 'experiencia_asesor_tesis'
            modelo = AdjuntoAsesorTesis()
            modelo.asesor_tesis = asesor_tesis
        elif tipo_documento == TIPO_DOCUMENTO_EVALUADOR_PROYECTO:
            evaluador_proyecto = get_object_or_404(EvaluadorProyecto, pk=kwargs.get('pk'))
            carpeta = 'experiencia_evaluador_proyecto'
            modelo = AdjuntoEvaluadorProyecto()
            modelo.evaluador_proyecto = evaluador_proyecto
        path = None
        if modelo:
            try:
                try:
                    os.mkdir(os.path.join(settings.MEDIA_ROOT, carpeta))
                except Exception:
                    pass
                ruta = request.FILES['file']
                extension = ruta.name.split(".")[-1]
                nombre_archivo = f"{uuid.uuid4()}.{extension}"
                archivo = default_storage.save('{}/{}'.format(carpeta, nombre_archivo), ruta.file)
                path = default_storage.path(archivo)
                modelo.nombre = ruta.name
                modelo.ruta = '{}/{}'.format(carpeta, nombre_archivo)
                modelo.save()
            except Exception:
                if path:
                    os.remove(path)
                return JsonResponse({'result': "Error de conexión, intente nuevamente"}, status=400)
        else:
            return JsonResponse({'result': "Error inesperado, intente nuevamente"}, status=400)
        return JsonResponse({'result': "ok"})


class ListaArchivosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tipo_documento = kwargs.get('tipo')
        adjuntos = None
        if kwargs.get('pk').isdigit() and dict(TIPO_DOCUMENTO_CHOICES).get(tipo_documento, None):
            if tipo_documento == TIPO_DOCUMENTO_DOCENTE:
                adjuntos = AdjuntoDocente.objects.filter(docente=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_LABORAL:
                adjuntos = AdjuntoLaboral.objects.filter(laboral=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_ASESOR_TESIS:
                adjuntos = AdjuntoAsesorTesis.objects.filter(asesor_tesis=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_EVALUADOR_PROYECTO:
                adjuntos = AdjuntoEvaluadorProyecto.objects.filter(evaluador_proyecto=kwargs.get('pk')).order_by('-id')
        if not adjuntos:
            adjuntos = AdjuntoLaboral.objects.none()
        draw, page = datatable_page(adjuntos, request)
        lista_adjuntos_data = []
        cont = 0
        for a in page.object_list:
            cont += 1
            lista_adjuntos_data.append([
                cont,
                a.nombre,
                '{} {}'.format(self.get_boton_descargar_archivo(a, tipo_documento),
                               self.get_boton_eliminar(a, tipo_documento)),
            ])
        data = {
            'draw': draw,
            'recordsTotal': adjuntos.count(),
            'recordsFiltered': adjuntos.count(),
            'data': lista_adjuntos_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a, tipo_documento):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminara" data-id={} data-tipo={}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id, tipo_documento)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_descargar_archivo(self, a, tipo_documento):
        boton_eliminar = '<a class="btn btn-info btn-sm " href={}><i class="fa fa-download"></i></a>'
        link = reverse("experiencia:descargar_archivo", kwargs={'pk': a.id, 'tipo': tipo_documento})
        boton_eliminar = boton_eliminar.format(link)
        boton = '{0}'.format(boton_eliminar)
        return boton


class DescargarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        tipo_documento = kwargs.get('tipo')
        adjunto = None
        if tipo_documento == TIPO_DOCUMENTO_LABORAL:
            adjunto = get_object_or_404(AdjuntoLaboral, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_DOCENTE:
            adjunto = get_object_or_404(AdjuntoDocente, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_ASESOR_TESIS:
            adjunto = get_object_or_404(AdjuntoAsesorTesis, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_EVALUADOR_PROYECTO:
            adjunto = get_object_or_404(AdjuntoEvaluadorProyecto, pk=pk)
        if adjunto:
            try:
                archivo = default_storage.open(adjunto.ruta)
                response = HttpResponse(archivo, content_type="application/x-www-form-urlencoded")
                response['Content-Disposition'] = 'inline; filename={}'.format(adjunto.nombre)
                return response
            except Exception:
                return JsonResponse({'result': "Error, intente nuevamente"})
        else:
            return JsonResponse({'result': "Error, intente nuevamente"})


class ListaDocenteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        docente = Docente.objects.none()
        if id_persona:
            docente = Docente.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(docente, request)
        lista_docente_data = []
        for a in page.object_list:
            lista_docente_data.append([
                '{}'.format(a.institucion),
                a.get_tipo_docente_display(),
                a.get_tipo_institucion_display() or '-',
                a.fecha_inicio,
                a.fecha_fin or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': docente.count(),
            'recordsFiltered': docente.count(),
            'data': lista_docente_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-docente" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editard" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_DOCENTE)
        boton = '{0}'.format(boton)
        return boton


class EliminarDocenteView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        docente = get_object_or_404(Docente, id=self.kwargs.get('pk'))
        docente.delete()
        msg = f'Registro eliminado correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class GuardarDocenteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_docente = request.GET.get('docente_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_docente:
            docente = get_object_or_404(Docente, pk=id_docente)
            form = DocenteForm(request.POST, instance=docente, prefix='d')
            if form.is_valid():
                docente = form.save(commit=False)
                docente.modificado_por = self.request.user.username
                docente.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = DocenteForm(request.POST, prefix='d')
            if form.is_valid():
                docente = form.save(commit=False)
                docente.persona = persona
                docente.creado_por = self.request.user.username
                docente.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ConsultaDocenteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        docente = get_object_or_404(Docente, pk=kwargs.get('pk'))
        data = {
            'id': docente.id,
            'institucion': '{}'.format(docente.institucion),
            'institucion_id': docente.institucion.id,
            'tipo_institucion': docente.tipo_institucion,
            'tipo_docente': docente.tipo_docente,
            'fecha_inicio': docente.fecha_inicio,
            'fecha_fin': docente.fecha_fin,
            'trabaja_actualmente': docente.trabaja_actualmente,
            'descripcion_cargo': docente.descripcion_cargo
        }
        return JsonResponse(data)


class ConsultaAsesorTesisView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        asesor = get_object_or_404(AsesorTesis, pk=kwargs.get('pk'))
        data = {
            'id': asesor.id,
            'universidad': '{}'.format(asesor.universidad),
            'universidad_id': asesor.universidad.id,
            'tesis': asesor.tesis,
            'tesista': asesor.tesista,
            'fecha_aceptacion_tesis': asesor.fecha_aceptacion_tesis,
            'enlace_fuente_repositorio_academico': asesor.enlace_fuente_repositorio_academico,
        }
        return JsonResponse(data)


class ConsultaEvaluadorProyectoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        evaluador_proyecto = get_object_or_404(EvaluadorProyecto, pk=kwargs.get('pk'))
        data = {
            'id': evaluador_proyecto.id,
            'anio': '{}'.format(evaluador_proyecto.anio),
            'pais': evaluador_proyecto.pais_id,
            'tipo_proyecto_formulado': evaluador_proyecto.tipo_proyecto_formulado,
            'experiencia': evaluador_proyecto.experiencia,
            'metodologia_evaluacion': evaluador_proyecto.metodologia_evaluacion,
            'entidad_financiadora': evaluador_proyecto.entidad_financiadora_id,
            'url_concurso': evaluador_proyecto.url_concurso,
            'nombre_concurso': evaluador_proyecto.nombre_concurso,
            'presupuesto_proyecto': evaluador_proyecto.presupuesto_proyecto,
        }
        return JsonResponse(data)


class ListaAsesorTesisView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        asesor = AsesorTesis.objects.none()
        if id_persona:
            asesor = AsesorTesis.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(asesor, request)
        lista_asesor_data = []
        for a in page.object_list:
            lista_asesor_data.append([
                '{}'.format(a.universidad),
                a.get_tesis_display(),
                a.tesista or '-',
                a.fecha_aceptacion_tesis,
                a.enlace_fuente_repositorio_academico or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': asesor.count(),
            'recordsFiltered': asesor.count(),
            'data': lista_asesor_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-asesor" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editara" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_ASESOR_TESIS)
        boton = '{0}'.format(boton)
        return boton


class EliminarAsesorView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        asesor = get_object_or_404(AsesorTesis, id=self.kwargs.get('pk'))
        asesor.delete()
        msg = f'Registro eliminado correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class ListaEvaluadorProyectoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        evaluador_proyecto = EvaluadorProyecto.objects.none()
        if id_persona:
            evaluador_proyecto = EvaluadorProyecto.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(evaluador_proyecto, request)
        lista_evaluador_data = []
        for a in page.object_list:
            lista_evaluador_data.append([
                '{}'.format(a.anio),
                a.get_experiencia_display(),
                a.get_tipo_proyecto_formulado_display() or '-',
                '{}'.format(a.entidad_financiadora) or '-',
                a.get_metodologia_evaluacion_display(),
                a.presupuesto_proyecto or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': evaluador_proyecto.count(),
            'recordsFiltered': evaluador_proyecto.count(),
            'data': lista_evaluador_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-evaluador" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editarep" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_EVALUADOR_PROYECTO)
        boton = '{0}'.format(boton)
        return boton


class EliminarEvaluadorView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        evaluador = get_object_or_404(EvaluadorProyecto, id=self.kwargs.get('pk'))
        evaluador.delete()
        msg = f'Registro eliminado correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class GuardarAsesorTesisView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_asesor = request.GET.get('asesor_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_asesor:
            asesor = get_object_or_404(AsesorTesis, pk=id_asesor)
            form = AsesorTesisForm(request.POST, instance=asesor, prefix='a')
            if form.is_valid():
                asesor = form.save(commit=False)
                asesor.modificado_por = self.request.user.username
                asesor.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = AsesorTesisForm(request.POST, prefix='a')
            if form.is_valid():
                asesor = form.save(commit=False)
                asesor.persona = persona
                asesor.creado_por = self.request.user.username
                asesor.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class GuardarEvaluadorProyectoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_evaluador = request.GET.get('evaluador_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_evaluador:
            evaluador = get_object_or_404(EvaluadorProyecto, pk=id_evaluador)
            form = EvaluadorProyectoForm(request.POST, instance=evaluador, prefix='ep')
            if form.is_valid():
                evaluador = form.save(commit=False)
                evaluador.modificado_por = self.request.user.username
                evaluador.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = EvaluadorProyectoForm(request.POST, prefix='ep')
            if form.is_valid():
                evaluador = form.save(commit=False)
                evaluador.persona = persona
                evaluador.creado_por = self.request.user.username
                evaluador.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
