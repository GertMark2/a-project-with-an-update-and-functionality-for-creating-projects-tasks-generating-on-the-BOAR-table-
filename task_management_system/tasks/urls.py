from django.urls import path
from .views import register_view, login_view, logout_view, home_view, task_create, task_detail, task_update, task_delete, task_list,project_create_view,project_task_list,project_task_list,project_detail_view,project_update_view,project_delete_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('task/create/', task_create, name='task_create'),  # Используем task_create вместо task_create_view
    path('task/<int:pk>/', task_detail, name='task_detail'),
    path('task/<int:pk>/update/', task_update, name='task_update'),
    path('task/<int:pk>/delete/', task_delete, name='task_delete'),
    path('tasks/', task_list, name='task_list'),
    path('project/create/', project_create_view, name='project_create'),
    path('projects-and-tasks/', project_task_list, name='project_task_list'),
    path('projects/',project_task_list, name='project_task_list'),
    path('project/<int:pk>/',project_detail_view, name='project_detail'),
    path('project/<int:pk>/update/',project_update_view, name='project_update'),
    path('project/<int:pk>/delete/',project_delete_view, name='project_delete'),
]
