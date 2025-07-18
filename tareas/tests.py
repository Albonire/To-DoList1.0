from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from datetime import date, time

# Create your tests here.

class TaskModelTest(TestCase):
    def setUp(self):
        """Set up a user for the tests."""
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_creacion_tarea_valida(self):
        """Test that a valid task can be created."""
        tarea = Task.objects.create(
            nombre='Tarea de prueba',
            descripcion='Descripción de la tarea.',
            fecha_vencimiento=date.today(),
            estado='pendiente',
            prioridad='media',
            usuario=self.user,
            dia_semana='Monday',
            hora_inicio=time(9, 0),
            duracion_minutos=60
        )
        self.assertEqual(str(tarea), 'Tarea de prueba')
        self.assertEqual(tarea.usuario, self.user)
        self.assertEqual(Task.objects.count(), 1)

    def test_str_representation(self):
        """Test the string representation of the Task model."""
        tarea = Task.objects.create(
            nombre='Mi Tarea Especial',
            descripcion='Descripción.',
            fecha_vencimiento=date.today(),
            usuario=self.user
        )
        self.assertEqual(str(tarea), 'Mi Tarea Especial')
