from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'estado', 'prioridad', 'fecha_vencimiento')
    list_filter = ('estado', 'prioridad', 'usuario', 'dia_semana')
    search_fields = ('nombre', 'descripcion')
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'usuario')
        }),
        ('Fechas y estado', {
            'fields': ('fecha_vencimiento', 'estado', 'prioridad')
        }),
        ('Integración con horario', {
            'fields': ('dia_semana', 'hora_inicio', 'duracion_minutos'),
            'classes': ('collapse',)
        }),
    )

# Register your models here.
