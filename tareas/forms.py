from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'prioridad', 'dia_semana', 'hora_inicio', 'duracion_minutos']
        widgets = {
            'fecha_vencimiento': forms.DateInput(
                attrs={
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
            'hora_inicio': forms.TimeInput(
                attrs={
                    'type': 'text',
                    'class': 'time-picker-input',
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
        dia_semana = cleaned_data.get('dia_semana')
        hora_inicio = cleaned_data.get('hora_inicio')
        
        # Si se especifica un día, la hora también es requerida.
        if dia_semana and not hora_inicio:
            self.add_error('hora_inicio', _('Debe especificar una hora de inicio si selecciona un día.'))
        
        # Si se especifica una hora, el día también es requerido.
        if hora_inicio and not dia_semana:
            self.add_error('dia_semana', _('Debe seleccionar un día si especifica una hora.'))
            
        return cleaned_data
