from django import template
from django.template import loader

from crispy_forms.utils import TEMPLATE_PACK

register = template.Library()


@register.simple_tag(name='field')
def custom_field(field, **kwargs):
    """Use crispy_forms as a base template for custom fields for forms"""
    template_path = '%s/field.html' % TEMPLATE_PACK
    label = kwargs.get('label', True)
    context = {
        'field': field,
        'form_show_errors': True,
        'form_show_labels': bool(label)
    }
    if isinstance(label, str):
        field.label = label
    columns = kwargs.get('cols', False)
    if columns:
        label_width = kwargs.get('label_width', 4)
        classname = kwargs.get('classname', '')
        form_class = kwargs.get('form_class', '')
        context.update({
            'label_class': 'col-lg-{}'.format(label_width),
            'field_class': 'col-lg-{} {}'.format(12 - label_width, classname),
            'form_class': 'form-horizontal {}'.format(form_class)
        })
    if kwargs.get('inline'):
        context.update({
            'inline_class': 'inline'
        })
    if kwargs.get('mask'):
        context.update({
            'field_class': '{} input_mask'.format(context.get('field_class')),
        })
        field.field.widget.attrs['data-inputmask'] = kwargs.get('mask')
    if kwargs.get('datepicker'):
        context.update({
            'field_class': '{} datepicker'.format(context.get('field_class'))
        })
    append = kwargs.get('append')
    if append:
        context.update({
            'crispy_appended_text': append
        })
        template_path = '%s/layout/prepended_appended_text.html' % TEMPLATE_PACK
    _template = loader.get_template(template_path)
    return _template.render(context)


@register.simple_tag
def list_filter(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v
    return updated.urlencode()
