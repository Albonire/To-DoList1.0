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
        from datetime import date
        queryset = Task.objects.filter(usuario=self.request.user).order_by('fecha_vencimiento')
        
        estado = self.request.GET.get('estado')
        if estado:
            if estado == 'completada':
                queryset = queryset.filter(estado='completada')
            elif estado == 'pendiente':
                queryset = queryset.filter(estado='pendiente', fecha_vencimiento__gte=date.today())
            elif estado == 'vencida':
                queryset = queryset.filter(estado='pendiente', fecha_vencimiento__lt=date.today())

        prioridad = self.request.GET.get('prioridad')
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

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
@require_POST
def toggle_task_complete(request, pk):
    """
    Cambia el estado de una tarea entre 'completada' y 'pendiente'.
    """
    try:
        task = Task.objects.get(pk=pk, usuario=request.user)
        
        if task.estado == 'completada':
            task.estado = 'pendiente' # Vuelve a pendiente al desmarcar
            message = "Tarea marcada como 'Pendiente'."
        else:
            task.estado = 'completada'
            message = "¡Tarea completada!"
            
        task.save()
        
        # Devuelve el estado dinámico para que el frontend se actualice correctamente
        return JsonResponse({'success': True, 'message': message, 'estado': task.dynamic_status})

    except Task.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Tarea no encontrada o no tienes permiso para editarla.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Ha ocurrido un error inesperado: {e}'}, status=500)

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
        'dia_semana',
        'hora_inicio',
        'duracion_minutos',
        'prioridad'  # Pasamos la prioridad para usarla en las clases CSS
    )

    tasks_list = []
    for task in tasks:
        task['hora_inicio'] = task['hora_inicio'].strftime('%H:%M')
        tasks_list.append(task)

    context = {
        'tasks_json': json.dumps(tasks_list),
    }
    
    return render(request, 'tareas/schedule.html', context)