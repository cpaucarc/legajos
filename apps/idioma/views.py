from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from apps.common.datatables_pagination import datatable_page
from apps.idioma.forms import IdiomaForm
from apps.idioma.models import Idioma
from apps.login.views import BaseLogin, ControlDocenteAdministrativo


class IdiomaCreateView(LoginRequiredMixin, BaseLogin, ControlDocenteAdministrativo, CreateView):
    template_name = 'idioma/crear.html'
    model = Idioma
    form_class = IdiomaForm
    msg = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'persona_id': self.persona.id
        })
        return context

    def form_valid(self, form):
        idioma = form.save(commit=False)
        idioma.creado_por = self.request.user.username
        idioma.persona = self.persona
        idioma.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Idioma creado con éxito')
        return reverse('idioma:crear_idioma', kwargs={'pk': self.persona.id})


class IdiomaUpdateView(LoginRequiredMixin, BaseLogin, UpdateView):
    template_name = 'idioma/crear.html'
    model = Idioma
    form_class = IdiomaForm

    def form_valid(self, form):
        idioma = form.save(commit=False)
        idioma.modificado_por = self.request.user.username
        idioma.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'persona_id': self.object.persona_id
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Idioma actualizada con éxito')
        return reverse('idioma:crear_idioma', kwargs={'pk': self.object.persona_id})


class ListaIdiomasView(LoginRequiredMixin, BaseLogin, View):
    def get(self, request, *args, **kwargs):
        search_param = self.request.GET.get('search[value]')
        filtro = self.request.GET.get('filtro')
        idiomas = Idioma.objects.none()
        if filtro:
            ''
        else:
            idiomas = Idioma.objects.filter(persona_id=self.kwargs.get('persona_id')).order_by('-fecha_modificacion')
        if len(search_param) > 3:
            idiomas = idiomas.filter(idioma__descripcion__icontains=search_param)
        draw, page = datatable_page(idiomas, request)
        lista_idiomas_data = []
        cont = 0
        for a in page.object_list:
            cont = cont + 1
            lista_idiomas_data.append([
                cont,
                '{}'.format(a.idioma),
                a.get_lectura_display(),
                a.get_conversacion_display(),
                a.get_escritura_display(),
                a.get_forma_aprendizaje_display(),
                'SI' if a.es_lengua_materna else 'NO',
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': idiomas.count(),
            'recordsFiltered': idiomas.count(),
            'data': lista_idiomas_data
        }
        return JsonResponse(data)

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminar-idioma" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        link = reverse('idioma:editar_idioma', kwargs={'pk': a.id})
        boton_editar = '<a class="btn btn-warning btn-sm" href="{0}"><i class="fa fa-edit"></i></a>'
        boton_editar = boton_editar.format(link)
        boton = '{0}'.format(boton_editar)
        return boton


class EliminarIdiomaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        idioma = get_object_or_404(Idioma, id=self.kwargs.get('pk'))
        idioma.delete()
        msg = f'Idioma eliminado correctamente'
        return Response({'msg': msg}, HTTP_200_OK)
