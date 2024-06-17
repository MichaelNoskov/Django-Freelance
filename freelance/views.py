"""This module contains the views for the application."""

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rest_framework.viewsets import ModelViewSet

from . import forms, models, serializers
from .permissions import AdminOrReadOnlyPermission, UserPermission


class OwnerRequiredMixin(ModelViewSet):
    """Mixin that adds an owner field."""

    def perform_create(self, serializer):
        """
        Create owner.

        Args:
            serializer: some serializer.
        """
        serializer.save(owner=self.request.user)

    permission_classes = (UserPermission,)

    class Meta:
        """Configuration class for owner mixin."""

        abstract = True


class LoginRequiredEditedMixin(LoginRequiredMixin):
    """Mixin that edits a login_url field."""

    login_url = reverse_lazy('login')

    class Meta:
        """Configuration class for login mixin."""

        abstract = True


class TaskViewSet(OwnerRequiredMixin):
    """API endpoint that allows tasks to be viewed."""

    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()


class StatusViewSet(ModelViewSet):
    """API endpoint that allows statuses to be viewed."""

    serializer_class = serializers.StatusSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    queryset = models.Status.objects.all()


class PositionViewSet(ModelViewSet):
    """API endpoint that allows posittions to be viewed."""

    serializer_class = serializers.PositionSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    queryset = models.Position.objects.all()


class CommentViewSet(ModelViewSet):
    """API endpoint that allows comments to be viewed."""

    def perform_create(self, serializer):
        """
        Create owner.

        Args:
            serializer: some serializer.
        """
        developer = models.Developer.objects.filter(developer=self.request.user).first()
        serializer.save(owner=developer)

    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()


class UserRegistrationView(CreateView):
    """API endpoint that allows users to register."""

    template_name = 'registration/register.html'
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredEditedMixin, DetailView):
    """API endpoint that allows users to watch theirs account profiles."""

    model = User
    template_name = 'profile.html'

    def get_object(self):
        """
        Get user object to render.

        Returns:
            user: asked user.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        """
        Add the data to the profile request's content.

        Args:
            kwargs: keyword args.

        Returns:
            context: some context data.
        """
        context = super().get_context_data(**kwargs)
        context['developer'] = models.Developer.objects.filter(
            developer=self.request.user.id,
        ).first()
        return context


class DeveloperTasksView(LoginRequiredEditedMixin, ListView):
    """API endpoint that allows developer's tasks to be viewed."""

    def get(self, request):
        """
        Get developer and queryset to render.

        Args:
            request: request object.

        Returns:
            response: HHTTPResponse.
        """
        self.developer = models.Developer.objects.filter(
            developer=self.request.user.id,
        ).first()
        self.queryset = [task.task for task in models.TaskDeveloper.objects.filter(
            developer=self.developer,
        )]
        return super().get(request)

    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks.html'


class OwnerTasksView(LoginRequiredEditedMixin, ListView):
    """API endpoint that allows your tasks to be viewed."""

    def get(self, request):
        """
        Get task object to render.

        Args:
            request: user's request.

        Returns:
            return: Response
        """
        self.queryset = models.Task.objects.filter(owner=request.user)
        return super().get(request)

    model = models.Task
    context_object_name = 'tasks'
    template_name = 'tasks.html'


class DeveloperCreatingView(LoginRequiredEditedMixin, CreateView):
    """API endpoint that allows developers to be created."""

    def get(self, request):
        """
        Redirect to the profile page if user allredy is a producer.

        Args:
            request: user's request.

        Returns:
            return: Response
        """
        if models.Developer.objects.filter(developer=request.user).first():
            return HttpResponseRedirect(reverse_lazy('profile'))
        return super().get(request)

    template_name = 'developer.html'
    form_class = forms.DeveloperCreatigForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        """
        Add existing fields to developer creating form.

        Args:
            form: some form

        Returns:
            return: Response
        """
        form.instance.developer = self.request.user
        return super().form_valid(form)


class CommentCreatingView(LoginRequiredEditedMixin, CreateView):
    """API endpoint that allows comments to be created."""

    template_name = 'solution.html'
    form_class = forms.CommentForm
    success_url = reverse_lazy('dev_tasks')

    def get_context_data(self, **kwargs):
        """
        Add the data to the comment creating request's content.

        Args:
            kwargs: keywoard args.

        Returns:
            context: context data
        """
        context = super().get_context_data(**kwargs)
        context['task_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        """
        Add existing fields to comment creation form.

        Args:
            form: some form.

        Returns:
            return: form validation.
        """
        form.instance.owner = models.Developer.objects.filter(
            developer=self.request.user,
        ).first()
        form.instance.task = models.Task.objects.filter(
            id=self.kwargs['pk'],
        ).first()
        return super().form_valid(form)


class TaskCreatingView(LoginRequiredEditedMixin, CreateView):
    """API endpoint that allows tasks to be created."""

    template_name = 'new_task.html'
    form_class = forms.TaskForm
    success_url = reverse_lazy('my_tasks')

    def form_valid(self, form):
        """
        Add existing fields to task creation form.

        Args:
            form: some form.

        Returns:
            return: Response
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class EditStatusView(LoginRequiredEditedMixin, UpdateView):
    """API endpoint that allows statuses to be edited."""

    model = models.Task
    template_name = 'edit.html'
    fields = ('status',)
    success_url = reverse_lazy('my_tasks')

    def get_context_data(self, **kwargs):
        """
        Add the data to the edit status request's content.

        Args:
            kwargs: keywoard args.

        Returns:
            context: context data.
        """
        context = super().get_context_data(**kwargs)
        context['task_id'] = self.kwargs['pk']
        return context


class TaskAdministrating(DetailView):
    """API endpoint that allows tasks to be viewd."""

    model = models.Task
    template_name = 'task.html'

    def get_context_data(self, **kwargs):
        """
        Add the data to the task request's content.

        Args:
            kwargs: keywoard args.

        Returns:
            context: context data.
        """
        context = super().get_context_data(**kwargs)
        context['developers'] = [
            dev.developer for dev in kwargs['object'].developers.all()
        ]
        return context


def log_out(request):
    """
    Veiw, that can logout users.

    Args:
        request: user's request.

    Returns:
        redirect: some another page.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('main_page')


def main_page(request):
    """
    Veiw, that redirects users to the main page.

    Args:
        request: user's request.

    Returns:
        redirect: some another page.
    """
    pages = {
    }
    return render(request, 'main.html', context={'pages': pages, 'title': 'Главная страница', 'user': request.user})
