from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.fecha_hora_inicio and self.fecha_hora_vencimiento:
            if self.fecha_hora_inicio > self.fecha_hora_vencimiento:
                from django.core.exceptions import ValidationError
                raise ValidationError(_('La fecha y hora de inicio no puede ser posterior a la de vencimiento.'))

# Create your models here.
