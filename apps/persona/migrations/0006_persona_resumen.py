# Generated by Django 3.2 on 2022-02-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0005_persona_ruta_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='resumen',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
    ]
