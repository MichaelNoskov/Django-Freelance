"""
This module defines the serializers for the application.

It includes serializers for tasks, positions, statuses, students and comments.
Each serializer is a Django REST Framework ModelSerializer,
which means it automatically generates fields based on the model it's serializing.
"""

from rest_framework import serializers

from .models import Comment, Position, Status, Task

ALL = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the Task model."""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Configuration class for task serializer."""

        model = Task
        fields = ALL


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for the status model."""

    class Meta:
        """Configuration class for status serializer."""

        model = Status
        fields = ALL


class PositionSerializer(serializers.ModelSerializer):
    """Serializer for the Position model."""

    class Meta:
        """Configuration class for position serializer."""

        model = Position
        fields = ALL


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """Configuration class for comment serializer."""

        model = Comment
        fields = ALL
