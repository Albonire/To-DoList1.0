from django import forms
from .models import Task, Task
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    # Definimos el campo de selección múltiple aquí para tener más control
    dia_semana = forms.MultipleChoiceField(
        choices=Task.DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        label=_("Días de la semana"),
        required=False
    )

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
        dias_semana = cleaned_data.get('dia_semana')
        hora_inicio = cleaned_data.get('hora_inicio')
        
        # Si se especifica al menos un día, la hora también es requerida.
        if dias_semana and not hora_inicio:
            self.add_error('hora_inicio', _('Debe especificar una hora de inicio si selecciona uno o más días.'))
        
        # Si se especifica una hora, al menos un día también es requerido.
        if hora_inicio and not dias_semana:
            self.add_error('dia_semana', _('Debe seleccionar al menos un día si especifica una hora.'))
            
        return cleaned_data
