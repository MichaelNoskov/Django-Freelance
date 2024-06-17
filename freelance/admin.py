"""
This module contains the admin interface configurations for the Task, Student, TaskStudent, and Comment models.

Each model has a corresponding admin class that extends admin.ModelAdmin and is decorated with @admin.register.

Administrator classes define list-based fields (list_display) and read-only fields (readonly_fields).
"""

from django.contrib import admin

from .models import Comment, Developer, Position, Status, Task, TaskDeveloper


class TaskDeveloperInline(admin.TabularInline):
    """TaskDeveloper admin configuration."""

    model = TaskDeveloper
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Task admin configuration."""

    model = Task
    inlines = (TaskDeveloperInline,)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Status admin configuration."""

    model = Status


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    """Developer admin configuration."""

    model = Developer
    inlines = (TaskDeveloperInline,)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """Position admin configuration."""

    model = Position


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin configuration."""

    model = Comment
    readonly_fields = ['publication_date']
