"""
This module defines the data models for the application.

It includes models for tasks, developers, positions, statuses and comments.
It also includes several utility classes and validation functions.

Each model is a Django model, which means it corresponds to a database table.
The fields on each model represent the columns in the database table,
and each instance of the model represents a row in the table.

The utility classes include mixins for adding a UUID primary key field
and a foreign key to the User model to other models.

The validation functions are used to ensure that the data stored in the models is valid.
They are used as validators on the appropriate model fields.
"""

from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

NAME = 'name'
STATUS = 'status'
TASK = 'task'
DEVELOPER = 'developer'
POSITION = 'position'


def time_traveler_trap(checking_date) -> None:
    """
    Validate that the provided date is not in the past.

    Args:
        checking_date (date): The date to validate.

    Raises:
        ValidationError: If the date is in the past.
    """
    if checking_date > timezone.now():
        raise ValidationError(
            'Date should be in the past',
        )


class UUIDMixin(models.Model):
    """Abstract base class that adds a UUID primary key field."""

    id = models.UUIDField(
        primary_key=True,
        blank=True,
        editable=False,
        default=uuid4,
    )

    class Meta:
        """Configuration class for UUIDMixin model."""

        abstract = True


class CategorialParametr(UUIDMixin):
    """Abstract base class that adds a name field and __str__ method."""

    name: models.TextField

    def __str__(self) -> str:
        """
        Return a string representation of the categorial object.

        Returns:
            str: A string representation of the categorial object.
        """
        return self.name

    class Meta:
        """Configuration class for CategorialParametr model."""

        abstract = True


class Task(UUIDMixin):
    """
    Model representing a task.

    Each task has a name, description, owner and status, and is associated with multiple developers.
    """

    name = models.TextField(_(NAME))
    description = models.TextField(_('description'), blank=True)
    owner = models.ForeignKey(User, verbose_name=_('owner'), on_delete=models.CASCADE)
    developers = models.ManyToManyField(
        'Developer',
        verbose_name=_('developers'),
        through='TaskDeveloper',
    )
    status = models.ForeignKey(
        'Status',
        verbose_name=_(STATUS),
        null=True,
        on_delete=models.SET_NULL,
    )
    created = models.DateTimeField(
        _('creation time'), default=timezone.now, validators=(time_traveler_trap,),
    )

    def save(self, *args, **kwargs) -> None:
        """
        Save object.

        Args:
            args: position args;
            kwargs: keyword args.

        Returns:
            return: saving.
        """
        time_traveler_trap(self.created)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: A string representation of the task.
        """
        return f'"{self.name}": {self.status}'

    class Meta:
        """Configuration class for Task model."""

        db_table = '"freelance"."task"'
        ordering = [NAME, STATUS]
        verbose_name = _(TASK)
        verbose_name_plural = _('tasks')


class Status(CategorialParametr):
    """
    Model representing a task status.

    Each status has a name (title).
    """

    name = models.TextField(_(STATUS), null=False, blank=False)

    def __str__(self) -> str:
        """
        Return a string representation of the status.

        Returns:
            str: A string representation of the status.
        """
        return self.name

    class Meta:
        """Configuration class for Status model."""

        db_table = '"freelance"."status"'
        ordering = [NAME]
        verbose_name = _(STATUS)
        verbose_name_plural = _('statuses')


class Developer(UUIDMixin):
    """
    Model representing a developer.

    Each developer is associated with one user, one position and multiple tasks.
    """

    developer = models.ForeignKey(User, verbose_name=_(DEVELOPER), on_delete=models.CASCADE)
    position = models.ForeignKey(
        'Position',
        verbose_name=_(POSITION),
        on_delete=models.SET_NULL,
        null=True,
    )
    tasks = models.ManyToManyField(
        'Task', verbose_name=_('tasks'), through='TaskDeveloper',
    )

    def __str__(self) -> str:
        """
        Return a string representation of the developer.

        Returns:
            str: A string representation of the developer.
        """
        return f'{self.developer.get_username()} ({str(self.position)})'

    class Meta:
        """Configuration class for Developer model."""

        db_table = '"freelance"."developer"'
        ordering = [DEVELOPER, POSITION]
        verbose_name = _(DEVELOPER)
        verbose_name_plural = _('developers')
        constraints = (
            models.UniqueConstraint(
                fields=(DEVELOPER,),
                name='developer_unique',
            ),
        )


class Position(CategorialParametr):
    """
    Model representing a task position.

    Each position has a name (title).
    """

    name = models.TextField(_(POSITION), null=False, blank=False)

    def __str__(self) -> str:
        """
        Return a string representation of the position.

        Returns:
            str: A string representation of the position.
        """
        return self.name

    class Meta:
        """Configuration class for Position model."""

        db_table = '"freelance"."position"'
        ordering = [NAME]
        verbose_name = _(POSITION)
        verbose_name_plural = _('positions')


class Comment(UUIDMixin):
    """
    Model representing a comment.

    Each comment is associated with a task and a developer, and has a conted text field and publication date.
    """

    task = models.ForeignKey(
        'Task', verbose_name=_(TASK), on_delete=models.CASCADE, related_name='comments',
    )
    comment_content = models.TextField(_('content'), blank=True)
    owner = models.ForeignKey(
        'Developer', verbose_name=_('owner'), on_delete=models.CASCADE,
    )

    publication_date = models.DateTimeField(
        verbose_name=_('publication time'),
        null=False,
        blank=False,
        default=timezone.now,
        editable=False,
    )

    class Meta:
        """Configuration class for Comment model."""

        db_table = '"freelance"."comment"'
        ordering = ['publication_date']
        verbose_name = _('comment')
        verbose_name_plural = _('comment')


class TaskDeveloper(models.Model):
    """Model representing the association between a task and a developer."""

    developer = models.ForeignKey(
        'Developer', verbose_name=_(DEVELOPER),  on_delete=models.CASCADE,
    )
    task = models.ForeignKey('Task', verbose_name=_(TASK), on_delete=models.CASCADE)

    class Meta:
        """Configuration class for TaskDeveloper model."""

        db_table = '"freelance"."task_developer"'
        unique_together = (
            (TASK, DEVELOPER),
        )
        verbose_name = _('relationship task developer')
        verbose_name_plural = _('relationships task developer')
