# Generated by Django 3.2 on 2022-07-21 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_alter_responsabilidadsocial_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsabilidadsocial',
            name='descripcion',
            field=models.TextField(blank=True, null=True, verbose_name='Descripción'),
        ),
    ]
