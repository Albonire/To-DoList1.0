# Generated by Django 5.2.1 on 2025-07-20 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0011_convert_days_to_json'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='dia_semana',
            field=models.JSONField(blank=True, default=list, verbose_name='Días de la semana'),
        ),
        migrations.AlterField(
            model_name='task',
            name='scheduled_dia_semana',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
