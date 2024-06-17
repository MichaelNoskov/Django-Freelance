"""
This module contains form classes for the User, Task, Comment, and Developer models.

Each form class extends forms.ModelForm and has a nested Meta class that defines the model and fields for the form.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Comment, Developer, Task


class RegistrationForm(UserCreationForm):
    """
    Form for creating User instances.

    The form uses the Task model and includes the 'username', 'password1' and 'password2' fields.
    """

    class Meta:
        """Configuration class for Registration form."""

        model = User
        fields = ('username', 'password1', 'password2')


class DeveloperCreatigForm(ModelForm):
    """
    Form for creating Developer instances.

    The form uses the Task model and includes the 'position' field.
    """

    class Meta:
        """Configuration class for Developer form."""

        model = Developer
        fields = ('position',)


class CommentForm(ModelForm):
    """
    Form for creatingComment instances.

    The form uses the Task model and includes the 'comment_content' field.
    """

    class Meta:
        """Configuration class for Comment form."""

        model = Comment
        fields = ('comment_content',)


class TaskForm(ModelForm):
    """
    Form for creating Task instances.

    The form uses the Task model and includes the 'name', 'description', 'status' and 'developers' fields.
    """

    class Meta:
        """Configuration class for Task form."""

        model = Task
        fields = ('name', 'description', 'status', 'developers', 'created')


class TaskEditForm(ModelForm):
    """
    Form for updating Task instances.

    The form uses the Task model and includes the 'status' field.
    """

    class Meta:
        """Configuration class for Task form."""

        model = Task
        fields = ('status',)
