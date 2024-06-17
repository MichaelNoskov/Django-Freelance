"""
This module defines the URL routes for the Django application.

The routes are defined in the `urlpatterns` list. Django will use this list to route requests based on the URL.

The module also sets up a default router for the Django Rest Framework (DRF) and registers several viewsets with it.

The DRF router will automatically generate appropriate URLs for the registered viewsets.
"""

from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from . import views

urlpatterns = (
    path('', views.main_page, name='main_page'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(next_page=reverse_lazy('profile')), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path(
        'become-human/',
        views.DeveloperCreatingView.as_view(),
        name='developer_evolution',
    ),
    path('dev-tasks/', views.DeveloperTasksView.as_view(), name='dev_tasks'),
    path('my-tasks/', views.OwnerTasksView.as_view(), name='my_tasks'),
    path('task/<uuid:pk>', views.TaskAdministrating.as_view(), name='task'),
    path('add-task', views.TaskCreatingView.as_view(), name='add_task'),
    path('comment/<uuid:pk>', views.CommentCreatingView.as_view(), name='add_comment'),
    path('edit-task/<uuid:pk>', views.EditStatusView.as_view(), name='edit_task'),
)
