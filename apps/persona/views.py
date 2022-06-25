import json
import os
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.db.models import Value, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from xhtml2pdf import pisa
from apps.common.constants import (DOCUMENT_TYPE_DNI, DOCUMENT_TYPE_CE, TIPO_PERSONA_DOCENTE,
                                   TIPO_PERSONA_ADMINISTRATIVO, TIPO_PERSONA_REGISTRADOR, TIPO_PERSONA_AUTORIDAD)
from apps.common.datatables_pagination import datatable_page
from apps.common.models import UbigeoDistrito, UbigeoProvincia, UbigeoDepartamento
from apps.distincion.models import Distincion
from apps.experiencia.models import Laboral, AsesorTesis, Docente, EvaluadorProyecto
from apps.formacion.models import Universitaria, Tecnico, Complementaria
from apps.idioma.models import Idioma
from apps.login.views import BaseLogin
from apps.persona.forms import PersonaForm, DatosGeneralesForm, ExportarCVForm
from apps.persona.models import Persona, DatosGenerales, Departamento
from apps.produccion.models import Cientifica


class PersonaCreateView(LoginRequiredMixin, BaseLogin, CreateView):
    template_name = 'persona/crear.html'
    model = Persona
    form_class = PersonaForm
    msg = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None)
        })
        return context

    def form_valid(self, form):
        form_dg = DatosGeneralesForm(self.request.POST or None)
        valid = True
        ruta = None
        if self.request.session.get('tipo_persona') == TIPO_PERSONA_REGISTRADOR:
            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_REGISTRADOR, TIPO_PERSONA_AUTORIDAD):
                self.msg = 'El usuario registrador solo puede registrar administrativo o docente, corregir'
                return self.form_invalid(form_dg)
        if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO):
            if not form_dg.is_valid():
                self.msg = 'Error en datos generales, verificar'
                return self.form_invalid(form_dg)
        if valid:
            if self.request.FILES:
                ruta = self.request.FILES['ruta_foto']
                extension = ruta.name.split(".")[-1]
                ruta.name = f"{uuid.uuid4()}.{extension}"
                if extension not in ('png', 'jpg', 'jpeg'):
                    self.msg = 'El archivo seleccionado debe ser de formato png, jpeg, o jpg'
                    return self.form_invalid(form)
                if ruta.size > 100000:
                    self.msg = 'El tamaño máximo permitido es 100Kb'
                    return self.form_invalid(form)
            persona = form.save(commit=False)
            if ruta:
                persona.ruta_foto = ruta
            persona.creado_por = self.request.user.username
            persona.save()
            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO):
                datos_generales = form_dg.save(commit=False)
                datos_generales.creado_por = self.request.user.username
                datos_generales.persona_id = persona.id
                datos_generales.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.msg:
            messages.warning(self.request, self.msg)
        else:
            messages.warning(self.request, 'Ha ocurrido un error al crear a la persona')
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None)
        })
        return self.render_to_response(context)

    def get_success_url(self):
        messages.success(self.request, 'Persona creada con éxito')
        return reverse('persona:crear_persona')


class PersonaUpdateView(LoginRequiredMixin, BaseLogin, UpdateView):
    template_name = 'persona/crear.html'
    model = Persona
    form_class = PersonaForm
    msg = None
    datos_generales = None

    def form_valid(self, form):
        ruta = None
        model_datos_generales = DatosGenerales.objects.filter(persona_id=self.object.id).last()
        if model_datos_generales:
            form_dg = DatosGeneralesForm(self.request.POST or None, instance=model_datos_generales)
        else:
            form_dg = DatosGeneralesForm(self.request.POST or None)
        valid = True
        if self.request.session.get('tipo_persona') == TIPO_PERSONA_REGISTRADOR:
            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_REGISTRADOR, TIPO_PERSONA_AUTORIDAD):
                self.msg = 'El usuario registrador solo puede actualizar administrativo o docente, corregir'
                return self.form_invalid(form_dg)
        if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO):
            if not form_dg.is_valid():
                self.msg = 'Error en datos generales, verificar'
                return self.form_invalid(form_dg)
        if valid:
            if self.request.FILES:
                ruta = self.request.FILES['ruta_foto']
                extension = ruta.name.split(".")[-1]
                ruta.name = f"{uuid.uuid4()}.{extension}"
                if extension not in ('png', 'jpg', 'jpeg'):
                    self.msg = 'El archivo seleccionado debe ser de formato png, jpeg, o jpg'
                    return self.form_invalid(form)
                if ruta.size > 100000:
                    self.msg = 'El tamaño máximo permitido es 100Kb'
                    return self.form_invalid(form)
            persona = form.save(commit=False)
            if ruta:
                persona.ruta_foto = ruta
            persona.modificado_por = self.request.user.username
            persona.save()
            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO):
                datos_generales = form_dg.save(commit=False)
                if self.datos_generales:
                    datos_generales.modificado_por = self.request.user.username
                datos_generales.creado_por = self.request.user.username
                datos_generales.persona_id = persona.id
                datos_generales.save()
            else:
                if model_datos_generales:
                    model_datos_generales.delete()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.msg:
            messages.warning(self.request, self.msg)
        else:
            messages.warning(self.request, 'Ha ocurrido un error al actualizar a la persona')
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None)
        })
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_generales = DatosGenerales.objects.filter(persona_id=self.object.id).last()
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None, instance=datos_generales),
            'MEDIA_URL': settings.MEDIA_URL
        })
        return context

    def get_success_url(self):
        messages.success(self.request, 'Persona actualizada con éxito')
        return reverse('persona:editar_persona', kwargs={'pk': self.object.id})


class BuscarPersonaAPIView(APIView):

    def get(self, request):
        numero_documento = self.request.GET.get('q', '')
        if numero_documento.isdigit() and len(numero_documento) == 8:
            tipo_documento = DOCUMENT_TYPE_DNI
        else:
            tipo_documento = DOCUMENT_TYPE_CE
        persona = Persona.objects.filter(tipo_documento=tipo_documento, numero_documento=numero_documento).first()
        data = []
        if persona:
            data.append({
                'id': persona.id,
                'text': persona.nombre_completo,
                'tipo_documento': persona.tipo_documento,
                'numero_documento': persona.numero_documento,
            })
        return Response(data, content_type='application/json')


class ListaPersonaView(LoginRequiredMixin, BaseLogin, View):
    def get(self, request, *args, **kwargs):
        search_param = self.request.GET.get('search[value]')
        filtro = self.request.GET.get('filtro')
        personas = Persona.objects.none()
        if filtro:
            ''
        else:
            personas = Persona.objects.filter(es_activo=True).order_by('-fecha_creacion')
            if self.request.session.get('tipo_persona') == TIPO_PERSONA_REGISTRADOR:
                personas = personas.filter(tipo_persona__in=(TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO))
        if len(search_param) > 3:
            personas = personas.annotate(
                search=Concat('apellido_paterno', Value(' '), 'apellido_materno', Value(' '), 'nombres')).filter(
                Q(search__icontains=search_param) | Q(numero_documento=search_param))
        draw, page = datatable_page(personas, request)
        lista_personas_data = []
        cont = 0
        for a in page.object_list:
            cont = cont + 1
            lista_personas_data.append([
                cont,
                '{} {}'.format(a.get_tipo_documento_display(), a.numero_documento),
                a.nombre_completo,
                a.celular or '-',
                a.correo_personal or '-',
                a.get_tipo_persona_display(),
                a.departamento.nombre if a.departamento else '-',
                (self.get_enlace_experiencia_laboral(a) + ' ' + self.get_enlace_formacion_academica(a) + ' ' +
                 self.get_enlace_idiomas(a) + ' ' + self.get_enlace_produccion(a) + ' ' +
                 self.get_enlace_distincion(a) + ' ' + self.get_exportar_cv(a)
                 ) if a.tipo_persona in (TIPO_PERSONA_DOCENTE, TIPO_PERSONA_ADMINISTRATIVO) else '',
                self.get_boton_editar(a),
                self.get_boton_eliminar(a),
            ])
        data = {
            'draw': draw,
            'recordsTotal': personas.count(),
            'recordsFiltered': personas.count(),
            'data': lista_personas_data
        }
        return JsonResponse(data)

    def get_enlace_experiencia_laboral(self, a):
        link = reverse('experiencia:experiencia_laboral', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-primary btn-sm separa-boton" href="{0}">
                <i class="fa fa-edit"></i>Experiencia laboral</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_formacion_academica(self, a):
        link = reverse('formacion:formacion_academica', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-info btn-sm separa-boton" href="{0}">
                <i class="fa fa-edit"></i>Formación académica</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_idiomas(self, a):
        link = reverse('idioma:crear_idioma', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-success btn-sm separa-boton" href="{0}">
                <i class="fa fa-edit"></i>Idiomas</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_produccion(self, a):
        link = reverse('produccion:cientifica', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-info btn-sm separa-boton" href="{0}">
                <i class="fa fa-edit"></i>Producción científica</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_distincion(self, a):
        link = reverse('distincion:distincion', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-primary btn-sm separa-boton" href="{0}">
                <i class="fa fa-edit"></i>Distinción o premio</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_exportar_cv(self, a):
        link = reverse('persona:exportar_cv', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-warning btn-sm separa-boton" href="{0}">
            <i class="fa fa-file"></i> Exportar CV</a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminarc" data-id={0}>
                      <i class="fa fa-trash"></i></button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        link = reverse('persona:editar_persona', kwargs={'pk': a.id})
        boton_editar = '<a class="btn btn-warning btn-sm" href="{0}"><i class="fa fa-edit"></i></a>'
        boton_editar = boton_editar.format(link)
        boton = '{0}'.format(boton_editar)
        return boton


class EliminarPersonaView(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        persona = get_object_or_404(Persona, id=self.kwargs.get('pk'))
        tipo_msg = ''
        persona.delete()
        msg = f'Persona eliminada correctamente'
        return Response({'msg': msg, 'tipo_msg': tipo_msg}, HTTP_200_OK)


class DepartamentosPorFacultadView(View):
    def get(self, request, *args, **kwargs):
        data = [{'codigo': '', 'nombre': '----------'}]
        facultad_id = request.GET.get('facultad_id', '')
        if facultad_id.isdigit():
            departamento = Departamento.objects.filter(facultad_id=facultad_id).values('id', 'nombre')
            data = list(departamento)
        return JsonResponse({'data': data})


class ProvinciaView(View):
    def get(self, request, *args, **kwargs):
        data = [{'codigo': '', 'nombre': '----------'}]
        dep_id = request.GET.get('dep_id', '')
        if dep_id.isdigit():
            provincias = UbigeoProvincia.objects.filter(
                departamento__cod_ubigeo_inei_departamento=dep_id
            ).annotate(
                codigo=F('cod_ubigeo_inei_provincia'),
                nombre=F('ubigeo_provincia'),
            ).values('codigo', 'nombre')
            data = list(provincias)
        return JsonResponse({'data': data})


class DistritoView(View):
    def get(self, request, *args, **kwargs):
        data = [{'codigo': '', 'nombre': '----------'}]
        dep_id = request.GET.get('dep_id', '')
        prov_id = request.GET.get('prov_id', '')
        if dep_id.isdigit() and prov_id.isdigit:
            distritos = UbigeoDistrito.objects.filter(
                departamento__cod_ubigeo_inei_departamento=dep_id, provincia__cod_ubigeo_inei_provincia=prov_id
            ).annotate(
                codigo=F('cod_ubigeo_inei_distrito'),
                nombre=F('ubigeo_distrito'),
            ).values('codigo', 'nombre')
            data = list(distritos)
        return JsonResponse({'data': data})


class ExportarCVView(TemplateView, BaseLogin):
    template_name = 'persona/exportar_cv.html'
    persona = None

    def get(self, request, *args, **kwargs):
        self.persona = get_object_or_404(Persona, pk=self.kwargs.get('pk'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'persona': self.persona,
            'form_exportar': ExportarCVForm(),
        })
        return context


class DescargarCVPdf(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="listado.pdf"'
        array_filtros = json.loads(self.request.GET.get('array_filtros'))
        p = get_object_or_404(Persona, pk=self.kwargs.get('pk'))
        foto_path = default_storage.path('{}'.format(p.ruta_foto))
        dep = UbigeoDepartamento.objects.filter(
            cod_ubigeo_inei_departamento=p.datosgenerales.ubigeo_departamento).last().ubigeo_departamento
        prov = UbigeoProvincia.objects.filter(
            cod_ubigeo_inei_provincia=p.datosgenerales.ubigeo_provincia).last().ubigeo_provincia
        dist = UbigeoDistrito.objects.filter(
            cod_ubigeo_inei_distrito=p.datosgenerales.ubigeo_distrito).last().ubigeo_distrito
        universitaria = None
        tecnico = None
        complementaria = None
        laboral = None
        docente = None
        asesor_tesis = None
        idiomas = None
        produccion_cientifica = None
        premios = None
        evaluador_proyecto = None
        for a in array_filtros:
            if a.get('opcion') == 'formacion_academica' and a.get('valor') == 'on':
                universitaria = Universitaria.objects.filter(persona=p)
                tecnico = Tecnico.objects.filter(persona=p)
                complementaria = Complementaria.objects.filter(persona=p)
            if a.get('opcion') == 'experiencia_laboral' and a.get('valor') == 'on':
                laboral = Laboral.objects.filter(persona=p)
                docente = Docente.objects.filter(persona=p)
                asesor_tesis = AsesorTesis.objects.filter(persona=p)
                evaluador_proyecto = EvaluadorProyecto.objects.filter(persona=p)
            if a.get('opcion') == 'idiomas' and a.get('valor') == 'on':
                idiomas = Idioma.objects.filter(persona=p)
            if a.get('opcion') == 'produccion_cientifica' and a.get('valor') == 'on':
                produccion_cientifica = Cientifica.objects.filter(persona=p)
            if a.get('opcion') == 'premios' and a.get('valor') == 'on':
                premios = Distincion.objects.filter(persona=p)
        data = {
            'array_filtros': array_filtros,
            'p': p,
            'dep': dep,
            'prov': prov,
            'dist': dist,
            'foto_path': foto_path,
            'universitaria': universitaria,
            'tecnico': tecnico,
            'complementaria': complementaria,
            'laboral': laboral,
            'docente': docente,
            'asesor_tesis': asesor_tesis,
            'evaluador_proyecto': evaluador_proyecto,
            'idiomas': idiomas,
            'produccion_cientifica': produccion_cientifica,
            'premios': premios,
        }
        template = get_template('persona/plantilla_pdf.html')
        html = template.render(data, request)
        nombre_archivo = f"{uuid.uuid4()}.pdf"
        path = f"{settings.STATIC_ROOT}/{nombre_archivo}"
        file = open(path, "w+b")
        pisa.CreatePDF(html, dest=file)
        file.seek(0)
        pdf = file.read()
        file.close()
        response.write(pdf)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                pass
        return response
