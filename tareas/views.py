import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Task, Schedule
from .forms import TaskForm, ScheduleForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import datetime

def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tareas/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(usuario=self.request.user)
        estado = self.request.GET.get('estado')
        prioridad = self.request.GET.get('prioridad')
        if estado:
            queryset = queryset.filter(estado=estado)
        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        return queryset

    def get_context_data(self, **kwargs):
        from datetime import date, timedelta
        context = super().get_context_data(**kwargs)
            
        context['estados'] = Task.ESTADO_CHOICES
        context['prioridades'] = Task.PRIORIDAD_CHOICES
        context['estado_actual'] = self.request.GET.get('estado', '')
        context['prioridad_actual'] = self.request.GET.get('prioridad', '')
        context['today'] = date.today()
        context['soon'] = date.today() + timedelta(days=2)
        
        tasks_list = list(Task.objects.filter(usuario=self.request.user).values())
        for task in tasks_list:
            for k, v in task.items():
                if isinstance(v, (datetime.date, datetime.time, datetime.datetime)):
                    task[k] = v.isoformat()
        context['tasks_json'] = json.dumps(tasks_list, default=json_serial)
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tareas/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/task_form.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tareas/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class ScheduleView(LoginRequiredMixin, ListView):
    model = Schedule
    template_name = 'tareas/schedule.html'
    context_object_name = 'schedules'

    def get_queryset(self):
        return Schedule.objects.filter(usuario=self.request.user).order_by('time_slot', 'day')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Organizar datos para el JavaScript
        schedule_data = {}
        for schedule in context['schedules']:
            if schedule.time_slot not in schedule_data:
                schedule_data[schedule.time_slot] = {}
            
            # Serializar fecha_vencimiento y otros posibles campos de tipo date/time
            task_info = None
            if schedule.tarea_relacionada:
                task_info = {
                    'id': schedule.tarea_relacionada.id,
                    'nombre': schedule.tarea_relacionada.nombre,
                    'estado': schedule.tarea_relacionada.estado,
                    'prioridad': schedule.tarea_relacionada.prioridad,
                    'fecha_vencimiento': schedule.tarea_relacionada.fecha_vencimiento.isoformat() if schedule.tarea_relacionada.fecha_vencimiento else None,
                }
            schedule_data[schedule.time_slot][schedule.day] = {
                'text': schedule.activity_text,
                'type': schedule.activity_type,
                'notes': schedule.notes,
                'has_task': schedule.tarea_relacionada is not None,
                'task_info': task_info
            }
        
        context['schedule_data_json'] = json.dumps(schedule_data, default=json_serial)
        context['activity_types'] = Schedule.ACTIVITY_TYPES
        context['days_of_week'] = Schedule.DAYS_OF_WEEK
        
        return context

class ScheduleCreateView(LoginRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'tareas/schedule_form.html'
    success_url = reverse_lazy('schedule')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ScheduleUpdateView(LoginRequiredMixin, UpdateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = 'tareas/schedule_form.html'
    success_url = reverse_lazy('schedule')

    def get_queryset(self):
        return Schedule.objects.filter(usuario=self.request.user)

class ScheduleDeleteView(LoginRequiredMixin, DeleteView):
    model = Schedule
    template_name = 'tareas/schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule')

    def get_queryset(self):
        return Schedule.objects.filter(usuario=self.request.user)

# Vista API para guardar actividades del horario via AJAX
@login_required
def save_schedule_activity(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            time_slot = data.get('time_slot')
            day = data.get('day')
            activity_text = data.get('text', '').strip()
            activity_type = data.get('type', 'other')
            notes = data.get('notes', '').strip()
            
            if not time_slot or not day:
                return JsonResponse({'error': 'Faltan datos requeridos'}, status=400)
            
            # Buscar actividad existente o crear nueva
            schedule, created = Schedule.objects.get_or_create(
                usuario=request.user,
                time_slot=time_slot,
                day=day,
                defaults={
                    'activity_text': activity_text,
                    'activity_type': activity_type,
                    'notes': notes
                }
            )
            
            if not created:
                # Actualizar actividad existente
                if not activity_text:
                    # Si no hay texto, eliminar la actividad
                    schedule.delete()
                    return JsonResponse({'status': 'deleted'})
                else:
                    schedule.activity_text = activity_text
                    schedule.activity_type = activity_type
                    schedule.notes = notes
                    schedule.save()
            
            return JsonResponse({'status': 'success'})
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Datos JSON inválidos'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vista para mostrar tareas relacionadas con horarios
@login_required
def tasks_with_schedule(request):
    """Vista para mostrar tareas que están integradas con el horario"""
    tasks_with_schedule = Task.objects.filter(
        usuario=request.user,
        agregar_al_horario=True
    ).order_by('dia_semana', 'hora_inicio')
    
    tasks_without_schedule = Task.objects.filter(
        usuario=request.user,
        agregar_al_horario=False
    ).order_by('fecha_vencimiento')
    
    context = {
        'tasks_with_schedule': tasks_with_schedule,
        'tasks_without_schedule': tasks_without_schedule,
        'days_of_week': Schedule.DAYS_OF_WEEK,
    }
    
    return render(request, 'tareas/tasks_with_schedule.html', context)
