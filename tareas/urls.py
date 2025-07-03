from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/new/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    
    # URLs para el horario
    path('schedule/', views.ScheduleView.as_view(), name='schedule'),
    path('schedule/new/', views.ScheduleCreateView.as_view(), name='schedule-create'),
    path('schedule/<int:pk>/edit/', views.ScheduleUpdateView.as_view(), name='schedule-update'),
    path('schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule-delete'),
    path('schedule/save-api/', views.save_schedule_activity, name='schedule-save-api'),
]
