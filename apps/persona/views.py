import json
import os
import uuid
import mimetypes
from builtins import print

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.db.models import Value, Q, F
from django.db.models.functions import Concat
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from xhtml2pdf import pisa
from PyPDF2 import PdfFileMerger, PdfFileReader
from django.forms import inlineformset_factory

from apps.common.constants import (DOCUMENT_TYPE_DNI, DOCUMENT_TYPE_CE, TIPO_PERSONA_DOCENTE,
                                   TIPO_PERSONA_ADMINISTRATIVO, TIPO_PERSONA_REGISTRADOR, TIPO_PERSONA_AUTORIDAD)
from apps.common.datatables_pagination import datatable_page

from apps.common.models import UbigeoDistrito, UbigeoProvincia, UbigeoDepartamento, Colegio
from apps.distincion.models import AdjuntoDistincion, Distincion
from apps.experiencia.models import AdjuntoAsesorTesis, AdjuntoDocente, AdjuntoEvaluadorProyecto, AdjuntoLaboral, \
    Laboral, AsesorTesis, Docente, EvaluadorProyecto
from apps.formacion.models import AdjuntoComplementaria, AdjuntoTecnico, AdjuntoUniversitaria, Universitaria, Tecnico, \
    Complementaria
from apps.idioma.models import Idioma
from apps.login.views import BaseLogin
from apps.persona.forms import PersonaForm, DatosGeneralesForm, ExportarCVForm, ColegiaturaFormset, ColegiaturaForm, \
    get_colegio_name, get_estado_colegiado
from apps.persona.models import Persona, DatosGenerales, Departamento, Colegiatura
from apps.produccion.models import AdjuntoCientifica, Cientifica


# Clase para registrar a una nueva persona
class PersonaCreateView(LoginRequiredMixin, BaseLogin, CreateView):
    template_name = 'persona/crear.html'
    model = Persona
    form_class = PersonaForm
    msg = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None),
            'colegiatura_formset': self.get_colegiatura_formset(),
        })
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_dg = DatosGeneralesForm(self.request.POST or None)
        colegiatura_formset = context['colegiatura_formset']
        valid = True
        ruta = None
        if self.request.session.get('tipo_persona') == TIPO_PERSONA_REGISTRADOR:
            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_REGISTRADOR, TIPO_PERSONA_AUTORIDAD):
                self.msg = 'El usuario registrador solo puede registrar administrativo o docente, corregir'
                return self.form_invalid(form_dg)

        if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE):
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

                if ruta.size > 2400000:
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

            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE):
                if colegiatura_formset.is_valid():
                    cont = 0
                    for e in colegiatura_formset:
                        if e.cleaned_data.get('DELETE') is False:
                            cont += 1
                    if cont == 0:
                        self.msg = 'Falta agregar miembro del equipo del proyecto de capacitación'
                        return self.form_invalid(form)
                    persona = form.save(commit=False)

                    cole_formset = colegiatura_formset.save(commit=False)
                    for f in cole_formset:
                        f.creado_por = self.request.user.username
                        f.persona_id = persona.id
                        f.persona = persona
                        f.save()
                else:
                    return self.form_invalid(form)

            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.msg:
            messages.warning(self.request, self.msg)
        else:
            messages.warning(self.request,
                             'Ha ocurrido un error al crear a la persona, revise si ha introducido bien todos los datos')
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None),
            'colegiatura_formset': self.get_colegiatura_formset(),
        })

        return self.render_to_response(context)

    def get_colegiatura_formset(self):
        return ColegiaturaFormset(self.request.POST or None)

    def get_success_url(self):
        messages.success(self.request, 'Persona creada con éxito')
        return reverse('persona:crear_persona')


# Clase para editar la información de una persona existente
class PersonaUpdateView(LoginRequiredMixin, BaseLogin, UpdateView):
    template_name = 'persona/crear.html'
    model = Persona
    form_class = PersonaForm
    msg = None
    datos_generales = None

    def form_valid(self, form):
        context = self.get_context_data()
        colegiatura_formset = context['colegiatura_formset']
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
                if ruta.size > 2400000:
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

            if form.cleaned_data.get('tipo_persona') in (TIPO_PERSONA_DOCENTE):
                if colegiatura_formset.is_valid():
                    persona = form.save(commit=False)
                    self.object.colegiatura_set.all().delete()
                    for e in colegiatura_formset:
                        e.creado_por = self.request.user.username
                        e.persona_id = persona.id
                        e.persona = persona
                        e.save()
                else:
                    return self.form_invalid(form)
            return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.msg:
            messages.warning(self.request, self.msg)
        else:
            messages.warning(self.request, 'Ha ocurrido un error al actualizar a la persona')
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None),
        })
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        datos_generales = DatosGenerales.objects.filter(persona_id=self.object.id).last()
        context.update({
            'form_datos_generales': DatosGeneralesForm(self.request.POST or None, instance=datos_generales),
            'colegiatura_formset': self.get_colegiatura_formset(),
            'MEDIA_URL': settings.MEDIA_URL
        })
        return context

    def get_colegiatura_formset(self):
        colegiatura = self.object.colegiatura_set.all()
        formset_initial = [{'id': e.id, 'colegio_profesional': e.colegio_profesional,
                            'colegio_profesional_persona': get_colegio_name(e.colegio_profesional),
                            'sede_colegio': e.sede_colegio, 'sede_colegio_persona': e.sede_colegio,
                            'codigo_colegiado': e.codigo_colegiado, 'codigo_colegiado_persona': e.codigo_colegiado,
                            'estado_colegiado': e.estado_colegiado,
                            'estado_colegiado_persona': get_estado_colegiado(e.estado_colegiado)}
                           for e in colegiatura]
        formset_colegiatura = inlineformset_factory(Persona, Colegiatura, form=ColegiaturaForm,
                                                    can_delete=True, extra=colegiatura.count())
        formset = formset_colegiatura(
            data=self.request.POST or None,
            initial=formset_initial,
        )
        return formset

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


# Clase que lista a las personas registradas en la BD
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

            if a.tipo_persona in (TIPO_PERSONA_DOCENTE):
                lista_personas_data.append([
                    cont,
                    '{} {}'.format(a.get_tipo_documento_display(), a.numero_documento),
                    a.nombre_completo,
                    a.celular or '-',
                    a.correo_personal or '-',
                    a.get_tipo_persona_display(),
                    a.departamento.nombre if a.departamento else '-',
                    (self.get_enlace_experiencia_laboral(a) + ' ' +
                     self.get_enlace_formacion_academica(a) + ' ' +
                     self.get_enlace_idiomas(a) + ' ' +
                     self.get_enlace_produccion(a) + ' ' +
                     self.get_enlace_distincion(a) + ' ' +
                     self.get_enlace_agregar_cursos(a) + ' ' +
                     self.get_exportar_cv(a)
                     ),
                    self.get_boton_editar(a),
                    self.get_boton_eliminar(a),
                ])
            elif a.tipo_persona in (TIPO_PERSONA_ADMINISTRATIVO):
                lista_personas_data.append([
                    cont,
                    '{} {}'.format(a.get_tipo_documento_display(), a.numero_documento),
                    a.nombre_completo,
                    a.celular or '-',
                    a.correo_personal or '-',
                    a.get_tipo_persona_display(),
                    a.departamento.nombre if a.departamento else '-',
                    (self.get_enlace_experiencia_laboral(a) + ' ' +
                     self.get_enlace_formacion_academica(a) + ' ' +
                     self.get_enlace_idiomas(a) + ' ' +
                     self.get_enlace_produccion(a) + ' ' +
                     self.get_enlace_distincion(a) + ' ' +
                     self.get_exportar_cv(a)
                     ),
                    self.get_boton_editar(a),
                    self.get_boton_eliminar(a),
                ])
            else:
                lista_personas_data.append([
                    cont,
                    '{} {}'.format(a.get_tipo_documento_display(), a.numero_documento),
                    a.nombre_completo,
                    a.celular or '-',
                    a.correo_personal or '-',
                    a.get_tipo_persona_display(),
                    a.departamento.nombre if a.departamento else '-',
                    '',
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
                    <i class="fa fa-edit"></i> Experiencia laboral
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_formacion_academica(self, a):
        link = reverse('formacion:formacion_academica', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-info btn-sm separa-boton" href="{0}">
                    <i class="fa fa-edit"></i> Formación académica
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_idiomas(self, a):
        link = reverse('idioma:crear_idioma', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-success btn-sm separa-boton" href="{0}">
                    <i class="fa fa-edit"></i> Idiomas
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_produccion(self, a):
        link = reverse('produccion:cientifica', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-info btn-sm separa-boton" href="{0}">
                    <i class="fa fa-edit"></i> Producción científica
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_distincion(self, a):
        link = reverse('distincion:distincion', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-primary btn-sm separa-boton" href="{0}">
                    <i class="fa fa-edit"></i> Distinción o premio
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_enlace_agregar_cursos(self, a):
        link = reverse('cursos:agregar_cursos', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-primary btn-sm separa-boton" href="{0}">
                    <i class="fa fa-edit"></i> Cursos dictados
                </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_exportar_cv(self, a):
        link = reverse('persona:exportar_cv', kwargs={'pk': a.id})
        boton = '''<a class="btn btn-warning btn-sm separa-boton" href="{0}">
                <i class="fa fa-file"></i> Exportar CV
            </a>'''
        boton = boton.format(link)
        boton = '{0}'.format(boton)
        return boton

    def get_boton_eliminar(self, a):
        boton_eliminar = '''<button class="btn btn-danger btn-sm eliminarc" data-id={0}>
                                <i class="fa fa-trash"></i>
                            </button>'''
        boton_eliminar = boton_eliminar.format(a.id)
        boton = '{0}'.format(boton_eliminar)
        return boton

    def get_boton_editar(self, a):
        link = reverse('persona:editar_persona', kwargs={'pk': a.id})
        boton_editar = '''<a class="btn btn-warning btn-sm" href="{0}">
                            <i class="fa fa-edit"></i>
                        </a>'''
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
            data += list(departamento)

        return JsonResponse({'data': data})


class ProvinciaView(View):
    def get(self, request, *args, **kwargs):
        data = [{'codigo': '', 'nombre': '----------'}]
        dep_id = request.GET.get('dep_id', '')

        if dep_id.isdigit():
            provincias = UbigeoProvincia.objects.filter(departamento__cod_ubigeo_inei_departamento=dep_id).annotate(
                codigo=F('cod_ubigeo_inei_provincia'), nombre=F('ubigeo_provincia')).values('codigo', 'nombre')
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


# CV Simple
class DescargarCVPdf(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        array_filtros = json.loads(self.request.GET.get('array_filtros'))

        p = get_object_or_404(Persona, pk=self.kwargs.get('pk'))
        foto_path = default_storage.path('{}'.format(p.ruta_foto))

        dep = UbigeoDepartamento.objects.filter(
            cod_ubigeo_inei_departamento=p.datosgenerales.ubigeo_departamento).last().ubigeo_departamento
        prov = UbigeoProvincia.objects.filter(
            cod_ubigeo_inei_provincia=p.datosgenerales.ubigeo_provincia).last().ubigeo_provincia
        dist = UbigeoDistrito.objects.filter(
            cod_ubigeo_inei_distrito=p.datosgenerales.ubigeo_distrito).last().ubigeo_distrito

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{pat}_{mat}_{nom}_CV_SIMPLE.pdf"'.format(
            pat=p.apellido_paterno, mat=p.apellido_materno, nom=p.nombres
        )
        # Datos de colegiatura
        sede = None
        codigo = None
        estado = None
        colegio = None
        colegiatura = Colegiatura.objects.filter(persona=p).last()
        if colegiatura:
            sede = colegiatura.sede_colegio
            codigo = colegiatura.codigo_colegiado
            estado = colegiatura.estado_colegiado
            colegio = colegiatura.colegio_profesional
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
            'colegio': colegio,
            'sede': sede,
            'codigo': codigo,
            'estado': estado,
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


class DescargarCVPdfDet6(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="listado.pdf"'
        array_filtros = json.loads(self.request.GET.get('array_filtros'))
        persona = get_object_or_404(Persona, pk=self.kwargs.get('pk'))
        foto_path = default_storage.path('{}'.format(persona.ruta_foto))
        dep = UbigeoDepartamento.objects.filter(
            cod_ubigeo_inei_departamento=persona.datosgenerales.ubigeo_departamento).last().ubigeo_departamento
        prov = UbigeoProvincia.objects.filter(
            cod_ubigeo_inei_provincia=persona.datosgenerales.ubigeo_provincia).last().ubigeo_provincia
        dist = UbigeoDistrito.objects.filter(
            cod_ubigeo_inei_distrito=persona.datosgenerales.ubigeo_distrito).last().ubigeo_distrito
        universitaria = None
        adjuntos_universitaria = []
        tecnico = None
        adjuntos_tecnico = []
        complementaria = None
        adjuntos_complementaria = []
        laboral = None
        adjuntos_laboral = []
        docente = None
        adjuntos_docente = []
        asesor_tesis = None
        adjuntos_asesor_tesis = []
        idiomas = None
        produccion_cientifica = None
        adjuntos_produccion_cientifica = []
        premios = None
        adjuntos_premios = []
        evaluador_proyecto = None
        adjuntos_evaluador_proyecto = []
        for a in array_filtros:
            if a.get('opcion') == 'formacion_academica' and a.get('valor') == 'on':
                universitaria = Universitaria.objects.filter(persona=persona)
                for uni in universitaria:
                    adjuntos_universitaria.append(
                        AdjuntoUniversitaria.objects.filter(universitaria=uni).order_by('-id'))

                tecnico = Tecnico.objects.filter(persona=persona)
                for tec in tecnico:
                    adjuntos_tecnico.append(AdjuntoTecnico.objects.filter(tecnico=tec).order_by('-id'))

                complementaria = Complementaria.objects.filter(persona=persona)
                for cmp in complementaria:
                    adjuntos_complementaria.append(
                        AdjuntoComplementaria.objects.filter(complementaria=cmp).order_by('-id'))

            if a.get('opcion') == 'experiencia_laboral' and a.get('valor') == 'on':
                laboral = Laboral.objects.filter(persona=persona)
                for lb in laboral:
                    adjuntos_laboral.append(AdjuntoLaboral.objects.filter(laboral=lb).order_by('-id'))

                docente = Docente.objects.filter(persona=persona)
                for doc in docente:
                    adjuntos_docente.append(AdjuntoDocente.objects.filter(docente=doc).order_by('-id'))

                asesor_tesis = AsesorTesis.objects.filter(persona=persona)
                for ast in asesor_tesis:
                    adjuntos_asesor_tesis.append(AdjuntoAsesorTesis.objects.filter(asesor_tesis=ast).order_by('-id'))

                evaluador_proyecto = EvaluadorProyecto.objects.filter(persona=persona)
                for evpy in evaluador_proyecto:
                    adjuntos_evaluador_proyecto.append(
                        AdjuntoEvaluadorProyecto.objects.filter(evaluador_proyecto=evpy).order_by('-id'))
            if a.get('opcion') == 'idiomas' and a.get('valor') == 'on':
                idiomas = Idioma.objects.filter(persona=persona)
            if a.get('opcion') == 'produccion_cientifica' and a.get('valor') == 'on':
                produccion_cientifica = Cientifica.objects.filter(persona=persona)
                for prdctf in produccion_cientifica:
                    adjuntos_produccion_cientifica.append(
                        AdjuntoCientifica.objects.filter(cientifica=prdctf).order_by('-id'))
            if a.get('opcion') == 'premios' and a.get('valor') == 'on':
                premios = Distincion.objects.filter(persona=persona)
                for prm in premios:
                    adjuntos_premios.append(AdjuntoDistincion.objects.filter(distincion=prm).order_by('-id'))

        docs = []
        # docs.append(path)
        for adju in adjuntos_universitaria:
            for univ in adju:
                docs.append(str(default_storage.path(univ.ruta)))

        for adjt in adjuntos_tecnico:
            for tec in adjt:
                docs.append(str(default_storage.path(tec.ruta)))

        for adjc in adjuntos_complementaria:
            for cmp in adjc:
                docs.append(str(default_storage.path(cmp.ruta)))

        for adjl in adjuntos_laboral:
            for lab in adjl:
                docs.append(str(default_storage.path(lab.ruta)))

        for adjd in adjuntos_docente:
            for doc in adjd:
                docs.append(str(default_storage.path(doc.ruta)))

        for adjat in adjuntos_asesor_tesis:
            for ast in adjat:
                docs.append(str(default_storage.path(ast.ruta)))

        for adjpc in adjuntos_produccion_cientifica:
            for pdc in adjpc:
                docs.append(str(default_storage.path(pdc.ruta)))

        for adjp in adjuntos_premios:
            for prm in adjp:
                docs.append(str(default_storage.path(prm.ruta)))

        for adjep in adjuntos_evaluador_proyecto:
            for evp in adjep:
                docs.append(str(default_storage.path(evp.ruta)))

        data = {
            'array_filtros': array_filtros,
            'p': persona,
            'dep': dep,
            'prov': prov,
            'dist': dist,
            'foto_path': foto_path,
            'universitaria': universitaria,
            'adjuntos_universitaria': adjuntos_universitaria,
            'tecnico': tecnico,
            'adjuntos_tecnico': adjuntos_tecnico,
            'complementaria': complementaria,
            'adjuntos_complementaria': adjuntos_complementaria,
            'laboral': laboral,
            'adjuntos_laboral': adjuntos_laboral,
            'docente': docente,
            'adjuntos_docente': adjuntos_docente,
            'asesor_tesis': asesor_tesis,
            'adjuntos_asesor_tesis': adjuntos_asesor_tesis,
            'evaluador_proyecto': evaluador_proyecto,
            'adjuntos_evaluador_proyecto': adjuntos_evaluador_proyecto,
            'idiomas': idiomas,
            'produccion_cientifica': produccion_cientifica,
            'adjuntos_produccion_cientifica': adjuntos_produccion_cientifica,
            'premios': premios,
            'adjuntos_premios': adjuntos_premios,
            'documentos': docs,
        }
        template = get_template('persona/plantilla_pdf_det.html')
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


class DescargarCVPdfDet3(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = 'experiencia_asesor_tesis/6518f9e6-c5a7-404d-afb5-346c160f0b17.pdf'
        # Define the full file path
        filepath = BASE_DIR + '/media/' + filename
        print("BASE DIR: ", BASE_DIR)
        print("filepath DIR: ", filepath)
        path = open(filepath, 'r')
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        filename = 'elarchivo.pdf'
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response


class DescargarCVPdfDet(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        persona = get_object_or_404(Persona, pk=self.kwargs.get('pk'))
        foto_path = default_storage.path('{}'.format(persona.ruta_foto))
        dep = UbigeoDepartamento.objects.filter(
            cod_ubigeo_inei_departamento=persona.datosgenerales.ubigeo_departamento).last().ubigeo_departamento
        prov = UbigeoProvincia.objects.filter(
            cod_ubigeo_inei_provincia=persona.datosgenerales.ubigeo_provincia).last().ubigeo_provincia
        dist = UbigeoDistrito.objects.filter(
            cod_ubigeo_inei_distrito=persona.datosgenerales.ubigeo_distrito).last().ubigeo_distrito

        # Datos de colegiatura
        sede = None
        codigo = None
        estado = None
        colegio = None
        colegiatura = Colegiatura.objects.filter(persona=persona).last()
        if colegiatura:
            sede = colegiatura.sede_colegio
            codigo = colegiatura.codigo_colegiado
            estado = colegiatura.estado_colegiado
            colegio = colegiatura.colegio_profesional

        universitaria = None
        adjuntos_universitaria = []
        tecnico = None
        adjuntos_tecnico = []
        complementaria = None
        adjuntos_complementaria = []
        laboral = None
        adjuntos_laboral = []
        docente = None
        adjuntos_docente = []
        asesor_tesis = None
        adjuntos_asesor_tesis = []
        idiomas = None
        produccion_cientifica = None
        adjuntos_produccion_cientifica = []
        premios = None
        adjuntos_premios = []
        evaluador_proyecto = None
        adjuntos_evaluador_proyecto = []

        array_filtros = json.loads(self.request.GET.get('array_filtros'))
        for a in array_filtros:
            if a.get('opcion') == 'formacion_academica' and a.get('valor') == 'on':
                universitaria = Universitaria.objects.filter(persona=persona)
                for uni in universitaria:
                    adjuntos_universitaria.append(
                        AdjuntoUniversitaria.objects.filter(universitaria=uni).order_by('-id'))

                tecnico = Tecnico.objects.filter(persona=persona)
                for tec in tecnico:
                    adjuntos_tecnico.append(AdjuntoTecnico.objects.filter(tecnico=tec).order_by('-id'))

                complementaria = Complementaria.objects.filter(persona=persona)
                for cmp in complementaria:
                    adjuntos_complementaria.append(
                        AdjuntoComplementaria.objects.filter(complementaria=cmp).order_by('-id'))
            if a.get('opcion') == 'experiencia_laboral' and a.get('valor') == 'on':
                laboral = Laboral.objects.filter(persona=persona)
                for lb in laboral:
                    adjuntos_laboral.append(AdjuntoLaboral.objects.filter(laboral=lb).order_by('-id'))

                docente = Docente.objects.filter(persona=persona)
                for doc in docente:
                    adjuntos_docente.append(AdjuntoDocente.objects.filter(docente=doc).order_by('-id'))

                asesor_tesis = AsesorTesis.objects.filter(persona=persona)
                for ast in asesor_tesis:
                    adjuntos_asesor_tesis.append(AdjuntoAsesorTesis.objects.filter(asesor_tesis=ast).order_by('-id'))

                evaluador_proyecto = EvaluadorProyecto.objects.filter(persona=persona)
                for evpy in evaluador_proyecto:
                    adjuntos_evaluador_proyecto.append(
                        AdjuntoEvaluadorProyecto.objects.filter(evaluador_proyecto=evpy).order_by('-id'))
            if a.get('opcion') == 'idiomas' and a.get('valor') == 'on':
                idiomas = Idioma.objects.filter(persona=persona)
            if a.get('opcion') == 'produccion_cientifica' and a.get('valor') == 'on':
                produccion_cientifica = Cientifica.objects.filter(persona=persona)
                for prdctf in produccion_cientifica:
                    adjuntos_produccion_cientifica.append(
                        AdjuntoCientifica.objects.filter(cientifica=prdctf).order_by('-id'))
            if a.get('opcion') == 'premios' and a.get('valor') == 'on':
                premios = Distincion.objects.filter(persona=persona)
                for prm in premios:
                    adjuntos_premios.append(AdjuntoDistincion.objects.filter(distincion=prm).order_by('-id'))

        data = {
            'array_filtros': array_filtros,
            'p': persona,
            'dep': dep,
            'prov': prov,
            'dist': dist,
            'colegio': colegio,
            'sede': sede,
            'codigo': codigo,
            'estado': estado,
            'foto_path': foto_path,
            'universitaria': universitaria,
            'adjuntos_universitaria': adjuntos_universitaria,
            'tecnico': tecnico,
            'adjuntos_tecnico': adjuntos_tecnico,
            'complementaria': complementaria,
            'adjuntos_complementaria': adjuntos_complementaria,
            'laboral': laboral,
            'adjuntos_laboral': adjuntos_laboral,
            'docente': docente,
            'adjuntos_docente': adjuntos_docente,
            'asesor_tesis': asesor_tesis,
            'adjuntos_asesor_tesis': adjuntos_asesor_tesis,
            'evaluador_proyecto': evaluador_proyecto,
            'adjuntos_evaluador_proyecto': adjuntos_evaluador_proyecto,
            'idiomas': idiomas,
            'produccion_cientifica': produccion_cientifica,
            'adjuntos_produccion_cientifica': adjuntos_produccion_cientifica,
            'premios': premios,
            'adjuntos_premios': adjuntos_premios,
        }

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{pat}_{mat}_{nom}_CV_DETALLADO.pdf"'.format(
            pat=persona.apellido_paterno, mat=persona.apellido_materno, nom=persona.nombres
        )

        template = get_template('persona/plantilla_pdf_det.html')
        html = template.render(data, request)
        nombre_archivo = f"{uuid.uuid4()}.pdf"
        path = f"{settings.STATIC_ROOT}/{nombre_archivo}"
        print("\n- Path 1: ", path, '\n')

        file = open(path, "w+b")
        pisa.CreatePDF(html, dest=file)
        file.seek(0)

        print("CV Simple creado")

        docs = []
        docs.append(path)
        for adju in adjuntos_universitaria:
            for univ in adju:
                # docs.append(default_storage.path(univ.ruta))
                docs.append("/media/" + univ.rut)
        for adjt in adjuntos_tecnico:
            for tec in adjt:
                # docs.append(f"{settings.STATIC_ROOT}/media/{tec.ruta}")
                docs.append("/media/" + tec.ruta)
        for adjc in adjuntos_complementaria:
            for cmp in adjc:
                docs.append("/media/" + cmp.ruta)
        for adjl in adjuntos_laboral:
            for lab in adjl:
                docs.append("/media/" + lab.ruta)
        for adjd in adjuntos_docente:
            for doc in adjd:
                docs.append("/media/" + doc.ruta)
        for adjat in adjuntos_asesor_tesis:
            for ast in adjat:
                docs.append("/media/" + ast.ruta)
        for adjpc in adjuntos_produccion_cientifica:
            for pdc in adjpc:
                docs.append("/media/" + pdc.ruta)
        for adjp in adjuntos_premios:
            for prm in adjp:
                docs.append("/media/" + prm.ruta)
        for adjep in adjuntos_evaluador_proyecto:
            for evp in adjep:
                docs.append("/media/" + evp.ruta)

        print("\nDocumentos: ", docs)

        merger = PdfFileMerger()
        ind = 0
        for doc_name in docs:
            ind += 1
            if doc_name.endswith('.pdf') is False:
                continue
            try:
                print(f" -> DocName {ind}:", doc_name)
                merger.append(PdfFileReader(open(doc_name, 'rb')), )
                print(f" - Merger {ind}:", merger, "\n")
            except Exception as e:
                print(f" Ocurrio un error: {e}")

        print("\nMerged files\n")
        nombre_archivo_merged = f"{uuid.uuid4()}.pdf"
        path_merged = f"{settings.STATIC_ROOT}/{nombre_archivo_merged}"

        print("\n- Path 2: ", path_merged, '\n')
        merger.write(path_merged)
        merger.close()

        print("Save merged file.\n")
        file = open(path_merged, "r+b")
        pdf = file.read()
        file.close()
        response.write(pdf)
        print("\n- Response: ", response, '\n')
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception as e:
                pass
        if os.path.exists(path_merged):
            try:
                os.remove(path_merged)
            except Exception as e:
                pass
        return response
