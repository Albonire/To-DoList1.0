from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tarea/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tarea/nueva/', views.TaskCreateView.as_view(), name='task-create'),
    path('tarea/<int:pk>/editar/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tarea/<int:pk>/eliminar/', views.TaskDeleteView.as_view(), name='task-delete'),
    
    # URLs para el horario
    path('horario/', views.ScheduleView.as_view(), name='schedule'),
    path('horario/nuevo/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('horario/<int:pk>/editar/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('horario/<int:pk>/eliminar/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('horario/api/save/', views.save_schedule_activity, name='schedule-save-api'),
]
