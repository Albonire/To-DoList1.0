# Generated by Django 5.2.1 on 2025-07-16 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0008_remove_task_agregar_al_horario_delete_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='recordatorio_enviado',
            field=models.BooleanField(default=False, verbose_name='Recordatorio enviado'),
        ),
    ]
