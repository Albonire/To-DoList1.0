from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, Schedule
from datetime import datetime, timedelta

@receiver(post_save, sender=Task)
def sync_task_to_schedule(sender, instance, created, **kwargs):
    """
    Actualiza o crea una entrada en el Schedule cuando una Tarea es guardada
    con la opción 'agregar_al_horario' activada.
    """
    if not instance.agregar_al_horario:
        # Si la tarea no debe estar en el horario, busca y elimina la entrada existente.
        if instance.dia_semana and instance.hora_inicio:
            hora_fin = (datetime.combine(datetime.today(), instance.hora_inicio) + 
                       timedelta(minutes=instance.duracion_minutos)).time()
            time_slot = f"{instance.hora_inicio.strftime('%H:%M')}-{hora_fin.strftime('%H:%M')}"
            
            Schedule.objects.filter(
                usuario=instance.usuario,
                time_slot=time_slot,
                day=instance.dia_semana,
                tarea_relacionada=instance
            ).delete()
        return

    if not instance.dia_semana or not instance.hora_inicio:
        return

    # Calcular hora de fin y time_slot
    hora_fin = (datetime.combine(datetime.today(), instance.hora_inicio) + 
               timedelta(minutes=instance.duracion_minutos)).time()
    time_slot = f"{instance.hora_inicio.strftime('%H:%M')}-{hora_fin.strftime('%H:%M')}"

    # Mapear prioridad a tipo de actividad
    prioridad_to_tipo = {
        'alta': 'study',
        'media': 'class', 
        'baja': 'routine'
    }
    activity_type = prioridad_to_tipo.get(instance.prioridad, 'other')

    # Crear o actualizar la actividad en el horario
    schedule, created = Schedule.objects.update_or_create(
        usuario=instance.usuario,
        tarea_relacionada=instance,
        defaults={
            'time_slot': time_slot,
            'day': instance.dia_semana,
            'activity_text': instance.nombre,
            'activity_type': activity_type,
            'notes': f"Tarea: {instance.descripcion[:100]}{'...' if len(instance.descripcion) > 100 else ''}"
        }
    )

@receiver(post_delete, sender=Task)
def delete_schedule_on_task_delete(sender, instance, **kwargs):
    """
    Elimina la entrada de horario correspondiente si se elimina una tarea.
    """
    if instance.agregar_al_horario:
        Schedule.objects.filter(tarea_relacionada=instance).delete()


@receiver(post_save, sender=Schedule)
def sync_schedule_to_task(sender, instance, created, **kwargs):
    """
    Crea o actualiza una Tarea cuando una entrada de Schedule es creada o modificada,
    a menos que sea una actividad del sistema o ya tenga una tarea relacionada.
    """
    # Evitar crear tareas para actividades del sistema
    system_activities = ['break', 'commute', 'meal']
    if instance.activity_type in system_activities:
        # Si la actividad se convierte en una del sistema, y tenía una tarea, desvincularla.
        if instance.tarea_relacionada:
            task = instance.tarea_relacionada
            task.agregar_al_horario = False
            task.save()
            instance.tarea_relacionada = None
        return

    # Si se crea una nueva actividad de horario (y no es del sistema), crear una tarea.
    if created and not instance.tarea_relacionada:
        # Extraer hora de inicio del time_slot
        try:
            hora_inicio_str = instance.time_slot.split('-')[0]
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
            # Calcular duración
            hora_fin_str = instance.time_slot.split('-')[1]
            hora_fin = datetime.strptime(hora_fin_str, '%H:%M').time()
            duracion = (datetime.combine(datetime.today(), hora_fin) - datetime.combine(datetime.today(), hora_inicio))
            duracion_minutos = duracion.total_seconds() / 60
        except (ValueError, IndexError):
            return # No se puede procesar el time_slot

        # Mapear tipo de actividad a prioridad
        tipo_to_prioridad = {
            'study': 'alta', 'class': 'media', 'workout': 'media',
            'routine': 'baja', 'social': 'baja', 'review': 'media', 'other': 'media'
        }
        prioridad = tipo_to_prioridad.get(instance.activity_type, 'media')

        # Calcular fecha de vencimiento (próximo día de la semana)
        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        try:
            dia_index = dias_semana.index(instance.day)
            hoy = datetime.today().date()
            dias_hasta_dia = (dia_index - hoy.weekday() + 7) % 7
            if dias_hasta_dia == 0: # Si es hoy, programar para la próxima semana
                dias_hasta_dia = 7
            fecha_vencimiento = hoy + timedelta(days=dias_hasta_dia)
        except ValueError:
            fecha_vencimiento = datetime.today().date() + timedelta(days=7)

        # Crear la tarea
        task = Task.objects.create(
            nombre=instance.activity_text,
            descripcion=instance.notes or f"Actividad del horario: {instance.activity_text}",
            fecha_vencimiento=fecha_vencimiento,
            estado='pendiente',
            prioridad=prioridad,
            usuario=instance.usuario,
            agregar_al_horario=True,
            dia_semana=instance.day,
            hora_inicio=hora_inicio,
            duracion_minutos=int(duracion_minutos)
        )
        # Asignar la tarea creada a este horario para evitar bucles
        instance.tarea_relacionada = task
        instance.save()

    # Si se actualiza una actividad de horario que tiene una tarea, actualizar la tarea.
    elif not created and instance.tarea_relacionada:
        task = instance.tarea_relacionada
        task.nombre = instance.activity_text
        task.descripcion = instance.notes or f"Actividad del horario: {instance.activity_text}"
        task.dia_semana = instance.day
        try:
            hora_inicio_str = instance.time_slot.split('-')[0]
            task.hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        except (ValueError, IndexError):
            pass # Mantener la hora de inicio si el formato es inválido
        task.save()

@receiver(post_delete, sender=Schedule)
def update_task_on_schedule_delete(sender, instance, **kwargs):
    """
    Actualiza la tarea relacionada si se elimina su entrada de horario.
    """
    if instance.tarea_relacionada:
        task = instance.tarea_relacionada
        task.agregar_al_horario = False
        task.save()
