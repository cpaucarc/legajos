# Generated by Django 3.2 on 2022-07-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formacion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjuntocomplementaria',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
        migrations.AlterField(
            model_name='adjuntotecnico',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
        migrations.AlterField(
            model_name='adjuntouniversitaria',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
        migrations.AlterField(
            model_name='complementaria',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
        migrations.AlterField(
            model_name='tecnico',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
        migrations.AlterField(
            model_name='universitaria',
            name='fecha_modificacion',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='fecha de modificación'),
        ),
    ]
