from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

class Task(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', _('Pendiente')),
        ('completada', _('Completada')),
        ('vencida', _('Vencida')),
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
        ('Sunday', _('Domingo')),
    ]

    nombre = models.CharField(max_length=200, verbose_name=_('Nombre'))
    descripcion = models.TextField(verbose_name=_('Descripción'))
    fecha_vencimiento = models.DateField(verbose_name=_('Fecha de vencimiento'))
    estado = models.CharField(max_length=20, choices=[('pendiente', _('Pendiente')), ('completada', _('Completada'))], default='pendiente', verbose_name=_('Estado'))
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media', verbose_name=_('Prioridad'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    
    # Campos activos para integración con horario
    dia_semana = models.JSONField(default=list, blank=True, null=True, verbose_name=_('Días de la semana'))
    hora_inicio = models.TimeField(blank=True, null=True, verbose_name=_('Hora de inicio'))
    duracion_minutos = models.IntegerField(default=60, verbose_name=_('Duración (minutos)'))
    
    # --- Campos de "memoria" para restaurar el horario ---
    scheduled_dia_semana = models.JSONField(default=list, blank=True, null=True)
    scheduled_hora_inicio = models.TimeField(blank=True, null=True)

    # Campo para notificaciones
    recordatorio_enviado = models.BooleanField(default=False, verbose_name=_('Recordatorio enviado'))

    @property
    def dynamic_status(self):
        if self.estado == 'completada':
            return 'completada'
        if self.fecha_vencimiento < date.today():
            return 'vencida'
        return 'pendiente'

    def get_dynamic_status_display(self):
        return dict(self.ESTADO_CHOICES).get(self.dynamic_status)
    
    def __str__(self):
        return self.nombre

