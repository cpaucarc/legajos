# Generated by Django 3.2 on 2022-02-16 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0003_catalogoidiomas'),
        ('persona', '0005_persona_ruta_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distincion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_por', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='creado por')),
                ('modificado_por', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='modificado por')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='fecha de creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='fecha de modificación')),
                ('distincion', models.CharField(max_length=250, verbose_name='Distinción')),
                ('descripcion', models.TextField(max_length=600, verbose_name='Descripción')),
                ('web_referencia', models.CharField(max_length=250, verbose_name='Web referencia')),
                ('fecha', models.DateField()),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.institucion')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.ubigeopais')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='persona.persona')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdjuntoDistincion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_por', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='creado por')),
                ('modificado_por', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='modificado por')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True, verbose_name='fecha de creación')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, verbose_name='fecha de modificación')),
                ('nombre', models.CharField(max_length=200, verbose_name='Nombre del documento')),
                ('ruta', models.TextField(max_length=500, verbose_name='Ruta del documento')),
                ('distincion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distincion.distincion')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
