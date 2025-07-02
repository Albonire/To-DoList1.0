from django import forms
from .models import Task, Schedule
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'fecha_hora_inicio', 'fecha_hora_vencimiento', 'estado', 'prioridad', 'agregar_al_horario', 'dia_semana', 'hora_inicio', 'duracion_minutos']
        widgets = {
            'fecha_vencimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': (date.today() - timedelta(days=365)).strftime('%Y-%m-%d'),  # 1 año atrás
                    'max': (date.today() + timedelta(days=365*5)).strftime('%Y-%m-%d'),  # 5 años adelante
                },
                format='%Y-%m-%d'
            ),
            'fecha_hora_inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'fecha_hora_vencimiento': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'hora_inicio': forms.TimeInput(
                attrs={
                    'type': 'time',
                },
                format='%H:%M'
            ),
            'duracion_minutos': forms.NumberInput(
                attrs={
                    'min': '15',
                    'max': '480',
                    'step': '15'
                }
            ),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos de horario condicionales
        self.fields['dia_semana'].required = False
        self.fields['hora_inicio'].required = False
        self.fields['duracion_minutos'].required = False

    def clean_fecha_vencimiento(self):
        fecha = self.cleaned_data.get('fecha_vencimiento')
        if fecha:
            # Validar que la fecha no sea muy lejana (opcional)
            if fecha > date.today() + timedelta(days=365*5):  # 5 años en el futuro
                raise ValidationError("La fecha no puede ser mayor a 5 años en el futuro.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_hora_inicio')
        fecha_venc = cleaned_data.get('fecha_hora_vencimiento')
        agregar_al_horario = cleaned_data.get('agregar_al_horario')
        dia_semana = cleaned_data.get('dia_semana')
        hora_inicio = cleaned_data.get('hora_inicio')
        
        if fecha_inicio and fecha_venc and fecha_inicio > fecha_venc:
            raise ValidationError(_('La fecha y hora de inicio no puede ser posterior a la de vencimiento.'))
        
        # Validar que si se marca agregar al horario, se completen los campos necesarios
        if agregar_al_horario:
            if not dia_semana:
                raise ValidationError(_('Debe seleccionar un día de la semana para agregar al horario.'))
            if not hora_inicio:
                raise ValidationError(_('Debe especificar una hora de inicio para agregar al horario.'))
        
        return cleaned_data

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['time_slot', 'day', 'activity_text', 'activity_type', 'notes']
        widgets = {
            'time_slot': forms.TextInput(
                attrs={
                    'placeholder': 'ej: 09:00-12:00',
                    'pattern': r'\d{1,2}:\d{2}-\d{1,2}:\d{2}',
                    'title': 'Formato: HH:MM-HH:MM'
                }
            ),
            'activity_text': forms.TextInput(
                attrs={
                    'placeholder': 'Descripción de la actividad'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Notas adicionales...'
                }
            ),
        }

    def clean_time_slot(self):
        time_slot = self.cleaned_data.get('time_slot')
        if time_slot:
            # Validar formato HH:MM-HH:MM
            import re
            if not re.match(r'^\d{1,2}:\d{2}-\d{1,2}:\d{2}$', time_slot):
                raise ValidationError(_('El formato debe ser HH:MM-HH:MM (ej: 09:00-12:00)'))
            
            # Validar que la hora de inicio sea menor que la de fin
            start, end = time_slot.split('-')
            start_hour, start_min = map(int, start.split(':'))
            end_hour, end_min = map(int, end.split(':'))
            
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            if start_minutes >= end_minutes:
                raise ValidationError(_('La hora de inicio debe ser anterior a la hora de fin'))
        
        return time_slot
