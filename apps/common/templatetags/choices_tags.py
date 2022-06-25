from django import template
from django.urls import reverse

register = template.Library()


@register.filter()
def nombre_medico_ultima_atencion(value):
    medico = ''
    for sospechoso in value:
        if sospechoso.estado == 'atendido':
            if sospechoso.personal:
                medico = sospechoso.personal.nombre_completo
            else:
                medico = 'Sin Datos Médico'
            break
    return medico


@register.filter()
def fecha_seguimiento_ultima_atencion(value):
    fecha_seguimiento = 'NO'
    for seguimiento in value:
        if seguimiento.estado == 'atendido':
            fecha_seguimiento = "<a href='{url_bandeja_300}'>{fecha_300}</a>".format(
                url_bandeja_300=reverse('ficha:ficha300_crear', kwargs={'paciente_uuid': seguimiento.paciente.uuid}),
                fecha_300=seguimiento.fecha_seguimiento.strftime('%d/%m/%Y')
            )
            break
    return fecha_seguimiento
