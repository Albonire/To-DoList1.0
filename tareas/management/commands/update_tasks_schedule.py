from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tareas.models import Task

class Command(BaseCommand):
    help = 'Update existing tasks to enable schedule integration'

    def handle(self, *args, **options):
        # For simplicity, update tasks for all users
        users = User.objects.all()
        total_updated = 0
        for user in users:
            tasks = Task.objects.filter(usuario=user)
            for task in tasks:
                if task.dia_semana and task.hora_inicio:
                    if not task.agregar_al_horario:
                        task.agregar_al_horario = True
                        task.save()
                        total_updated += 1
                        self.stdout.write(f'Updated task {task.id} for user {user.username}')
                else:
                    self.stdout.write(f'Skipped task {task.id} for user {user.username} (missing dia_semana or hora_inicio)')
        self.stdout.write(self.style.SUCCESS(f'Total tasks updated: {total_updated}'))
