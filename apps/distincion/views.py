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

from apps.common.datatables_pagination import datatable_page
from apps.distincion.forms import DistincionForm
from apps.distincion.models import Distincion, AdjuntoDistincion
from apps.login.views import BaseLogin, ControlDocenteAdministrativo
from apps.persona.models import Persona


class DistincionView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, TemplateView):
    template_name = 'distincion/distincion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_distincion': DistincionForm(),
        })
        return context


class GuardarDistincionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id_distincion = request.GET.get('distincion_id')
        persona = get_object_or_404(Persona, pk=kwargs.get('pk'))
        if id_distincion:
            distincion = get_object_or_404(Distincion, pk=id_distincion)
            form = DistincionForm(request.POST, instance=distincion)
            if form.is_valid():
                distincion = form.save(commit=False)
                distincion.modificado_por = self.request.user.username
                distincion.save()
                response = JsonResponse({'msg': 'Se realizó la actualización correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})
        else:
            form = DistincionForm(request.POST)
            if form.is_valid():
                distincion = form.save(commit=False)
                distincion.persona = persona
                distincion.creado_por = self.request.user.username
                distincion.save()
                response = JsonResponse({'msg': 'Se realizó el registro correctamente'})
                return response
            else:
                return JsonResponse({'error': f"{form.errors}"})


class ListaDistincionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_persona = kwargs.get('pk')
        distincion = Distincion.objects.none()
        if id_persona:
            distincion = Distincion.objects.filter(persona_id=id_persona).order_by('-id')
        draw, page = datatable_page(distincion, request)
        lista_distincion_data = []
        for a in page.object_list:
            lista_distincion_data.append([
                a.distincion,
                a.descripcion,
                '{}'.format(a.institucion),
                a.fecha,
                self.get_boton_archivos(a),
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': distincion.count(),
            'recordsFiltered': distincion.count(),
            'data': lista_distincion_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-distincion" data-id={0}>
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
        boton = '''<button class="btn btn-info btn-sm archivosd" data-id={}>
                    <i class="fa fa-eye"></i></a></button>'''
        boton = boton.format(a.id)
        boton = '{0}'.format(boton)
        return boton


class EliminarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        distincion = get_object_or_404(AdjuntoDistincion, pk=kwargs.get('pk'))
        distincion.delete()
        return JsonResponse({'result': 'ok'})


class SubirArchivosView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        distincion = get_object_or_404(Distincion, pk=kwargs.get('pk'))
        carpeta = 'distincion'
        modelo = AdjuntoDistincion()
        modelo.distincion = distincion
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
            print("\n\nDefault Storage", default_storage)
            print("Archivo", archivo)
            print("Ruta Name", ruta.name)
            print("Default Storage Path2", default_storage.path(archivo), '\n\n')
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
            adjuntos = AdjuntoDistincion.objects.filter(distincion=kwargs.get('pk')).order_by('-id')
        if not adjuntos:
            adjuntos = AdjuntoDistincion.objects.none()
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
        link = reverse("distincion:descargar_archivo", kwargs={'pk': a.id})
        boton_eliminar = boton_eliminar.format(link)
        boton = '{0}'.format(boton_eliminar)
        return boton


class DescargarArchivoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        adjunto = get_object_or_404(AdjuntoDistincion, pk=pk)
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


class ConsultaDistincionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        distincion = get_object_or_404(Distincion, pk=kwargs.get('pk'))
        data = {
            'id': distincion.id,
            'id_institucion': distincion.institucion_id,
            'distincion': distincion.distincion,
            'descripcion': distincion.descripcion,
            'id_pais': distincion.pais_id,
            'web_referencia': distincion.web_referencia,
            'fecha': distincion.fecha,
        }
        return JsonResponse(data)


class EliminarDistincionView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        distincion = get_object_or_404(Distincion, id=self.kwargs.get('pk'))
        distincion.delete()
        msg = f'Distincion o premio eliminada correctamente'
        return Response({'msg': msg}, HTTP_200_OK)
