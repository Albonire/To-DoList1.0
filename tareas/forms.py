from django import forms
from .models import Task
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['nombre', 'descripcion', 'fecha_vencimiento', 'fecha_hora_inicio', 'fecha_hora_vencimiento', 'estado', 'prioridad']
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
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

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
        if fecha_inicio and fecha_venc and fecha_inicio > fecha_venc:
            raise ValidationError(_('La fecha y hora de inicio no puede ser posterior a la de vencimiento.'))
        return cleaned_data
