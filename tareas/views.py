import json
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
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

@login_required
def schedule_view(request):
    days_of_week = Task.DAYS_OF_WEEK
    time_slots = [f"{h:02d}:00" for h in range(7, 23)]  # 7:00 to 22:00

    tasks = Task.objects.filter(
        usuario=request.user,
        dia_semana__isnull=False,
        hora_inicio__isnull=False
    )

    schedule_data = {}
    for task in tasks:
        time_slot_key = task.hora_inicio.strftime('%H:00')
        
        if time_slot_key not in schedule_data:
            schedule_data[time_slot_key] = {}
        
        schedule_data[time_slot_key][task.dia_semana] = {
            'text': task.nombre,
            'type': 'task',
            'notes': task.descripcion,
            'has_task': True,
            'task_info': {
                'id': task.id,
                'nombre': task.nombre,
                'estado': task.get_estado_display(),
                'prioridad': task.get_prioridad_display(),
                'fecha_vencimiento': task.fecha_vencimiento.isoformat() if task.fecha_vencimiento else None,
            }
        }

    context = {
        'schedule_data_json': json.dumps(schedule_data, default=json_serial),
        'days_of_week': days_of_week,
        'time_slots': time_slots,
        'schedule_data': schedule_data,
    }
    
    return render(request, 'tareas/schedule.html', context)
