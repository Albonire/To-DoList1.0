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
    fecha_hora_inicio = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha y hora de inicio'))
    fecha_hora_vencimiento = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha y hora de vencimiento'))
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
        if self.fecha_hora_inicio and self.fecha_hora_vencimiento:
            if self.fecha_hora_inicio > self.fecha_hora_vencimiento:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('La fecha y hora de inicio no puede ser posterior a la de vencimiento.'))

    def save(self, *args, **kwargs):
        # Guardar la tarea primero
        super().save(*args, **kwargs)
        
        # Si se marca para agregar al horario, crear/actualizar la actividad
        if self.agregar_al_horario and self.dia_semana and self.hora_inicio:
            self._actualizar_actividad_horario()
        elif not self.agregar_al_horario:
            # Si se desmarca, eliminar la actividad del horario
            self._eliminar_actividad_horario()
    
    def _actualizar_actividad_horario(self):
        """Actualiza o crea la actividad en el horario basada en la tarea"""
        if not self.dia_semana or not self.hora_inicio:
            return
            
        # Calcular hora de fin
        hora_fin = (datetime.combine(datetime.today(), self.hora_inicio) + 
                   timedelta(minutes=self.duracion_minutos)).time()
        
        # Crear slot de tiempo
        time_slot = f"{self.hora_inicio.strftime('%H:%M')}-{hora_fin.strftime('%H:%M')}"
        
        # Mapear prioridad a tipo de actividad
        prioridad_to_tipo = {
            'alta': 'study',
            'media': 'class', 
            'baja': 'routine'
        }
        activity_type = prioridad_to_tipo.get(self.prioridad, 'other')
        
        # Crear o actualizar la actividad en el horario
        schedule, created = Schedule.objects.get_or_create(
            usuario=self.usuario,
            time_slot=time_slot,
            day=self.dia_semana,
            defaults={
                'activity_text': self.nombre,
                'activity_type': activity_type,
                'notes': f"Tarea: {self.descripcion[:100]}{'...' if len(self.descripcion) > 100 else ''}"
            }
        )
        
        if not created:
            # Actualizar actividad existente
            schedule.activity_text = self.nombre
            schedule.activity_type = activity_type
            schedule.notes = f"Tarea: {self.descripcion[:100]}{'...' if len(self.descripcion) > 100 else ''}"
            schedule.save()
    
    def _eliminar_actividad_horario(self):
        """Elimina la actividad del horario asociada a esta tarea"""
        if self.dia_semana and self.hora_inicio:
            hora_fin = (datetime.combine(datetime.today(), self.hora_inicio) + 
                       timedelta(minutes=self.duracion_minutos)).time()
            time_slot = f"{self.hora_inicio.strftime('%H:%M')}-{hora_fin.strftime('%H:%M')}"
            
            Schedule.objects.filter(
                usuario=self.usuario,
                time_slot=time_slot,
                day=self.dia_semana,
                activity_text=self.nombre
            ).delete()

# Create your models here.
