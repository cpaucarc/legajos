# Generated by Django 3.2 on 2022-07-18 19:12

import apps.common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0016_alter_datosgenerales_dedicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='ruc',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[apps.common.models.validate_ruc], verbose_name='RUC'),
        ),
    ]
