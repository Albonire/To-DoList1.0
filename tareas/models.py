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
    
    def save(self, *args, **kwargs):
        # Bandera para evitar bucles infinitos
        if hasattr(self, '_syncing_from_task'):
            super().save(*args, **kwargs)
            return
            
        # Guardar primero el horario
        super().save(*args, **kwargs)
        
        # Si no tiene tarea relacionada y no es una actividad del sistema, crear una tarea
        if not self.tarea_relacionada and not self._is_system_activity():
            self._crear_tarea_desde_horario()
        elif self.tarea_relacionada:
            # Si tiene tarea relacionada, actualizar la tarea
            self._actualizar_tarea_desde_horario()
    
    def _is_system_activity(self):
        """Determina si es una actividad del sistema (no debe crear tarea)"""
        system_activities = ['break', 'commute', 'meal']
        return self.activity_type in system_activities
    
    def _crear_tarea_desde_horario(self):
        """Crea una nueva tarea basada en la actividad del horario"""
        # Extraer hora de inicio del time_slot
        hora_inicio_str = self.time_slot.split('-')[0]
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        except ValueError:
            return
        # Mapear tipo de actividad a prioridad
        tipo_to_prioridad = {
            'study': 'alta',
            'class': 'media',
            'workout': 'media',
            'routine': 'baja',
            'social': 'baja',
            'review': 'media',
            'other': 'media'
        }
        prioridad = tipo_to_prioridad.get(self.activity_type, 'media')
        # Calcular fecha de vencimiento (próximo día de la semana)
        from datetime import date, timedelta
        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        dia_index = dias_semana.index(self.day)
        hoy = date.today()
        dias_hasta_dia = (dia_index - hoy.weekday()) % 7
        if dias_hasta_dia == 0:
            dias_hasta_dia = 7
        fecha_vencimiento = hoy + timedelta(days=dias_hasta_dia)
        # Crear la tarea
        tarea = Task.objects.create(
            nombre=self.activity_text,
            descripcion=self.notes or f"Actividad del horario: {self.activity_text}",
            fecha_vencimiento=fecha_vencimiento,
            estado='pendiente',
            prioridad=prioridad,
            usuario=self.usuario,
            agregar_al_horario=False,
            dia_semana=self.day,
            hora_inicio=hora_inicio,
            duracion_minutos=60
        )
        # Asignar la tarea creada a este horario
        self.tarea_relacionada = tarea
        self._syncing_from_task = True
        print(f"[DEBUG][_crear_tarea_desde_horario] self.pk={self.pk}, tarea_relacionada={self.tarea_relacionada}")
        if self.pk:
            print("[DEBUG][_crear_tarea_desde_horario] Usando save(update_fields=['tarea_relacionada'])")
            super().save(update_fields=['tarea_relacionada'])
        else:
            print("[DEBUG][_crear_tarea_desde_horario] Usando save() normal")
            super().save()
    
    def _actualizar_tarea_desde_horario(self):
        """Actualiza la tarea relacionada con los datos del horario"""
        if not self.tarea_relacionada:
            return
            
        # Extraer hora de inicio
        hora_inicio_str = self.time_slot.split('-')[0]
        try:
            hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        except ValueError:
            return
        
        # Actualizar la tarea sin disparar la sincronización inversa
        self.tarea_relacionada._syncing_from_schedule = True
        self.tarea_relacionada.nombre = self.activity_text
        self.tarea_relacionada.descripcion = self.notes or f"Actividad del horario: {self.activity_text}"
        self.tarea_relacionada.dia_semana = self.day
        self.tarea_relacionada.hora_inicio = hora_inicio
        self.tarea_relacionada.save()
        delattr(self.tarea_relacionada, '_syncing_from_schedule')

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
    
    def save(self, *args, **kwargs):
        print(f"[DEBUG][Task.save] Guardando tarea: {self.nombre}, agregar_al_horario={self.agregar_al_horario}, dia_semana={self.dia_semana}, hora_inicio={self.hora_inicio}")
        if hasattr(self, '_syncing_from_schedule'):
            print("[DEBUG][Task.save] _syncing_from_schedule detectado, guardado directo.")
            super().save(*args, **kwargs)
            return
        super().save(*args, **kwargs)
        if self.agregar_al_horario and self.dia_semana and self.hora_inicio:
            print("[DEBUG][Task.save] Llamando a _actualizar_actividad_horario")
            self._actualizar_actividad_horario()
        elif not self.agregar_al_horario:
            print("[DEBUG][Task.save] Llamando a _eliminar_actividad_horario")
            self._eliminar_actividad_horario()
    
    def _actualizar_actividad_horario(self):
        print(f"[DEBUG][_actualizar_actividad_horario] Ejecutando para tarea: {self.nombre}, usuario={self.usuario}, dia_semana={self.dia_semana}, hora_inicio={self.hora_inicio}, duracion_minutos={self.duracion_minutos}")
        if not self.dia_semana or not self.hora_inicio:
            print("[DEBUG][_actualizar_actividad_horario] Faltan campos requeridos, no se crea Schedule.")
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
        # Enlazar la tarea relacionada y guardar
        schedule.tarea_relacionada = self
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
