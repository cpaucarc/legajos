import os
import uuid

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.common.constants import (TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA, TIPO_DOCUMENTO_CHOICES,
                                   TIPO_DOCUMENTO_FORMACION_TECNICA, TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA,
                                   TIPO_DOCUMENTO_FORMACION_MAESTRIA)
from apps.common.datatables_pagination import datatable_page
from apps.experiencia.forms import EvaluadorProyectoForm
from apps.formacion.forms import UniversitariaForm, TecnicoForm, ComplementariaForm, MaestriaForm
from apps.formacion.models import (Universitaria, AdjuntoUniversitaria, Tecnico, AdjuntoTecnico, Complementaria,
                                   AdjuntoComplementaria, Maestria, AdjuntoMaestria)
from apps.login.views import BaseLogin, ControlDocenteAdministrativo
from apps.persona.models import Persona


class FormacionAcademicaView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'formacion/formacion_academica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_universitaria': UniversitariaForm(prefix='u'),
            'form_tecnico': TecnicoForm(prefix='t'),
            'form_complementaria': ComplementariaForm(prefix='c'),
            'form_maestria': MaestriaForm(prefix='m'),
            'form_evaluador': EvaluadorProyectoForm(prefix='ep'),
        })
        return context


class GuardarUniversitariaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_universitaria = request.GET.get('universitaria_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_universitaria:
            universitaria = get_object_or_404(Universitaria, pk=id_universitaria)
            form = UniversitariaForm(request.POST, instance=universitaria, prefix='u')
            if form.is_valid():
                universitaria = form.save(commit=False)
                universitaria.modificado_por = self.request.user.username
                universitaria.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = UniversitariaForm(request.POST, prefix='u')
            if form.is_valid():
                universitaria = form.save(commit=False)
                universitaria.persona = persona
                universitaria.creado_por = self.request.user.username
                universitaria.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ListaUniversitariaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        universitaria = Universitaria.objects.none()
        if id_persona:
            universitaria = Universitaria.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(universitaria, request)
        lista_universitaria_data = []
        for a in page.object_list:
            lista_universitaria_data.append([
                '{}'.format(a.centro_estudios),
                a.get_grado_obtenido_display(),
                a.nombre_grado or '-',
                a.fecha_inicio or '-',
                a.fecha_fin or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': universitaria.count(),
            'recordsFiltered': universitaria.count(),
            'data': lista_universitaria_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-universitaria" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editaru" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA)
        boton = '{0}'.format(boton)
        return boton


class EliminarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tipo_documento = kwargs.get('tipo')
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA:
            universitaria = get_object_or_404(AdjuntoUniversitaria, pk=kwargs.get('pk'))
            universitaria.delete()
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_TECNICA:
            tecnico = get_object_or_404(AdjuntoTecnico, pk=kwargs.get('pk'))
            tecnico.delete()
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA:
            complementaria = get_object_or_404(AdjuntoComplementaria, pk=kwargs.get('pk'))
            complementaria.delete()
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_MAESTRIA:
            maestria = get_object_or_404(AdjuntoMaestria, pk=kwargs.get('pk'))
            maestria.delete()
        return JsonResponse({'result': 'ok'})


class SubirArchivosView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        carpeta = None
        modelo = None
        tipo_documento = kwargs.get('tipo')
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA:
            universitaria = get_object_or_404(Universitaria, pk=kwargs.get('pk'))
            carpeta = 'formacion_universitaria'
            modelo = AdjuntoUniversitaria()
            modelo.universitaria = universitaria
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_TECNICA:
            tecnico = get_object_or_404(Tecnico, pk=kwargs.get('pk'))
            carpeta = 'formacion_tecnica'
            modelo = AdjuntoTecnico()
            modelo.tecnico = tecnico
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA:
            complementaria = get_object_or_404(Complementaria, pk=kwargs.get('pk'))
            carpeta = 'formacion_complementaria'
            modelo = AdjuntoComplementaria()
            modelo.complementaria = complementaria
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_MAESTRIA:
            maestria = get_object_or_404(Maestria, pk=kwargs.get('pk'))
            carpeta = 'maestria'
            modelo = AdjuntoMaestria()
            modelo.maestria = maestria
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
            if tipo_documento == TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA:
                adjuntos = AdjuntoUniversitaria.objects.filter(universitaria=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_FORMACION_TECNICA:
                adjuntos = AdjuntoTecnico.objects.filter(tecnico=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA:
                adjuntos = AdjuntoComplementaria.objects.filter(complementaria=kwargs.get('pk')).order_by('-id')
            elif tipo_documento == TIPO_DOCUMENTO_FORMACION_MAESTRIA:
                adjuntos = AdjuntoMaestria.objects.filter(maestria=kwargs.get('pk')).order_by('-id')
        if not adjuntos:
            adjuntos = AdjuntoUniversitaria.objects.none()
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
        link = reverse("formacion:descargar_archivo", kwargs={'pk': a.id, 'tipo': tipo_documento})
        boton_eliminar = boton_eliminar.format(link)
        boton = '{0}'.format(boton_eliminar)
        return boton


class DescargarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        tipo_documento = kwargs.get('tipo')
        adjunto = None
        if tipo_documento == TIPO_DOCUMENTO_FORMACION_UNIVERSITARIA:
            adjunto = get_object_or_404(AdjuntoUniversitaria, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_TECNICA:
            adjunto = get_object_or_404(AdjuntoTecnico, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA:
            adjunto = get_object_or_404(AdjuntoComplementaria, pk=pk)
        elif tipo_documento == TIPO_DOCUMENTO_FORMACION_MAESTRIA:
            adjunto = get_object_or_404(AdjuntoMaestria, pk=pk)
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


class ConsultaUniversitariaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        universitaria = get_object_or_404(Universitaria, pk=kwargs.get('pk'))
        data = {
            'id': universitaria.id,
            'nombre_grado': universitaria.nombre_grado,
            'grado_obtenido': universitaria.grado_obtenido,
            'centro_estudios': '{}'.format(universitaria.centro_estudios),
            'centro_estudios_id': universitaria.centro_estudios_id,
            'facultad': universitaria.facultad,
            'fecha_inicio': universitaria.fecha_inicio,
            'fecha_fin': universitaria.fecha_fin,
            'pais_estudios': universitaria.pais_estudios_id,
        }
        return JsonResponse(data)


class GuardarTecnicoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_tecnico = request.GET.get('tecnico_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_tecnico:
            tecnico = get_object_or_404(Tecnico, pk=id_tecnico)
            form = TecnicoForm(request.POST, instance=tecnico, prefix='t')
            if form.is_valid():
                tecnico = form.save(commit=False)
                tecnico.modificado_por = self.request.user.username
                tecnico.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = TecnicoForm(request.POST, prefix='t')
            if form.is_valid():
                tecnico = form.save(commit=False)
                tecnico.persona = persona
                tecnico.creado_por = self.request.user.username
                tecnico.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ListaTecnicoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        tecnico = Tecnico.objects.none()
        if id_persona:
            tecnico = Tecnico.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(tecnico, request)
        lista_tecnico_data = []
        for a in page.object_list:
            lista_tecnico_data.append([
                '{}'.format(a.centro_estudios),
                a.nombre_carrera or '-',
                a.fecha_inicio or '-',
                a.fecha_fin or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': tecnico.count(),
            'recordsFiltered': tecnico.count(),
            'data': lista_tecnico_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-tecnico" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editart" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_FORMACION_TECNICA)
        boton = '{0}'.format(boton)
        return boton


class ConsultaTecnicoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tecnico = get_object_or_404(Tecnico, pk=kwargs.get('pk'))
        data = {
            'id': tecnico.id,
            'centro_estudios': '{}'.format(tecnico.centro_estudios),
            'centro_estudios_id': tecnico.centro_estudios_id,
            'nombre_carrera': tecnico.nombre_carrera,
            'fecha_inicio': tecnico.fecha_inicio,
            'fecha_fin': tecnico.fecha_fin,
        }
        return JsonResponse(data)


class GuardarComplementariaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_complementaria = request.GET.get('complementaria_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_complementaria:
            complementaria = get_object_or_404(Complementaria, pk=id_complementaria)
            form = ComplementariaForm(request.POST, instance=complementaria, prefix='c')
            if form.is_valid():
                complementaria = form.save(commit=False)
                complementaria.modificado_por = self.request.user.username
                complementaria.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = ComplementariaForm(request.POST, prefix='c')
            if form.is_valid():
                complementaria = form.save(commit=False)
                complementaria.persona = persona
                complementaria.creado_por = self.request.user.username
                complementaria.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ListaComplementariaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        complementaria = Complementaria.objects.none()
        if id_persona:
            complementaria = Complementaria.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(complementaria, request)
        lista_complementaria_data = []
        for a in page.object_list:
            lista_complementaria_data.append([
                a.capacitacion_complementaria,
                '{}'.format(a.centro_estudios),
                '{}'.format(a.pais_estudios),
                a.get_frecuencia_display() or '-',
                a.cantidad or '-',
                a.fecha_inicio or '-',
                a.fecha_fin or '-',
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': complementaria.count(),
            'recordsFiltered': complementaria.count(),
            'data': lista_complementaria_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-complementaria" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        boton = '''<button class="btn btn-warning btn-sm carga-editarc" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, a):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, TIPO_DOCUMENTO_FORMACION_COMPLEMENTARIA)
        boton = '{0}'.format(boton)
        return boton


class ConsultaComplementariaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        complementaria = get_object_or_404(Complementaria, pk=kwargs.get('pk'))
        data = {
            'id': complementaria.id,
            'capacitacion_complementaria': '{}'.format(complementaria.capacitacion_complementaria),
            'centro_estudios_id': complementaria.centro_estudios_id,
            'pais_estudios_id': complementaria.pais_estudios_id,
            'centro_estudios': '{}'.format(complementaria.centro_estudios),
            'frecuencia': complementaria.frecuencia,
            'cantidad': complementaria.cantidad,
            'fecha_inicio': complementaria.fecha_inicio,
            'fecha_fin': complementaria.fecha_fin,
        }
        return JsonResponse(data)


class EliminarComplementariaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        complementaria = get_object_or_404(Complementaria, id=self.kwargs.get('pk'))
        complementaria.delete()
        msg = f'Formación complementaria eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class EliminarTecnicoView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        tecnico = get_object_or_404(Tecnico, id=self.kwargs.get('pk'))
        tecnico.delete()
        msg = f'Formación técnica eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class EliminarUniversitariaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        universitaria = get_object_or_404(Universitaria, id=self.kwargs.get('pk'))
        universitaria.delete()
        msg = f'Formación universitaria eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)


class ListaMaestriaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        maestria = Maestria.objects.none()
        if id_persona:
            maestria = Maestria.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(maestria, request)
        lista_maestria_data = []
        for mst in page.object_list:
            lista_maestria_data.append([
                mst.denominacion,
                '{}'.format(mst.centro_estudios),
                '{}'.format(mst.pais_estudios),
                mst.get_modalidad_display() or '-',
                "{} meses".format(mst.duracion) or '-',
                mst.fecha_inicio or '-',
                mst.fecha_fin or '-',
                self.get_boton_archivos(mst),
                self.get_boton_editar(mst),
                self.get_boton_eliminar(mst),
            ])
        data = {
            'draw': draw,
            'recordsTotal': maestria.count(),
            'recordsFiltered': maestria.count(),
            'data': lista_maestria_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, mst):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-maestria" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(mst.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, mst):
        boton = '''<button class="btn btn-warning btn-sm carga-editar-maestria" data-id={}>
                        <i class="fa fa-edit"></i></a></button>'''
        boton = boton.format(mst.id)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_archivos(self, mst):
        boton = '''<button class="btn btn-info btn-sm archivose" data-id={} data-tipo={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(mst.id, TIPO_DOCUMENTO_FORMACION_MAESTRIA)
        boton = '{0}'.format(boton)
        return boton


class ConsultaMaestriaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        maestria = get_object_or_404(Maestria, pk=kwargs.get('pk'))
        data = {
            'id': maestria.id,
            'denominacion': '{}'.format(maestria.denominacion),
            'centro_estudios_id': maestria.centro_estudios_id,
            'pais_estudios_id': maestria.pais_estudios_id,
            'centro_estudios': '{}'.format(maestria.centro_estudios),
            'modalidad': maestria.modalidad,
            'duracion': maestria.duracion,
            'fecha_inicio': maestria.fecha_inicio,
            'fecha_fin': maestria.fecha_fin,
        }
        return JsonResponse(data)


class GuardarMaestriaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_maestria = request.GET.get('maestria_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_maestria:
            maestria = get_object_or_404(Maestria, pk=id_maestria)
            form = MaestriaForm(request.POST, instance=maestria, prefix='m')
            if form.is_valid():
                maestria = form.save(commit=False)
                maestria.modificado_por = self.request.user.username
                maestria.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = MaestriaForm(request.POST, prefix='m')
            if form.is_valid():
                maestria = form.save(commit=False)
                maestria.persona = persona
                maestria.creado_por = self.request.user.username
                maestria.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class EliminarMaestriaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        maestria = get_object_or_404(Maestria, id=self.kwargs.get('pk'))
        maestria.delete()
        msg = f'Maestría eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)