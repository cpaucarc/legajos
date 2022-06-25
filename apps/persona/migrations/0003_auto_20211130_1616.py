# Generated by Django 3.2 on 2021-11-30 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20211130_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='facultad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='persona.facultad'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='codigo',
            field=models.CharField(max_length=45, unique=True, verbose_name='Código'),
        ),
        migrations.AlterField(
            model_name='facultad',
            name='codigo',
            field=models.CharField(max_length=45, unique=True, verbose_name='Código'),
        ),
    ]
