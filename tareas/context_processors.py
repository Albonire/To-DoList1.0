from datetime import datetime

def greeting_context_processor(request):
    """
    Proporciona un saludo dinámico basado en la hora del día.
    """
    greeting = "Hola"
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Buenos días"
    elif 12 <= current_hour < 19:
        greeting = "Buenas tardes"
    else:
        greeting = "Buenas noches"
        
    return {
        'greeting': greeting
    }
