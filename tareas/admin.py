from django.contrib import admin
from .models import Task, Schedule

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'estado', 'prioridad', 'fecha_vencimiento', 'fecha_hora_vencimiento', 'agregar_al_horario')
    list_filter = ('estado', 'prioridad', 'usuario', 'fecha_hora_vencimiento', 'agregar_al_horario', 'dia_semana')
    search_fields = ('nombre', 'descripcion')
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'usuario')
        }),
        ('Fechas y estado', {
            'fields': ('fecha_vencimiento', 'fecha_hora_inicio', 'fecha_hora_vencimiento', 'estado', 'prioridad')
        }),
        ('Integración con horario', {
            'fields': ('agregar_al_horario', 'dia_semana', 'hora_inicio', 'duracion_minutos'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'day', 'time_slot', 'activity_text', 'activity_type')
    list_filter = ('activity_type', 'day', 'usuario')
    search_fields = ('activity_text', 'notes', 'usuario__username')
    ordering = ('day', 'time_slot')

# Register your models here.
