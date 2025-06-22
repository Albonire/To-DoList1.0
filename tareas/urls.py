from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('tarea/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tarea/nueva/', views.TaskCreateView.as_view(), name='task-create'),
    path('tarea/<int:pk>/editar/', views.TaskUpdateView.as_view(), name='task-update'),
    path('tarea/<int:pk>/eliminar/', views.TaskDeleteView.as_view(), name='task-delete'),
]
