import json
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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
            messages.success(request, '¡Tu cuenta ha sido creada! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tareas/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(usuario=self.request.user).order_by('fecha_vencimiento')
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
        
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tareas/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/task_form.html'
    success_url = reverse_lazy('task-list')
    success_message = "✅ ¡Tarea creada con éxito!"

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tareas/task_form.html'
    success_url = reverse_lazy('task-list')
    success_message = "📝 ¡Tarea actualizada correctamente!"

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tareas/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
    success_message = "🗑️ ¡Tarea eliminada!"

    def get_queryset(self):
        return Task.objects.filter(usuario=self.request.user)

@login_required
def schedule_view(request):
    """
    Prepara y muestra las tareas del usuario en una vista de horario.
    """
    tasks = Task.objects.filter(
        usuario=request.user,
        dia_semana__isnull=False,
        hora_inicio__isnull=False
    ).values(
        'id',
        'nombre',
        'descripcion',
        'dia_semana',
        'hora_inicio',
        'duracion_minutos'
    )

    tasks_list = []
    for task in tasks:
        task['hora_inicio'] = task['hora_inicio'].strftime('%H:%M')
        tasks_list.append(task)

    context = {
        'tasks_json': json.dumps(tasks_list),
    }
    
    return render(request, 'tareas/schedule.html', context)