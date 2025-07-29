from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task

@receiver(pre_save, sender=Task)
def task_pre_save_handler(sender, instance, **kwargs):
    """
    Manejador para la lógica de negocio antes de guardar una tarea.
    - Mueve la información del horario a campos de respaldo al completar una tarea.
    - Restaura la información del horario desde los campos de respaldo al desmarcarla.
    """
    # Si es una tarea nueva, no hay estado anterior para comparar.
    if instance.pk is None:
        return

    try:
        # Obtenemos el estado de la tarea como está en la base de datos AHORA MISMO.
        original_task = Task.objects.get(pk=instance.pk)
        original_estado = original_task.estado
    except Task.DoesNotExist:
        # La tarea aún no existe en la BD, no hacemos nada.
        return

    # Lógica que antes estaba en el método save()
    # Si se está marcando como completada
    if instance.estado == 'completada' and original_estado != 'completada':
        instance.scheduled_dia_semana = instance.dia_semana
        instance.scheduled_hora_inicio = instance.hora_inicio
        instance.dia_semana = None
        instance.hora_inicio = None
    # Si se está desmarcando (volviendo a pendiente)
    elif instance.estado == 'pendiente' and original_estado == 'completada':
        instance.dia_semana = instance.scheduled_dia_semana
        instance.hora_inicio = instance.scheduled_hora_inicio
