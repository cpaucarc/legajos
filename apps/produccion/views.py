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

from apps.common.constants import (OBRA_CAPITULO_LIBRO, OBRA_LIBRO, TIPO_DOC_REVISION_PARES,
                                   TIPO_DOC_RESULTADO_INVESTIGACION)
from apps.common.datatables_pagination import datatable_page
from apps.login.views import BaseLogin, ControlDocenteAdministrativo
from apps.persona.models import Persona
from apps.produccion.forms import CientificaForm
from apps.produccion.models import Cientifica, AdjuntoCientifica


class CientificaView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'produccion/cientifica.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_cientifica': CientificaForm(),
        })
        return context


class GuardarCientificaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_cientifica = request.GET.get('cientifica_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_cientifica:
            cientifica = get_object_or_404(Cientifica, pk=id_cientifica)
            form = CientificaForm(request.POST, instance=cientifica)
            if form.is_valid():
                cientifica = form.save(commit=False)
                cientifica.modificado_por = self.request.user.username
                cientifica.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = CientificaForm(request.POST)
            if form.is_valid():
                cientifica = form.save(commit=False)
                cientifica.persona = persona
                cientifica.creado_por = self.request.user.username
                cientifica.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ListaCientificaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        cientifica = Cientifica.objects.none()
        if id_persona:
            cientifica = Cientifica.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(cientifica, request)
        lista_cientifica_data = []
        for a in page.object_list:
            lista_cientifica_data.append([
                a.get_tipo_obra_display(),
                a.titulo,
                a.autor,
                a.fecha_publicacion,
                a.revista,
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': cientifica.count(),
            'recordsFiltered': cientifica.count(),
            'data': lista_cientifica_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-cientifica" data-id={0}>
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
        boton = '''<button class="btn btn-info btn-sm archivosc" data-id={} data-tipo_obra={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id, a.tipo_obra)
        boton = '{0}'.format(boton)
        return boton


class EliminarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cientifica = get_object_or_404(AdjuntoCientifica, pk=kwargs.get('pk'))
        cientifica.delete()
        return JsonResponse({'result': 'ok'})


class SubirArchivosView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cientifica = get_object_or_404(Cientifica, pk=kwargs.get('pk'))
        tipo_doc_adjunto = self.request.POST.get('tipo_documento_adjunto')
        carpeta = 'produccion_cientifica'
        modelo = AdjuntoCientifica()
        modelo.cientifica = cientifica
        modelo.tipo_obra = cientifica.tipo_obra
        if cientifica.tipo_obra in (OBRA_LIBRO, OBRA_CAPITULO_LIBRO):
            if tipo_doc_adjunto in (TIPO_DOC_REVISION_PARES, TIPO_DOC_RESULTADO_INVESTIGACION):
                modelo.tipo_documento_adjunto = tipo_doc_adjunto
            else:
                return JsonResponse({'result': "Error de validación actualizar y reintentar"}, status=400)
        path = None
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
        return JsonResponse({'result': "ok"})


class ListaArchivosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        adjuntos = None
        if kwargs.get('pk').isdigit():
            adjuntos = AdjuntoCientifica.objects.filter(cientifica=kwargs.get('pk')).order_by('-id')
        if not adjuntos:
            adjuntos = AdjuntoCientifica.objects.none()
        draw, page = datatable_page(adjuntos, request)
        lista_adjuntos_data = []
        cont = 0
        for a in page.object_list:
            cont += 1
            lista_adjuntos_data.append([
                cont,
                a.nombre,
                '{} {}'.format(self.get_boton_descargar_archivo(a),
                               self.get_boton_eliminar(a)),
            ])
        data = {
            'draw': draw,
            'recordsTotal': adjuntos.count(),
            'recordsFiltered': adjuntos.count(),
            'data': lista_adjuntos_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminara" data-id={}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_descargar_archivo(self, a):
        boton_eliminar = '<a class="btn btn-info btn-sm " href={}><i class="fa fa-download"></i></a>'
        link = reverse("produccion:descargar_archivo", kwargs={'pk': a.id})
        boton_eliminar = boton_eliminar.format(link)
        boton = '{0}'.format(boton_eliminar)
        return boton


class DescargarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        adjunto = get_object_or_404(AdjuntoCientifica, pk=pk)
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


class ConsultaCientificaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cientifica = get_object_or_404(Cientifica, pk=kwargs.get('pk'))
        data = {
            'id': cientifica.id,
            'categoria_trabajo': cientifica.categoria_trabajo,
            'tipo_obra': cientifica.tipo_obra,
            'funcion': '{}'.format(cientifica.funcion),
            'titulo': cientifica.titulo,
            'sub_titulo': cientifica.sub_titulo,
            'revista': cientifica.revista,
            'volumen': cientifica.volumen,
            'fasciculo': cientifica.fasciculo,
            'rango_paginas': cientifica.rango_paginas,
            'fecha_publicacion': cientifica.fecha_publicacion,
            'tipo_cita': cientifica.tipo_cita,
            'cita': cientifica.cita,
            'descripcion': cientifica.descripcion,
            'orden_autoria': cientifica.orden_autoria,
            'autor': cientifica.autor,
            'pais_publicacion': '{}'.format(cientifica.pais_publicacion),
            'id_pais_publicacion': cientifica.pais_publicacion_id,
            'tipo_congreso': cientifica.tipo_congreso,
        }
        return JsonResponse(data)


class EliminarCientificaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        cientifica = get_object_or_404(Cientifica, id=self.kwargs.get('pk'))
        cientifica.delete()
        msg = f'Producción cientifica eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)
