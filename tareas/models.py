from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

class Task(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', _('Pendiente')),
        ('en_progreso', _('En progreso')),
        ('completada', _('Completada')),
    ]

    PRIORIDAD_CHOICES = [
        ('alta', _('Alta')),
        ('media', _('Media')),
        ('baja', _('Baja')),
    ]
    
    DAYS_OF_WEEK = [
        ('Monday', _('Lunes')),
        ('Tuesday', _('Martes')),
        ('Wednesday', _('Miércoles')),
        ('Thursday', _('Jueves')),
        ('Friday', _('Viernes')),
        ('Saturday', _('Sábado')),
    ]

    nombre = models.CharField(max_length=200, verbose_name=_('Nombre'))
    descripcion = models.TextField(verbose_name=_('Descripción'))
    fecha_vencimiento = models.DateField(verbose_name=_('Fecha de vencimiento'))
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name=_('Estado'))
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media', verbose_name=_('Prioridad'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    
    # Campos para integración con horario
    dia_semana = models.CharField(max_length=10, choices=DAYS_OF_WEEK, blank=True, null=True, verbose_name=_('Día de la semana'))
    hora_inicio = models.TimeField(blank=True, null=True, verbose_name=_('Hora de inicio'))
    duracion_minutos = models.IntegerField(default=60, verbose_name=_('Duración (minutos)'))
    
    # Campo para notificaciones
    recordatorio_enviado = models.BooleanField(default=False, verbose_name=_('Recordatorio enviado'))
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Si la tarea se marca como completada, se elimina del horario.
        if self.estado == 'completada':
            self.dia_semana = None
            self.hora_inicio = None
        super().save(*args, **kwargs)
    

# Create your models here.
