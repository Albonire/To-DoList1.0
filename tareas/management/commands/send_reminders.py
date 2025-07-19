from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
from tareas.models import Task
from datetime import date, timedelta
from django.conf import settings
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Envía recordatorios por correo para las tareas que vencen pronto.'

    def handle(self, *args, **options):
        tomorrow = date.today() + timedelta(days=1)
        
        # Tareas que vencen mañana, que no están completadas y de las que no se ha enviado recordatorio
        tasks_to_remind = Task.objects.filter(
            fecha_vencimiento=tomorrow,
            estado__in=['pendiente', 'en_progreso'],
            recordatorio_enviado=False
        )

        if not tasks_to_remind.exists():
            self.stdout.write(self.style.SUCCESS('No hay tareas que necesiten un recordatorio para mañana.'))
            return

        self.stdout.write(f'Encontradas {tasks_to_remind.count()} tareas para recordar...')

        for task in tasks_to_remind:
            user = task.usuario
            if user.email:
                subject = f'Recordatorio de tarea: {task.nombre}'
                
                # Usaremos una plantilla de Django para el correo
                message = render_to_string('tareas/email/reminder_email.txt', {
                    'user': user,
                    'task': task,
                })

                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    
                    # Marcar como enviado
                    task.recordatorio_enviado = True
                    task.save()
                    
                    self.stdout.write(self.style.SUCCESS(f'Correo enviado para la tarea "{task.nombre}" a {user.email}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al enviar correo para la tarea "{task.nombre}": {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'La tarea "{task.nombre}" no tiene un usuario con email.'))

        self.stdout.write(self.style.SUCCESS('Proceso de recordatorios finalizado.'))
