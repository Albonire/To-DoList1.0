from django.contrib import admin
from .models import Task, Schedule

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'estado', 'prioridad', 'fecha_vencimiento', 'agregar_al_horario', 'tarea_en_horario')
    list_filter = ('estado', 'prioridad', 'usuario', 'agregar_al_horario', 'dia_semana')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('tarea_en_horario',)
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'usuario')
        }),
        ('Fechas y estado', {
            'fields': ('fecha_vencimiento', 'estado', 'prioridad')
        }),
        ('Integración con horario', {
            'fields': ('agregar_al_horario', 'dia_semana', 'hora_inicio', 'duracion_minutos', 'tarea_en_horario'),
            'classes': ('collapse',)
        }),
    )
    
    def tarea_en_horario(self, obj):
        """Muestra si la tarea está en el horario y su información"""
        if obj.agregar_al_horario and obj.dia_semana and obj.hora_inicio:
            return f"Sí - {obj.dia_semana} {obj.hora_inicio}"
        return "No"
    tarea_en_horario.short_description = 'En horario'

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'day', 'time_slot', 'activity_text', 'activity_type', 'tarea_relacionada_info')
    list_filter = ('day', 'activity_type', 'usuario')
    search_fields = ('activity_text', 'notes')
    readonly_fields = ('tarea_relacionada_info',)
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'day', 'time_slot', 'activity_text', 'activity_type')
        }),
        ('Detalles', {
            'fields': ('notes', 'tarea_relacionada', 'tarea_relacionada_info')
        }),
    )
    
    def tarea_relacionada_info(self, obj):
        """Muestra información de la tarea relacionada"""
        if obj.tarea_relacionada:
            tarea = obj.tarea_relacionada
            return f"{tarea.nombre} ({tarea.estado}, {tarea.prioridad})"
        return "Sin tarea relacionada"
    tarea_relacionada_info.short_description = 'Tarea relacionada'

# Register your models here.
