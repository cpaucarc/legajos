# Generated by Django 3.2 on 2022-07-21 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0003_auto_20220721_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='responsabilidadsocial',
            options={'ordering': ['-fecha_fin', 'titulo']},
        ),
    ]
