from datetime import datetime, date
from .models import Task

def greeting_context_processor(request):
    """
    Proporciona un saludo dinámico y un recuento de las tareas de hoy.
    """
    context = {}
    
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        context['greeting'] = "Good morning"
    elif 12 <= current_hour < 19:
        context['greeting'] = "Good afternoon"
    else:
        context['greeting'] = "Good evening"
        
    if request.user.is_authenticated:
        tasks_today_count = Task.objects.filter(
            usuario=request.user,
            fecha_vencimiento=date.today(),
            estado='pendiente'
        ).count()
        context['tasks_today_count'] = tasks_today_count
    else:
        context['tasks_today_count'] = 0

    return context
