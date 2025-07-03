from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta

class Schedule(models.Model):
    ACTIVITY_TYPES = [
        ('class', _('Clase')),
        ('study', _('Estudio')),
        ('workout', _('Ejercicio')),
        ('meal', _('Comida')),
        ('routine', _('Rutina')),
        ('commute', _('Transporte')),
        ('break', _('Descanso')),
        ('social', _('Social')),
        ('review', _('Repaso')),
        ('open', _('Abierto')),
        ('other', _('Otro')),
    ]
    
    DAYS_OF_WEEK = [
        ('Monday', _('Lunes')),
        ('Tuesday', _('Martes')),
        ('Wednesday', _('Miércoles')),
        ('Thursday', _('Jueves')),
        ('Friday', _('Viernes')),
        ('Saturday', _('Sábado')),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    time_slot = models.CharField(max_length=20, verbose_name=_('Horario'))  # ej: "09:00-12:00"
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, verbose_name=_('Día'))
    activity_text = models.CharField(max_length=200, verbose_name=_('Descripción'))
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, verbose_name=_('Tipo'))
    notes = models.TextField(blank=True, verbose_name=_('Notas'))
    
    # Campo para relación con tarea
    tarea_relacionada = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Tarea relacionada'))
    
    class Meta:
        unique_together = ['usuario', 'time_slot', 'day']
        verbose_name = _('Horario')
        verbose_name_plural = _('Horarios')
    
    def __str__(self):
        return f"{self.usuario.username} - {self.day} {self.time_slot}: {self.activity_text}"
    

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

    nombre = models.CharField(max_length=200, verbose_name=_('Nombre'))
    descripcion = models.TextField(verbose_name=_('Descripción'))
    fecha_vencimiento = models.DateField(verbose_name=_('Fecha de vencimiento'))
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name=_('Estado'))
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media', verbose_name=_('Prioridad'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    
    # Campos para integración con horario
    agregar_al_horario = models.BooleanField(default=False, verbose_name=_('Agregar al horario semanal'))
    dia_semana = models.CharField(max_length=10, choices=Schedule.DAYS_OF_WEEK, blank=True, null=True, verbose_name=_('Día de la semana'))
    hora_inicio = models.TimeField(blank=True, null=True, verbose_name=_('Hora de inicio'))
    duracion_minutos = models.IntegerField(default=60, verbose_name=_('Duración (minutos)'))
    
    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        # Validación: si se agrega al horario, debe tener día y hora
        if self.agregar_al_horario:
            if not self.dia_semana:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('Debe seleccionar un día de la semana para agregar al horario.'))
            if not self.hora_inicio:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('Debe especificar una hora de inicio para agregar al horario.'))
    

# Create your models here.
