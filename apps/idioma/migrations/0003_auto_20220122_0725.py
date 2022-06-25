# Generated by Django 3.2 on 2022-01-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idioma', '0002_idioma_persona'),
    ]

    operations = [
        migrations.AddField(
            model_name='idioma',
            name='creado_por',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='creado por'),
        ),
        migrations.AddField(
            model_name='idioma',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='fecha de creación'),
        ),
        migrations.AddField(
            model_name='idioma',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, verbose_name='fecha de modificación'),
        ),
        migrations.AddField(
            model_name='idioma',
            name='modificado_por',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='modificado por'),
        ),
    ]
