from datetime import datetime, date
from .models import Task

def greeting_context_processor(request):
    """
    Proporciona un saludo dinámico y un recuento de las tareas de hoy.
    """
    context = {}
    
    # Saludo dinámico
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        context['greeting'] = "Buenos días"
    elif 12 <= current_hour < 19:
        context['greeting'] = "Buenas tardes"
    else:
        context['greeting'] = "Buenas noches"
        
    # Recuento de tareas para hoy (solo para usuarios autenticados)
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
