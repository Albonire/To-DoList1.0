from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError

# Create your tests here.

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_creacion_tarea_valida(self):
        tarea = Task.objects.create(
            nombre='Tarea de prueba',
            descripcion='Descripción',
            fecha_vencimiento=date.today(),
            fecha_hora_inicio=datetime.now(),
            fecha_hora_vencimiento=datetime.now() + timedelta(hours=1),
            estado='pendiente',
            prioridad='media',
            usuario=self.user
        )
        self.assertEqual(str(tarea), 'Tarea de prueba')

    def test_fecha_inicio_posterior_a_vencimiento(self):
        tarea = Task(
            nombre='Tarea inválida',
            descripcion='Descripción',
            fecha_vencimiento=date.today(),
            fecha_hora_inicio=datetime.now() + timedelta(hours=2),
            fecha_hora_vencimiento=datetime.now(),
            estado='pendiente',
            prioridad='media',
            usuario=self.user
        )
        with self.assertRaises(ValidationError):
            tarea.clean()
