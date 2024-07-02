from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TaskForm, ProjectForm
from django.contrib.auth import login, authenticate, logout
from .models import Task, Project


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('project_task_list')  # перенаправление на страницу проектов и задач
    else:
        form = CustomAuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'tasks/home.html')

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # Устанавливаем текущего пользователя как владельца задачи
            task.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')  # Перенаправление на список задач после удаления
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_list(request):
    user = request.user
    tasks = Task.objects.filter(assigned_to=user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  # Устанавливаем текущего пользователя как владельца проекта
            project.save()
            return redirect('project_task_list')  #  перенаправление на страницу проектов и задач
    else:
        form = ProjectForm()
    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def project_task_list(request):
    projects = Project.objects.filter(owner=request.user)
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/project_task_list.html', {'projects': projects, 'tasks': tasks})



@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'tasks/project_detail.html', {'project': project})

@login_required
def project_update_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/project_form.html', {'form': form})

@login_required
def project_delete_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        # Обработка удаления проекта
        project.delete()
        return redirect('project_task_list')  # Перенаправление на список проектов после удаления

    return render(request, 'tasks/project_confirm_delete.html', {'project': project})
